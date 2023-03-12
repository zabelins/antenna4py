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

    def __init__(self):
        self.obj_gendeg = pe.gen_deg.Gendeg()
        self.obj_genmod = pe.gen_mod.Genmod()
        self.obj_genbnd = pe.gen_bnd.Genbnd()
        # временные вектора сигналов
        self.vec_sigdeg = np.array([])
        self.vec_sigamp = np.array([])
        self.vec_sigbnd = np.array([])
        # временные вектора помех
        self.vec_intdeg = np.array([])
        self.vec_intamp = np.array([])
        self.vec_intbnd = np.array([])
        # наличие модуляции
        self.flag_mod = 0
        self.vec_code = []

    def set(self):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры модели сигналов и помех (L2):")
        print("\t-")
        self.obj_gendeg.print()
        self.obj_genmod.print()
        self.obj_genbnd.print()

    def calc_out(self, out_set, id_script, var_par):
        # распаковка исходных данных
        id_amp0, id_deg1, id_amp1, id_bnd1, id_demod, vec_time = 0, 0, 0, 0, 0, out_set[1]
        # получение режимов для генератора
        if id_script == 0:
            # статический режим ДН
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [0, 0, 0, 0, 0]
        elif id_script == 1:
            # время - произвольная модуляция
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [2, 0, 2, 0, 1]
        elif id_script == 2:
            # время - линейное изменение угла
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [1, 1, 1, 2, 0]
        elif id_script == 3:
            # время - выборка случайной одиночной помехи
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [3, 2, 3, 1, 0]
        elif id_script == 4:
            # время - выборка случайной мерцающей помехи
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [0, 3, 4, 4, 0]
        elif id_script == 5:
            # время - выборка шумовой помехи с накоплением
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [5, 4, 6, 1, 1]
        elif id_script == 6:
            # время - выборка импульсной помехи с накоплением
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [5, 5, 7, 1, 1]
        elif id_script == 7:
            # время - выборка мерцающей помехи с накоплением
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [5, 6, 8, 1, 1]
        elif id_script == 8:
            # параметр - изменение полосы
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [1, 1, 1, 6, 0]
        elif id_script == 9:
            # параметр - изменение амплитуды
            id_amp0, id_deg1, id_amp1, id_bnd1, id_demod = [9, 0, 3, 0, 1]
        # вычисляем вектора изменения сигналов от времени
        self.vec_sigdeg = self.obj_gendeg.get_vec(vec_time, 0, 0)
        self.vec_sigamp = self.obj_genmod.get_vec(vec_time, id_amp0, var_par, 0)
        self.vec_sigbnd = self.obj_genbnd.get_vec(vec_time, 0, 0, 0)
        # вычисляем вектора изменения помех от времени
        self.vec_intdeg = self.obj_gendeg.get_vec(vec_time, id_deg1, 1)
        self.vec_intamp = self.obj_genmod.get_vec(vec_time, id_amp1, var_par, 1)
        self.vec_intbnd = self.obj_genbnd.get_vec(vec_time, id_bnd1, var_par, 1)
        # добавляем постоянную составляющую сигнала
        self.vec_sigamp = self.vec_sigamp + math.pow(10, -12)
        # определяем необходимость демодуляции
        if id_demod == 1 and self.obj_genmod.sig_mod != 0:
            self.flag_mod = 1
            self.vec_code = self.obj_genmod.get_code()

    def get_out(self):
        out_env = []
        out_env.append(self.vec_sigdeg)
        out_env.append(self.vec_sigamp)
        out_env.append(self.vec_sigbnd)
        out_env.append(self.vec_intdeg)
        out_env.append(self.vec_intamp)
        out_env.append(self.vec_intbnd)
        out_env.append(self.flag_mod)
        out_env.append(self.vec_code)
        return out_env

    def print_out(self):
        # проверка типа векторов на ndarray
        condit_1 = cl.is_ndarray([self.vec_sigdeg, self.vec_sigamp, self.vec_sigbnd])
        condit_2 = cl.is_ndarray([self.vec_intdeg, self.vec_intamp, self.vec_intbnd])
        # вывод размерностей векторов
        if condit_1 and condit_2:
            print("Сигналы и помехи:")
            print("\tvec_sigdeg.shape = ", self.vec_sigdeg.shape)
            print("\tvec_sigamp.shape = ", self.vec_sigamp.shape)
            print("\tvec_sigbnd.shape = ", self.vec_sigbnd.shape)
            print("\tvec_intdeg.shape = ", self.vec_intdeg.shape)
            print("\tvec_intamp.shape = ", self.vec_intamp.shape)
            print("\tvec_intbnd.shape = ", self.vec_intbnd.shape)
            print("\tvec_code.shape = ", len(self.vec_code))
        else:
            print("Ошибка проверки векторов сигналов и помех")




