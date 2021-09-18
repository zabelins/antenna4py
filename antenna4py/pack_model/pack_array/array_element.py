import math
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели элемента АР (L3)")

class Element:
    """Класс моделирования элементов антенной решётки"""

    def __init__(self, id):
        self.id = id
        self.f_cen = []
        self.elem_type = []

    def set(self, init):
        self.f_cen = np.array(init[1])
        self.elem_type = np.array(init[6])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.f_cen)
        res.append(self.elem_type)
        return res

    def print(self):
        print(" --- Параметры модели элемента АР (L3) --- ")
        print("id = ", self.id)
        print("f_cen = ", self.f_cen)
        print("elem_type = ", self.elem_type)

    def print_short(self):
        print(" --- Параметры модели элемента АР (L3) --- ")
        print("array_element = ", self.get())

    def get_gain(self, deg):
        # усиление сигнала для заданного угла обзора
        res = []
        if (self.elem_type == 1):
            # изотропный излучатель, КНД=1.00 dBi
            res = 1.0
        if (self.elem_type == 2):
            # дипольный излучатель, КНД=2.15 dBi
            res = 1.28 * abs(math.cos(deg))
        return res

