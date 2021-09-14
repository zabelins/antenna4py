import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль настроек динамического моделирования (L2)")

class Model:
    """Класс расчёта диапазонов изменения параметров моделирования"""

    def __init__(self, id):
        self.id = id
        self.id_var = []
        self.pattern_line = []
        self.pattern_step = []
        self.time_line = []
        self.time_step = []
        self.var_line = []
        self.var_step = []
        self.save_calc = []
        self.vec_pattern = []
        self.vec_time = []
        self.vec_var = []

    def set(self, init):
        self.id_var = np.array(init[1])
        self.pattern_line = np.array(init[2])
        self.pattern_step = np.array(init[3])
        self.time_line = np.array(init[4])
        self.time_step = np.array(init[5])
        self.var_line = np.array(init[6])
        self.var_step = np.array(init[7])
        self.save_calc = np.array(init[8])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_var)
        res.append(self.pattern_line)
        res.append(self.pattern_step)
        res.append(self.time_line)
        res.append(self.time_step)
        res.append(self.var_line)
        res.append(self.var_step)
        res.append(self.save_calc)
        return res

    def print(self):
        print(" --- Настройки динамического моделирования (L2) --- ")
        print("id = ", self.id)
        print("id_var = ", self.id_var)
        print("pattern_line = ", self.pattern_line)
        print("pattern_step = ", self.pattern_step)
        print("time_line = ", self.time_line)
        print("time_step = ", self.time_step)
        print("var_line = ", self.var_line)
        print("var_step = ", self.var_step)
        print("save_calc = ", self.save_calc)

    def print_short(self):
        print(" --- Настройки динамического моделирования (L2) --- ")
        print("settings = ", self.get())

    def calc_out(self):
        # определяем диапазон изменения параметров
        phi_min, phi_max = [self.pattern_line[0], self.pattern_line[1] + self.pattern_step]
        time_min, time_max = [self.time_line[0], self.time_line[1] + self.time_step]
        var_min, var_max = [self.var_line[0], self.var_line[1] + self.var_step]
        # создаём вектора изменения параметров
        self.vec_pattern = np.arange(phi_min, phi_max, self.pattern_step)
        self.vec_time = np.arange(time_min, time_max, self.time_step)
        self.vec_var = np.arange(var_min, var_max, self.var_step)

    def get_out(self):
        res = []
        res.append(self.vec_pattern)
        res.append(self.vec_time)
        res.append(self.vec_var)
        res.append(self.pattern_step)
        res.append(self.time_step)
        return res

    def print_out(self):
        bool_out = (self.vec_time != []) and (self.vec_pattern != []) and (self.vec_var != [])
        if (bool_out == True):
            print("Размерности векторов динамических параметров:")
            print("vec_pattern.shape = ", self.vec_pattern.shape)
            print("vec_time.shape = ", self.vec_time.shape)
            print("vec_var.shape = ", self.vec_var.shape)
        else:
            print("Вектора динамических параметров отсутствуют")