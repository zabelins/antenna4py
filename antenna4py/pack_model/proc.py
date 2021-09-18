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
        self.id_type = []
        self.id_crit = []
        self.id_alg = []
        self.time_calc = []
        self.vec_amp1 = []
        self.vec_phi1 = []
        self.vec_weight1 = []
        self.vec_amp2 = []
        self.vec_phi2 = []
        self.vec_weight2 = []
        self.list_tradalg = pp.trad_alg.Trad_alg(1)
        self.list_neuroalg = pp.nn_alg.Neuro_alg(1)
        self.list_kalman = pp.kalman.Kalman(1)

    def set(self, init):
        self.id_type = init[1]
        self.id_crit = init[2]
        self.id_alg = init[3]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_type)
        res.append(self.id_crit)
        res.append(self.id_alg)
        return res

    def print(self):
        print(" --- Параметры модели сигнального процессора (L2) --- ")
        print("id = ", self.id)
        print("id_type = ", self.id_type)
        print("id_crit = ", self.id_crit)
        print("id_alg = ", self.id_alg)
        self.list_tradalg.print_short()
        self.list_neuroalg.print_short()
        self.list_kalman.print_short()

    def print_short(self):
        print(" --- Параметры модели сигнального процессора (L2) --- ")
        print("proc = ", self.get())

    def calc_out(self, out_array):
        # распаковка исходных данных
        vec_test = out_array[0]
        vec_sig, vec_int, vec_nois = [out_array[1], out_array[2], out_array[3]]
        matrix_sig, matrix_int, matrix_nois = [out_array[4], out_array[5], out_array[6]]
        # вычисление начального вектора ВК
        self.calc_strartWC(vec_test)
        # вычисление оптимальных векторов ВК
        self.calc_optimWC(vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois)

    def get_out(self):
        res = []
        res.append(self.vec_amp1)
        res.append(self.vec_phi1)
        res.append(self.vec_weight1)
        res.append(self.vec_amp2)
        res.append(self.vec_phi2)
        res.append(self.vec_weight2)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_buf1 = isinstance(self.vec_amp1, np.ndarray)
        bool_buf2 = isinstance(self.vec_phi1, np.ndarray)
        bool_buf3 = isinstance(self.vec_weight1, np.ndarray)
        bool_buf4 = isinstance(self.vec_amp2, np.ndarray)
        bool_buf5 = isinstance(self.vec_phi2, np.ndarray)
        bool_buf6 = isinstance(self.vec_weight2, np.ndarray)
        bool_res1 = (bool_buf1 == True) and (bool_buf2 == True) and (bool_buf3 == True)
        bool_res2 = (bool_buf4 == True) and (bool_buf5 == True) and (bool_buf6 == True)
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True):
            print("Размерности векторов ВК:")
            print("vec_amp1.shape = ", self.vec_amp1.shape)
            print("vec_phi1.shape = ", self.vec_phi1.shape)
            print("vec_weight1.shape = ", self.vec_weight1.shape)
            print("vec_amp2.shape = ", self.vec_amp2.shape)
            print("vec_phi2.shape = ", self.vec_phi2.shape)
            print("vec_weight2.shape = ", self.vec_weight2.shape)
        else:
            print("Ошибка проверки типа векторов ВК")

    def calc_strartWC(self, vec_test):
        # вычисление начального вектора ВК
        len_num = vec_test.shape[0]
        self.vec_amp1 = np.ones(shape=[len_num], dtype=complex)
        self.vec_phi1 = np.zeros(shape=[len_num], dtype=complex)
        self.vec_weight1 = self.vec_amp1  # не корректно, ради теста!

    def calc_optimWC(self, vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois):
        # вычисление оптимального вектора ВК
        len_time, len_num = [vec_sig.shape[0], vec_sig.shape[2]]
        self.vec_amp2 = np.zeros(shape=[len_time, len_num], dtype=complex)
        self.vec_phi2 = np.zeros(shape=[len_time, len_num], dtype=complex)
        self.vec_weight2 = np.zeros(shape=[len_time, len_num], dtype=complex)
        # запускаем цикл по времени
        for i in range(len_time):
            mu = abs(matrix_nois[i][0][0])
            matrix = np.linalg.inv(matrix_int[i] + matrix_nois[i])
            vector = np.conj(vec_sig[i][0])
            self.vec_weight2[i] = mu * matrix.dot(vector)
        #print(self.vec_weight2)

    def calc_weights(self):
        # вычисление весовых коэффициентов ААР
        pass


