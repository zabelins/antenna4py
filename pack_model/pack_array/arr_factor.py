import math
import cmath
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from numpy.polynomial.chebyshev import Chebyshev

if __name__ == "__main__":
    print("Вы запустили модуль модели множителя АР (L3)")

class Factor:
    """Класс моделирования множителя антенной решётки"""
    con_c = 3 * math.pow(10, 8)

    def __init__(self):
        # параметры моделирования
        self.vec_deg = np.array([])
        # параметры решётки
        self.arr_frq = 0
        self.arr_size = 0
        self.arr_step = 0
        self.arr_dist = 0
        self.arr_effect = 0
        self.arr_noise = 0
        # прарметры предобработки
        self.acc_size = 0
        # параметры амплитудных и фазовых ошибок
        self.err_distphi = 0
        self.err_distamp = 0
        self.err_maxphi = 0
        self.err_maxamp = 0
        # параметры сигналов
        self.msg_carr = 0

    def set(self, init0, init1, init2):
        self.vec_deg = init0[0]
        self.arr_frq = init2[0]
        self.arr_size = init2[1]
        self.arr_step = init2[2]
        self.arr_dist = init2[3]
        self.arr_effect = init2[4]
        self.arr_noise = init2[5]
        self.acc_size = init2[7]
        self.err_distphi = init2[8]
        self.err_distamp = init2[9]
        self.err_maxphi = init2[10]
        self.err_maxamp = init2[11]
        self.msg_carr = init1[13]

    def get(self):
        res = []
        res.append(self.vec_deg)
        res.append(self.arr_frq)
        res.append(self.arr_size)
        res.append(self.arr_step)
        res.append(self.arr_dist)
        res.append(self.arr_effect)
        res.append(self.arr_noise)
        res.append(self.acc_size)
        res.append(self.err_distphi)
        res.append(self.err_distamp)
        res.append(self.err_maxphi)
        res.append(self.err_maxamp)
        res.append(self.msg_carr)
        return res

    def print(self):
        print("Параметры модели множителя АР (L3):")
        print("\tvec_deg = ", self.vec_deg)
        print("\tarr_frq = ", self.arr_frq)
        print("\tarr_size = ", self.arr_size)
        print("\tarr_step = ", self.arr_step)
        print("\tarr_dist = ", self.arr_dist)
        print("\tarr_effect = ", self.arr_effect)
        print("\tarr_noise = ", self.arr_noise)
        print("\tacc_size = ", self.acc_size)
        print("\terr_distphi = ", self.err_distphi)
        print("\terr_distamp = ", self.err_distamp)
        print("\terr_maxphi = ", self.err_maxphi)
        print("\terr_maxamp = ", self.err_maxamp)
        print("\tmsg_carr = ", self.msg_carr)

    def get_preproc(self, vec_sig, vec_int, vec_nois, vec_sum, vec_time, flag_mod):
        # предапертурная обработка сигналов
        # демодуляция полезного сигнала
        vec_sig, vec_int, vec_nois, vec_sum = self.demodulation(vec_sig, vec_int, vec_nois, vec_sum, vec_time, flag_mod)
        # накопление векторов сигналов
        vec_sig, vec_int, vec_nois, vec_sum = self.accumulation(vec_sig, vec_int, vec_nois, vec_sum, vec_time)
        return [vec_sig, vec_int, vec_nois, vec_sum]

    def demodulation(self, vec_sig, vec_int, vec_nois, vec_sum, vec_time, flag_mod):
        # демодуляция полезного сигнала
        if flag_mod == 1:
            # цикл по сигналам
            for i in range(vec_sig.shape[0]):
                vec_sig[i] = np.transpose(self.filter_band(vec_sig[i].T, vec_time))
            # цикл по помехам
            for i in range(vec_int.shape[0]):
                vec_int[i] = np.transpose(self.filter_band(vec_int[i].T, vec_time))
            # цикл по шуму
            for i in range(vec_nois.shape[0]):
                vec_nois[i] = np.transpose(self.filter_band(vec_nois[i].T, vec_time))
            vec_sum[0] = np.transpose(self.filter_band(vec_sum[0].T, vec_time))
            print("Осуществляется демодуляция...")
        return [vec_sig, vec_int, vec_nois, vec_sum]

    def accumulation(self, vec_sig, vec_int, vec_nois, vec_sum, vec_time):
        # накопление векторов сигналов
        vec_sig = self.get_vecacc(vec_sig, vec_time)
        vec_int = self.get_vecacc(vec_int, vec_time)
        vec_nois = self.get_vecacc(vec_nois, vec_time)
        vec_sum = self.get_vecacc(vec_sum, vec_time)
        return [vec_sig, vec_int, vec_nois, vec_sum]

    def get_vecacc(self, vec_sig, vec_time):
        vec_acc = np.zeros(shape=[vec_sig.shape[0], vec_time.shape[0], self.arr_size], dtype=complex)
        # получить усреднённый вектор
        for t in range(vec_time.shape[0]):
            if t != 0 and int(self.acc_size) != 0 and t < int(self.acc_size):
                # переходной режим усреднения
                win_var = t
                vec_acc[:, t, :] = np.sum(vec_sig[:, t - win_var: t, :], axis=1) / win_var
            elif int(self.acc_size) != 0 and t >= int(self.acc_size):
                # рабочий режим усреднения
                vec_acc[:, t, :] = np.sum(vec_sig[:, t - int(self.acc_size): t, :], axis=1) / int(self.acc_size)
            else:
                vec_acc[:, t, :] = vec_sig[:, t, :]
        return vec_acc

    def get_vecnoise(self, vec_time):
        # формирование собственных шумов решётки
        vec_nois = np.zeros(shape=[1, vec_time.shape[0], self.arr_size], dtype=complex)
        # если есть временная шкала
        if vec_time.shape[0] > 1:
            vec_nois_abs = np.zeros(shape=[self.arr_size, vec_time.shape[0]], dtype=float)
            vec_nois_arg = np.zeros(shape=[self.arr_size, vec_time.shape[0]], dtype=float)
            # цикл по элементам
            for i in range(self.arr_size):
                # цикл по времени
                for j in range(vec_time.shape[0]):
                    # амплитуда = распр. Рэлея, фаза = равномерное распр.
                    vec_nois_abs[i][j] = np.random.rayleigh(scale=self.arr_noise)
                    vec_nois_arg[i][j] = np.random.rand() * 2 * np.pi
            # конвертация
            vec_nois_re = np.sin(vec_nois_arg) * vec_nois_abs
            vec_nois_im = np.cos(vec_nois_arg) * vec_nois_abs
            # фильтрация собственных шумов + повышение уровня порога (?)
            vec_nois_buf = vec_nois_re.T + 1j * vec_nois_im.T
            # проверка
            #plt.plot(vec_time, np.real(vec_nois_re[0]))
            #plt.show()
            # формирование корректного формата
            for i in range(vec_time.shape[0]):
                vec_nois[0][i] = vec_nois_buf[i]
        return vec_nois

    def filter_band(self, vec_mod, vec_time):
        # фильтрация шума в полосе [2.5 МГц, 7.5 МГц]
        frq_sampl = 1 / (vec_time[1] - vec_time[0])
        frq_min, frq_max = self.msg_carr / 2, self.msg_carr + self.msg_carr / 2
        [b11, a11] = signal.ellip(5, 0.5, 60, [frq_min * 2 / frq_sampl, frq_max * 2 / frq_sampl], btype='bandpass', analog=False, output='ba')
        bandpass_out = signal.filtfilt(b11, a11, vec_mod)
        # когерентная демодуляция
        coherent_carr = np.cos(np.dot(2 * np.pi * self.msg_carr, vec_time))
        coherent_demod = bandpass_out * (coherent_carr * 2)
        # фильтрация сигнала в полосе [0, 2.5 МГц]
        frq_high = frq_min
        [b12, a12] = signal.ellip(5, 0.5, 60, (frq_high * 2 / frq_sampl), btype='lowpass', analog=False, output='ba')
        lowpass_out = signal.filtfilt(b12, a12, coherent_demod)
        return lowpass_out

    def get_signal(self, amp, deg, num, rand):
        # комплексный сигнал для заданного элемента фазированной антенной решётки
        wave_len = self.con_c / self.arr_frq
        real_step = self.arr_step * wave_len / 2
        fun_u = 2 * math.pi * real_step / wave_len * math.sin(deg)
        fun_sig = amp * cmath.exp(1j * fun_u * (num - 1)) * cmath.exp(1j * rand)
        return fun_sig

    def get_dist(self, num):
        # АФР для заданного элемента антенной решётки
        res = []
        if self.arr_dist == 0:
            # равномерное распределение
            res = 1.0
        if self.arr_dist == 1:
            # косинусное распределение
            res = 0.4 + 0.6 * math.cos(math.pi * (num-1) / (self.arr_size-1) - math.pi/2)
        if self.arr_dist == 2:
            # распределение чебышева
            res = 1.0
            # нужно использовать Chebyshev()
        return res

    def get_randamp(self):
        # амплитудные ошибки сигнала
        res = []
        if self.err_distamp == 0:
            # гауссовское распределение ошибок
            res = np.random.normal(loc=1.0, scale=self.err_maxamp)
        return res

    def get_randphi(self):
        # фазовые ошибки сигнала
        res = []
        if self.err_distphi == 0:
            # равномерное распределение ошибок
            res = np.random.uniform(-self.err_maxphi, self.err_maxphi)
        if self.err_distphi == 1:
            # гауссовское распределение ошибок
            res = np.random.normal(loc=0.0, scale=self.err_maxphi)
        return res

    def get_eqvec(self, vec_sigdeg, vec_band):
        # вычисление вектора эквивалентных углов сигнала
        len_time, len_realsig, vec_eqdeg = vec_sigdeg.shape[0], vec_sigdeg.shape[1], []
        # кол-во всех помех (экв.+реал.), кол-во экв. помех для каждой реальной помехи,
        # число l для каждой реальной помехи, отн. полоса для каждой реальной помехи
        num_sig = np.zeros([len_time])
        eq4real = np.zeros([len_time, len_realsig])
        pair4real = np.zeros([len_time, len_realsig])
        band4real = np.zeros([len_time, len_realsig])
        # цикл по времени
        for i in range(len_time):
            buf_eqdeg = []
            # цикл по реальным сигалам
            for j in range(len_realsig):
                # вычисление углов эквивалентных сигналов
                [eqdeg, num_eq, pair, band] = self.get_eqsig(vec_sigdeg[i][j], vec_band[i][j])
                buf_eqdeg.append(eqdeg)
                eq4real[i][j] = num_eq
                pair4real[i][j] = pair
                band4real[i][j] = band
                num_sig[i] = num_sig[i] + eq4real[i][j]
            vec_eqdeg.append(buf_eqdeg)
        return [vec_eqdeg, num_sig, eq4real, pair4real, band4real]

    def get_eqsig(self, deg, band):
        # вычисление моментального вектора эквивалентных углов для реального сигнала
        band_otn, num_eq = band / self.arr_frq, 0
        # количество эквивалентных сигналов
        band_omega = band * 2 * math.pi
        carr_omega = self.arr_frq * 2 * math.pi
        deg_rad = math.radians(deg)
        l0 = abs(round(self.arr_size * band_omega * math.pi * self.arr_step * math.sin(deg_rad / (2 * carr_omega))))
        num_eq = num_eq + l0 * 2 + 1
        # новый вектор углов сигнала
        eqdeg = np.zeros(shape=[int(num_eq)])
        # заполняем вектор сигнала: [real_sig, -L, +L, -2L, +2L...]
        l = 0
        for i in range(int(num_eq)):
            if i == 0:
                # реальный сигнал
                eqdeg[i] = deg
            if i % 2 != 0:
                # эквивалентный сигнал
                l = l + 1
                eqdeg[i] = math.degrees(math.radians(deg) - 2 * l / (self.arr_size * self.arr_step))
                eqdeg[i+1] = math.degrees(math.radians(deg) + 2 * l / (self.arr_size * self.arr_step))
        # обозначение выходящих за пределы ДН углов числом 361
        for i in range(eqdeg.shape[0]):
            if eqdeg[i] <= self.vec_deg[0] or eqdeg[i] >= self.vec_deg[-1]:
                eqdeg[i] = 361.0
        return [eqdeg, num_eq, l0, band_otn]

    def get_eqamp(self, l0, l_var, f_otn):
        # вычисление множителя дискретного разложения Фурье для эквивалентных сигналов
        l0_max = round(self.arr_size / 2)
        coef_fourier = 0.0
        if int(l0) != 0:
            for k in range(int(l0_max)+1):
                arg_func1 = (f_otn * k * self.arr_step * math.pi) / 2
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