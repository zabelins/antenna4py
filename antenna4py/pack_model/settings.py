import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль настроек динамического моделирования (L2)")

class Model:
    """Класс расчёта диапазонов изменения параметров моделирования"""

    def __init__(self, id):
        self.id = id
        # диапазон углов
        self.pattern_line = []
        self.pattern_step = []
        # диапазон времени
        self.time_line = []
        self.time_step = []
        # диапазон параметров
        self.var_line = []
        self.var_step = []
        # координатная сетка
        self.vec_pattern = []
        self.vec_time = []
        self.vec_var = []

    def set(self, init):
        self.pattern_line = np.array(init[0])
        self.pattern_step = np.array(init[1])
        self.time_line = np.array(init[2])
        self.time_step = np.array(init[3])
        self.var_line = np.array(init[4])
        self.var_step = np.array(init[5])

    def get(self):
        res = []
        res.append(self.pattern_line)
        res.append(self.pattern_step)
        res.append(self.time_line)
        res.append(self.time_step)
        res.append(self.var_line)
        res.append(self.var_step)
        return res

    def print(self):
        print("Настройки динамического моделирования (L2):")
        print("\tpattern_line = ", self.pattern_line)
        print("\tpattern_step = ", self.pattern_step)
        print("\ttime_line = ", self.time_line)
        print("\ttime_step = ", self.time_step)
        print("\tvar_line = ", self.var_line)
        print("\tvar_step = ", self.var_step)

    def calc_out(self, id_script):
        # один временной отсчёт для статического режима
        if id_script == 0:
            self.time_line = [0, 0]
            self.time_step = 1
        # один параметрический отсчёт для статического и временного режимов
        if id_script >= 0 and id_script <= 5:
            self.var_line = [0, 0]
            self.var_step = 1
        # определяем диапазон изменения параметров
        phi_min, phi_max = [self.pattern_line[0], self.pattern_line[1] + self.pattern_step]
        time_min, time_max = [self.time_line[0], self.time_line[1] + self.time_step]
        var_min, var_max = [self.var_line[0], self.var_line[1] + self.var_step]
        # создаём вектора изменения параметров
        self.vec_pattern = np.arange(phi_min, phi_max, self.pattern_step)
        self.vec_time = np.arange(time_min, time_max, self.time_step)
        self.vec_var = np.arange(var_min, var_max, self.var_step)

    def get_out(self):
        out_set = []
        out_set.append(self.vec_pattern)
        out_set.append(self.vec_time)
        out_set.append(self.vec_var)
        return out_set

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res = cl.is_ndarray([self.vec_time, self.vec_pattern, self.vec_var])
        # вывод размерностей векторов
        if bool_res == True:
            print("Размерности векторов динамических параметров:")
            print("\tvec_pattern.shape = ", self.vec_pattern.shape)
            print("\tvec_time.shape = ", self.vec_time.shape)
            print("\tvec_var.shape = ", self.vec_var.shape)
        else:
            print("Ошибка проверки типа векторов динамических параметров")