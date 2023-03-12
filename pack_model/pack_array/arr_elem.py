import math
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели элемента АР (L3)")

class Element:
    """Класс моделирования элементов антенной решётки"""

    def __init__(self):
        # параметры решётки
        self.arr_frq = 0
        # параметры элементов решётки
        self.elm_type = 0

    def set(self, init):
        self.arr_frq = init[0]
        self.elm_type = init[6]

    def get(self):
        res = []
        res.append(self.arr_frq)
        res.append(self.elm_type)
        return res

    def print(self):
        print("Параметры модели элемента АР (L3):")
        print("\tarr_frq = ", self.arr_frq)
        print("\telm_type = ", self.elm_type)

    def get_gain(self, deg):
        # усиление сигнала для заданного угла обзора
        res = []
        if self.elm_type == 0:
            # изотропный излучатель, КНД=1.00 dBi
            res = 1.0
        if self.elm_type == 1:
            # дипольный излучатель, КНД=2.15 dBi
            res = 1.28 * abs(math.cos(deg))
        return res