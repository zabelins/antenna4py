# модуль модели сигналов и помех

import pack_model.pack_environment as pe
from pack_model.pack_environment import *
import pack_calc.calc_list as cl
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели сигналов и помех (L2)")
    print("Модуль использует пакет:", pe.NAME)

class Env:
    def __init__(self, id):
        self.id = id
        self.id_config = []
        self.mod_sig = []
        self.mod_int = []
        self.deg_sig = []
        self.deg_int = []
        self.am_sig = []
        self.am_int = []
        self.am_nois = []
        self.fband_sig = []
        self.fband_int = []
        self.vec_degsig = []
        self.vec_degint = []
        self.vec_amsig = []
        self.vec_amint = []
        self.vec_amnois = []
        self.vec_fbandsig = []
        self.vec_fbandint = []
        self.list_gen = pe.signal_generator.Generator(1)
    def set(self, init):
        self.id_config = np.array(init[1])
        self.mod_sig = np.array(init[2])
        self.mod_int = np.array(init[6])
        self.deg_sig = np.array(init[3])
        self.deg_int = np.array(init[7])
        self.am_sig = np.array(init[4])
        self.am_int = np.array(init[8])
        self.am_nois = np.array(init[10])
        self.fband_sig = np.array(init[5])
        self.fband_int = np.array(init[9])
    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_config)
        res.append(self.mod_sig)
        res.append(self.mod_int)
        res.append(self.deg_sig)
        res.append(self.deg_int)
        res.append(self.am_sig)
        res.append(self.am_int)
        res.append(self.am_nois)
        res.append(self.fband_sig)
        res.append(self.fband_int)
        return res
    def print(self):
        print(" --- Параметры модели сигналов и помех (L2) --- ")
        print("id = ", self.id)
        print("id_config = ", self.id_config)
        print("mod_sig = ", self.mod_sig)
        print("mod_int = ", self.mod_int)
        print("deg_sig = ", self.deg_sig)
        print("deg_int = ", self.deg_int)
        print("am_sig = ", self.am_sig)
        print("am_int = ", self.am_int)
        print("am_nois = ", self.am_nois)
        print("fband_sig = ", self.fband_sig)
        print("fband_int = ", self.fband_int)
        self.list_gen.print_short()
    def print_short(self):
        print(" --- Параметры модели сигналов и помех (L2) --- ")
        print("environment = ", self.get())
    def calc_out(self, out_set):
        # распаковка исходных данных
        vec_time, vec_var = [out_set[1], out_set[1]]
        # создаём единичный вектор без модуляции
        vec_ones = np.ones(vec_time.shape[0])
        # создаём вектора изменения сигналов и помех от времени
        self.vec_degsig = cl.ones_modul(vec_ones, self.deg_sig)
        self.vec_degint = cl.ones_modul(vec_ones, self.deg_int)
        self.vec_amsig = cl.ones_modul(vec_ones, self.am_sig)
        self.vec_amint = cl.ones_modul(vec_ones, self.am_int)
        self.vec_amnois = cl.ones_modul(vec_ones, self.am_nois)
        self.vec_fbandsig = cl.ones_modul(vec_ones, self.fband_sig)
        self.vec_fbandint = cl.ones_modul(vec_ones, self.fband_int)
        # нужно добавить разные типы расстановки помех
        # нужно добавить разные типы амплитудных модуляций
        # нужно добавить разные типы частотных модуляций
        # нужно придумать также зависимость от параметра
    def get_out(self):
        res = []
        res.append(self.vec_degsig)
        res.append(self.vec_degint)
        res.append(self.vec_amsig)
        res.append(self.vec_amint)
        res.append(self.vec_amnois)
        res.append(self.vec_fbandsig)
        res.append(self.vec_fbandint)
        return res
    def print_out(self):
        print("Размерности векторов сигналов и помех от времени:")
        print("vec_degsig.shape = ", self.vec_degsig.shape)
        print("vec_degint.shape = ", self.vec_degint.shape)
        print("vec_amsig.shape = ", self.vec_amsig.shape)
        print("vec_amint.shape = ", self.vec_amint.shape)
        print("vec_amnois.shape = ", self.vec_amnois.shape)
        print("vec_fbandsig.shape = ", self.vec_fbandsig.shape)
        print("vec_fbandint.shape = ", self.vec_fbandint.shape)

