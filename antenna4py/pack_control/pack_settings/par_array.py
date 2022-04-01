import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров антенной решётки (L3)")

class Par_array:
    """Класс исходных параметров антенной решётки"""

    def __init__(self, id):
        self.id = id
        # центральная частота для антенной системы
        self.f_cen = 3 * math.pow(10, 9)
        # параметры множителя решётки
        self.array_N = 10
        self.array_beta = 1
        self.array_dist = 0
        self.array_effect = 0
        self.array_nois = 1/4
        # параметры элементов решётки (0=изотроп, 1=диполь)
        self.elem_type = 0
        # параметры амплитудных ошибок (0=гаусс)
        # параметры фазовых ошибок (0=равномер, 1=гаусс)
        self.error_distphi = 0
        self.error_distamp = 0
        self.error_maxphi = 0 * math.pi
        self.error_maxamp = 0

    def set(self, init):
        self.f_cen = init[0]
        self.array_N = init[1]
        self.array_beta = init[2]
        self.array_dist = init[3]
        self.array_effect = init[4]
        self.array_nois = init[5]
        self.elem_type = init[6]
        self.error_distphi = init[7]
        self.error_distamp = init[8]
        self.error_maxphi = init[9]
        self.error_maxamp = init[10]

    def get(self):
        res = []
        res.append(self.f_cen)
        res.append(self.array_N)
        res.append(self.array_beta)
        res.append(self.array_dist)
        res.append(self.array_effect)
        res.append(self.array_nois)
        res.append(self.elem_type)
        res.append(self.error_distphi)
        res.append(self.error_distamp)
        res.append(self.error_maxphi)
        res.append(self.error_maxamp)
        return res

    def print(self):
        print("Параметры антенной решётки (L3):")
        print("\tf_cen = ", self.f_cen)
        print("\tarray_N = ", self.array_N)
        print("\tarray_beta = ", self.array_beta)
        print("\tarray_dist = ", self.array_dist)
        print("\tarray_effect = ", self.array_effect)
        print("\tarray_nois = ", self.array_nois)
        print("\telem_type = ", self.elem_type)
        print("\terror_distphi = ", self.error_distphi)
        print("\terror_distamp = ", self.error_distamp)
        print("\terror_maxphi = ", self.error_maxphi)
        print("\terror_maxamp = ", self.error_maxamp)
