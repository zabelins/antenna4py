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
        # центральная частота для антенной системы
        self.f_cen = []
        # параметры множителя решётки
        self.array_N = []
        self.array_beta = []
        self.array_dist = []
        self.array_effect = []
        # параметры амплитудных и фазовых ошибок
        self.error_distphi = []
        self.error_distamp = []
        self.error_maxphi = []
        self.error_maxamp = []

    def set(self, init):
        self.f_cen = np.array(init[0])
        self.array_N = np.array(init[1])
        self.array_beta = np.array(init[2])
        self.array_dist = np.array(init[3])
        self.array_effect = np.array(init[4])
        self.error_distphi = np.array(init[7])
        self.error_distamp = np.array(init[8])
        self.error_maxphi = np.array(init[9])
        self.error_maxamp = np.array(init[10])

    def get(self):
        res = []
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
        print("Параметры модели множителя АР (L3):")
        print("\tf_cen = ", self.f_cen)
        print("\tarray_N = ", self.array_N)
        print("\tarray_beta = ", self.array_beta)
        print("\tarray_dist = ", self.array_dist)
        print("\tarray_effect = ", self.array_effect)
        print("\terror_distphi = ", self.error_distphi)
        print("\terror_distamp = ", self.error_distamp)
        print("\terror_maxphi = ", self.error_maxphi)
        print("\terror_maxamp = ", self.error_maxamp)

    def get_signal(self, amp, deg, num, rand):
        # комплексный сигнал для заданного элемента антенной решётки
        lambda_cen = self.con_c / self.f_cen
        step_array = self.array_beta * lambda_cen / 2
        fun_u = 2 * math.pi * step_array / lambda_cen * math.sin(deg) #float64
        fun_sig = amp * cmath.exp(1j * fun_u * (num - 1)) * cmath.exp(1j * rand)
        return fun_sig

    def get_dist(self, num_var):
        # АФР для заданного элемента антенной решётки
        res = []
        if self.array_dist == 0:
            # равномерное распределение
            res = 1.0
        if self.array_dist == 1:
            # косинусное распределение
            res = 0.4 + 0.6 * math.cos(math.pi * (num_var-1) / (self.array_N-1) - math.pi/2)
        if self.array_dist == 2:
            # распределение чебышева
            res = 1.0
            # нужно использовать Chebyshev()
        return res

    def get_randamp(self):
        # амплитудные ошибки сигнала
        res = []
        if self.error_distamp == 0:
            # гауссовское распределение ошибок
            res = np.random.normal(loc=1.0, scale=self.error_maxamp)
        return res

    def get_randphi(self):
        # фазовые ошибки сигнала
        res = []
        if self.error_distphi == 0:
            # равномерное распределение ошибок
            res = np.random.uniform(-self.error_maxphi, self.error_maxphi)
        if self.error_distphi == 1:
            # гауссовское распределение ошибок
            res = np.random.normal(loc=0.0, scale=self.error_maxphi)
        return res

    def get_eqvec(self, vec_deg, vec_band):
        # вычисление временного вектора эквивалентных углов сигнала
        len_time, len_sig = vec_deg.shape[0], vec_deg.shape[1]
        # кол-во всех помех (экв.+реал.) (от времени)
        num_all = np.zeros([len_time])
        # кол-во экв. помех для каждой реальной помехи (от времени)
        num_eq4real = np.zeros([len_time, len_sig])
        # число l для каждой реальной помехи (от времени)
        l4real = np.zeros([len_time, len_sig])
        # отн. полоса для каждой реальной помехи (от времени)
        f_otn4real = np.zeros([len_time, len_sig])
        # углы всех помех (от времени)
        vec_eqdeg = []
        for i in range(len_time):
            buf_eqdeg = []
            for j in range(len_sig):
                # вычисление углов эквивалентных сигналов
                buf = self.get_eqsig(vec_deg[i][j], vec_band[i][j])
                buf_eqdeg.append(buf[0])
                num_eq4real[i][j] = buf[1]
                l4real[i][j] = buf[2]
                f_otn4real[i][j] = buf[3]
                num_all[i] = num_all[i] + num_eq4real[i][j]
            vec_eqdeg.append(buf_eqdeg)
        return [vec_eqdeg, num_all, num_eq4real, l4real, f_otn4real]

    def get_eqsig(self, deg, band):
        # вычисление моментального вектора эквивалентных углов сигнала
        f_otn = band / self.f_cen
        # количество эквивалентных помех сигнала
        num_eq = 0
        buf1 = self.array_N * band * 2 * math.pi**2 * self.array_beta
        buf2 = buf1 * math.sin(math.radians(deg) / (4 * self.f_cen * math.pi))
        l0 = abs(round(buf2))
        num_eq = num_eq + l0 * 2 + 1
        # новый вектор углов сигнала
        vec_eqdeg = np.zeros(shape=[int(num_eq)])
        # заполняем вектор помех: [real_sig, -L, +L, -2L, +2L...]
        l = 0
        for i in range(int(num_eq)):
            if (i == 0):
                vec_eqdeg[i] = deg
            if (i % 2 != 0):
                l = l + 1
                vec_eqdeg[i] = math.degrees(math.radians(deg) - 2 * l / (self.array_N * self.array_beta))
                vec_eqdeg[i+1] = math.degrees(math.radians(deg) + 2 * l / (self.array_N * self.array_beta))
        # обозначение выходящих за пределы ДН углов числом 361
        range_show = [-90, 90]
        for i in range(vec_eqdeg.shape[0]):
            if vec_eqdeg[i] <= range_show[0] or vec_eqdeg[i] >= range_show[1]:
                vec_eqdeg[i] = 361.0
        return [vec_eqdeg, num_eq, l0, f_otn]

    def get_eqamp(self, array_N, l0, l_var, f_otn):
        # вычисление множителя дискретного разложения Фурье для эквивалентных сигналов
        l0_max = round(array_N / 2)
        coef_fourier = 0.0
        if int(l0) != 0:
            for k in range(int(l0_max)+1):
                arg_func1 = (f_otn * k * self.array_beta * math.pi) / 2
                arg_func2 = (2 * math.pi * k * l_var) / (l0_max + 1)
                buf = (1 / (l0_max+1)) * self.get_freqdist(arg_func1) * math.cos(arg_func2)
                coef_fourier = coef_fourier + buf
        else:
            coef_fourier = 1.0
        return coef_fourier

    def get_freqdist(self, x_var):
        # форма распределения частот входного сигнала
        if x_var != 0.0:
            # соответствует прямоугольному импульсу
            res = np.sin(x_var) / x_var
        else:
            res = 1.0
        return res