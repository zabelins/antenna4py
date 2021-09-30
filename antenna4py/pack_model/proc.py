import pack_model.pack_processor as pp
from pack_model.pack_processor import *
import pack_calc.calc_list as cl
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели сигнального процессора (L2)")
    print("Модуль использует пакет:", pp.NAME)

class Proc:
    """Класс моделирования сигнального процессора адаптивной антенны"""

    def __init__(self, id):
        self.list_trad = pp.trad.Trad_alg(1)
        self.list_neuro = pp.neuro.Neuro_alg(1)
        self.list_kalman = pp.kalman.Kalman(1)
        self.id = id
        # номера критерия и алгоритма адаптации
        self.alg_crit = []
        self.alg_type = []
        self.alg_delay = []
        # тип управления
        self.control_type = []
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
        res.append(self.control_type)
        return res

    def print(self):
        print("Параметры модели сигнального процессора (L2):")
        print("\talg_crit = ", self.alg_crit)
        print("\talg_type = ", self.alg_type)
        print("\tcontrol_type = ", self.control_type)
        self.list_trad.print()
        self.list_neuro.print()
        self.list_kalman.print()

    def calc_out(self, out_array2nd):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = out_array2nd[0], out_array2nd[1], out_array2nd[2]
        matrix_sig, matrix_int, matrix_nois = out_array2nd[3], out_array2nd[4], out_array2nd[5]
        # фильтр Калмана
        buf = self.list_kalman.calc_matrix(matrix_sig, matrix_int, matrix_nois)
        matrix_sig, matrix_int, matrix_nois = buf
        # вычисление векторов ВК
        self.calc_weights(vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois)
        # учёт задержки на вычисления
        self.calc_delay()
        # вычисление ОСШП
        self.calc_snir(matrix_sig, matrix_int, matrix_nois)

    def get_out1nd(self):
        # получить вектора для отрисовки ДН
        res = []
        res.append(self.vec_insnir)
        res.append(self.vec_outsnir)
        res.append(self.mean_insnir)
        res.append(self.mean_outsnir)
        return res

    def get_out2nd(self):
        # получить вектора для вычислений
        res = []
        res.append(self.vec_inweight)
        res.append(self.vec_outweight)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_insnir, self.vec_outsnir, self.mean_insnir, self.mean_outsnir])
        bool_res2 = cl.is_ndarray([self.vec_inweight, self.vec_outweight])
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True):
            print("Размерности векторов ВК:")
            print("\tvec_insnir.shape = ", self.vec_insnir.shape)
            print("\tvec_outsnir.shape = ", self.vec_outsnir.shape)
            print("\tmean_insnir.shape = ", self.mean_insnir.shape)
            print("\tmean_outsnir.shape = ", self.mean_outsnir.shape)
            print("\tvec_inweight.shape = ", self.vec_inweight.shape)
            print("\tvec_outweight.shape = ", self.vec_outweight.shape)
        else:
            print("Ошибка проверки типа векторов ВК")

    def calc_weights(self, vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois):
        # вычисление весовых коэффициентов ААР
        len_time, len_num = [vec_sig.shape[0], vec_sig.shape[2]]
        # определение размерности векторов
        self.vec_inweight = np.ones(shape=[len_num], dtype=complex)
        self.vec_outweight = np.ones(shape=[len_time, len_num], dtype=complex)
        # вычисление оптимальных векторов
        if (self.alg_type == 1):
            # алгоритм прямого обращения матрицы
            self.vec_outweight = self.list_trad.get_invers(vec_sig, matrix_sig, matrix_int, matrix_nois)
        if (self.alg_type == 2):
            # нейросетевой алгоритм вычисления ВК
            self.vec_outweight = np.ones(shape=[len_time, len_num], dtype=complex)

    def calc_snir(self, matrix_sig, matrix_int, matrix_nois):
        # вычисление осшп
        len_time = matrix_sig.shape[0]
        # инициализируем размеры векторов
        self.vec_insnir = np.zeros(shape=[len_time])
        self.vec_outsnir = np.zeros(shape=[len_time])
        self.mean_insnir = np.zeros(shape=[1])
        self.mean_outsnir = np.zeros(shape=[1])
        # цикл по времени
        for i in range(len_time):
            # мощности до оптимизации
            power_insig = self.list_trad.calc_power(self.vec_inweight, matrix_sig[i])
            power_inint = self.list_trad.calc_power(self.vec_inweight, matrix_int[i])
            power_innois = self.list_trad.calc_power(self.vec_inweight, matrix_nois[i])
            # мощности после оптимизации
            power_outsig = self.list_trad.calc_power(self.vec_outweight[i], matrix_sig[i])
            power_outint = self.list_trad.calc_power(self.vec_outweight[i], matrix_int[i])
            power_outnois = self.list_trad.calc_power(self.vec_outweight[i], matrix_nois[i])
            # вычисление осшп
            self.vec_insnir[i] = abs(power_insig) / (abs(power_inint) + abs(power_innois))
            self.vec_outsnir[i] = abs(power_outsig) / (abs(power_outint) + abs(power_outnois))
            self.mean_insnir = self.mean_insnir + self.vec_insnir[i]
            self.mean_outsnir = self.mean_outsnir + self.vec_outsnir[i]
        # деление на общее количество
        self.mean_insnir = self.mean_insnir / len_time
        self.mean_outsnir = self.mean_outsnir / len_time

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






