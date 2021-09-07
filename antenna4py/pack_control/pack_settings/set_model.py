if __name__ == "__main__":
    print("Вы запустили модуль настроек ПО (L3)")

class Set_model:
    """Класс настроек динамического моделирования в ПО"""

    def __init__(self, id):
        self.id = id
        self.id_var = 1
        self.pattern_line = [-90, 90]
        self.pattern_step = 0.25
        self.time_line = [0, 5]
        self.time_step = 0.5
        self.var_line = [0, 5]
        self.var_step = 1
        self.save_calc = 1

    def set(self, init):
        self.id_var = init[0]
        self.pattern_line = init[1]
        self.pattern_step = init[2]
        self.time_line = init[3]
        self.time_step = init[4]
        self.var_line = init[5]
        self.var_step = init[6]
        self.save_calc = init[7]

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
        print(" --- Значения настроек ПО (L3) --- ")
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
        print(" --- Значения настроек ПО (L3) --- ")
        print("settings_sw = ", self.get())
