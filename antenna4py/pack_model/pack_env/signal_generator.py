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

    def set(self):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры генератора сигналов (L3):")
        print("\t-")

    def get_vecdeg(self, vec_time, static_deg, mode_deg):
        # вычисление вектора изменения углов
        len_deg, len_time = static_deg.shape[0], vec_time.shape[0]
        vec_mod = []
        # выбор режима
        if mode_deg == 0:
            # углы без изменений
            vec_mod = np.ones(shape=[len_deg, len_time])
        if mode_deg == 1:
            # линейное изменение углов
            vec_mod = self.get_degline(len_deg, len_time)
        if mode_deg == 2:
            # рандомное изменение углов одиночной помехи
            vec_mod = self.get_degrand(len_deg, len_time)
        if mode_deg == 3:
            # рандомное изменение углов мерцающей помехи
            vec_mod = self.get_deg2rand(len_deg, len_time)
        # вектора после модуляции
        vec_deg = cl.ones_modul(vec_mod, static_deg)
        return vec_deg

    def get_vecamp(self, vec_time, var_amp, mode_amp, freq_amp, static_shift, dynamic_shift):
        # вычисление вектора изменения амплитуд
        len_amp, len_time = var_amp.shape[0], vec_time.shape[0]
        vec_mod = []
        print('mode_amp = ', mode_amp)
        # выбор режима
        if mode_amp == 0:
            # амплитуды без изменений
            vec_mod = np.ones(shape=[len_amp, len_time])
        if mode_amp == 1:
            # синусоидальный сигнал
            vec_mod = self.get_ampsin(len_amp, freq_amp, vec_time, static_shift, dynamic_shift)
        if mode_amp == 2:
            # прямоугольные импульсы
            vec_mod = self.get_amppulse(len_amp, freq_amp, vec_time, static_shift, dynamic_shift)
        if mode_amp == 3:
            # короткие импульсы
            vec_mod = self.get_ampshort(len_amp, freq_amp, vec_time, static_shift, dynamic_shift)
        if mode_amp == 4:
            # рандомное изменение амплитуд одиночной помехи
            vec_mod = self.get_amprand(len_amp, len_time)
        if mode_amp == 5:
            # рандомное изменение амплитуд мерцающей помехи
            vec_mod = self.get_amp2rand(len_amp, len_time)
        vec_amp = cl.ones_modul(vec_mod, var_amp)
        return vec_amp

    def get_vecband(self, vec_time, var_band, mode_band):
        # вычисление вектора изменения частотных полос
        len_band, len_time = var_band.shape[0], vec_time.shape[0]
        vec_mod = []
        # выбор режима
        if mode_band == 0:
            # частотные полосы без изменений
            vec_mod = np.ones(shape=[len_band, len_time])
        if mode_band == 1:
            # рандомное изменение частотных полос
            vec_mod = self.get_bandrand(len_band, len_time)
        if mode_band == 2:
            # рандомное изменение частотных полос
            vec_mod = self.get_bandrand(len_band, len_time)
        vec_band = cl.ones_modul(vec_mod, var_band)
        return vec_band

    def get_degline(self, len_deg, len_time):
        # линейное изменение углов от -1 до 1
        vec_mod = np.ones(shape=[len_deg, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_deg):
                vec_mod[j][i] = (2 * i / (len_time-1)) - 1
        return vec_mod

    def get_degrand(self, len_deg, len_time):
        # рандомные значения углов по равномерному распределению от -1 до 1
        vec_mod = np.ones(shape=[len_deg, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_deg):
                vec_mod[j][i] = np.random.uniform(-1, 1)
        return vec_mod

    def get_deg2rand(self, len_deg, len_time):
        # рандомные значения 2 углов по равномерному распределению от -1 до 1
        if len_deg != 2:
            print("Ошибка размерности, необходимы 2 угловых значения")
            exit()
        vec_mod = np.ones(shape=[len_deg, len_time])
        diff_deg = np.zeros(shape=[len_time])
        # цикл по времени
        for i in range(len_time):
            # нормальное распределение, среднее = ок. 13 град., СКО = ок. 9 град.
            flag = 0
            while flag == 0:
                diff_deg[i] = abs(np.random.normal(loc=(2.0/13), scale=(2.0/20)))
                # проверка на допустимое значение
                if diff_deg[i] < 2.0:
                    flag = 1
            # цикл по сигналам
            vec_mod[0][i] = np.random.uniform(-1, 1-diff_deg[i])
            vec_mod[1][i] = vec_mod[0][i] + diff_deg[i]
        print('diff_deg.mean = ', diff_deg.mean() * 90)
        return vec_mod

    def get_ampsin(self, len_amp, var_freq, vec_time, static_shift, dynamic_shift):
        # синусоида амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # время 1 ед = 1 мс
        vec_time = vec_time * math.pow(10, -3)
        # круговые частоты и фазы
        freq = 2 * math.pi * var_freq
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                # итоговая модуляция
                vec_mod[i][j] = np.sin(freq * vec_time[j] + static_shift + dynamic_shift) * 0.5 + 0.5
            dynamic_shift = dynamic_shift * (-1)
        return vec_mod

    def get_amppulse(self, len_amp, var_freq, vec_time, static_shift, dynamic_shift):
        # импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # время 1 ед = 1 мс
        vec_time = vec_time * math.pow(10, -3)
        # круговые частоты и фазы
        freq = 2 * math.pi * var_freq
        # цикл по сигналам
        for i in range(len_amp):
            # итоговая модуляция
            vec_mod[i] = sg.square(freq * vec_time + static_shift + dynamic_shift) * 0.5 + 0.5
            dynamic_shift = dynamic_shift * (-1)
        return vec_mod

    def get_ampshort(self, len_amp, var_freq, vec_time, static_shift, dynamic_shift):
        # короткие импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # индикатор инверсии
        static_shift = math.pi / 2
        for i in range(len_amp):
            vec_mod1 = self.get_amppulse(1, var_freq, vec_time, 0, 0)
            vec_mod2 = self.get_amppulse(1, var_freq*2, vec_time, 0, 0)
            vec_mod3 = self.get_amppulse(1, var_freq/2, vec_time, static_shift, 0)
            static_shift = static_shift * (-1)
            # импульсы длительностью 1/4 периода через один
            vec_mod[i] = vec_mod1 * vec_mod2 * vec_mod3
        return vec_mod

    def get_amprand(self, len_amp, len_time):
        # рандомные значения амплитуд мерцающей помехи
        # нормальное распределение, среднее = 1, СКО = 0.3, строго > 0
        vec_mod = np.ones(shape=[len_amp, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_amp):
                vec_mod[j][i] = abs(np.random.normal(loc=1.0, scale=0.5))
        return vec_mod

    def get_amp2rand(self, len_amp, len_time):
        # рандомные значения амплитуд мерцающей помехи
        # нормальное распределение, среднее = 1, СКО = 0.3, строго > 0
        if len_amp != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        vec_mod = np.ones(shape=[len_amp, len_time])
        # цикл по времени
        for i in range(len_time):
            vec_mod[0][i] = abs(np.random.normal(loc=0.2, scale=0.1))
            vec_mod[1][i] = abs(vec_mod[0][i] + np.random.normal(loc=0.0, scale=0.05))
        return vec_mod

    def get_bandrand(self, len_band, len_time):
        # рандомные значения частотных полос одиночной помехи
        # равномерное распределение от 0 до 1
        vec_mod = np.ones(shape=[len_band, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_band):
                vec_mod[j][i] = np.random.uniform(0, 1)
        return vec_mod

    def get_band2rand(self, len_band, len_time):
        # рандомные значения частотных полос мерцающей помехи
        # равномерное распределение от 0 до 1
        if len_band != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        vec_mod = np.ones(shape=[len_band, len_time])
        # цикл по времени
        for i in range(len_time):
            vec_mod[0][i] = np.random.uniform(0, 1)
            vec_mod[1][i] = vec_mod[0][i]
        return vec_mod

