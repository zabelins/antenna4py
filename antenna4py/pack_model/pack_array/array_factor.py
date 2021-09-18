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
        self.f_cen = []
        self.array_N = []
        self.array_beta = []
        self.array_dist = []
        self.array_effect = []
        self.error_distphi = []
        self.error_distamp = []
        self.error_maxphi = []
        self.error_maxamp = []

    def set(self, init):
        self.f_cen = np.array(init[1])
        self.array_N = np.array(init[2])
        self.array_beta = np.array(init[3])
        self.array_dist = np.array(init[4])
        self.array_effect = np.array(init[5])
        self.error_distphi = np.array(init[7])
        self.error_distamp = np.array(init[8])
        self.error_maxphi = np.array(init[9])
        self.error_maxamp = np.array(init[10])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.f_cen)
        res.append(self.array_N)
        res.append(self.array_beta)
        res.append(self.array_dist)
        res.append(self.array_effect)
        res.append(self.error_distphi)
        res.append(self.error_distamp)
        res.append(self.error_maxphi)
        res.append(self.error_maxamp)
        return res

    def print(self):
        print(" --- Параметры модели множителя АР (L3) --- ")
        print("id = ", self.id)
        print("f_cen = ", self.f_cen)
        print("array_N = ", self.array_N)
        print("array_beta = ", self.array_beta)
        print("array_dist = ", self.array_dist)
        print("array_effect = ", self.array_effect)
        print("error_distphi = ", self.error_distphi)
        print("error_distamp = ", self.error_distamp)
        print("error_maxphi = ", self.error_maxphi)
        print("error_maxamp = ", self.error_maxamp)

    def print_short(self):
        print(" --- Параметры модели множителя АР (L3) --- ")
        print("array_factor = ", self.get())

    def get_signal(self, amp, deg, num, rand):
        # комплексный сигнал для заданного элемента антенной решётки
        lambda_cen = self.con_c / self.f_cen
        step_array = self.array_beta * lambda_cen / 2
        fun_u = 2 * math.pi * step_array / lambda_cen * math.sin(deg) #float64
        fun_sig = amp * cmath.exp(1j * fun_u * (num - 1)) * cmath.exp(1j * rand)
        return fun_sig

    def get_dist(self, num_all, num_var):
        # АФР для заданного элемента антенной решётки
        res = []
        if (self.array_dist == 1):
            # равномерное распределение
            res = 1.0
        if (self.array_dist == 2):
            # косинусное распределение
            res = 0.4 + 0.6 * math.cos(math.pi * (num_var-1) / (num_all-1) - math.pi/2)
        if (self.array_dist == 3):
            # распределение чебышева
            # нужно использовать Chebyshev()
            res = []
        return res

    def get_randamp(self):
        # амплитудные ошибки сигнала
        res = []
        if (self.error_distamp == 1):
            # гауссовское распределение ошибок
            res = np.random.normal(loc=1.0, scale=self.error_maxamp)
        return res

    def get_randphi(self):
        # фазовые ошибки сигнала
        res = []
        if (self.error_distphi == 1):
            # равномерное распределение ошибок
            res = np.random.uniform(-self.error_maxphi, self.error_maxphi)
        if (self.error_distphi == 2):
            # гауссовское распределение ошибок
            res = np.random.normal(loc=0.0, scale=self.error_maxphi)
        return res

    def get_eqvec(self, len_time, len_sig, vec_deg, vec_fband, num_all):
        # вычисление временного вектора эквивалентных углов сигнала
        vec_eqdegsig = []
        len_eqsig, sumlen_eqsig = np.zeros([len_time, len_sig]), np.zeros([len_time])
        l0_maxsig, f_otnsig = np.zeros([len_time, len_sig]), np.zeros([len_time, len_sig])
        for i in range(len_time):
            buf_eqdeg = []
            for j in range(len_sig):
                # вычисление углов эквивалентных сигналов
                buf = self.get_eqsig(vec_deg[i][j], vec_fband[i][j], num_all)
                buf_eqdeg.append(buf[0])
                len_eqsig[i][j] = buf[1]
                l0_maxsig[i][j] = buf[2]
                f_otnsig[i][j] = buf[3]
                sumlen_eqsig[i] = sumlen_eqsig[i] + len_eqsig[i][j]
            vec_eqdegsig.append(buf_eqdeg)
        return [vec_eqdegsig, len_eqsig, sumlen_eqsig, l0_maxsig, f_otnsig]

    def get_eqsig(self, deg, fband, num_all):
        # вычисление моментального вектора эквивалентных углов сигнала
        f_otn = fband / self.f_cen
        # количество эквивалентных помех сигнала
        len_eqsig = 0
        buf1 = num_all * fband * 2 * math.pi**2 * self.array_beta
        buf2 = buf1 * math.sin(math.radians(deg) / (4 * self.f_cen * math.pi))
        l0_max = abs(round(buf2))
        len_eqsig = len_eqsig + l0_max * 2 + 1
        # новый вектор углов сигнала
        vec_eqdeg = np.zeros(shape=[int(len_eqsig)])
        # заполняем вектор помех: [real_sig, -L, +L, -2L, +2L...]
        l = 0
        for i in range(int(len_eqsig)):
            if (i == 0):
                vec_eqdeg[i] = deg
            if (i % 2 != 0):
                l = l + 1
                vec_eqdeg[i] = math.degrees(math.radians(deg) - 2 * l / (num_all * self.array_beta))
                vec_eqdeg[i+1] = math.degrees(math.radians(deg) + 2 * l / (num_all * self.array_beta))
        # обозначение выходящих за пределы ДН углов числом 361
        range_show = [-90, 90]
        for i in range(vec_eqdeg.shape[0]):
            if (vec_eqdeg[i] < range_show[0]) or (vec_eqdeg[i] > range_show[1]):
                vec_eqdeg[i] = 361
        return [vec_eqdeg, len_eqsig, l0_max, f_otn]

    def get_eqamp(self, num_all, l0_max, l_var, f_otn):
        # вычисление множителя дискретного разложения Фурье для эквивалентных сигналов
        l0_maxreal = round(num_all / 2)
        coef_fourier = 0.0
        if (int(l0_max) != 0):
            for k in range(int(l0_maxreal)+1):
                arg_func1 = (f_otn * k * self.array_beta * math.pi) / 2
                arg_func2 = (2 * math.pi * k * l_var) / (l0_maxreal + 1)
                buf = (1 / (l0_maxreal+1)) * self.get_freqdist(arg_func1) * math.cos(arg_func2)
                coef_fourier = coef_fourier + buf
        else:
            coef_fourier = 1.0
        return coef_fourier

    def get_freqdist(self, x_var):
        # форма распределения частот входного сигнала
        if (x_var != 0.0):
            # соответствует прямоугольному импульсу
            res = np.sin(x_var) / x_var
        else:
            res = 1.0
        return res