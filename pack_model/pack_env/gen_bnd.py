import math
import pack_calc.calc_list as cl
import numpy as np
import scipy.signal as sg

if __name__ == "__main__":
    print("Вы запустили модуль генератора полосы (L3)")

class Genbnd:
    """Класс моделирования генератора частотной полосы"""

    def __init__(self):
        # параметры решётки
        self.arr_frq = 0
        # параметры сигналов
        self.sig_bnd = 0
        # параметры помех
        self.int_bnd = 0
        # параметры выборки
        self.learn_size = 0

    def set(self, init0, init1):
        self.arr_frq = init1[0]
        self.sig_bnd = np.array(init0[2])
        self.int_bnd = np.array(init0[8])
        self.learn_size = init0[16]

    def get(self):
        res = []
        res.append(self.arr_frq)
        res.append(self.sig_bnd)
        res.append(self.int_bnd)
        res.append(self.learn_size)
        return res

    def print(self):
        print("Параметры генератора полос (L3):")
        print("\tarr_frq = ", self.arr_frq)
        print("\tsig_bnd = ", self.sig_bnd)
        print("\tint_bnd = ", self.int_bnd)
        print("\tlearn_size = ", self.learn_size)

    def get_vec(self, vec_time, id_bnd, var_par, is_int):
        # вычисление вектора изменения частотных полос
        bnd, vec_mod = [], []
        # выбор режима
        if id_bnd == 0:
            # статический режим - исходная частотная полоса
            bnd = self.get_par(is_int)
            vec_mod = np.ones(shape=[bnd.shape[0], vec_time.shape[0]])
        elif id_bnd == 1:
            # статический режим - частотная полоса 0%
            bnd = np.array([0])
            vec_mod = np.ones(shape=[bnd.shape[0], vec_time.shape[0]])
        elif id_bnd == 2:
            # статический режим - частотная полоса 10%
            bnd = np.array([self.arr_frq * 0.1])
            vec_mod = np.ones(shape=[bnd.shape[0], vec_time.shape[0]])
        elif id_bnd == 3:
            # время - выборка случайной частотной полосы для 1 помехи
            bnd = np.array([self.arr_frq * 0.1])
            vec_mod = self.bnd_rand(bnd.shape[0], vec_time.shape[0])
        elif id_bnd == 4:
            # время - выборка случайных частотных полос для 2 помех
            bnd = np.array([self.arr_frq * 0.1, self.arr_frq * 0.1])
            vec_mod = self.bnd_2rand(bnd.shape[0], vec_time.shape[0])
        elif id_bnd == 5:
            # время - выборка случайных частотных полос для 2 помех с накоплением
            bnd = np.array([self.arr_frq * 0.1, self.arr_frq * 0.1])
            vec_mod = self.bnd_2rand(bnd.shape[0], vec_time.shape[0])
        elif id_bnd == 6:
            # параметр - переменная частотная полоса (от 0 до 10%)
            bnd = self.arr_frq * var_par
            vec_mod = np.ones(shape=[bnd.shape[0], vec_time.shape[0]])
        vec_bnd = cl.ones_modul(vec_mod, bnd)
        return vec_bnd

    def bnd_rand(self, len_bnd, len_time):
        self.check_bnd(len_bnd, 1)
        # рандомные значения частотных полос одиночной помехи
        vec_mod = np.ones(shape=[len_bnd, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_bnd):
                # равномерное распределение от 0 до 1
                vec_mod[j][i] = np.random.uniform(0, 1)
        return vec_mod

    def bnd_2rand(self, len_bnd, len_time):
        # рандомные значения частотных полос мерцающей помехи
        self.check_bnd(len_bnd, 2)
        vec_mod = np.ones(shape=[len_bnd, len_time])
        # цикл по времени
        for i in range(len_time):
            # равномерное распределение от 0 до 1
            vec_mod[0][i] = np.random.uniform(0, 1)
            vec_mod[1][i] = vec_mod[0][i]
        return vec_mod

    def bnd_blinkgen(self, len_bnd, len_time):
        # рандомные значения частотных полос мерцающей помехи
        self.check_bnd(len_bnd, 2)
        vec_mod = np.ones(shape=[len_bnd, len_time])
        last_seq, new_seq, new_bnd = 0, 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            new_seq = np.int(np.floor(i/self.learn_size) + 1)
            # срабатывание переключателя модуляции
            if new_seq != last_seq:
                # равномерное распределение от 0 до 1
                new_bnd = np.random.uniform(0, 1)
            # формирование значений за текущий такт
            vec_mod[0][i] = new_bnd
            vec_mod[1][i] = new_bnd
            last_seq = new_seq
        return vec_mod

    def get_par(self, is_int):
        # сигнал или помеха
        bnd = []
        if is_int == 0:
            # сигнал
            bnd = self.sig_bnd
        elif is_int == 1:
            # помеха
            bnd = self.int_bnd
        return bnd

    def check_bnd(self, len_bnd, req_bnd):
        # проверка размерности полос
        if len_bnd != req_bnd:
            print("Ошибка, размерность полос не равна " + str(req_bnd))
            exit()
