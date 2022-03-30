import pack_model.pack_proc as pp
from pack_model.pack_proc import *
import pack_calc.calc_list as cl
import numpy as np
import time

if __name__ == "__main__":
    print("Вы запустили модуль модели сигнального процессора (L2)")
    print("Модуль использует пакет:", pp.NAME)

class Proc:
    """Класс моделирования сигнального процессора адаптивной антенны"""

    def __init__(self, id):
        self.obj_trad = pp.trad.Trad_alg(1)
        self.obj_neuro = pp.neuro.Neuro_alg(1)
        self.obj_kalman = pp.kalman.Kalman(1)
        self.id = id
        # номера критерия и алгоритма адаптации
        self.alg_crit = []
        self.alg_type = []
        self.alg_delay = []
        # тип управления
        self.control_type = []
        # суммарный входной вектор
        self.vec_sum = []
        # вектора весов и осшп
        self.vec_inweight = []
        self.vec_insnir = []
        self.vec_outweight = []
        self.vec_outsnir = []
        # усреднённые осшп
        self.mean_insnir = []
        self.mean_outsnir = []

    def set(self, init):
        self.alg_crit = init[0]
        self.alg_type = init[1]
        self.alg_delay = init[2]
        self.control_type = init[5]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.alg_type)
        res.append(self.alg_delay)
        res.append(self.control_type)
        return res

    def print(self):
        print("Параметры модели сигнального процессора (L2):")
        print("\talg_crit = ", self.alg_crit)
        print("\talg_type = ", self.alg_type)
        print("\talg_delay = ", self.alg_delay)
        print("\tcontrol_type = ", self.control_type)
        self.obj_trad.print()
        self.obj_neuro.print()
        self.obj_kalman.print()

    def calc_out(self, out_array):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = out_array[5], out_array[6], out_array[7]
        matrix_sig, matrix_int, matrix_nois = out_array[8], out_array[9], out_array[10]
        # суммирование векторов
        self.get_vecsum(vec_sig, vec_int, vec_nois)
        # начало фиксации времени
        start_time = time.time()
        # фильтр Калмана
        matrix_sig, matrix_int, matrix_nois = self.obj_kalman.calc_matrix(matrix_sig, matrix_int, matrix_nois)
        # вычисление векторов ВК
        self.calc_weights(vec_sig, matrix_sig, matrix_int, matrix_nois)
        # конец фиксации времени
        print("time_adapt = ", time.time() - start_time)
        # учёт задержки на вычисления
        self.calc_delay()
        # вычисление ОСШП
        self.calc_snir(matrix_sig, matrix_int, matrix_nois)

    def get_out(self):
        out_proc = []
        out_proc.append(self.vec_sum)
        out_proc.append(self.vec_inweight)
        out_proc.append(self.vec_outweight)
        out_proc.append(self.vec_insnir)
        out_proc.append(self.vec_outsnir)
        out_proc.append(self.mean_insnir)
        out_proc.append(self.mean_outsnir)
        return out_proc

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_sum, self.vec_inweight, self.vec_outweight])
        bool_res2 = cl.is_ndarray([self.vec_insnir, self.vec_outsnir])
        # вывод размерностей векторов
        if bool_res1 == True and bool_res2 == True:
            print("Размерности векторов ВК:")
            print("\tvec_sum.shape = ", self.vec_sum.shape)
            print("\tvec_inweight.shape = ", self.vec_inweight.shape)
            print("\tvec_outweight.shape = ", self.vec_outweight.shape)
            print("\tvec_insnir.shape = ", self.vec_insnir.shape)
            print("\tvec_outsnir.shape = ", self.vec_outsnir.shape)
            print("\tmean_insnir.shape = ", 1)
            print("\tmean_outsnir.shape = ", 1)
        else:
            print("Ошибка проверки типа векторов ВК")

    def calc_weights(self, vec_sig, matrix_sig, matrix_int, matrix_nois):
        # вычисление весовых коэффициентов ААР
        len_time, len_num = [vec_sig.shape[0], vec_sig.shape[2]]
        # определение размерности векторов
        self.vec_inweight = np.ones(shape=[len_num], dtype=complex)
        self.vec_outweight = np.ones(shape=[len_time, len_num], dtype=complex)
        # вычисление оптимальных векторов
        if self.alg_type == 0:
            # алгоритм прямого обращения матрицы
            self.vec_outweight = self.obj_trad.calc_out(vec_sig, matrix_sig, matrix_int, matrix_nois)
        if self.alg_type == 1:
            # нейросетевой алгоритм вычисления ВК
            self.vec_outweight = self.obj_neuro.calc_out(self.vec_sum)

    def calc_snir(self, matrix_sig, matrix_int, matrix_nois):
        # вычисление осшп
        len_time = matrix_sig.shape[0]
        # инициализируем размеры векторов
        self.vec_insnir = np.zeros(shape=[len_time, 1])
        self.vec_outsnir = np.zeros(shape=[len_time, 1])
        self.mean_insnir = np.zeros(shape=[1])
        self.mean_outsnir = np.zeros(shape=[1])
        # цикл по времени
        for i in range(len_time):
            # мощности до оптимизации
            power_insig = self.obj_trad.calc_power(self.vec_inweight, matrix_sig[i])
            power_inint = self.obj_trad.calc_power(self.vec_inweight, matrix_int[i])
            power_innois = self.obj_trad.calc_power(self.vec_inweight, matrix_nois[i])
            # мощности после оптимизации
            power_outsig = self.obj_trad.calc_power(self.vec_outweight[i], matrix_sig[i])
            power_outint = self.obj_trad.calc_power(self.vec_outweight[i], matrix_int[i])
            power_outnois = self.obj_trad.calc_power(self.vec_outweight[i], matrix_nois[i])
            # вычисление осшп
            self.vec_insnir[i][0] = self.get_pow2db(abs(power_insig)/(abs(power_inint)+abs(power_innois)))
            self.vec_outsnir[i][0] = self.get_pow2db(abs(power_outsig) / (abs(power_outint) + abs(power_outnois)))
        # вычисление среднего осшп
        self.mean_insnir = np.mean(self.vec_insnir)
        self.mean_outsnir = np.mean(self.vec_outsnir)

    def calc_delay(self):
        # вычисление задержки по времени на вычисления
        if self.alg_delay == 1:
            # если есть задержка на 1 такт
            len_time, len_num = self.vec_outweight.shape[0], self.vec_outweight.shape[1]
            buf_outweight = np.ones(shape=[len_time, len_num], dtype=complex)
            # округление до целого
            self.alg_delay = int(self.alg_delay)
            # цикл по времени
            for i in range(len_time):
                if i == 0:
                    buf_outweight[i] = self.vec_inweight
                else:
                    buf_outweight[i] = self.vec_outweight[i-1]
            # перезапись оптимальных весов
            self.vec_outweight = buf_outweight

    def get_pow2db(self, num):
        # перевод мощности в децибеллы
        return 10 * np.log10(abs(num))

    def get_vecsum(self, vec_sig, vec_int, vec_nois):
        # суммируем вектора для каждого момента времени
        len_time, len_num = vec_sig.shape[0], vec_sig.shape[2]
        self.vec_sum = np.zeros(shape=[len_time, len_num], dtype=complex)
        # суммируем вектора для каждого момента времени
        for i in range(len_time):
            self.vec_sum[i] = self.get_varsum(vec_sig[i], vec_int[i], vec_nois[i])

    def get_varsum(self, vec_sig, vec_int, vec_nois):
        # суммарный входной вектор на ААР в заданный момент времени
        len_num = vec_sig.shape[1]
        vec_sum = np.zeros(shape=[len_num], dtype=complex)
        vec_sum = vec_sum + np.sum(vec_sig, axis=0)
        vec_sum = vec_sum + np.sum(vec_int, axis=0)
        #vec_sum = vec_sum + np.sum(vec_nois, axis=0)
        return vec_sum





