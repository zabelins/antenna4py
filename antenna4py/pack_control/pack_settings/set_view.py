if __name__ == "__main__":
    print("Вы запустили модуль настроек вывода информации (L3)")

class Set_view:
    """Класс настроек вывода информации для пользователя"""

    def __init__(self, id):
        self.id = id
        self.graph_style = 1
        self.graph_norm = 1
        self.graph_mean = 0
        self.graph_db = 1
        self.graph_legend = 1
        self.graph_strleg = ["g1", "g2", "g3", "g4", "g5"]
        self.approx = 0
        self.animation = 1

    def set(self, init):
        self.graph_style = init[0]
        self.graph_norm = init[1]
        self.graph_mean = init[2]
        self.graph_db = init[3]
        self.graph_legend = init[4]
        self.graph_strleg = init[5]
        self.approx = init[6]
        self.animation = init[7]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.graph_style)
        res.append(self.graph_norm)
        res.append(self.graph_mean)
        res.append(self.graph_db)
        res.append(self.graph_legend)
        res.append(self.graph_strleg)
        res.append(self.approx)
        res.append(self.animation)
        return res

    def print(self):
        print(" --- Значения настроек вывода информации (L3) --- ")
        print("id = ", self.id)
        print("graph_style = ", self.graph_style)
        print("graph_norm = ", self.graph_norm)
        print("graph_mean = ", self.graph_mean)
        print("graph_db = ", self.graph_db)
        print("graph_legend = ", self.graph_legend)
        print("graph_strleg = ", self.graph_strleg)
        print("approx = ", self.approx)
        print("animation = ", self.animation)

    def print_short(self):
        print(" --- Значения настроек вывода информации (L3) --- ")
        print("settings_view = ", self.get())
