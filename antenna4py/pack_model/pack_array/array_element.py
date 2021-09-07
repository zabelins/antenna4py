import math
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели элемента АР (L3)")

class Element:
    """Класс моделирования элементов антенной решётки"""

    def __init__(self, id):
        self.id = id
        self.f_cen = []
        self.id_elem = []
        self.id_effect = []

    def set(self, init):
        self.f_cen = np.array(init[3])
        self.id_elem = np.array(init[9])
        self.id_effect = np.array(init[10])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.f_cen)
        res.append(self.id_elem)
        res.append(self.id_effect)
        return res

    def print(self):
        print(" --- Параметры модели элемента АР (L3) --- ")
        print("id = ", self.id)
        print("f_cen = ", self.f_cen)
        print("id_elem = ", self.id_elem)
        print("id_effect = ", self.id_effect)

    def print_short(self):
        print(" --- Параметры модели элемента АР (L3) --- ")
        print("array_element = ", self.get())

    def get_out(self, deg):
        # усиление сигнала для заданного угла обзора
        res = []
        if (self.id_elem == 1):
            # изотропный излучатель, КНД=1.00 dBi
            res = 1.0
        if (self.id_elem == 2):
            # дипольный излучатель, КНД=2.15 dBi
            res = 1.28 * abs(math.cos(deg))
        return res

