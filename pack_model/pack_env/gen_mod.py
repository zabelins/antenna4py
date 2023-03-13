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
        vec_inf, vec_mod = [], []
        [amp, frq, mod, inf] = self.get_par(is_int)
        # выбор режима
        if id_amp == 0:
            # статический режим - исходная амплитуда
            vec_inf = self.information(0, vec_time, amp, 0, 0, 0)
            vec_mod = self.modulation(0, vec_time, vec_inf)
        elif id_amp == 1:
            # статический режим - единичная амплитуда
            amp = np.array([1])
            vec_inf = self.information(0, vec_time, amp, 0, 0, 0)
            vec_mod = self.modulation(0, vec_time, vec_inf)
        elif id_amp == 2:
            # время - произвольная модуляция с исходной амплитудой
            vec_inf = self.information(inf, vec_time, amp, frq, self.shift_static, self.shift_dynamic)
            vec_mod = self.modulation(mod, vec_time, vec_inf)   # модуляция [0,1]
        elif id_amp == 3:
            # время - выборка случайной одиночной помехи
            vec_inf = self.information(6, vec_time, amp, 0, 0, 0)
            vec_mod = self.modulation(0, vec_time, vec_inf)
        elif id_amp == 4:
            # время - выборка случайной мерцающей помехи
            vec_inf = self.information(7, vec_time, amp, 0, 0, 0)
            vec_mod = self.modulation(0, vec_time, vec_inf)
        elif id_amp == 5:
            # время - выборка потока битов с накоплением
            vec_inf = self.information(8, vec_time, amp, frq, 0, 0)
            vec_mod = self.modulation(1, vec_time, vec_inf)
        elif id_amp == 6:
            # время - выборка шумовой помехи с накоплением
            vec_inf = self.information(9, vec_time, amp, frq, 0, 0)
            vec_mod = self.modulation(2, vec_time, vec_inf)
        elif id_amp == 7:
            # время - выборка импульсной помехи с накоплением
            vec_inf = self.information(10, vec_time, amp, frq, self.shift_static, self.shift_dynamic)
            vec_mod = self.modulation(2, vec_time, vec_inf)
        elif id_amp == 8:
            # время - выборка мерцающей помехи с накоплением
            vec_inf = self.information(11, vec_time, amp, self.int_frq, self.shift_static, self.shift_dynamic)
            vec_mod = self.modulation(1, vec_time, vec_inf)
        elif id_amp == 9:
            # параметр - модулированная амплитуда
            amp = amp * var_par
            vec_inf = self.information(inf, vec_time, amp, frq, self.shift_static, self.shift_dynamic)
            vec_mod = self.modulation(mod, vec_time, vec_inf)
        vec_amp = cl.ones_modul(vec_mod, amp)
        return vec_amp

    def information(self, inf, vec_time, amp, frq, shift_static, shift_dynamic):
        vec_inf = []
        # выбор модулирующей огибающей
        if inf == 0:
            # постоянный сигнал
            vec_inf = np.ones(shape=[amp.shape[0], vec_time.shape[0]])
        elif inf == 1:
            # модуляция - длинные импульсы
            vec_inf = self.inf_meander(vec_time, amp.shape[0], frq, shift_static, shift_dynamic)
        elif inf == 2:
            # модуляция - короткие импульсы
            vec_inf = self.inf_pulse(vec_time, amp.shape[0], frq, shift_static, shift_dynamic)
        elif inf == 3:
            # модуляция - синусоидальный сигнал
            vec_inf = self.inf_sin(vec_time, amp.shape[0], frq, shift_static, shift_dynamic)
        elif inf == 4:
            # модуляция - поток битов
            vec_inf = self.inf_bit(vec_time, amp.shape[0], frq)
        elif inf == 5:
            # модуляция - фазовый шум
            vec_inf = self.inf_noisephs(vec_time, amp.shape[0])
        elif inf == 6:
            # обучение - случайные амплитуда (1 помеха)
            vec_inf = self.inf_rand(vec_time.shape[0], amp.shape[0])
        elif inf == 7:
            # обучение - случайные амплитуды (2 помехи)
            vec_inf = self.inf_2rand(vec_time.shape[0], amp.shape[0])
        elif inf == 8:
            # обучение с накоплением - поток битов
            vec_inf = self.inf_bitgen(vec_time, amp.shape[0], frq)
        elif inf == 9:
            # обучение с накоплением - шумовая помеха
            vec_inf = self.inf_noisegen(vec_time, amp.shape[0])
        elif inf == 10:
            # обучение с накоплением - импульсная помеха
            vec_inf = self.inf_pulsegen(vec_time, amp.shape[0], frq, shift_static, shift_dynamic)
        elif inf == 11:
            # обучение с накоплением - мерцающая помеха
            vec_inf = self.inf_blinkgen(vec_time, amp.shape[0], frq, shift_static, shift_dynamic)
        return vec_inf

    def modulation(self, mod, vec_time, vec_inf):
        vec_mod = []
        # выбор модуляции радиосигнала
        if mod == 0:
            # без модуляции
            vec_mod = vec_inf * 1
        elif mod == 1:
            # фазовая (BPSK)
            vec_mod = self.mod_PM(vec_time, vec_inf)
        elif mod == 2:
            # обучение с накоплением - фазовая (BPSK)
            vec_mod = self.mod_randPM(vec_time, vec_inf)
        return vec_mod

    def inf_meander(self, vec_time, len_amp, frq_amp, shift_static, shift_dynamic):
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

    def inf_pulse(self, vec_time, len_amp, frq_amp, shift_static, shift_dynamic):
        # короткие импульсы амплитудой от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        # индикатор инверсии
        shift_static = math.pi / 2
        for i in range(len_amp):
            vec_inf1 = self.inf_meander(vec_time, 1, frq_amp, 0, 0)
            vec_inf2 = self.inf_meander(vec_time, 1, frq_amp*2, 0, 0)
            vec_inf3 = self.inf_meander(vec_time, 1, frq_amp/2, shift_static, 0)
            shift_static = shift_static * (-1)
            # импульсы длительностью 1/4 периода через один
            vec_inf[i] = vec_inf1 * vec_inf2 * vec_inf3
        return vec_inf

    def inf_sin(self, vec_time, len_amp, frq_amp, shift_static, shift_dynamic):
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

    def inf_bit(self, vec_time, len_amp, frq_amp):
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

    def inf_noisephs(self, vec_time, len_amp):
        # равномерное распределение от 0 до 1
        len_time = vec_time.shape[0]
        vec_inf = np.zeros(shape=[len_amp, len_time])
        vec_inf = vec_inf + np.random.rand(vec_inf.shape[0], vec_inf.shape[1]) * 2
        return vec_inf

    def inf_rand(self, len_time, len_amp):
        # рандомные значения амплитуды помехи
        self.check_amp(len_amp, 1)
        vec_inf = np.zeros(shape=[len_amp, len_time])
        # цикл по сигналам
        for i in range(len_amp):
            # цикл по времени
            for j in range(len_time):
                # распределение Рэлея, стандарт. откл=1, строго > 0
                vec_inf_abs = np.random.rayleigh(scale=1)
                vec_inf_arg = np.random.rand() * 2 * np.pi
                vec_inf[i][j] = np.sin(vec_inf_arg) * vec_inf_abs
        return vec_inf

    def inf_2rand(self, len_time, len_amp):
        # рандомные значения амплитуд мерцающей помехи
        self.check_amp(len_amp, 2)
        vec_inf = np.ones(shape=[len_amp, len_time])
        # цикл по времени
        for i in range(len_time):
            # распределение Рэлея, стандарт. откл=0.2, строго > 0
            vec_inf[0][i] = abs(np.random.rayleigh(scale=0.5))
            vec_inf[1][i] = abs(np.random.rayleigh(scale=0.5))
        return vec_inf

    def inf_bitgen(self, vec_time, len_amp, frq):
        vec_inf = self.inf_bit(vec_time, len_amp, frq)
        return vec_inf

    def inf_noisegen(self, vec_time, len_amp):
        vec_inf = self.inf_noisephs(vec_time, len_amp)
        return vec_inf

    def inf_pulsegen(self, vec_time, len_amp, frq, shift_static, shift_dynamic):
        vec_inf = self.inf_pulse(vec_time, len_amp, frq, shift_static, shift_dynamic)
        return vec_inf

    def inf_blinkgen(self, vec_time, len_amp, frq_amp, shift_static, shift_dynamic):
        # рандомные значения амплитуд мерцающей помехи
        # распределение Рэлея, стандарт. откл=0.2, строго > 0
        self.check_amp(len_amp, 2)
        len_time = vec_time.shape[0]
        vec_inf = np.ones(shape=[len_amp, len_time])
        last_seq, new_seq, new_amp = 0, 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            new_seq = np.int(np.floor(i / self.learn_size) + 1)
            # срабатывание переключателя модуляции
            if new_seq != last_seq:
                # определение случайных параметров
                new_amp = np.abs(np.random.rayleigh(scale=0.6))
                new_shift = np.random.uniform(-math.pi, math.pi)
                new_frq = np.abs(np.random.normal(loc=frq_amp, scale=frq_amp/10))
                # формирование значений на текущий пакет
                vec_seq = vec_time[i:i+self.learn_size]
                res = self.inf_sin(len_amp, vec_seq, new_frq, new_shift, shift_dynamic)
                vec_inf[:, i:i + self.learn_size] = res * new_amp
            last_seq = new_seq
        return vec_inf

    def mod_PM(self, vec_time, vec_inf):
        vec_mod = np.cos(np.dot(2 * np.pi * self.msg_carr, vec_time) + np.pi * (vec_inf - 1) + np.pi / 4)
        return vec_mod

    def mod_randPM(self, vec_time, vec_inf):
        # поток бит с произвольной амплитудой
        len_time = vec_time.shape[0]
        vec_mod = np.cos(np.dot(2 * np.pi * self.msg_carr, vec_time) + np.pi * (vec_inf - 1) + np.pi / 4)
        last_seq, new_seq, new_amp = 0, 0, 1
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            new_seq = np.int(np.floor(i / self.learn_size) + 1)
            # срабатывание переключателя модуляции
            if new_seq != last_seq:
                new_amp = np.random.uniform(1, 100)
            vec_mod[0][i] = vec_mod[0][i] * new_amp
            last_seq = new_seq
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

    def check_amp(self, len_amp, req_amp):
        # проверка размерности амплитуд
        if len_amp != req_amp:
            print("Ошибка, размерность амплитуд не равна " + str(req_amp))
            exit()

    def get_code(self):
        return self.mod_code
