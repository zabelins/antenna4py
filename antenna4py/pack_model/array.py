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
        self.vec_eqdegsig = []
        self.vec_eqdegint = []
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
        vec_ampsig, vec_ampint, vec_ampnois = [out_env[2], out_env[3], out_env[4]]
        vec_fbandsig, vec_fbandint = [out_env[5], out_env[6]]
        # вычисление входного комплексного сигнала по элементам и углам
        self.calc_testsig(vec_pattern, vec_ampsig)
        # вычисление входных сигналов и помех от времени
        self.calc_realsig(vec_degsig, vec_degint, vec_ampsig, vec_ampint, vec_ampnois, vec_fbandsig, vec_fbandint)

    def get_out(self):
        res = []
        res.append(self.vec_test)
        res.append(self.vec_sig)
        res.append(self.vec_int)
        res.append(self.vec_nois)
        res.append(self.matrix_sig)
        res.append(self.matrix_int)
        res.append(self.matrix_nois)
        res.append(self.vec_eqdegsig)
        res.append(self.vec_eqdegint)
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
        print("vec_eqdegsig.shape = ", len(self.vec_eqdegsig))
        print("vec_eqdegint.shape = ", len(self.vec_eqdegint))

    def calc_testsig(self, vec_pattern, vec_ampsig):
        # вычисление вектора входного сигнала по всем углам для построения ДН (10x721)
        len_pattern = vec_pattern.shape[0]
        self.vec_test = np.zeros(shape=[self.N, len_pattern], dtype=complex)
        buf = np.zeros(shape=[len_pattern], dtype=complex)
        for i in range(self.N):
            # вычисление номера элемента
            num = i + 1
            # амплитуды для заданного элемента
            amp_sig = vec_ampsig[0]
            amp_dist = self.list_factor.get_dist(self.N, num)
            amp_rand = self.list_factor.get_randamp()
            # фазы для заданного элемента
            deg_rand = self.list_factor.get_randphi()
            # амплитуды для заданного угла обзора
            for j in range(len_pattern):
                deg = math.radians(vec_pattern[j])
                amp_elem = self.list_element.get_out(deg)
                amp = amp_sig * amp_elem * amp_dist * amp_rand
                buf[j] = self.list_factor.get_out(amp, deg, num, deg_rand)
            self.vec_test[i] = buf
            buf = np.zeros(shape=[len_pattern], dtype=complex)

    def calc_realsig(self, vec_degsig, vec_degint, vec_ampsig, vec_ampint, vec_ampnois, vec_fbandsig, vec_fbandint):
        # вычисление векторов входных сигналов и помех в зависимости от времени для заданных углов прихода
        len_time, len_sig, len_int = [vec_degsig.shape[0], vec_degsig.shape[1], vec_degint.shape[1]]
        # расчёт вектора и параметров эквивалентных сигналов
        buf = self.list_factor.get_eqvec(len_time, len_sig, vec_degsig, vec_fbandsig, self.N)
        self.vec_eqdegsig, len_eqsig, sumlen_eqsig, l0_maxsig, f_otnsig = buf
        # расчёт вектора и параметров эквивалентных помех
        buf = self.list_factor.get_eqvec(len_time, len_int, vec_degint, vec_fbandint, self.N)
        self.vec_eqdegint, len_eqint, sumlen_eqint, l0_maxint, f_otnint = buf
        # инициализируем размеры векторов и матриц
        self.vec_sig = np.zeros(shape=[len_time, int(sumlen_eqsig.max()), self.N], dtype=complex)
        self.vec_int = np.zeros(shape=[len_time, int(sumlen_eqint.max()), self.N], dtype=complex)
        self.vec_nois = np.zeros(shape=[len_time, 1, self.N], dtype=complex)
        self.matrix_sig = np.zeros(shape=[len_time, self.N, self.N], dtype=complex)
        self.matrix_int = np.zeros(shape=[len_time, self.N, self.N], dtype=complex)
        self.matrix_nois = np.zeros(shape=[len_time, self.N, self.N], dtype=complex)
        vec_coefsig = np.zeros(shape=[len_time, int(sumlen_eqsig.max())])
        vec_coefint = np.zeros(shape=[len_time, int(sumlen_eqint.max())])
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление векторов сигналов и помех
            self.vec_sig[i] = self.calc_vector(vec_ampsig[i], self.vec_eqdegsig[i], len_eqsig[i], sumlen_eqsig[i])
            self.vec_int[i] = self.calc_vector(vec_ampint[i], self.vec_eqdegint[i], len_eqint[i], sumlen_eqint[i])
            # вычисление матриц сигналов и помех
            self.matrix_sig[i], vec_coefsig[i] = self.calc_matrix(self.vec_sig[i], l0_maxsig[i], f_otnsig[i], sumlen_eqsig[i])
            self.matrix_int[i], vec_coefint[i] = self.calc_matrix(self.vec_int[i], l0_maxint[i], f_otnint[i], sumlen_eqint[i])
            # коррекция амплитуд векторов сигналов и помех
            self.vec_sig[i] = self.edit_vector(self.vec_sig[i], vec_coefsig[i], sumlen_eqsig[i])
            self.vec_int[i] = self.edit_vector(self.vec_int[i], vec_coefint[i], sumlen_eqint[i])
            # вычисление вектора и матрицы для шума (!!! vec_nois должен быть рандомным !!!)
            self.vec_nois[i] = np.ones(shape=[1, self.N], dtype=complex) * vec_ampnois[i]
            self.matrix_nois[i] = np.eye(self.N, dtype=complex) * math.pow(vec_ampnois[i], 2)
        #print("vec_sig = ", self.vec_sig[0])
        #print("vec_int = ", self.vec_int[0])

    def calc_vector(self, var_amp, var_eqdeg, len_eqsig, sumlen_eqsig):
        # вычисление вектора сигнала для одного момента времени
        len_sig = var_amp.shape[0]
        vec = np.zeros(shape=[int(sumlen_eqsig), self.N], dtype=complex)
        index = 0
        # запускаем цикл по реальным сигналам
        for i in range(len_sig):
            # запускаем цикл по эквивалентным сигналам
            for j in range(int(len_eqsig[i])):
                vec_buf = np.zeros(shape=[self.N], dtype=complex)
                # запускаем цикл по элементам АР
                for k in range(self.N):
                    if (var_eqdeg[i][j] != 361.0):
                        # вычисление номера элемента
                        num = k + 1
                        # амплитуды для заданного элемента
                        amp_sig = var_amp[i]
                        amp_dist = self.list_factor.get_dist(self.N, num)
                        amp_rand = self.list_factor.get_randamp()
                        # фазы для заданного элемента
                        deg_rand = self.list_factor.get_randphi()
                        # амплитуды для заданного угла обзора
                        deg = math.radians(var_eqdeg[i][j])
                        amp_elem = self.list_element.get_out(deg)
                        amp = amp_sig * amp_elem * amp_dist * amp_rand
                        vec_buf[k] = vec_buf[k] + self.list_factor.get_out(amp, deg, num, deg_rand)
                    else:
                        vec_buf[k] = vec_buf[k]
                vec[index] = vec_buf
                index = index + 1
        #print(vec)
        return vec

    def calc_matrix(self, vec, l0_max, f_otn, sumlen_eqsig):
        # вычисление корреляционной матрицы для одного момента времени
        matrix = np.zeros(shape=[self.N, self.N], dtype=complex)
        vec_coef = np.zeros(shape=[int(sumlen_eqsig)])
        len_realsig = l0_max.shape[0]
        index = 0
        # запускаем цикл по реальным сигналам
        for i in range(len_realsig):
            # запускаем цикл по эквивалентным парам
            for j in range(int(l0_max[i])+1):
                # вычисление коэффициена дискретного разложения Фурье
                coef_fourier = self.list_factor.get_eqamp(self.N, l0_max[i], j, f_otn[i])
                if (j == 0):
                    # расчёт корреляционной матрицы реального сигнала
                    var_vec = vec[index].T
                    matrix_buf = coef_fourier * np.outer(np.conj(var_vec), var_vec.T)
                    # суммирование матриц
                    matrix = matrix + matrix_buf
                    vec_coef[index] = coef_fourier
                    index = index + 1
                else:
                    # расчёт корреляционной матрицы эквивалентных пар сигналов
                    var_vec0 = vec[index].T
                    var_vec1 = vec[index+1].T
                    matrix0_buf = np.outer(np.conj(var_vec0), var_vec0.T)
                    matrix1_buf = np.outer(np.conj(var_vec1), var_vec1.T)
                    matrix_buf = (coef_fourier / 2) * (matrix0_buf + matrix1_buf)
                    # суммирование матриц
                    matrix = matrix + matrix_buf
                    vec_coef[index] = coef_fourier / 2
                    vec_coef[index+1] = coef_fourier / 2
                    index = index + 2
        #print(matrix)
        #print(vec_coef)
        return [matrix, vec_coef]

    def edit_vector(self, var_sig, var_coefsig, sumlen_eq):
        # умножение векторов на коэффициенты Фурье
        for i in range(int(sumlen_eq)):
            var_sig[i] = var_sig[i] * math.sqrt(var_coefsig[i])
        return var_sig