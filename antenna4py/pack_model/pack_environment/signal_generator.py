import math
import pack_calc.calc_list as cl
import numpy as np
import scipy.signal as sg

if __name__ == "__main__":
    print("Вы запустили модуль генератора сигналов (L3)")

class Generator:
    """Класс моделирования генератора сигналов"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Параметры генератора сигналов (L3) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Параметры генератора сигналов (L3) --- ")
        print("signal_generator = ", self.get())

    def get_vecdeg(self, vec_time, var_deg, id_modulation):
        # вычисление вектора изменения углов
        len_deg = var_deg.shape[0]
        len_time = vec_time.shape[0]
        vec_mod = []
        print("len_deg = ", len_deg)
        print("len_time = ", len_time)
        if (id_modulation == 0):
            # углы без изменений
            vec_mod = np.ones(shape=[len_deg, len_time])
        if (id_modulation == 1):
            # линейное изменение углов
            vec_mod = self.get_degline(len_deg, len_time)
        # вектора после модуляции
        vec_deg = cl.ones_modul(vec_mod, var_deg)
        return vec_deg

    def get_vecamp(self, vec_time, var_amp, var_freq, id_modulation):
        # вычисление вектора изменения амплитуд
        len_amp = var_amp.shape[0]
        len_time = vec_time.shape[0]
        vec_mod = []
        if (id_modulation == 0):
            # амплитуды без изменений
            vec_mod = np.ones(shape=[len_amp, len_time])
        if (id_modulation == 1):
            # синусоидальный сигнал
            vec_mod = self.get_sin(len_amp, var_freq, vec_time, 0)
        if (id_modulation == 2):
            # прямоугольные импульсы
            vec_mod = self.get_pulse(len_amp, var_freq, vec_time, 0)
        if (id_modulation == 3):
            # короткие импульсы
            vec_mod = self.get_shortpulse(len_amp, var_freq, vec_time, 0)
        vec_amp = cl.ones_modul(vec_mod, var_amp)
        return vec_amp

    def get_vecband(self, vec_time, var_band, id_modulation):
        # вычисление вектора изменения частотных полос
        len_band = var_band.shape[0]
        len_time = vec_time.shape[0]
        vec_mod = []
        if (id_modulation == 0):
            # частотные полосы без изменений
            vec_mod = np.ones(shape=[len_band, len_time])
        vec_band = cl.ones_modul(vec_mod, var_band)
        return vec_band

    def get_degline(self, len_deg, len_time):
        # линейная модуляция от -1 до 1
        vec_mod = np.ones(shape=[len_deg, len_time])
        # цикл по сигналам
        for i in range(len_deg):
            # цикл по времени
            for j in range(len_time):
                vec_mod[i][j] = (2 * j / (len_time-1)) - 1
        return vec_mod

    def get_sin(self, len_amp, var_freq, vec_time, shift):
        # синусоида амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # круговые частоты и фазы
        freq = 2 * math.pi * var_freq
        shift = 2 * math.pi * shift
        # индикатор инверсии
        buf_sign = math.pi / 2
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                # время 1 ед = 1 мс
                var_time = vec_time[j] * math.pow(10, -6)
                # итоговая модуляция
                vec_mod[i][j] = np.sin(freq * var_time + shift + buf_sign) * 0.5 + 0.5
            buf_sign = buf_sign * (-1)
        return vec_mod

    def get_pulse(self, len_amp, var_freq, vec_time, shift):
        # импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # время 1 ед = 1 мс
        vec_time = vec_time * math.pow(10, -6)
        # круговые частоты и фазы
        freq = 2 * math.pi * var_freq
        shift = 2 * math.pi * shift - math.pi / 2
        # индикатор инверсии
        buf_sign = math.pi / 2
        # цикл по сигналам
        for i in range(len_amp):
            # итоговая модуляция
            vec_mod[i] = sg.square(freq * vec_time + shift + buf_sign) * 0.5 + 0.5
            buf_sign = buf_sign * (-1)
        return vec_mod

    def get_shortpulse(self, len_amp, var_freq, vec_time, shift):
        # короткие импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # индикатор инверсии
        buf_sign = 1
        for i in range(len_amp):
            vec_mod1 = self.get_pulse(1, var_freq, vec_time, 0)
            vec_mod2 = self.get_pulse(1, var_freq*2, vec_time, 0)
            vec_mod3 = self.get_pulse(1, var_freq/2, vec_time, 0.25 * buf_sign)
            buf_sign = buf_sign * (-1)
            # импульсы длительностью 1/4 периода через один
            vec_mod[i] = vec_mod1 * vec_mod2 * vec_mod3
        return vec_mod


