import pack_model.pack_processor as pp
from pack_model.pack_processor import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели сигнального процессора (L2)")
    print("Модуль использует пакет:", pp.NAME)

class Proc:
    """Класс моделирования сигнального процессора адаптивной антенны"""

    def __init__(self, id):
        self.id = id
        self.adapt_type = []
        self.alg_crit = []
        self.alg_type = []
        self.vec_weights1 = []
        self.vec_weights2 = []
        self.list_trad = pp.trad.Trad_alg(1)
        self.list_neuro = pp.neuro.Neuro_alg(1)
        self.list_kalman = pp.kalman.Kalman(1)

    def set(self, init):
        self.adapt_type = init[1]
        self.alg_crit = init[2]
        self.alg_type = init[3]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.adapt_type)
        res.append(self.alg_crit)
        res.append(self.alg_type)
        return res

    def print(self):
        print(" --- Параметры модели сигнального процессора (L2) --- ")
        print("id = ", self.id)
        print("adapt_type = ", self.adapt_type)
        print("alg_crit = ", self.alg_crit)
        print("alg_type = ", self.alg_type)
        self.list_trad.print_short()
        self.list_neuro.print_short()
        self.list_kalman.print_short()

    def print_short(self):
        print(" --- Параметры модели сигнального процессора (L2) --- ")
        print("proc = ", self.get())

    def calc_out(self, out_array):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = [out_array[1], out_array[2], out_array[3]]
        matrix_sig, matrix_int, matrix_nois = [out_array[4], out_array[5], out_array[6]]
        # вычисление векторов ВК
        self.calc_weights(vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois)

    def get_out(self):
        res = []
        res.append(self.vec_weights1)
        res.append(self.vec_weights2)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_buf1 = isinstance(self.vec_weights1, np.ndarray)
        bool_buf2 = isinstance(self.vec_weights2, np.ndarray)
        # вывод размерностей векторов
        if (bool_buf1 == True) and (bool_buf2 == True):
            print("Размерности векторов ВК:")
            print("vec_weights1.shape = ", self.vec_weights1.shape)
            print("vec_weights2.shape = ", self.vec_weights2.shape)
        else:
            print("Ошибка проверки типа векторов ВК")

    def calc_weights(self, vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois):
        # вычисление весовых коэффициентов ААР
        len_time, len_num = [vec_sig.shape[0], vec_sig.shape[2]]
        # определение размерности векторов
        self.vec_weights1 = np.ones(shape=[len_num], dtype=complex)
        self.vec_weights2 = np.ones(shape=[len_time, len_num], dtype=complex)
        # вычисление оптимальных векторов
        if (self.alg_type == 1):
            # алгоритм прямого обращения матрицы
            self.vec_weights2 = self.list_trad.get_invers(vec_sig, matrix_sig, matrix_int, matrix_nois)
        if (self.alg_type == 2):
            # нейросетевой алгоритм вычисления ВК
            self.vec_weights2 = np.ones(shape=[len_time, len_num], dtype=complex)








