import math

import pack_model.pack_array as pa
from pack_model.pack_array import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели антенной решётки (L2)")
    print("Модуль использует пакет:", pa.NAME)

class Array:
    """Класс моделирования антенной решётки"""

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
        # распаковка исходных данных
        vec_pattern = out_set[0]
        vec_degsig, vec_degint = [out_env[0], out_env[1]]
        vec_amsig, vec_amint, vec_amnois = [out_env[2], out_env[3], out_env[4]]
        vec_fbandsig, vec_fbandint = [out_env[5], out_env[6]]
        # вычисление входного комплексного сигнала по элементам и углам
        self.calc_testsig(vec_pattern, vec_amsig)
        # вычисление входных сигналов и помех от времени
        self.calc_realsig(vec_degsig, vec_degint, vec_amsig, vec_amint, vec_amnois, vec_fbandsig, vec_fbandint)

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
        # вычисление вектора входного сигнала по элементам и углам (10x721)
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

    def calc_realsig(self, vec_degsig, vec_degint, vec_amsig, vec_amint, vec_amnois, vec_fbandsig, vec_fbandint):
        # вычисление векторов входных сигналов и помех от времени
        len_time = vec_degsig.shape[0]
        len_sig, len_int = [vec_degsig.shape[1], vec_degint.shape[1]]
        self.vec_sig = np.zeros(shape=[len_time, len_sig, self.N], dtype=complex)
        self.vec_int = np.zeros(shape=[len_time, len_int, self.N], dtype=complex)
        self.vec_nois = np.zeros(shape=[len_time, 1, self.N], dtype=complex)
        self.matrix_sig = np.zeros(shape=[len_time, self.N, self.N], dtype=complex)
        self.matrix_int = np.zeros(shape=[len_time, self.N, self.N], dtype=complex)
        self.matrix_nois = np.zeros(shape=[len_time, self.N, self.N], dtype=complex)
        # запускаем цикл по времени
        for i in range(len_time):
            buf1 = self.calc_corr(vec_degsig[i], vec_amsig[i], vec_fbandsig[i])
            buf2 = self.calc_corr(vec_degint[i], vec_amint[i], vec_fbandint[i])
            self.vec_sig[i], self.matrix_sig[i] = buf1
            self.vec_int[i], self.matrix_int[i] = buf2
            # vec_nois вычисляется некорректно, должен быть рандомным
            self.vec_nois[i] = np.ones(shape=[1, self.N], dtype=complex) * vec_amnois[i]
            self.matrix_nois[i] = np.eye(self.N, dtype=complex) * math.pow(vec_amnois[i], 2)

    def calc_corr(self, var_deg, var_amp, var_fband):
        # вычисление вектора и корреляционной матрицы для одного момента времени
        len_deg = var_deg.shape[0]
        vec = np.zeros(shape=[len_deg, self.N], dtype=complex)
        # запускаем цикл по реальным сигналам
        for i in range(len_deg):
            # вычисление углов эквивалентных сигналов
            buf = self.list_factor.get_eqsig(var_deg[i], var_fband[i], self.N)
            var_eqdeg, num_eqsig, l0_max, f_otn = [buf[0], buf[1], buf[2], buf[3]]
            len_eqdeg = var_eqdeg.shape[0]
            print("--- GGG ---")
            print("var_eqdeg = ", var_eqdeg)
            print("num_eqsig = ", num_eqsig)
            print("l0_max = ", l0_max)
            print("f_otn = ", f_otn)
            # запускаем цикл по эквивалентным сигналам
            vec_buf = np.zeros(shape=[self.N], dtype=complex)
            for j in range(len_eqdeg):
                # запускаем цикл по элементам АР
                for k in range(self.N):
                    if (var_eqdeg[j] != 361.0):
                        # вычисление номера элемента
                        num = k + 1
                        # амплитуды для заданного элемента
                        #amp_sig = var_amp[i] / len_eqdeg
                        amp_sig = var_amp[i] * self.list_factor.get_eqamp(self.N, num)
                        amp_dist = self.list_factor.get_dist(self.N, num)
                        amp_rand = self.list_factor.get_randamp()
                        # фазы для заданного элемента
                        deg_rand = self.list_factor.get_randphi()
                        # амплитуды для заданного угла обзора
                        deg = math.radians(var_eqdeg[j])
                        amp_elem = self.list_element.get_out(deg)
                        amp = amp_sig * amp_elem * amp_dist * amp_rand
                        vec_buf[k] = vec_buf[k] + self.list_factor.get_out(amp, deg, num, deg_rand)
                    else:
                        vec_buf[k] = vec_buf[k]
            vec[i] = vec_buf
            #print("vec_buf = ", vec_buf)
        # вычисление корреляционной матрицы
        matrix = np.zeros(shape=[self.N, self.N], dtype=complex)
        # запускаем цикл по реальным сигналам
        for i in range(len_deg):
            # вычисление углов эквивалентных сигналов
            buf = self.list_factor.get_eqsig(var_deg[i], var_fband[i], self.N)
            var_eqdeg, num_eqsig, l0_max, f_otn = [buf[0], buf[1], buf[2], buf[3]]
            len_eqdeg = var_eqdeg.shape[0]
            # расчёт корреляционной матрицы
            vec0 = vec[i].T
            vec1 = np.conj(vec0)
            vec2 = vec0.T
            matrix_buf = np.outer(vec1, vec2)
            matrix = matrix + matrix_buf
        # осталось добавить расчёт широкополосных сигналов
        return [vec, matrix]