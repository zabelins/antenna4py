import pack_model.pack_environment as pe
from pack_model.pack_environment import *
import pack_calc.calc_list as cl
import numpy as np
import math

if __name__ == "__main__":
    print("Вы запустили модуль модели сигналов и помех (L2)")
    print("Модуль использует пакет:", pe.NAME)

class Env:
    """Класс моделирования сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.list_gen = pe.signal_generator.Generator(1)
        self.id = id
        # параметры сигналов
        self.sig_deg = []
        self.sig_amp = []
        self.sig_band = []
        # параметры помех
        self.int_deg = []
        self.int_amp = []
        self.int_band = []
        # параметры шума
        self.nois_amp = []
        # врменные вектора сигналов
        self.vec_sigdeg = []
        self.vec_sigamp = []
        self.vec_sigband = []
        # врменные вектора помех
        self.vec_intdeg = []
        self.vec_intamp = []
        self.vec_intband = []
        # врменные вектора шума
        self.vec_noisamp = []

    def set(self, init):
        self.sig_deg = np.array(init[0])
        self.sig_amp = np.array(init[1])
        self.sig_band = np.array(init[2])
        self.int_deg = np.array(init[3])
        self.int_amp = np.array(init[4])
        self.int_band = np.array(init[5])
        self.nois_amp = np.array(init[6])

    def get(self):
        res = []
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_band)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_band)
        res.append(self.nois_amp)
        return res

    def print(self):
        print("Параметры модели сигналов и помех (L2):")
        print("\tsig_deg = ", self.sig_deg)
        print("\tsig_amp = ", self.sig_amp)
        print("\tsig_band = ", self.sig_band)
        print("\tint_deg = ", self.int_deg)
        print("\tint_amp = ", self.int_amp)
        print("\tint_band = ", self.int_band)
        print("\tnois_amp = ", self.nois_amp)
        self.list_gen.print()

    def calc_out(self, out_set, f_cen, par_band, id_script):
        # распаковка исходных данных
        vec_time = out_set[1]
        # определение необходимой модуляции для заданного динамического сценария
        id_intamp, id_intdeg, id_intband, freq_mod = 0, 0, 0, 0
        if (id_script >= 1) and (id_script <= 3):
            # если амплитудная модуляция
            id_intamp = id_script
            freq_mod = f_cen * 2 / math.pow(10, 3)
        elif (id_script == 4):
            # если изменение углов
            id_intdeg = 1
            self.int_deg, self.int_amp, self.int_band = np.array([90]), np.array([1]), np.array([par_band])
        elif (id_script == 5):
            # если рандомные помехи, максимальная полоса 10%
            id_intamp, id_intdeg, id_intband = 4, 2, 1
            max_band = f_cen / 10
            self.int_deg, self.int_amp, self.int_band = np.array([90]), np.array([1]), np.array([max_band])
        elif (id_script == 6):
            # если параметрическое моделирование - изменение углов
            id_intdeg = 1
            self.int_deg, self.int_amp, self.int_band = np.array([90]), np.array([1]), np.array([par_band])
        # создаём вектора изменения сигналов от времени
        self.vec_sigdeg = self.list_gen.get_vecdeg(vec_time, self.sig_deg, 0)
        self.vec_sigamp = self.list_gen.get_vecamp(vec_time, self.sig_amp, freq_mod, 0)
        self.vec_sigband = self.list_gen.get_vecband(vec_time, self.sig_band, 0)
        # создаём вектора изменения помех от времени
        self.vec_intdeg = self.list_gen.get_vecdeg(vec_time, self.int_deg, id_intdeg)
        self.vec_intamp = self.list_gen.get_vecamp(vec_time, self.int_amp, freq_mod, id_intamp)
        self.vec_intband = self.list_gen.get_vecband(vec_time, self.int_band, id_intband)
        # создаём вектора изменения шума от времени
        self.vec_noisamp = self.list_gen.get_vecamp(vec_time, self.nois_amp, freq_mod, 0)

    def get_out(self):
        res = []
        res.append(self.vec_sigdeg)
        res.append(self.vec_sigamp)
        res.append(self.vec_sigband)
        res.append(self.vec_intdeg)
        res.append(self.vec_intamp)
        res.append(self.vec_intband)
        res.append(self.vec_noisamp)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_sigdeg, self.vec_sigamp, self.vec_sigband])
        bool_res2 = cl.is_ndarray([self.vec_intdeg, self.vec_intamp, self.vec_intband, self.vec_noisamp])
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True):
            print("Размерности векторов сигналов и помех от времени:")
            print("\tvec_sigdeg.shape = ", self.vec_sigdeg.shape)
            print("\tvec_sigamp.shape = ", self.vec_sigamp.shape)
            print("\tvec_sigband.shape = ", self.vec_sigband.shape)
            print("\tvec_intdeg.shape = ", self.vec_intdeg.shape)
            print("\tvec_intamp.shape = ", self.vec_intamp.shape)
            print("\tvec_intband.shape = ", self.vec_intband.shape)
            print("\tvec_noisamp.shape = ", self.vec_noisamp.shape)
        else:
            print("Ошибка проверки типа векторов сигналов и помех от времени")


