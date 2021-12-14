import pack_model.pack_env as pe
from pack_model.pack_env import *
import pack_calc.calc_list as cl
import numpy as np
import math

if __name__ == "__main__":
    print("Вы запустили модуль модели сигналов и помех (L2)")
    print("Модуль использует пакет:", pe.NAME)

class Env:
    """Класс моделирования сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.obj_gen = pe.signal_generator.Generator(1)
        self.id = id
        # параметры сигналов
        self.sig_deg = []
        self.sig_amp = []
        self.sig_band = []
        # параметры помех
        self.int_deg = []
        self.int_amp = []
        self.int_band = []
        # параметры модуляции
        self.shift_dynamic = []
        self.shift_static = []
        # временные вектора сигналов
        self.vec_sigdeg = []
        self.vec_sigamp = []
        self.vec_sigband = []
        # временные вектора помех
        self.vec_intdeg = []
        self.vec_intamp = []
        self.vec_intband = []

    def set(self, init):
        self.sig_deg = np.array(init[0])
        self.sig_amp = np.array(init[1])
        self.sig_band = np.array(init[2])
        self.int_deg = np.array(init[3])
        self.int_amp = np.array(init[4])
        self.int_band = np.array(init[5])
        self.shift_dynamic = np.array(init[6])
        self.shift_static = np.array(init[7])

    def get(self):
        res = []
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_band)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_band)
        res.append(self.shift_dynamic)
        res.append(self.shift_static)
        return res

    def print(self):
        print("Параметры модели сигналов и помех (L2):")
        print("\tsig_deg = ", self.sig_deg)
        print("\tsig_amp = ", self.sig_amp)
        print("\tsig_band = ", self.sig_band)
        print("\tint_deg = ", self.int_deg)
        print("\tint_amp = ", self.int_amp)
        print("\tint_band = ", self.int_band)
        print("\tshift_dynamic = ", self.shift_dynamic)
        print("\tshift_static = ", self.shift_static)
        self.obj_gen.print()

    def calc_out(self, out_set, id_script, par_band):
        # распаковка исходных данных
        vec_time = out_set[1]
        # получение режимов для генератора
        mode_amp, mode_deg, mode_band, freq_amp = self.get_modegen(id_script, par_band)
        # вычисляем вектора изменения сигналов от времени
        self.vec_sigdeg = self.obj_gen.get_vecdeg(vec_time, self.sig_deg, 0)
        self.vec_sigamp = self.obj_gen.get_vecamp(vec_time, self.sig_amp, 0, 0, 0, 0)
        self.vec_sigband = self.obj_gen.get_vecband(vec_time, self.sig_band, 0)
        # вычисляем вектора изменения помех от времени
        self.vec_intdeg = self.obj_gen.get_vecdeg(vec_time, self.int_deg, mode_deg)
        self.vec_intamp = self.obj_gen.get_vecamp(vec_time, self.int_amp, mode_amp, freq_amp, self.shift_static, self.shift_dynamic)
        self.vec_intband = self.obj_gen.get_vecband(vec_time, self.int_band, mode_band)

    def get_out(self):
        out_env = []
        out_env.append(self.vec_sigdeg)
        out_env.append(self.vec_sigamp)
        out_env.append(self.vec_sigband)
        out_env.append(self.vec_intdeg)
        out_env.append(self.vec_intamp)
        out_env.append(self.vec_intband)
        return out_env

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_sigdeg, self.vec_sigamp, self.vec_sigband])
        bool_res2 = cl.is_ndarray([self.vec_intdeg, self.vec_intamp, self.vec_intband])
        # вывод размерностей векторов
        if bool_res1 == True and bool_res2 == True:
            print("Размерности векторов сигналов и помех от времени:")
            print("\tvec_sigdeg.shape = ", self.vec_sigdeg.shape)
            print("\tvec_sigamp.shape = ", self.vec_sigamp.shape)
            print("\tvec_sigband.shape = ", self.vec_sigband.shape)
            print("\tvec_intdeg.shape = ", self.vec_intdeg.shape)
            print("\tvec_intamp.shape = ", self.vec_intamp.shape)
            print("\tvec_intband.shape = ", self.vec_intband.shape)
        else:
            print("Ошибка проверки типа векторов сигналов и помех от времени")

    def get_modegen(self, id_script, par_band):
        # выдать номера режимов для генератора
        mode_amp, mode_deg, mode_band, freq_amp = 0, 0, 0, 0
        if id_script >= 1 and id_script <= 3:
            # если амплитудная модуляция, 1 КГц
            mode_amp = id_script
            freq_amp = 1 * math.pow(10, 3)
        elif id_script == 5:
            # если рандомные помехи, максимальная полоса 10%
            mode_amp, mode_deg, mode_band = 4, 2, 1
            self.int_deg, self.int_amp, self.int_band = np.array([90]), np.array([1]), np.array([par_band])
        elif id_script == 4 or id_script == 6:
            # если изменение углов
            mode_deg = 1
            self.int_deg, self.int_amp, self.int_band = np.array([90]), np.array([1]), np.array([par_band])
        return mode_amp, mode_deg, mode_band, freq_amp



