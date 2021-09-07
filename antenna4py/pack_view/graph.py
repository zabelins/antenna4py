import pack_view.pack_graph as pg
from pack_view.pack_graph import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода графика (L2)")
    print("Модуль использует пакет:", pg.NAME)

class Graph:
    """Класс вывода графиков для пользователя"""

    def __init__(self, id):
        self.id = id
        self.graph_style = []
        self.graph_norm = []
        self.graph_mean = []
        self.graph_db = []
        self.graph_legend = []
        self.graph_strleg = []
        self.animation = []
        self.list_pattern = pg.pattern.Pattern(1)
        self.list_charact = pg.characteristics.Characteristics(1)

    def set(self, init):
        self.graph_style = init[1]
        self.graph_norm = init[2]
        self.graph_mean = init[3]
        self.graph_db = init[4]
        self.graph_legend = init[5]
        self.graph_strleg = init[6]
        self.animation = init[8]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.graph_style)
        res.append(self.graph_norm)
        res.append(self.graph_mean)
        res.append(self.graph_db)
        res.append(self.graph_legend)
        res.append(self.graph_strleg)
        res.append(self.animation)
        return res

    def print(self):
        print(" --- Параметры вывода графика (L2) --- ")
        print("id = ", self.id)
        print("graph_style = ", self.graph_style)
        print("graph_norm = ", self.graph_norm)
        print("graph_mean = ", self.graph_mean)
        print("graph_db = ", self.graph_db)
        print("graph_legend = ", self.graph_legend)
        print("graph_strleg = ", self.graph_strleg)
        print("animation = ", self.animation)
        self.list_pattern.print_short()
        self.list_charact.print_short()

    def print_short(self):
        print(" --- Параметры вывода графика (L2) --- ")
        print("graph = ", self.get())

    def draw_pattern(self, x, y, deg_int=[]):
        vec_par = self.get()
        self.list_pattern.draw_pattern(x, y, vec_par, deg_int)

    def draw_charact(self, x, y, str=[]):
        vec_par = self.get()
        self.list_charact.draw_charact(x, y, vec_par, str)

