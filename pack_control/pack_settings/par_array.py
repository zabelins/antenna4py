import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров антенной решётки (L3)")

class Par_array:
    """Класс исходных параметров антенной решётки"""

    def __init__(self):
        # МНОЖИТЕЛЬ РЕШЁТКИ
        # центральная частота (flt), число элементов (int), шаг решётки (flt)
        # распределение (0=нет,1=да), взаим. связь (0=нет), амплитуда шума (flt)
        self.arr_frq = 9 * math.pow(10, 9)
        self.arr_size = 16
        self.arr_step = 1
        self.arr_dist = 0
        self.arr_effect = 0
        self.arr_noise = 1 * math.pow(10, -6)
        # ИЗЛУЧАТЕЛИ РЕШЁТКИ
        # тип (0=изотроп, 1=диполь)
        self.elm_type = 0
        # ПРЕДОБРАБОТКА
        # накопление сигналов (int)
        self.acc_size = 0
        # АМПЛИТУДНО-ФАЗОВЫЕ ОШИБКИ
        # амп. ошибки (0=гаусс), фаз. ошибки (0=равномер, 1=гаусс), границы (flt)
        self.err_distphi = 0
        self.err_distamp = 0
        self.err_maxphi = 0 * math.pi
        self.err_maxamp = 0

    def set(self, init):
        self.arr_frq = init[0]
        self.arr_size = init[1]
        self.arr_step = init[2]
        self.arr_dist = init[3]
        self.arr_effect = init[4]
        self.arr_noise = init[5]
        self.elm_type = init[6]
        self.acc_size = init[7]
        self.err_distphi = init[8]
        self.err_distamp = init[9]
        self.err_maxphi = init[10]
        self.err_maxamp = init[11]

    def get(self):
        res = []
        res.append(self.arr_frq)
        res.append(self.arr_size)
        res.append(self.arr_step)
        res.append(self.arr_dist)
        res.append(self.arr_effect)
        res.append(self.arr_noise)
        res.append(self.elm_type)
        res.append(self.acc_size)
        res.append(self.err_distphi)
        res.append(self.err_distamp)
        res.append(self.err_maxphi)
        res.append(self.err_maxamp)
        return res

    def print(self):
        print("Параметры антенной решётки (L3):")
        print("\tarr_frq = ", self.arr_frq)
        print("\tarr_size = ", self.arr_size)
        print("\tarr_step = ", self.arr_step)
        print("\tarr_dist = ", self.arr_dist)
        print("\tarr_effect = ", self.arr_effect)
        print("\tarr_noise = ", self.arr_noise)
        print("\telm_type = ", self.elm_type)
        print("\tacc_size = ", self.acc_size)
        print("\terr_distphi = ", self.err_distphi)
        print("\terr_distamp = ", self.err_distamp)
        print("\terr_maxphi = ", self.err_maxphi)
        print("\terr_maxamp = ", self.err_maxamp)
