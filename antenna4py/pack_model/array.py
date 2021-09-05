# модуль модели антенной решётки
import math

import pack_model.pack_array as pa
from pack_model.pack_array import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели антенной решётки (L2)")
    print("Модуль использует пакет:", pa.NAME)

class Array:
    def __init__(self, id):
        self.id = id
        self.N = []
        self.vec_test = []
        self.vec_sig = []
        self.vec_int = []
        self.vec_nois = []
        self.matrix_sig = []
        self.matrix_int = []
        self.matrix_nois = []
        self.list_factor = pa.array_factor.Factor(1)
        self.list_element = pa.array_element.Element(1)
    def set(self, init):
        self.N = np.array(init[1])
    def get(self):
        res = []
        res.append(self.id)
        res.append(self.N)
        return res
    def print(self):
        print(" --- Параметры модели антенной решётки (L2) --- ")
        print("id = ", self.id)
        print("N = ", self.N)
        self.list_factor.print_short()
        self.list_element.print_short()
    def print_short(self):
        print(" --- Параметры модели антенной решётки (L2) --- ")
        print("array = ", self.get())
    def calc_out(self, out_set, out_env):
        vec_pattern = out_set[0]
        vec_ampsig = out_env[2]
        # вычисление входного комплексного сигнала по элементам и углам
        self.calc_testsig(vec_pattern, vec_ampsig)
        # вычисление входных сигналов и помех от времени
        self.calc_arrayout(out_env)
    def get_out(self):
        res = []
        res.append(self.vec_test)
        res.append(self.vec_sig)
        res.append(self.vec_int)
        res.append(self.vec_nois)
        res.append(self.matrix_sig)
        res.append(self.matrix_int)
        res.append(self.matrix_nois)
        return res
    def print_out(self):
        print("Размерности векторов и матриц от антенной решётки:")
        print("vec_test.shape = ", self.vec_test.shape)
        print("vec_sig.shape = ", self.vec_sig.shape)
        print("vec_int.shape = ", self.vec_int.shape)
        print("vec_nois.shape = ", self.vec_nois.shape)
        print("matrix_sig.shape = ", self.matrix_sig.shape)
        print("matrix_int.shape = ", self.matrix_int.shape)
        print("matrix_nois.shape = ", self.matrix_nois.shape)
    def calc_testsig(self, vec_pattern, vec_ampsig):
        # вычисление входного комплексного сигнала по элементам и углам (10x721)
        len_pattern = vec_pattern.shape[0]
        self.vec_test = np.zeros(shape=[self.N, len_pattern], dtype=complex)
        buf = np.zeros(shape=[len_pattern], dtype=complex)
        for num_var in range(self.N):
            # вычисление номера элемента
            num = num_var + 1
            # амплитуды для заданного элемента
            amp_sig = vec_ampsig[0]
            amp_dist = self.list_factor.get_dist(self.N, num)
            amp_rand = self.list_factor.get_randamp()
            # фазы для заданного элемента
            deg_rand = self.list_factor.get_randphi()
            # амплитуды для заданного угла обзора
            for deg_var in range(len_pattern):
                deg = math.radians(vec_pattern[deg_var])
                amp_elem = self.list_element.get_out(deg)
                amp = amp_sig * amp_elem * amp_dist * amp_rand
                buf[deg_var] = self.list_factor.get_out(amp, deg, num, deg_rand)
            self.vec_test[num_var] = buf
            buf = np.zeros(shape=[len_pattern], dtype=complex)
    def calc_arrayout(self, out_env):
        vec_degsig = out_env[0]
        vec_degint = out_env[1]
        vec_amsig = out_env[2]
        vec_amint = out_env[3]
        vec_amnois = out_env[4]
        vec_fbandsig = out_env[5]
        vec_fbandint = out_env[6]
        len_time = vec_degsig.shape[0]
        len_sig = vec_degsig.shape[1]
        len_int = vec_degint.shape[1]
        self.vec_sig = np.ones(shape=[len_time, len_sig, self.N], dtype=complex)
        self.vec_int = np.ones(shape=[len_time, len_int, self.N], dtype=complex)
        self.matrix_sig = np.ones(shape=[len_time, self.N, self.N], dtype=complex)
        self.matrix_int = np.ones(shape=[len_time, self.N, self.N], dtype=complex)
        # запускаем цикл по времени
        for i in range(len_time):
            buf1 = self.calc_corr(vec_degsig[i], vec_amsig[i], vec_fbandsig[i])
            buf2 = self.calc_corr(vec_degint[i], vec_amint[i], vec_fbandint[i])
            self.vec_sig[i], self.matrix_sig[i] = buf1
            self.vec_int[i], self.matrix_int[i] = buf2
        # упрощённые вектор и матрица для шума
        self.vec_nois = np.ones(shape=[len_time, 1, self.N], dtype=complex)
        self.matrix_nois = np.ones(shape=[len_time, self.N, self.N], dtype=complex)
        # !!! ОШИБКА В МАТРИЦЕ ШУМА, ДОЛЖНА БЫТЬ ЕДИНИЧНОЙ
    def calc_corr(self, vec_deg, vec_amp, vec_fband):
        # вычисление вектора и корреляционной матрицы для заданного момента времени
        len_numsig = vec_deg.shape[0]
        vec = np.ones(shape=[len_numsig, self.N], dtype=complex)
        matrix = np.ones(shape=[self.N, self.N], dtype=complex)
        # запускаем цикл по номерам сигналов
        for i in range(len_numsig):
            ## вычисление эквивалентных углов для заданного момента времени
            #vec_degnew = self.list_factor.get_eqsig(vec_deg[i], vec_fband[i], self.N)
            #len_degnew = vec_degnew[0].shape[0]
            # запускаем цикл по элементам АР
            for j in range(self.N):
                # вычисление номера элемента
                num = j + 1
                # амплитуды для заданного элемента
                amp_sig = vec_amp[i]
                amp_dist = self.list_factor.get_dist(self.N, num)
                amp_rand = self.list_factor.get_randamp()
                # фазы для заданного элемента
                deg_rand = self.list_factor.get_randphi()
                # амплитуды для заданного угла обзора
                deg = math.radians(vec_deg[i])
                amp_elem = self.list_element.get_out(deg)
                amp = amp_sig * amp_elem * amp_dist * amp_rand
                vec[i][j] = self.list_factor.get_out(amp, deg, num, deg_rand)
        # вычисление корреляционной матрицы
        for i in range(len_numsig):
            vec0 = vec[i].T
            # расчёт корреляционной матрицы
            vec1 = np.conj(vec0)
            vec2 = vec0.T
            matrix_buf = np.outer(vec1, vec2)
            matrix = matrix + matrix_buf
        # осталось добавить расчёт широкополосных сигналов
        return [vec, matrix]