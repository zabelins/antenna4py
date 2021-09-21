import math
import pack_calc.calc_list as cl
import pack_model.pack_array as pa
from pack_model.pack_array import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели антенной решётки (L2)")
    print("Модуль использует пакет:", pa.NAME)

class Array:
    """Класс моделирования антенной решётки"""

    def __init__(self, id):
        self.list_factor = pa.array_factor.Factor(1)
        self.list_element = pa.array_element.Element(1)
        self.id = id
        # центральная частота для антенной системы
        self.f_cen = []
        # параметры множителя решётки
        self.array_N = []
        # тестовый вектор
        self.vec_test = []
        # вектора эквивалентных углов
        self.vec_eqdegsig = []
        self.vec_eqdegint = []
        # входные комплексные вектора
        self.vec_sig = []
        self.vec_int = []
        self.vec_nois = []
        # корреляционные матрицы
        self.matrix_sig = []
        self.matrix_int = []
        self.matrix_nois = []

    def set(self, init):
        self.f_cen = np.array(init[0])
        self.array_N = np.array(init[1])

    def get(self):
        res = []
        res.append(self.f_cen)
        res.append(self.array_N)
        return res

    def print(self):
        print("Параметры модели антенной решётки (L2):")
        print("\tf_cen = ", self.f_cen)
        print("\tarray_N = ", self.array_N)
        self.list_factor.print()
        self.list_element.print()

    def calc_out(self, out_set, out_env):
        # распаковка исходных данных
        vec_pattern = out_set[0]
        vec_sigdeg, vec_sigamp, vec_sigband = out_env[0], out_env[1], out_env[2]
        vec_intdeg, vec_intamp, vec_intband = out_env[3], out_env[4], out_env[5]
        vec_noisamp = out_env[6]
        # вычисление входного комплексного сигнала по элементам и углам
        self.calc_testsig(vec_pattern, vec_sigamp)
        # вычисление входных сигналов и помех от времени
        self.calc_realsig(vec_sigdeg, vec_sigamp, vec_sigband, vec_intdeg, vec_intamp, vec_intband, vec_noisamp)

    def get_out1nd(self):
        # получить вектора для отрисовки ДН
        res = []
        res.append(self.vec_test)
        res.append(self.vec_eqdegsig)
        res.append(self.vec_eqdegint)
        return res

    def get_out2nd(self):
        # получить вектора для вычислений
        res = []
        res.append(self.vec_sig)
        res.append(self.vec_int)
        res.append(self.vec_nois)
        res.append(self.matrix_sig)
        res.append(self.matrix_int)
        res.append(self.matrix_nois)
        return res

    def print_out(self):
        # проверка типа векторов и матриц на ndarray и list
        bool_res1 = cl.is_list([self.vec_eqdegsig, self.vec_eqdegint])
        bool_res2 = cl.is_ndarray([self.vec_test, self.vec_sig, self.vec_int, self.vec_nois])
        bool_res3 = cl.is_ndarray([self.matrix_sig, self.matrix_int, self.matrix_nois])
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True) and (bool_res3 == True):
            print("Размерности векторов и матриц от антенной решётки:")
            print("\tvec_test.shape = ", self.vec_test.shape)
            print("\tvec_eqdegsig.shape = ", len(self.vec_eqdegsig))
            print("\tvec_eqdegint.shape = ", len(self.vec_eqdegint))
            print("\tvec_sig.shape = ", self.vec_sig.shape)
            print("\tvec_int.shape = ", self.vec_int.shape)
            print("\tvec_nois.shape = ", self.vec_nois.shape)
            print("\tmatrix_sig.shape = ", self.matrix_sig.shape)
            print("\tmatrix_int.shape = ", self.matrix_int.shape)
            print("\tmatrix_nois.shape = ", self.matrix_nois.shape)
        else:
            print("Ошибка проверки типа векторов и матриц от антенной решётки")

    def calc_testsig(self, vec_pattern, vec_sigamp):
        # вычисление вектора входного сигнала по всем углам для построения ДН (10x721)
        len_pattern = vec_pattern.shape[0]
        self.vec_test = np.zeros(shape=[self.array_N, len_pattern], dtype=complex)
        for i in range(self.array_N):
            # вычисление текущего номера элемента
            num = i + 1
            # амплитуды для заданного элемента
            amp_sig = vec_sigamp[0]
            amp_dist = self.list_factor.get_dist(num)
            amp_rand = self.list_factor.get_randamp()
            # фазы для заданного элемента
            deg_rand = self.list_factor.get_randphi()
            # амплитуды для заданного угла обзора
            buf = np.zeros(shape=[len_pattern], dtype=complex)
            for j in range(len_pattern):
                deg = math.radians(vec_pattern[j])
                amp_elem = self.list_element.get_gain(deg)
                amp = amp_sig * amp_elem * amp_dist * amp_rand
                buf[j] = self.list_factor.get_signal(amp, deg, num, deg_rand)
            self.vec_test[i] = buf

    def calc_realsig(self, vec_sigdeg, vec_sigamp, vec_sigband, vec_intdeg, vec_intamp, vec_intband, vec_noisamp):
        # вычисление векторов входных сигналов и помех в зависимости от времени для заданных углов прихода
        len_time, len_sig, len_int = [vec_sigdeg.shape[0], vec_sigdeg.shape[1], vec_intdeg.shape[1]]
        # расчёт вектора и параметров эквивалентных сигналов
        buf = self.list_factor.get_eqvec(vec_sigdeg, vec_sigband)
        self.vec_eqdegsig, len_eqsig, sumlen_eqsig, l0_maxsig, f_otnsig = buf
        # расчёт вектора и параметров эквивалентных помех
        buf = self.list_factor.get_eqvec(vec_intdeg, vec_intband)
        self.vec_eqdegint, len_eqint, sumlen_eqint, l0_maxint, f_otnint = buf
        # вычисления размеров для векторов и матриц
        # max - максимум по столбцу, gmax - глобальный максимум
        gmaxlen_eqsig, gmaxlen_eqint = int(sumlen_eqsig.max()), int(sumlen_eqint.max())
        maxlen_eqsig, maxlen_eqint = np.zeros(shape=[len_sig]), np.zeros(shape=[len_int])
        buf = len_eqsig.T
        for i in range(len_sig):
            maxlen_eqsig[i] = buf[i].max()
        buf = len_eqint.T
        for i in range(len_int):
            maxlen_eqint[i] = buf[i].max()
        # инициализируем вектора и матрицы
        self.vec_sig = np.zeros(shape=[len_time, gmaxlen_eqsig, self.array_N], dtype=complex)
        self.vec_int = np.zeros(shape=[len_time, gmaxlen_eqint, self.array_N], dtype=complex)
        self.vec_nois = np.zeros(shape=[len_time, 1, self.array_N], dtype=complex)
        self.matrix_sig = np.zeros(shape=[len_time, self.array_N, self.array_N], dtype=complex)
        self.matrix_int = np.zeros(shape=[len_time, self.array_N, self.array_N], dtype=complex)
        self.matrix_nois = np.zeros(shape=[len_time, self.array_N, self.array_N], dtype=complex)
        vec_coefsig = np.zeros(shape=[len_time, gmaxlen_eqsig])
        vec_coefint = np.zeros(shape=[len_time, gmaxlen_eqint])
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление векторов сигналов и помех
            self.vec_sig[i] = self.calc_vector(vec_sigamp[i], self.vec_eqdegsig[i], len_eqsig[i], maxlen_eqsig)
            self.vec_int[i] = self.calc_vector(vec_intamp[i], self.vec_eqdegint[i], len_eqint[i], maxlen_eqint)
            # вычисление матриц сигналов и помех
            self.matrix_sig[i], vec_coefsig[i] = self.calc_matrix(self.vec_sig[i], l0_maxsig[i], f_otnsig[i], maxlen_eqsig)
            self.matrix_int[i], vec_coefint[i] = self.calc_matrix(self.vec_int[i], l0_maxint[i], f_otnint[i], maxlen_eqint)
            # коррекция амплитуд векторов сигналов и помех
            self.vec_sig[i] = self.edit_vector(self.vec_sig[i], vec_coefsig[i], gmaxlen_eqsig)
            self.vec_int[i] = self.edit_vector(self.vec_int[i], vec_coefint[i], gmaxlen_eqint)
            # вычисление вектора и матрицы для шума (!!! vec_nois должен быть рандомным !!!)
            self.vec_nois[i] = np.ones(shape=[1, self.array_N], dtype=complex) * vec_noisamp[i]
            self.matrix_nois[i] = np.eye(self.array_N, dtype=complex) * math.pow(vec_noisamp[i], 2)

    def calc_vector(self, var_amp, var_eqdeg, len_eqsig, maxlen_eqsig):
        # вычисление вектора сигнала для одного момента времени
        len_sig = var_amp.shape[0]
        gmaxlen_eqsig = 0
        for i in range(maxlen_eqsig.shape[0]):
            gmaxlen_eqsig = gmaxlen_eqsig + int(maxlen_eqsig[i])
        vec = np.zeros(shape=[gmaxlen_eqsig, self.array_N], dtype=complex)
        index = 0
        # запускаем цикл по реальным сигналам
        for i in range(len_sig):
            # запускаем цикл по эквивалентным сигналам
            for j in range(int(len_eqsig[i])):
                # запускаем цикл по элементам АР
                vec_buf = np.zeros(shape=[self.array_N], dtype=complex)
                for k in range(self.array_N):
                    if (var_eqdeg[i][j] != 361.0):
                        # вычисление текущего номера элемента
                        num = k + 1
                        # амплитуды для заданного элемента
                        amp_sig = var_amp[i]
                        amp_dist = self.list_factor.get_dist(num)
                        amp_rand = self.list_factor.get_randamp()
                        # фазы для заданного элемента
                        deg_rand = self.list_factor.get_randphi()
                        # амплитуды для заданного угла обзора
                        deg = math.radians(var_eqdeg[i][j])
                        amp_elem = self.list_element.get_gain(deg)
                        amp = amp_sig * amp_elem * amp_dist * amp_rand
                        vec_buf[k] = vec_buf[k] + self.list_factor.get_signal(amp, deg, num, deg_rand)
                    else:
                        vec_buf[k] = vec_buf[k]
                vec[index] = vec_buf
                index = index + 1
            index = int(maxlen_eqsig[i])
        return vec

    def calc_matrix(self, vec, l0_max, f_otn, maxlen_eqsig):
        # вычисление корреляционной матрицы для одного момента времени
        len_realsig = l0_max.shape[0]
        gmaxlen_eqsig = 0
        for i in range(maxlen_eqsig.shape[0]):
            gmaxlen_eqsig = gmaxlen_eqsig + int(maxlen_eqsig[i])
        matrix = np.zeros(shape=[self.array_N, self.array_N], dtype=complex)
        vec_coef = np.zeros(shape=[gmaxlen_eqsig])
        index = 0
        # запускаем цикл по реальным сигналам
        for i in range(len_realsig):
            # запускаем цикл по эквивалентным парам
            for j in range(int(l0_max[i])+1):
                # вычисление коэффициена дискретного разложения Фурье
                coef_fourier = self.list_factor.get_eqamp(self.array_N, l0_max[i], j, f_otn[i])
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
            index = int(maxlen_eqsig[i])
        return [matrix, vec_coef]

    def edit_vector(self, var_sig, var_coefsig, gmaxlen_eqsig):
        # умножение векторов на коэффициенты Фурье
        for i in range(gmaxlen_eqsig):
            var_sig[i] = var_sig[i] * math.sqrt(var_coefsig[i])
        return var_sig