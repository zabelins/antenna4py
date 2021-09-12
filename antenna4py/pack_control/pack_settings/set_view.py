if __name__ == "__main__":
    print("Вы запустили модуль настроек вывода информации (L3)")

class Set_view:
    """Класс настроек вывода информации для пользователя"""

    def __init__(self, id):
        self.id = id
        self.pattern_style = 1
        self.pattern_norm = 1
        self.pattern_mean = 0
        self.pattern_db = 1
        self.pattern_legend = 1
        self.pattern_strleg = ["p1", "p2", "p3", "p4", "p5"]
        self.charact_style = 1
        self.charact_norm = 1
        self.charact_mean = 0
        self.charact_db = 1
        self.charact_legend = 1
        self.charact_strleg = ["c1", "c2", "c3", "c4", "c5"]
        self.approx = 0
        self.animation = 1

    def set(self, init):
        self.pattern_style = init[0]
        self.pattern_norm = init[1]
        self.pattern_mean = init[2]
        self.pattern_db = init[3]
        self.pattern_legend = init[4]
        self.pattern_strleg = init[5]
        self.charact_style = init[6]
        self.charact_norm = init[7]
        self.charact_mean = init[8]
        self.charact_db = init[9]
        self.charact_legend = init[10]
        self.charact_strleg = init[11]
        self.approx = init[12]
        self.animation = init[13]
    def get(self):
        res = []
        res.append(self.id)
        res.append(self.pattern_style)
        res.append(self.pattern_norm)
        res.append(self.pattern_mean)
        res.append(self.pattern_db)
        res.append(self.pattern_legend)
        res.append(self.pattern_strleg)
        res.append(self.charact_style)
        res.append(self.charact_norm)
        res.append(self.charact_mean)
        res.append(self.charact_db)
        res.append(self.charact_legend)
        res.append(self.charact_strleg)
        res.append(self.approx)
        res.append(self.animation)
        return res

    def print(self):
        print(" --- Значения настроек вывода информации (L3) --- ")
        print("id = ", self.id)
        print("pattern_style = ", self.pattern_style)
        print("pattern_norm = ", self.pattern_norm)
        print("pattern_mean = ", self.pattern_mean)
        print("pattern_db = ", self.pattern_db)
        print("pattern_legend = ", self.pattern_legend)
        print("pattern_strleg = ", self.pattern_strleg)
        print("charact_style = ", self.charact_style)
        print("charact_norm = ", self.charact_norm)
        print("charact_mean = ", self.charact_mean)
        print("charact_db = ", self.charact_db)
        print("charact_legend = ", self.charact_legend)
        print("charact_strleg = ", self.charact_strleg)
        print("approx = ", self.approx)
        print("animation = ", self.animation)

    def print_short(self):
        print(" --- Значения настроек вывода информации (L3) --- ")
        print("settings_view = ", self.get())
