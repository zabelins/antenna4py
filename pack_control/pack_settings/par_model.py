import math

if __name__ == "__main__":
    print("Вы запустили модуль настроек ПО (L3)")

class Par_model:
    """Класс параметров моделирования"""

    def __init__(self):
        # СЕТКА УГЛОВ
        # диапазон (flt), шаг (flt) / 1 ед = 1 град.
        self.deg_line = [-90, 90]
        self.deg_step = 0.25
        # СЕТКА ВРЕМЕНИ
        # диапазон (flt), шаг (flt), множитель (flt) / 1 ед = 1 мкс
        # по умолчанию 10, для обучения max=300..500
        # по умолчанию 0.05, для Калмана T=1, T/2=0.5, T/4=0.25
        self.time_line = [0, 500]
        self.time_step = 0.1
        self.time_coef = 1 * math.pow(10, -3)
        # СЕТКА ПАРАМЕТРОВ
        # диапазон (flt), шаг (flt), 1 ед = 100%
        self.par_line = [0, 1]
        self.par_step = 0.1

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
        print("Параметры динамического моделирования (L3):")
        print("\tdeg_line = ", self.deg_line)
        print("\tdeg_step = ", self.deg_step)
        print("\ttime_line = ", self.time_line)
        print("\ttime_step = ", self.time_step)
        print("\ttime_coef = ", self.time_coef)
        print("\tpar_line = ", self.par_line)
        print("\tpar_step = ", self.par_step)

