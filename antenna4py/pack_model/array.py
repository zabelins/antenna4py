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
        self.obj_factor = pa.array_factor.Factor(1)
        self.obj_element = pa.array_element.Element(1)
        self.id = id
        # центральная частота для антенной системы
        self.f_cen = []
        # параметры множителя решётки
        self.array_N = []
        self.array_nois = []
        # тестовый вектор
        self.vec_test = []
        # временные вектора эквивалентных углов
        self.vec_eqdegsig = []
        self.vec_eqdegint = []
        # временной вектор осшп
        self.vec_snir = []
        self.mean_snir = []
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
        self.array_nois = np.array(init[5])

    def get(self):
        res = []
        res.append(self.f_cen)
        res.append(self.array_N)
        res.append(self.array_nois)
        return res

    def print(self):
        print("Параметры модели антенной решётки (L2):")
        print("\tf_cen = ", self.f_cen)
        print("\tarray_N = ", self.array_N)
        print("\tarray_nois = ", self.array_nois)
        self.obj_factor.print()
        self.obj_element.print()

    def calc_out(self, out_set, out_env):
        # распаковка исходных данных
        vec_pattern = out_set[0]
        vec_sigdeg, vec_sigamp, vec_sigband = out_env[0], out_env[1], out_env[2]
        vec_intdeg, vec_intamp, vec_intband = out_env[3], out_env[4], out_env[5]
        # вычисление входного комплексного сигнала по элементам и углам
        self.calc_testsig(vec_pattern, vec_sigamp)
        # вычисление входных сигналов и помех от времени
        self.calc_realsig(vec_sigdeg, vec_sigamp, vec_sigband, vec_intdeg, vec_intamp, vec_intband)
        # вычисление входного осшп
        self.calc_snir(vec_sigamp, vec_intamp)

    def get_out(self):
        out_array = []
        out_array.append(self.vec_test)
        out_array.append(self.vec_eqdegsig)
        out_array.append(self.vec_eqdegint)
        out_array.append(self.vec_snir)
        out_array.append(self.mean_snir)
        out_array.append(self.vec_sig)
        out_array.append(self.vec_int)
        out_array.append(self.vec_nois)
        out_array.append(self.matrix_sig)
        out_array.append(self.matrix_int)
        out_array.append(self.matrix_nois)
        return out_array

    def print_out(self):
        # проверка типа векторов и матриц на ndarray и list
        condit_1 = cl.is_list([self.vec_eqdegsig, self.vec_eqdegint])
        condit_2 = cl.is_ndarray([self.vec_test, self.vec_sig, self.vec_int, self.vec_nois])
        condit_3 = cl.is_ndarray([self.vec_snir, self.matrix_sig, self.matrix_int, self.matrix_nois])
        # вывод размерностей векторов
        if condit_1 and condit_2 and condit_3:
            print("Размерности векторов и матриц от антенной решётки:")
            print("\tvec_test.shape = ", self.vec_test.shape)
            print("\tvec_eqdegsig.shape = ", len(self.vec_eqdegsig))
            print("\tvec_eqdegint.shape = ", len(self.vec_eqdegint))
            print("\tvec_snir.shape = ", self.vec_snir.shape)
            print("\tmean_snir.shape = ", 1)
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
            amp_dist = self.obj_factor.get_dist(num)
            amp_rand = self.obj_factor.get_randamp()
            # фазы для заданного элемента
            deg_rand = self.obj_factor.get_randphi()
            # амплитуды для заданного угла обзора
            buf = np.zeros(shape=[len_pattern], dtype=complex)
            for j in range(len_pattern):
                deg = math.radians(vec_pattern[j])
                amp_elem = self.obj_element.get_gain(deg)
                amp = amp_sig * amp_elem * amp_dist * amp_rand
                buf[j] = self.obj_factor.get_signal(amp, deg, num, deg_rand)
            self.vec_test[i] = buf

    def calc_realsig(self, vec_sigdeg, vec_sigamp, vec_sigband, vec_intdeg, vec_intamp, vec_intband):
        # вычисление векторов входных сигналов и помех в зависимости от времени для заданных углов прихода
        len_time, len_sig, len_int = vec_sigdeg.shape[0], vec_sigdeg.shape[1], vec_intdeg.shape[1]
        # расчёт вектора и параметров эквивалентных сигналов
        self.vec_eqdegsig, num_all_sig, num_eq4real_sig, l4real_sig, f_otn4real_sig = self.obj_factor.get_eqvec(vec_sigdeg, vec_sigband)
        # расчёт вектора и параметров эквивалентных помех
        self.vec_eqdegint, num_all_int, num_eq4real_int, l4real_int, f_otn4real_int = self.obj_factor.get_eqvec(vec_intdeg, vec_intband)
        # вычисления размеров для векторов и матриц
        # max - максимум по столбцу, gmax - глобальный максимум
        max_all_sig, max_all_int = int(num_all_sig.max()), int(num_all_int.max())
        max_eq4real_sig, max_eq4real_int = np.zeros(shape=[len_sig]), np.zeros(shape=[len_int])
        buf = num_eq4real_sig.T
        for i in range(len_sig):
            max_eq4real_sig[i] = buf[i].max()
        buf = num_eq4real_int.T
        for i in range(len_int):
            max_eq4real_int[i] = buf[i].max()
        # инициализируем вектора и матрицы
        self.init_vecmatrix(len_time, max_all_sig, max_all_int)
        vec_coefsig = np.zeros(shape=[len_time, max_all_sig])
        vec_coefint = np.zeros(shape=[len_time, max_all_int])
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление векторов сигналов и помех
            self.vec_sig[i] = self.calc_vector(vec_sigamp[i], self.vec_eqdegsig[i], num_eq4real_sig[i], max_eq4real_sig)
            self.vec_int[i] = self.calc_vector(vec_intamp[i], self.vec_eqdegint[i], num_eq4real_int[i], max_eq4real_int)
            # вычисление матриц сигналов и помех
            self.matrix_sig[i], vec_coefsig[i] = self.calc_matrix(self.vec_sig[i], l4real_sig[i], f_otn4real_sig[i], max_eq4real_sig)
            self.matrix_int[i], vec_coefint[i] = self.calc_matrix(self.vec_int[i], l4real_int[i], f_otn4real_int[i], max_eq4real_int)
            # коррекция амплитуд векторов сигналов и помех
            self.vec_sig[i] = self.edit_vector(self.vec_sig[i], vec_coefsig[i], max_all_sig)
            self.vec_int[i] = self.edit_vector(self.vec_int[i], vec_coefint[i], max_all_int)
            # вычисление вектора и матрицы для шума
            self.vec_nois[i] = self.calc_nois()
            self.matrix_nois[i] = self.calc_matrixnois(i)

    def calc_vector(self, var_amp, var_eqdeg, var_num_eq4real, max_eq4real):
        # вычисление вектора сигнала для одного момента времени
        len_sig = var_amp.shape[0]
        gmaxlen_eqsig = 0
        for i in range(max_eq4real.shape[0]):
            gmaxlen_eqsig = gmaxlen_eqsig + int(max_eq4real[i])
        vec = np.zeros(shape=[gmaxlen_eqsig, self.array_N], dtype=complex)
        index = 0
        # запускаем цикл по реальным сигналам
        for i in range(len_sig):
            # запускаем цикл по эквивалентным сигналам
            for j in range(int(var_num_eq4real[i])):
                # запускаем цикл по элементам АР
                vec_buf = np.zeros(shape=[self.array_N], dtype=complex)
                for k in range(self.array_N):
                    if var_eqdeg[i][j] != 361.0:
                        # вычисление текущего номера элемента
                        num = k + 1
                        # амплитуды для заданного элемента
                        amp_sig = var_amp[i]
                        amp_dist = self.obj_factor.get_dist(num)
                        amp_rand = self.obj_factor.get_randamp()
                        # фазы для заданного элемента
                        deg_rand = self.obj_factor.get_randphi()
                        # амплитуды для заданного угла обзора
                        deg = math.radians(var_eqdeg[i][j])
                        amp_elem = self.obj_element.get_gain(deg)
                        amp = amp_sig * amp_elem * amp_dist * amp_rand
                        vec_buf[k] = vec_buf[k] + self.obj_factor.get_signal(amp, deg, num, deg_rand)
                    else:
                        vec_buf[k] = vec_buf[k]
                vec[index] = vec_buf
                index = index + 1
            index = int(max_eq4real[i])
        return vec

    def calc_matrix(self, vec, l0_max, f_otn, max_eq4real):
        # вычисление корреляционной матрицы для одного момента времени
        len_realsig = l0_max.shape[0]
        gmaxlen_eqsig = 0
        for i in range(max_eq4real.shape[0]):
            gmaxlen_eqsig = gmaxlen_eqsig + int(max_eq4real[i])
        matrix = np.zeros(shape=[self.array_N, self.array_N], dtype=complex)
        vec_coef = np.zeros(shape=[gmaxlen_eqsig])
        index = 0
        # запускаем цикл по реальным сигналам
        for i in range(len_realsig):
            # запускаем цикл по эквивалентным парам
            for j in range(int(l0_max[i])+1):
                # вычисление коэффициена дискретного разложения Фурье
                coef_fourier = self.obj_factor.get_eqamp(self.array_N, l0_max[i], j, f_otn[i])
                if j == 0:
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
            index = int(max_eq4real[i])
        return [matrix, vec_coef]

    def calc_nois(self):
        # вычисление векторов теплового шума
        flag = 0
        if flag == 0:
            # средние вектора шума
            vec_nois = np.zeros(shape=[1, self.array_N], dtype=complex)
        else:
            # мгновенные вектора шума
            vec_nois = np.zeros(shape=[1, self.array_N], dtype=complex)
            for i in range(self.array_N):
                vec_nois[0][i] = np.random.normal(loc=0.0, scale=self.array_nois)
        return vec_nois

    def calc_matrixnois(self, i):
        # вычисление матриц шума
        flag = 0
        if flag == 0:
            # матрица средней мощности (дисперсии) шума
            matrix = np.eye(self.array_N, dtype=complex) * math.pow(self.array_nois, 2)
        else:
            # матрица мгновенной мощности шума
            var_vec = self.vec_nois[i][0]
            matrix = np.diag(var_vec**2)
        return matrix

    def edit_vector(self, var_sig, var_coefsig, max_eqandreal):
        # умножение векторов на коэффициенты Фурье
        for i in range(max_eqandreal):
            var_sig[i] = var_sig[i] * math.sqrt(var_coefsig[i])
        return var_sig

    def init_vecmatrix(self, len_time, max_all_sig, max_all_int):
        # инициализация векторов и матриц
        self.vec_sig = np.zeros(shape=[len_time, max_all_sig, self.array_N], dtype=complex)
        self.vec_int = np.zeros(shape=[len_time, max_all_int, self.array_N], dtype=complex)
        self.vec_nois = np.zeros(shape=[len_time, 1, self.array_N], dtype=complex)
        self.matrix_sig = np.zeros(shape=[len_time, self.array_N, self.array_N], dtype=complex)
        self.matrix_int = np.zeros(shape=[len_time, self.array_N, self.array_N], dtype=complex)
        self.matrix_nois = np.zeros(shape=[len_time, self.array_N, self.array_N], dtype=complex)

    def calc_snir(self, vec_sigamp, vec_intamp):
        # вычислить временную зависимость осшп
        len_time = vec_sigamp.shape[0]
        self.vec_snir = np.zeros(shape=[len_time, 1])
        pow_nois = np.square(self.array_nois)
        # запускаем цикл по времени
        for i in range(len_time):
            # перевод в мощности
            pow_sig = np.square(vec_sigamp[i])
            pow_int = np.square(vec_intamp[i])
            # суммирование
            pow_sig = pow_sig.sum()
            pow_int = pow_int.sum()
            # вычисление осшп
            self.vec_snir[i][0] = self.get_pow2db(pow_sig/(pow_int+pow_nois))
        # вычисление среднего осшп
        self.mean_snir = self.vec_snir.mean()

    def get_pow2db(self, num):
        # перевод мощности в децибеллы
        return 10 * np.log10(abs(num))
