# модуль моделирования сигнального процессора

import pack_model.pack_processor as pp
from pack_model.pack_processor import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели сигнального процессора (L2)")
    print("Модуль использует пакет:", pp.NAME)

class Processor:
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
        res.append(self.time_calc)
        return res
    def print(self):
        print(" --- Параметры модели сигнального процессора (L2) --- ")
        print("id = ", self.id)
        print("id_type = ", self.id_type)
        print("id_crit = ", self.id_crit)
        print("id_alg = ", self.id_alg)
        print("time_calc = ", self.time_calc)
        self.list_tradalg.print_short()
        self.list_neuroalg.print_short()
        self.list_kalman.print_short()
    def print_short(self):
        print(" --- Параметры модели сигнального процессора (L2) --- ")
        print("processor = ", self.get())
    def calc_out(self, out_array):
        len_num = out_array[0].shape[0]
        self.vec_amp1 = np.ones(shape=[len_num], dtype=complex)
        self.vec_phi1 = np.zeros(shape=[len_num], dtype=complex)
        self.vec_weight1 = self.vec_amp1  # не корректно, ради теста!
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
        print("Размерности векторов ВК:")
        print("vec_amp1.shape = ", self.vec_amp1.shape)
        print("vec_phi1.shape = ", self.vec_phi1.shape)
        print("vec_weight1.shape = ", self.vec_weight1.shape)
        print("vec_amp2.shape = ", self.vec_amp2.shape)
        print("vec_phi2.shape = ", self.vec_phi2.shape)
        print("vec_weight2.shape = ", self.vec_weight2.shape)
    def calc_optout(self, out_array):
        len_time = out_array[1].shape[0]
        len_num = out_array[1].shape[2]
        self.vec_amp2 = np.zeros(shape=[len_time, len_num], dtype=complex)
        self.vec_phi2 = np.zeros(shape=[len_time, len_num], dtype=complex)
        self.vec_weight2 = np.zeros(shape=[len_time, len_num], dtype=complex)
        # запускаем цикл по времени
        #for i in range(len_time):

