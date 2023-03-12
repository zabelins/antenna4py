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
            vec_mod = self.calc_bandrand(bnd.shape[0], vec_time.shape[0])
        elif id_bnd == 4:
            # время - выборка случайных частотных полос для 2 помех
            bnd = np.array([self.arr_frq * 0.1, self.arr_frq * 0.1])
            vec_mod = self.calc_band2rand(bnd.shape[0], vec_time.shape[0], 0)
        elif id_bnd == 5:
            # время - выборка случайных частотных полос для 2 помех с накоплением
            bnd = np.array([self.arr_frq * 0.1, self.arr_frq * 0.1])
            vec_mod = self.calc_band2rand(bnd.shape[0], vec_time.shape[0], 1)
        elif id_bnd == 6:
            # параметр - переменная частотная полоса (от 0 до 10%)
            bnd = self.arr_frq * var_par
            vec_mod = np.ones(shape=[bnd.shape[0], vec_time.shape[0]])
        vec_bnd = cl.ones_modul(vec_mod, bnd)
        return vec_bnd

    def calc_bandrand(self, len_bnd, len_time):
        # рандомные значения частотных полос одиночной помехи
        # равномерное распределение от 0 до 1
        vec_mod = np.ones(shape=[len_bnd, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_bnd):
                vec_mod[j][i] = np.random.uniform(0, 1)
        return vec_mod

    def calc_band2rand(self, len_bnd, len_time, is_switch):
        # рандомные значения частотных полос мерцающей помехи
        # равномерное распределение от 0 до 1
        if len_bnd != 2:
            print("Ошибка размерности, необходимы 2 амплитудных значения")
            exit()
        if is_switch == 0:
            self.learn_size = 1
        vec_mod = np.ones(shape=[len_bnd, len_time])
        last_batch, now_batch = -1, -1
        now_bnd1, now_bnd2 = 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            now_batch = np.int(np.floor(i/self.learn_size))
            # срабатывание переключателя модуляции
            if now_batch != last_batch:
                now_bnd1 = np.random.uniform(0, 1)
                now_bnd2 = now_bnd1
            # формирование значений за текущий такт
            vec_mod[0][i] = now_bnd1
            vec_mod[1][i] = now_bnd2
            last_batch = now_batch
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

