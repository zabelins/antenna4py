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
        self.animation = []
        self.list_pattern = pg.pattern.Pattern(1)
        self.list_charact = pg.characteristics.Characteristics(1)
        self.list_timefreq = pg.timefreq.TimeFreq(1)

    def set(self, init):
        self.animation = init[20]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.animation)
        return res

    def print(self):
        print(" --- Параметры вывода графика (L2) --- ")
        print("id = ", self.id)
        print("animation = ", self.animation)
        self.list_pattern.print_short()
        self.list_charact.print_short()
        self.list_timefreq.print_short()

    def print_short(self):
        print(" --- Параметры вывода графика (L2) --- ")
        print("graph = ", self.get())

    def draw_pattern(self, x, y, deg_int=[]):
        # отобразить диаграмму направленности
        self.list_pattern.draw_pattern(x, y, deg_int)

    def draw_charact(self, x, y, str=[]):
        # отобразить характеристики подавления
        self.list_charact.draw_charact(x, y, str)

    def draw_timefreq(self, x, y, str=[]):
        # отобразить частотно-временные характеристики сигналов и помех
        self.list_timefreq.draw_time(x, y, str)

