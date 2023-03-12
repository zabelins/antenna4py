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

    def __init__(self):
        self.obj_elem = pa.arr_elem.Element()
        self.obj_factor = pa.arr_factor.Factor()
        # параметры решётки
        self.arr_frq = 0
        self.arr_size = 0
        self.arr_noise = 0
        # форма комплексной огибающей
        self.vec_sigcpl = np.array([])
        self.vec_intcpl = np.array([])
        self.vec_sumcpl = np.array([])
        # тестовый вектор
        self.vec_test = np.array([])
        # временные вектора эквивалентных углов
        self.vec_eqdegsig = np.array([])
        self.vec_eqdegint = np.array([])
        # временной вектор осшп
        self.vec_snir = np.array([])
        self.mean_snir = np.array([])
        # входные комплексные вектора
        self.vec_sig = np.array([])
        self.vec_int = np.array([])
        self.vec_nois = np.array([])
        self.vec_sum = np.array([])
        # корреляционные матрицы
        self.matrix_sig = np.array([])
        self.matrix_int = np.array([])
        self.matrix_nois = np.array([])
        self.matrix_sum = np.array([])
        # вектора коэффициентов (скрытые)
        self.vec_coefsig = np.array([])
        self.vec_coefint = np.array([])

    def set(self, init):
        self.arr_frq = init[0]
        self.arr_size = init[1]
        self.arr_noise = init[5]

    def get(self):
        res = []
        res.append(self.arr_frq)
        res.append(self.arr_size)
        res.append(self.arr_noise)
        return res

    def print(self):
        print("Параметры модели антенной решётки (L2):")
        print("\tarr_frq = ", self.arr_frq)
        print("\tarr_size = ", self.arr_size)
        print("\tarr_noise = ", self.arr_noise)
        self.obj_elem.print()
        self.obj_factor.print()

    def calc_out(self, out_set, out_env):
        # распаковка исходных данных
        vec_deg, vec_time, flag_mod = out_set[0], out_set[1], out_env[6]
        vec_sigdeg, vec_sigamp, vec_sigbnd = out_env[0], out_env[1], out_env[2]
        vec_intdeg, vec_intamp, vec_intbnd = out_env[3], out_env[4], out_env[5]
        # единичный тестовый сигнал по элементам и углам (для диаграммы направленности)
        self.calc_test(vec_deg)
        # вектора комплексных амплитуд и ковариационные матрицы от времени
        self.calc_array(vec_time, vec_sigdeg, vec_sigamp, vec_sigbnd, vec_intdeg, vec_intamp, vec_intbnd, flag_mod)
        # вычисление входного осшп
        self.calc_snir()

    def get_out(self):
        out_array = []
        out_array.append(self.vec_sigcpl)
        out_array.append(self.vec_intcpl)
        out_array.append(self.vec_sumcpl)
        out_array.append(self.vec_test)
        out_array.append(self.vec_eqdegsig)
        out_array.append(self.vec_eqdegint)
        out_array.append(self.vec_snir)
        out_array.append(self.mean_snir)
        out_array.append(self.vec_sig)
        out_array.append(self.vec_int)
        out_array.append(self.vec_nois)
        out_array.append(self.vec_sum)
        out_array.append(self.matrix_sig)
        out_array.append(self.matrix_int)
        out_array.append(self.matrix_nois)
        out_array.append(self.matrix_sum)
        return out_array

    def print_out(self):
        # проверка типа векторов и матриц на ndarray и list
        condit_1 = cl.is_list([self.vec_eqdegsig, self.vec_eqdegint])
        condit_2 = cl.is_ndarray([self.vec_test, self.vec_sig, self.vec_int, self.vec_nois, self.vec_sum])
        condit_3 = cl.is_ndarray([self.vec_snir, self.matrix_sig, self.matrix_int, self.matrix_nois, self.matrix_sum])
        condit_4 = cl.is_ndarray([self.vec_sigcpl, self.vec_intcpl, self.vec_sumcpl])
        # вывод размерностей векторов
        if condit_1 and condit_2 and condit_3 and condit_4:
            print("Антенная решётка:")
            print("\tvec_sigcpl.shape = ", self.vec_sigcpl.shape)
            print("\tvec_intcpl.shape = ", self.vec_intcpl.shape)
            print("\tvec_sumcpl.shape = ", self.vec_sumcpl.shape)
            print("\tvec_test.shape = ", self.vec_test.shape)
            print("\tvec_eqdegsig.shape = ", len(self.vec_eqdegsig))
            print("\tvec_eqdegint.shape = ", len(self.vec_eqdegint))
            print("\tvec_snir.shape = ", self.vec_snir.shape)
            print("\tmean_snir.shape = ", 1)
            print("\tvec_sig.shape = ", self.vec_sig.shape)
            print("\tvec_int.shape = ", self.vec_int.shape)
            print("\tvec_nois.shape = ", self.vec_nois.shape)
            print("\tvec_sum.shape = ", self.vec_sum.shape)
            print("\tmatrix_sig.shape = ", self.matrix_sig.shape)
            print("\tmatrix_int.shape = ", self.matrix_int.shape)
            print("\tmatrix_nois.shape = ", self.matrix_nois.shape)
            print("\tmatrix_sum.shape = ", self.matrix_sum.shape)
        else:
            print("Ошибка проверки векторов и матриц антенной решётки")

    def calc_test(self, vec_deg):
        # вычисление матрицы отклика решётки на единичный сигнал (для построения ДН 10х721)
        self.vec_test = np.zeros(shape=[self.arr_size, vec_deg.shape[0]], dtype=complex)
        # цикл по элементам решётки
        for i in range(self.arr_size):
            num = i + 1
            # амплитуды для заданного элемента (?)
            amp_sig = 1
            amp_dist = self.obj_factor.get_dist(num)
            amp_rand = self.obj_factor.get_randamp()
            # фазы для заданного элемента
            deg_rand = self.obj_factor.get_randphi()
            # цикл по углам обзора
            for j in range(vec_deg.shape[0]):
                deg = math.radians(vec_deg[j])
                amp_elem = self.obj_elem.get_gain(deg)
                amp = amp_sig * amp_elem * amp_dist * amp_rand
                self.vec_test[i][j] = self.obj_factor.get_signal(amp, deg, num, deg_rand)

    def calc_array(self, vec_time, vec_sigdeg, vec_sigamp, vec_sigbnd, vec_intdeg, vec_intamp, vec_intbnd, flag_mod):
        # вычисление векторов комплексных амплитуд и корреляционных матриц
        len_time, len_sig, len_int = vec_sigdeg.shape[0], vec_sigdeg.shape[1], vec_intdeg.shape[1]
        # расчёт векторов и параметров для эквивалентных сигналов и помех
        self.vec_eqdegsig, num_sig, eq4real0, pair4real0, bnd4real0 = self.obj_factor.get_eqvec(vec_sigdeg, vec_sigbnd)
        self.vec_eqdegint, num_int, eq4real1, pair4real1, bnd4real1 = self.obj_factor.get_eqvec(vec_intdeg, vec_intbnd)
        # количество сигналов (экв+реал), количество эквивалентных сигналов
        max_sig, max_eq4real0 = int(num_sig.max()), np.amax(eq4real0, axis=0)
        max_int, max_eq4real1 = int(num_int.max()), np.amax(eq4real1, axis=0)
        # вычисление векторов комплексных амплитуд
        self.vec_sig = self.get_vec(vec_sigamp, self.vec_eqdegsig, eq4real0, max_sig, max_eq4real0, len_time)
        self.vec_int = self.get_vec(vec_intamp, self.vec_eqdegint, eq4real1, max_int, max_eq4real1, len_time)
        self.vec_nois = self.obj_factor.get_vecnoise(vec_time)
        self.vec_sum = self.get_vecsum()
        # предапертурная обработка сигналов
        vec = self.obj_factor.get_preproc(self.vec_sig, self.vec_int, self.vec_nois, self.vec_sum, vec_time, flag_mod)
        self.vec_sig, self.vec_int, self.vec_nois, self.vec_sum = vec[0], vec[1], vec[2], vec[3]
        # вычисление корреляционных матриц
        self.matrix_sig, self.vec_coefsig = self.get_matrix(self.vec_sig, pair4real0, bnd4real0, max_sig, max_eq4real0, len_time)
        self.matrix_int, self.vec_coefint = self.get_matrix(self.vec_int, pair4real1, bnd4real1, max_int, max_eq4real1, len_time)
        self.matrix_nois = self.get_matrixnois(len_time)
        self.matrix_sum = self.matrix_sig + self.matrix_int + self.matrix_nois
        # коррекция амплитуд векторов сигналов и помех
        self.vec_sig = self.edit_vec(self.vec_sig, self.vec_coefsig, max_sig, len_time)
        self.vec_int = self.edit_vec(self.vec_int, self.vec_coefint, max_int, len_time)
        # комплексная огибающая с элемента решётки
        self.vec_sigcpl = self.vec_sig[:, :, 0].T
        self.vec_intcpl = self.vec_int[:, :, 0].T
        self.vec_sumcpl = self.vec_sum[:, :, 0].T

    def calc_snir(self):
        # вычислить временную зависимость осшп
        self.vec_snir = np.zeros(shape=[self.vec_sigcpl.shape[0], 1])
        # запускаем цикл по времени
        for i in range(self.vec_sigcpl.shape[0]):
            # перевод в мощности
            pow_sig = np.square(self.vec_sigcpl[i])
            pow_int = np.square(self.vec_intcpl[i])
            # вычисление осшп
            self.vec_snir[i][0] = self.get_pow2db(pow_sig.sum() / (pow_int.sum() + np.square(self.arr_noise)))
        # вычисление среднего осшп
        self.mean_snir = self.vec_snir.mean()

    def get_vec(self, vec_sigcpl, vec_eqdeg, vec_eq4real, max_sig, max_eq4real, len_time):
        # вычисление вектора сигнала для одного момента времени
        # инициализация вектора
        vec_sig = np.zeros(shape=[max_sig, len_time, self.arr_size], dtype=complex)
        # запускаем цикл по времени
        for t in range(len_time):
            index = 0
            # запускаем цикл по реальным сигналам
            for i in range(vec_sigcpl.shape[1]):
                # запускаем цикл по эквивалентным сигналам
                for j in range(int(vec_eq4real[t][i])):
                    # если сигнал попадает в сектор
                    if vec_eqdeg[t][i][j] != 361.0:
                        # запускаем цикл по элементам АР
                        for k in range(self.arr_size):
                            # вычисление текущего номера элемента
                            num = k + 1
                            # амплитуды для заданного элемента
                            amp_sig = vec_sigcpl[t][i]
                            amp_dist = self.obj_factor.get_dist(num)
                            amp_rand = self.obj_factor.get_randamp()
                            # фазы для заданного элемента
                            deg_rand = self.obj_factor.get_randphi()
                            # амплитуды для заданного угла обзора
                            deg = math.radians(vec_eqdeg[t][i][j])
                            amp_elem = self.obj_elem.get_gain(deg)
                            amp = amp_sig * amp_elem * amp_dist * amp_rand
                            vec_sig[index][t][k] = vec_sig[index][t][k] + self.obj_factor.get_signal(amp, deg, num, deg_rand)
                    index = index + 1
                index = int(max_eq4real[i])
        return vec_sig

    def get_matrix(self, vec, pair4real, bnd4real, max_sig, max_eq4real, len_time):
        # вычисление корреляционной матрицы для одного момента времени
        matrix = np.zeros(shape=[len_time, self.arr_size, self.arr_size], dtype=complex)
        vec_coef = np.zeros(shape=[max_sig, len_time])
        # запускаем цикл по времени
        for t in range(len_time):
            index = 0
            # запускаем цикл по реальным сигналам
            for i in range(pair4real.shape[1]):
                # запускаем цикл по эквивалентным парам
                for j in range(int(pair4real[t][i])+1):
                    # вычисление коэффициена дискретного разложения Фурье
                    coef_fourier = self.obj_factor.get_eqamp(pair4real[t][i], j, bnd4real[t][i])
                    if j == 0:
                        # расчёт корреляционной матрицы реального сигнала
                        var_vec = vec[index][t].T
                        matrix_buf = coef_fourier * np.outer(np.conj(var_vec), var_vec.T)
                        # суммирование матриц
                        matrix[t] = matrix[t] + matrix_buf
                        vec_coef[index][t] = coef_fourier
                        index = index + 1
                    else:
                        # расчёт корреляционной матрицы эквивалентных пар сигналов
                        var_vec0 = vec[index][t].T
                        var_vec1 = vec[index+1][t].T
                        matrix0_buf = np.outer(np.conj(var_vec0), var_vec0.T)
                        matrix1_buf = np.outer(np.conj(var_vec1), var_vec1.T)
                        matrix_buf = (coef_fourier / 2) * (matrix0_buf + matrix1_buf)
                        # суммирование матриц
                        matrix[t] = matrix[t] + matrix_buf
                        vec_coef[index][t] = coef_fourier / 2
                        vec_coef[index+1][t] = coef_fourier / 2
                        index = index + 2
                index = int(max_eq4real[i])
        return [matrix, vec_coef]

    def edit_vec(self, var_sig, var_coefsig, max_eqandreal, len_time):
        # умножение векторов на коэффициенты Фурье
        # запускаем цикл по времени
        for t in range(len_time):
            for i in range(max_eqandreal):
                var_sig[i][t] = var_sig[i][t] * math.sqrt(var_coefsig[i][t])
        return var_sig

    def get_matrixnois(self, len_time):
        # инициализация
        matrix = np.zeros(shape=[len_time, self.arr_size, self.arr_size], dtype=complex)
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление матриц шума
            if np.abs(self.vec_nois[0][i][0]) == 0:
                # матрица средней мощности (дисперсии) шума
                matrix[i] = np.eye(self.arr_size, dtype=complex) * math.pow(self.arr_noise, 2)
            else:
                # матрица мгновенной мощности шума
                var_vec = self.vec_nois[0][i]
                matrix[i] = np.diag(np.abs(var_vec)**2)
        return matrix

    def get_vecsum(self):
        # суммарный вектор комплексных амплитуд для каждого момента времени
        vec_sum = np.sum(self.vec_sig, axis=0) + np.sum(self.vec_int, axis=0) + np.sum(self.vec_nois, axis=0)
        return np.array([vec_sum])

    def get_pow2db(self, num):
        # перевод мощности в децибеллы
        return 10 * np.log10(abs(num))
