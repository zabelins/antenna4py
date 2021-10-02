if __name__ == "__main__":
    print("Вы запустили модуль настроек ПО (L3)")

class Set_model:
    """Класс настроек динамического моделирования в ПО"""

    def __init__(self, id):
        self.id = id
        # диапазон углов, 1 ед = 1 град
        self.pattern_line = [-90, 90]
        self.pattern_step = 0.25
        # диапазон времени, 1 ед = 1 мс
        self.time_line = [0, 10]
        self.time_step = 0.01
        # для Калмана T=1, T/2=0.5, T/4=0.25
        # по умолчанию 0.05
        # диапазон параметров, 1 ед = 10%
        self.var_line = [0, 0.1]
        self.var_step = 0.01

    def set(self, init):
        self.pattern_line = init[0]
        self.pattern_step = init[1]
        self.time_line = init[2]
        self.time_step = init[3]
        self.var_line = init[4]
        self.var_step = init[5]

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
        print("Настройки динамического моделирования (L3):")
        print("\tpattern_line = ", self.pattern_line)
        print("\tpattern_step = ", self.pattern_step)
        print("\ttime_line = ", self.time_line)
        print("\ttime_step = ", self.time_step)
        print("\tvar_line = ", self.var_line)
        print("\tvar_step = ", self.var_step)

