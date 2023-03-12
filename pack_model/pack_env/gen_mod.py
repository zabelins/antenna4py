import math
import pack_calc.calc_list as cl
import numpy as np
import scipy.signal as signal

if __name__ == "__main__":
    print("Вы запустили модуль генератора модуляции (L3)")

class Genmod:
    """Класс моделирования генератора модуляции"""

    def __init__(self):
        # параметры решётки
        self.arr_frq = 0
        # параметры сигналов
        self.sig_amp = 0
        self.sig_frq = 0
        self.sig_mod = 0
        self.sig_inf = 0
        # параметры помех
        self.int_amp = 0
        self.int_frq = 0
        self.int_mod = 0
        self.int_inf = 0
        # параметры модуляции
        self.msg_code = 0
        self.msg_carr = 0
        self.shift_dynamic = 0
        self.shift_static = 0
        # параметры выборки
        self.learn_size = 0
        # выходной параметр
        self.mod_code = []

    def set(self, init0, init1):
        self.arr_frq = init1[0]
        self.sig_amp = np.array(init0[1])
        self.sig_frq = init0[3]
        self.sig_mod = init0[4]
        self.sig_inf = init0[5]
        self.int_amp = np.array(init0[7])
        self.int_frq = init0[9]
        self.int_mod = init0[10]
        self.int_inf = init0[11]
        self.msg_code = init0[12]
        self.msg_carr = init0[13]
        self.shift_dynamic = np.array(init0[14])
        self.shift_static = np.array(init0[15])
        self.learn_size = init0[16]

    def get(self):
        res = []
        res.append(self.arr_frq)
        res.append(self.sig_amp)
        res.append(self.sig_frq)
        res.append(self.sig_mod)
        res.append(self.sig_inf)
        res.append(self.int_amp)
        res.append(self.int_frq)
        res.append(self.int_mod)
        res.append(self.int_inf)
        res.append(self.msg_code)
        res.append(self.msg_carr)
        res.append(self.shift_dynamic)
        res.append(self.shift_static)
        res.append(self.learn_size)
        return res

    def print(self):
        print("Параметры генератора модуляции (L3):")
        print("\tarr_frq = ", self.arr_frq)
        print("\tsig_amp = ", self.sig_amp)
        print("\tsig_frq = ", self.sig_frq)
        print("\tsig_mod = ", self.sig_mod)
        print("\tsig_inf = ", self.sig_inf)
        print("\tint_amp = ", self.int_amp)
        print("\tint_frq = ", self.int_frq)
        print("\tint_mod = ", self.int_mod)
        print("\tint_inf = ", self.int_inf)
        print("\tmsg_code = ", self.msg_code)
        print("\tmsg_carr = ", self.msg_carr)
        print("\tshift_dynamic = ", self.shift_dynamic)
        print("\tshift_static = ", self.shift_static)
        print("\tlearn_size = ", self.learn_size)

    def get_vec(self, vec_time, id_amp, var_par, is_int):
        # вычисление вектора изменения амплитуд
        vec_mod = []
        [amp, frq, mod, inf] = self.get_par(is_int)
        # выбор режима
        if id_amp == 0:
            # статический режим - исходная амплитуда
            vec_mod = self.information(0, amp, 0, 0, 0, vec_time)
        elif id_amp == 1:
            # статический режим - единичная амплитуда
            amp = np.array([1])
            vec_mod = self.information(0, amp, 0, 0, 0, vec_time)
        elif id_amp == 2:
            # время - произвольная модуляция с исходной амплитудой
            vec_mod = self.information(inf, amp, frq, self.shift_static, self.shift_dynamic, vec_time)
            vec_mod = self.modulation(mod, vec_mod, vec_time)   # модуляция [0,1]
        elif id_amp == 3:
            # время - выборка случайной одиночной помехи
            vec_mod = self.information(6, amp, 0, 0, 0, vec_time)
        elif id_amp == 4:
            # время - выборка случайной мерцающей помехи
            vec_mod = self.information(7, amp, 0, 0, 0, vec_time)   # нужна размерность амплитуд 2!
        elif id_amp == 5:
            # время - выборка потока битов с накоплением
            vec_mod = self.information(4, amp, frq, 0, 0, vec_time)
            vec_mod = self.modulation(1, vec_mod, vec_time)
        elif id_amp == 6:
            # время - выборка шумовой помехи с накоплением
            vec_mod = self.information(5, amp, frq, 0, 0, vec_time)
            vec_mod = self.modulation(1, vec_mod, vec_time)
        elif id_amp == 7:
            # время - выборка импульсной помехи с накоплением
            vec_mod = self.information(1, amp, frq, self.shift_static, self.shift_dynamic, vec_time)
            vec_mod = self.modulation(1, vec_mod, vec_time)
        elif id_amp == 8:
            # время - выборка мерцающей помехи с накоплением
            vec_mod = self.information(8, amp, self.int_frq, self.shift_static, self.shift_dynamic, vec_time) # нужна размерность амплитуд 2!
            vec_mod = self.modulation(1, vec_mod, vec_time)
        elif id_amp == 9:
            # параметр - модулированная амплитуда
            amp = amp * var_par
            vec_mod = self.information(inf, amp, frq, self.shift_static, self.shift_dynamic, vec_time)
            vec_mod = self.modulation(mod, vec_mod, vec_time)
        vec_amp = cl.ones_modul(vec_mod, amp)
        return vec_amp

    def information(self, inf, var_amp, var_frq, var_shiftst, var_shiftdn, vec_time):
        vec_inf = []
        # выбор модулирующей огибающей
        if inf == 0:
            # постоянный сигнал
            vec_inf = np.ones(shape=[var_amp.shape[0], vec_time.shape[0]])
        elif inf == 1:
            # короткие импульсы
            vec_inf = self.inf_short(var_amp.shape[0], vec_time, var_frq, var_shiftst, var_shiftdn)
        elif inf == 2:
            # длинные импульсы
            vec_inf = self.inf_pulse(var_amp.shape[0], vec_time, var_frq, var_shiftst, var_shiftdn)
        elif inf == 3:
            # синусоидальный сигнал
            vec_inf = self.inf_sin(var_amp.shape[0], vec_time, var_frq, var_shiftst, var_shiftdn)
        elif inf == 4:
            # поток битов
            vec_inf = self.inf_bit(var_amp.shape[0], vec_time, var_frq)
        elif inf == 5:
            # фазовый шум
            vec_inf = self.inf_noisephs(var_amp.shape[0], vec_time)
        elif inf == 6:
            # рандомная амплитуда (1 помеха)
            vec_inf = self.inf_1rand(var_amp.shape[0], vec_time.shape[0])
        elif inf == 7:
            # рандомные амплитуды (2 помехи)
            vec_inf = self.inf_2rand(var_amp.shape[0], vec_time.shape[0], 0)
        elif inf == 8:
            # рандомные амплитуды (временной ряд для мерцающей помехи)
            vec_inf = self.inf_2randmod(var_amp.shape[0], vec_time, var_frq, var_shiftst, var_shiftdn, 1)
        return vec_inf

    def modulation(self, mod, vec_mod0, vec_time):
        # частота дискретизации (100 МГц)
        vec_mod, frq_samp = [], 1 / (vec_time[1] - vec_time[0])
        # выбор типа модуляции
        if mod == 0:
            # без модуляции
            vec_mod = vec_mod0 * 1
        elif mod == 1:
            # фазовая (BPSK)
            vec_mod = np.cos(np.dot(2 * np.pi * self.msg_carr, vec_time) + np.pi * (vec_mod0 - 1) + np.pi / 4)
        elif mod == 2:
            # фазовая (BPSK) - накопление с переменной амплитудой
            vec_mod = self.mod_randPM(vec_time, vec_mod0)
        return vec_mod

    def inf_sin(self, len_amp, vec_time, frq_amp, shift_static, shift_dynamic):
        # синусоида амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        # круговые частоты и фазы
        frq = 2 * math.pi * frq_amp
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                vec_inf[i][j] = np.real(np.exp(1j * (frq * vec_time[j] + shift_static + shift_dynamic)) * 0.5 + 0.5)
            shift_dynamic = shift_dynamic * (-1)
        return vec_inf

    def inf_pulse(self, len_amp, vec_time, frq_amp, shift_static, shift_dynamic):
        # импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        # круговые частоты и фазы
        frq = 2 * math.pi * frq_amp
        # цикл по сигналам
        for i in range(len_amp):
            # итоговая модуляция
            vec_inf[i] = signal.square(frq * vec_time + shift_static + shift_dynamic) * 0.5 + 0.5
            shift_dynamic = shift_dynamic * (-1)
        return vec_inf

    def inf_short(self, len_amp, vec_time, frq_amp, shift_static, shift_dynamic):
        # короткие импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        # индикатор инверсии
        shift_static = math.pi / 2
        for i in range(len_amp):
            vec_inf1 = self.inf_pulse(1, vec_time, frq_amp, 0, 0)
            vec_inf2 = self.inf_pulse(1, vec_time, frq_amp*2, 0, 0)
            vec_inf3 = self.inf_pulse(1, vec_time, frq_amp/2, shift_static, 0)
            shift_static = shift_static * (-1)
            # импульсы длительностью 1/4 периода через один
            vec_inf[i] = vec_inf1 * vec_inf2 * vec_inf3
        return vec_inf

    def inf_bit(self, len_amp, vec_time, frq_amp):
        # поток бит амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        # параметры
        rand_is = 0
        # последовательность 31 символ
        if rand_is == 0:
            mod_code = np.random.randint(0, 2, self.msg_code)
        else:
            mod_code = [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0]
            mod_code = mod_code[0:self.msg_code]
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                vec_inf[i][j] = mod_code[math.floor(vec_time[j] * frq_amp)]
        self.mod_code = mod_code
        return vec_inf

    def inf_noisephs(self, len_amp, vec_time):
        # равномерное распределение от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.zeros(shape=[len_amp, len_time])
        vec_inf = vec_inf + np.random.rand(vec_inf.shape[0], vec_inf.shape[1]) * 2
        return vec_inf

    def inf_1rand(self, len_amp, len_time):
        # рандомные значения амплитуды помехи
        # распределение Рэлея, стандарт. откл=1, строго > 0
        if len_amp != 1:
            print("Ошибка размерности, необходимо 1 амплитудное значение")
            exit()
        vec_inf = np.zeros(shape=[len_amp, len_time])
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                vec_inf_abs = np.random.rayleigh(scale=1)
                vec_inf_arg = np.random.rand() * 2 * np.pi
                vec_inf[i][j] = np.sin(vec_inf_arg) * vec_inf_abs
        return vec_inf

    def inf_2rand(self, len_amp, len_time, is_switch):
        # рандомные значения амплитуд мерцающей помехи
        # распределение Рэлея, стандарт. откл=0.2, строго > 0
        if len_amp != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        if is_switch == 0:
            self.learn_size = 1
        vec_inf = np.ones(shape=[len_amp, len_time])
        last_batch, now_batch = -1, -1
        now_maxamp1, now_maxamp2 = 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i / self.learn_size))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                now_maxamp1 = abs(np.random.rayleigh(scale=0.5))
                now_maxamp2 = abs(np.random.rayleigh(scale=0.5))
            # формирование значений за текущий такт
            vec_inf[0][i] = now_maxamp1
            vec_inf[1][i] = now_maxamp2
            last_batch = now_batch
        return vec_inf

    def inf_2randmod(self, len_amp, vec_time, frq_amp, shift_static, shift_dynamic, is_switch):
        # рандомные значения амплитуд мерцающей помехи
        # распределение Рэлея, стандарт. откл=0.2, строго > 0
        if len_amp != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        if is_switch == 0:
            self.learn_size = 1
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        last_batch, now_batch, now_maxamp = -1, -1, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i / self.learn_size))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                # определение случайных параметров
                now_maxamp = np.abs(np.random.rayleigh(scale=0.6))
                now_shift = np.random.uniform(-math.pi, math.pi)
                now_frq = np.abs(np.random.normal(loc=frq_amp, scale=frq_amp/10))
                # формирование значений на текущий пакет
                vec_batch = vec_time[i:i+self.learn_size]
                res = self.inf_sin(len_amp, vec_batch, now_frq, now_shift, shift_dynamic)
                vec_inf[:, i:i + self.learn_size] = res * now_maxamp
            last_batch = now_batch
        return vec_inf

    def mod_randPM(self, vec_time, vec_mod0):
        # поток бит с произвольной амплитудой
        len_time = vec_time.shape[0]
        vec_mod = np.cos(np.dot(2 * np.pi * self.msg_carr, vec_time) + np.pi * (vec_mod0 - 1) + np.pi / 4)
        last_batch, now_batch, now_amp = -1, -1, 1
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i / self.learn_size))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                now_amp = np.random.uniform(0.5, 10)
            vec_mod[0][i] = vec_mod[0][i] * now_amp
            last_batch = now_batch
        return vec_mod

    def get_par(self, is_int):
        # сигнал или помеха
        amp, frq, mod, inf = [], [], [], []
        if is_int == 0:
            # сигнал
            amp, frq, mod, inf = self.sig_amp, self.sig_frq, self.sig_mod, self.sig_inf
        elif is_int == 1:
            # помеха
            amp, frq, mod, inf = self.int_amp, self.int_frq, self.int_mod, self.int_inf
        return [amp, frq, mod, inf]

    def get_code(self):
        return self.mod_code
