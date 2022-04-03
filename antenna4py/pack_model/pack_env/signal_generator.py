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
        # интервал переключения временной последовательности
        self.swith_range = 21

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
            vec_mod = self.calc_degline(len_deg, len_time)
        if mode_deg == 2:
            # рандомное изменение углов одиночной помехи
            vec_mod = self.calc_degrand(len_deg, len_time)
        if mode_deg == 3:
            # рандомное изменение углов мерцающей помехи
            vec_mod = self.calc_deg2rand(len_deg, len_time, 0)
        if mode_deg == 4:
            # рандомное изменение углов мерцающей помехи (временные последовательности)
            vec_mod = self.calc_deg2rand(len_deg, len_time, 1)
        # вектора после модуляции
        vec_deg = cl.ones_modul(vec_mod, static_deg)
        return vec_deg

    def get_vecamp(self, vec_time, var_amp, mode_amp, freq_amp, shift_static, shift_dynamic):
        self.freq_amp = freq_amp
        # вычисление вектора изменения амплитуд
        len_amp, len_time = var_amp.shape[0], vec_time.shape[0]
        vec_mod = []
        # выбор режима
        if mode_amp == 0:
            # амплитуды без изменений
            vec_mod = np.ones(shape=[len_amp, len_time])
        if mode_amp == 1:
            # синусоидальный сигнал
            vec_mod = self.calc_ampsin(len_amp, vec_time, freq_amp, shift_static, shift_dynamic)
        if mode_amp == 2:
            # прямоугольные импульсы
            vec_mod = self.calc_amppulse(len_amp, vec_time, freq_amp, shift_static, shift_dynamic)
        if mode_amp == 3:
            # короткие импульсы
            vec_mod = self.calc_ampshort(len_amp, vec_time, freq_amp, shift_static, shift_dynamic)
        if mode_amp == 4:
            # рандомное изменение амплитуд одиночной помехи
            vec_mod = self.calc_amprand(len_amp, len_time)
        if mode_amp == 5:
            # рандомное изменение амплитуд мерцающей помехи
            vec_mod = self.calc_amp2rand(len_amp, len_time, 0)
        if mode_amp == 6:
            # рандомное изменение амплитуд мерцающей помехи (временные последовательности)
            vec_mod = self.calc_amp2sinrand(len_amp, vec_time, freq_amp, shift_static, shift_dynamic, 1)
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
            vec_mod = self.calc_bandrand(len_band, len_time)
        if mode_band == 2:
            # рандомное изменение частотных полос
            vec_mod = self.calc_band2rand(len_band, len_time, 0)
        if mode_band == 3:
            # рандомное изменение частотных полос (временные последовательности)
            vec_mod = self.calc_band2rand(len_band, len_time, 1)
        vec_band = cl.ones_modul(vec_mod, var_band)
        return vec_band

    def calc_degline(self, len_deg, len_time):
        # линейное изменение углов от -1 до 1
        vec_mod = np.ones(shape=[len_deg, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_deg):
                vec_mod[j][i] = (2 * i / (len_time-1)) - 1
        return vec_mod

    def calc_degrand(self, len_deg, len_time):
        # рандомные значения углов по равномерному распределению от -1 до 1
        vec_mod = np.ones(shape=[len_deg, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_deg):
                vec_mod[j][i] = np.random.uniform(-1, 1)
        return vec_mod

    def calc_deg2rand(self, len_deg, len_time, is_switch):
        # рандомные значения 2 углов по равномерному распределению от -1 до 1
        if len_deg != 2:
            print("Ошибка размерности, необходимы 2 угловых значения")
            exit()
        if is_switch == 0:
            self.swith_range = 1
        vec_mod = np.ones(shape=[len_deg, len_time])
        diff_deg = np.zeros(shape=[len_time])
        last_batch, now_batch = -1, -1
        now_deg1, now_deg2, diff_deg_var = 0, 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i/self.swith_range))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                # нормальное распределение для разности углов, среднее = ок. 25 град., СКО = ок. 9 град.
                flag = 0
                while flag == 0:
                    diff_deg_var = abs(np.random.normal(loc=(2.0/7), scale=(2.0/20)))
                    # проверка на допустимое значение [0,180] град
                    if diff_deg_var < 2.0:
                        flag = 1
                # равномерное распределение для 1-й из 2-х помех
                now_deg1 = np.random.uniform(-1, 1-diff_deg_var)
                now_deg2 = now_deg1 + diff_deg_var
            # формирование значений за текущий такт
            vec_mod[0][i] = now_deg1
            vec_mod[1][i] = now_deg2
            diff_deg[i] = diff_deg_var
            last_batch = now_batch
        print('diff_deg.mean = ', diff_deg.mean() * 90)
        return vec_mod

    def calc_ampsin(self, len_amp, vec_time, freq_amp, shift_static, shift_dynamic):
        # синусоида амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # время 1 ед = 1 мс
        vec_time = vec_time * math.pow(10, -3)
        # круговые частоты и фазы
        freq = 2 * math.pi * freq_amp
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                # итоговая модуляция
                vec_mod[i][j] = np.sin(freq * vec_time[j] + shift_static + shift_dynamic) * 0.5 + 0.5
            shift_dynamic = shift_dynamic * (-1)
        return vec_mod

    def calc_amppulse(self, len_amp, vec_time, freq_amp, shift_static, shift_dynamic):
        # импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # время 1 ед = 1 мс
        vec_time = vec_time * math.pow(10, -3)
        # круговые частоты и фазы
        freq = 2 * math.pi * freq_amp
        # цикл по сигналам
        for i in range(len_amp):
            # итоговая модуляция
            vec_mod[i] = sg.square(freq * vec_time + shift_static + shift_dynamic) * 0.5 + 0.5
            shift_dynamic = shift_dynamic * (-1)
        return vec_mod

    def calc_ampshort(self, len_amp, vec_time, freq_amp, shift_static, shift_dynamic):
        # короткие импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        # индикатор инверсии
        shift_static = math.pi / 2
        for i in range(len_amp):
            vec_mod1 = self.calc_amppulse(1, vec_time, freq_amp, 0, 0)
            vec_mod2 = self.calc_amppulse(1, vec_time, freq_amp*2, 0, 0)
            vec_mod3 = self.calc_amppulse(1, vec_time, freq_amp/2, shift_static, 0)
            shift_static = shift_static * (-1)
            # импульсы длительностью 1/4 периода через один
            vec_mod[i] = vec_mod1 * vec_mod2 * vec_mod3
        return vec_mod

    def calc_amprand(self, len_amp, len_time):
        # рандомные значения амплитуд мерцающей помехи
        # распределение Рэлея, стандарт. откл=0.2, строго > 0
        vec_mod = np.ones(shape=[len_amp, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_amp):
                vec_mod[j][i] = abs(np.random.rayleigh(scale=0.5))
        return vec_mod

    def calc_amp2rand(self, len_amp, len_time, is_switch):
        # рандомные значения амплитуд мерцающей помехи
        # распределение Рэлея, стандарт. откл=0.2, строго > 0
        if len_amp != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        if is_switch == 0:
            self.swith_range = 1
        vec_mod = np.ones(shape=[len_amp, len_time])
        last_batch, now_batch = -1, -1
        now_maxamp1, now_maxamp2 = 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i / self.swith_range))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                now_maxamp1 = abs(np.random.rayleigh(scale=0.5))
                now_maxamp2 = abs(np.random.rayleigh(scale=0.5))
            # формирование значений за текущий такт
            vec_mod[0][i] = now_maxamp1
            vec_mod[1][i] = now_maxamp2
            last_batch = now_batch
        return vec_mod

    def calc_amp2sinrand(self, len_amp, vec_time, freq_amp, shift_static, shift_dynamic, is_switch):
        # рандомные значения амплитуд мерцающей помехи
        # распределение Рэлея, стандарт. откл=0.2, строго > 0
        if len_amp != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        if is_switch == 0:
            self.swith_range = 1
        len_time = vec_time.shape[0]
        vec_mod = np.ones(shape=[len_amp, len_time])
        last_batch, now_batch, now_maxamp = -1, -1, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i / self.swith_range))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                # формирование значений на текущий пакет
                now_maxamp = np.abs(np.random.rayleigh(scale=0.6))
                now_shift = np.random.uniform(-math.pi, math.pi)
                vec_batch = vec_time[i:i+self.swith_range]
                res = self.calc_ampsin(len_amp, vec_batch, freq_amp, shift_static, now_shift)
                vec_mod[:, i:i + self.swith_range] = res * now_maxamp
            last_batch = now_batch
        return vec_mod

    def calc_bandrand(self, len_band, len_time):
        # рандомные значения частотных полос одиночной помехи
        # равномерное распределение от 0 до 1
        vec_mod = np.ones(shape=[len_band, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_band):
                vec_mod[j][i] = np.random.uniform(0, 1)
        return vec_mod

    def calc_band2rand(self, len_band, len_time, is_switch):
        # рандомные значения частотных полос мерцающей помехи
        # равномерное распределение от 0 до 1
        if len_band != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        if is_switch == 0:
            self.swith_range = 1
        vec_mod = np.ones(shape=[len_band, len_time])
        last_batch, now_batch = -1, -1
        now_band1, now_band2 = 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i/self.swith_range))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                now_band1 = np.random.uniform(0, 1)
                now_band2 = now_band1
            # формирование значений за текущий такт
            vec_mod[0][i] = now_band1
            vec_mod[1][i] = now_band2
            last_batch = now_batch
        return vec_mod

