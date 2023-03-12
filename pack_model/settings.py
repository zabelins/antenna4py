import math
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль настроек динамического моделирования (L2)")

class Model:
    """Класс расчёта диапазонов изменения параметров моделирования"""

    def __init__(self):
        # диапазон углов
        self.deg_line = []
        self.deg_step = 0
        # диапазон времени
        self.time_line = []
        self.time_step = 0
        self.time_coef = 0
        # диапазон параметров
        self.par_line = []
        self.par_step = 0
        # координатная сетка
        self.vec_deg = np.array([])
        self.vec_time = np.array([])
        self.vec_par = np.array([])

    def set(self, init):
        self.deg_line = init[0]
        self.deg_step = init[1]
        self.time_line = init[2]
        self.time_step = init[3]
        self.time_coef = init[4]
        self.par_line = init[5]
        self.par_step = init[6]

    def get(self):
        res = []
        res.append(self.deg_line)
        res.append(self.deg_step)
        res.append(self.time_line)
        res.append(self.time_step)
        res.append(self.time_coef)
        res.append(self.par_line)
        res.append(self.par_step)
        return res

    def print(self):
        print("Настройки динамического моделирования (L2):")
        print("\tdeg_line = ", self.deg_line)
        print("\tdeg_step = ", self.deg_step)
        print("\ttime_line = ", self.time_line)
        print("\ttime_step = ", self.time_step)
        print("\ttime_coef = ", self.time_coef)
        print("\tpar_line = ", self.par_line)
        print("\tpar_step = ", self.par_step)

    def calc_out(self, id_script):
        # создаём вектора изменения параметров
        self.calc_vecdeg()
        self.calc_vectime(id_script)
        self.calc_vecpar(id_script)

    def calc_vecdeg(self):
        # сетка углов
        deg_min, deg_max = [self.deg_line[0], self.deg_line[1] + self.deg_step]
        self.vec_deg = np.arange(deg_min, deg_max, self.deg_step)

    def calc_vectime(self, id_script):
        # сетка времени
        if id_script == 0:
            # статический режим
            self.time_line = [0, 1]
            self.time_step = 1
        time_min, time_max = [self.time_line[0], self.time_line[1]]
        self.vec_time = np.arange(time_min, time_max, self.time_step) * self.time_coef

    def calc_vecpar(self, id_script):
        # сетка параметров
        par_coef, par_add = 1, 0
        if id_script < 8:
            # статический и временной режимы
            self.par_line = [0, 1]
            self.par_step = 1
        elif id_script == 8:
            # изменение частотной полосы
            par_coef, par_add = 0.1, 0
        elif id_script == 9:
            # изменение амплитуды
            par_coef, par_add = 1, self.par_step
        par_min, par_max = [self.par_line[0], self.par_line[1]]
        self.vec_par = np.arange(par_min, par_max, self.par_step) * par_coef + par_add

    def get_out(self):
        out_set = []
        out_set.append(self.vec_deg)
        out_set.append(self.vec_time)
        out_set.append(self.vec_par)
        return out_set

    def print_out(self):
        # проверка типа векторов на ndarray
        condit = cl.is_ndarray([self.vec_time, self.vec_deg, self.vec_par])
        # вывод размерностей векторов
        if condit:
            print("Настройки модели:")
            print("\tvec_deg.shape = ", self.vec_deg.shape)
            print("\tvec_time.shape = ", self.vec_time.shape)
            print("\tvec_par.shape = ", self.vec_par.shape)
        else:
            print("Ошибка проверки векторов настройки модели")