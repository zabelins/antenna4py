import math
import cmath
import numpy as np
from numpy.polynomial.chebyshev import Chebyshev

if __name__ == "__main__":
    print("Вы запустили модуль модели множителя АР (L3)")

class Factor:
    """Класс моделирования множителя антенной решётки"""
    con_c = 3 * math.pow(10, 8)

    def __init__(self, id):
        self.id = id
        self.beta = []
        self.f_cen = []
        self.noise_phimax = []
        self.noise_ampmax = []
        self.noize_phidist = []
        self.noize_ampdist = []
        self.id_dist = []
        self.id_effect = []

    def set(self, init):
        self.beta = np.array(init[2])
        self.f_cen = np.array(init[3])
        self.noise_phimax = np.array(init[4])
        self.noise_ampmax = np.array(init[5])
        self.noize_phidist = np.array(init[6])
        self.noize_ampdist = np.array(init[7])
        self.id_dist = np.array(init[8])
        self.id_effect = np.array(init[10])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.beta)
        res.append(self.f_cen)
        res.append(self.noise_phimax)
        res.append(self.noise_ampmax)
        res.append(self.noize_phidist)
        res.append(self.noize_ampdist)
        res.append(self.id_dist)
        res.append(self.id_effect)
        return res

    def print(self):
        print(" --- Параметры модели множителя АР (L3) --- ")
        print("id = ", self.id)
        print("beta = ", self.beta)
        print("f_cen = ", self.f_cen)
        print("noise_phimax = ", self.noise_phimax)
        print("noise_ampmax = ", self.noise_ampmax)
        print("noize_phidist = ", self.noize_phidist)
        print("noize_ampdist = ", self.noize_ampdist)
        print("id_dist = ", self.id_dist)
        print("id_effect = ", self.id_effect)

    def print_short(self):
        print(" --- Параметры модели множителя АР (L3) --- ")
        print("array_factor = ", self.get())

    def get_out(self, amp, deg, num, rand):
        # комплексный сигнал для заданного элемента антенной решётки
        lambda_cen = self.con_c / self.f_cen
        step_array = self.beta * lambda_cen / 2
        fun_u = 2 * math.pi * step_array / lambda_cen * math.sin(deg) #float64
        fun_sig = amp * cmath.exp(1j * fun_u * (num - 1)) * cmath.exp(1j * rand)
        return fun_sig

    def get_dist(self, num_all, num_var):
        # АФР для заданного элемента антенной решётки
        res = []
        if (self.id_dist == 1):
            # равномерное распределение
            res = 1.0
        if (self.id_dist == 2):
            # косинусное распределение
            res = 0.4 + 0.6 * math.cos(math.pi * (num_var-1) / (num_all-1) - math.pi/2)
        if (self.id_dist == 3):
            # распределение чебышева
            # нужно использовать Chebyshev()
            res = []
        return res

    def get_randamp(self):
        # амплитудные ошибки сигнала
        res = []
        if (self.noize_ampdist == 1):
            # гауссовское распределение ошибок
            res = np.random.normal(loc=1.0, scale=self.noise_ampmax)
        return res

    def get_randphi(self):
        # фазовые ошибки сигнала
        res = []
        if (self.noize_phidist == 1):
            # равномерное распределение ошибок
            res = np.random.uniform(-self.noise_phimax, self.noise_phimax)
        if (self.noize_phidist == 2):
            # гауссовское распределение ошибок
            res = np.random.normal(loc=0.0, scale=self.noise_phimax)
        return res

    def get_eqsig(self, deg, fband, num_all):
        # преобразование значения сигнала в вектор эквивалентных сигналов
        f_otn = fband / self.f_cen
        # количество эквивалентных помех сигнала
        num_eqsig = 0
        buf1 = num_all * fband * 2 * math.pi**2 * self.beta
        buf2 = buf1 * math.sin(math.radians(deg) / (4 * self.f_cen * math.pi))
        l0_max = abs(round(buf2))
        num_eqsig = num_eqsig + l0_max * 2 + 1
        # новый вектор углов сигнала
        vec_eqdeg = np.zeros(shape=[int(num_eqsig)])
        # заполняем вектор помех: [real_sig, -L, +L, -2L, +2L...]
        l = 0
        for i in range(int(num_eqsig)):
            if (i == 0):
                vec_eqdeg[i] = deg
            if (i % 2 != 0):
                l = l + 1
                vec_eqdeg[i] = math.degrees(math.radians(deg) - 2 * l / (num_all * self.beta))
                vec_eqdeg[i+1] = math.degrees(math.radians(deg) + 2 * l / (num_all * self.beta))
        # обозначение выходящих за пределы ДН углов числом 361
        range_show = [-90, 90]
        for i in range(vec_eqdeg.shape[0]):
            if (vec_eqdeg[i] < range_show[0]) or (vec_eqdeg[i] > range_show[1]):
                vec_eqdeg[i] = 361
        return [vec_eqdeg, num_eqsig, l0_max, f_otn]

    def get_eqamp(self, num_all, num_var):
        #f_otn = fband / self.f_cen
        #l0_max = num_all / 2;
        #A2l = np.zeros(shape=[l0_max, self.N], dtype='float64')
        #for k in range(l0_max):
        #    buf0 = 1 / (l0_max+1)
        #    buf1 = f_otn * 2 * math.pi * k * self.beta * math.pi /(2 * self.f_cen * 2 * math.pi)
        #    A2l[k] = buf0 * sum( self.get_freqdist(buf1) * math.cos(2 * math.pi * k * l_var / (l0_max + 1)))
        return 1.0

    def get_freqdist(self, y_var):
        return np.sin(y_var) / y_var