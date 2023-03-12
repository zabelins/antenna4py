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

    def __init__(self):
        self.obj_trad = pp.trad.Trad_alg()
        self.obj_neuro = pp.neuro.Neuro_alg()
        self.obj_kalman = pp.kalman.Kalman()
        # номера критерия и алгоритма адаптации
        self.alg_crit = 0
        self.alg_type = 0
        self.alg_delay = 0
        # тип управления
        self.ctl_type = 0
        # вектора весов и осшп
        self.vec_inweight = np.array([])
        self.vec_insnir = np.array([])
        self.vec_outweight = np.array([])
        self.vec_outsnir = np.array([])
        # усреднённые осшп
        self.mean_insnir = np.array([])
        self.mean_outsnir = np.array([])

    def set(self, init):
        self.alg_crit = init[0]
        self.alg_type = init[1]
        self.alg_delay = init[2]
        self.ctl_type = init[5]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.alg_type)
        res.append(self.alg_delay)
        res.append(self.ctl_type)
        return res

    def print(self):
        print("Параметры модели сигнального процессора (L2):")
        print("\talg_crit = ", self.alg_crit)
        print("\talg_type = ", self.alg_type)
        print("\talg_delay = ", self.alg_delay)
        print("\tctl_type = ", self.ctl_type)
        self.obj_trad.print()
        self.obj_neuro.print()
        self.obj_kalman.print()

    def calc_out(self, out_array):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois, vec_sum = out_array[8], out_array[9], out_array[10], out_array[11]
        matrix_sig, matrix_int, matrix_nois, matrix_sum = out_array[12], out_array[13], out_array[14], out_array[15]
        # фильтр Калмана
        matrix_sig, matrix_int, matrix_nois = self.obj_kalman.get_matrix(matrix_sig, matrix_int, matrix_nois)
        # вычисление векторов ВК
        self.calc_weights(vec_sig, matrix_sig, matrix_int, matrix_nois, vec_sum)
        # учёт задержки на вычисления
        self.calc_delay()
        # вычисление ОСШП
        self.calc_snir(matrix_sig, matrix_int, matrix_nois)

    def get_out(self):
        out_proc = []
        out_proc.append(self.vec_inweight)
        out_proc.append(self.vec_outweight)
        out_proc.append(self.vec_insnir)
        out_proc.append(self.vec_outsnir)
        out_proc.append(self.mean_insnir)
        out_proc.append(self.mean_outsnir)
        return out_proc

    def print_out(self):
        # проверка типа векторов на ndarray
        condit_1 = cl.is_ndarray([self.vec_inweight, self.vec_outweight])
        condit_2 = cl.is_ndarray([self.vec_insnir, self.vec_outsnir])
        # вывод размерностей векторов
        if condit_1 and condit_2:
            print("Сигнальный процессор:")
            print("\tvec_inweight.shape = ", self.vec_inweight.shape)
            print("\tvec_outweight.shape = ", self.vec_outweight.shape)
            print("\tvec_insnir.shape = ", self.vec_insnir.shape)
            print("\tvec_outsnir.shape = ", self.vec_outsnir.shape)
            print("\tmean_insnir.shape = ", 1)
            print("\tmean_outsnir.shape = ", 1)
        else:
            print("Ошибка проверки векторов сигнального процессора")

    def calc_weights(self, vec_sig, matrix_sig, matrix_int, matrix_nois, vec_sum):
        # вычисление весовых коэффициентов ААР
        # начало фиксации времени
        start_time = time.time()
        # начальные веса
        self.vec_inweight = np.conj(vec_sig[0][0]) / np.real(vec_sig[0][0][0])
        # оптимальные веса
        if self.alg_type == 0:
            # традиционные алгоритмы
            self.vec_outweight = self.obj_trad.get_weights(vec_sig, matrix_sig, matrix_int, matrix_nois)
        elif self.alg_type == 1:
            # нейросетевые алгоритмы
            self.vec_outweight = self.obj_neuro.get_weights(vec_sum[0])
        # конец фиксации времени
        print("time_adapt = ", time.time() - start_time)

    def calc_snir(self, matrix_sig, matrix_int, matrix_nois):
        # вычисление осшп
        len_time = matrix_sig.shape[0]
        self.vec_insnir = np.zeros(shape=[len_time, 1])
        self.vec_outsnir = np.zeros(shape=[len_time, 1])
        vec_ininr = np.zeros(shape=[len_time, 1])
        # цикл по времени
        for i in range(len_time):
            # мощности до оптимизации
            pow_insig = self.obj_trad.get_power(self.vec_inweight, matrix_sig[i])
            pow_inint = self.obj_trad.get_power(self.vec_inweight, matrix_int[i])
            pow_innois = self.obj_trad.get_power(self.vec_inweight, matrix_nois[i])
            # мощности после оптимизации
            pow_outsig = self.obj_trad.get_power(self.vec_outweight[i], matrix_sig[i])
            pow_outint = self.obj_trad.get_power(self.vec_outweight[i], matrix_int[i])
            pow_outnois = self.obj_trad.get_power(self.vec_outweight[i], matrix_nois[i])
            # вычисление осшп
            self.vec_insnir[i][0] = self.get_pow2db(abs(pow_insig)/(abs(pow_inint)+abs(pow_innois)))
            self.vec_outsnir[i][0] = self.get_pow2db(abs(pow_outsig) / (abs(pow_outint) + abs(pow_outnois)))
            vec_ininr[i][0] = self.get_pow2db(abs(pow_inint) / abs(pow_outnois))
        # вычисление среднего осшп
        self.mean_insnir = np.mean(self.vec_insnir)
        self.mean_outsnir = np.mean(self.vec_outsnir)
        mean_ininr = np.mean(vec_ininr)
        print("mean_ininr = ", mean_ininr)

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





