import math
import pack_calc.calc_list as cl
import numpy as np
import scipy.signal as sg

if __name__ == "__main__":
    print("Вы запустили модуль генератора углов (L3)")

class Gendeg:
    """Класс моделирования генератора углов"""

    def __init__(self):
        # параметры решётки
        self.arr_frq = 0
        # параметры сигналов
        self.sig_deg = 0
        # параметры помех
        self.int_deg = 0
        # параметры выборки
        self.learn_size = 0

    def set(self, init0, init1):
        self.arr_frq = init1[0]
        self.sig_deg = np.array(init0[0])
        self.int_deg = np.array(init0[6])
        self.learn_size = init0[16]

    def get(self):
        res = []
        res.append(self.arr_frq)
        res.append(self.sig_deg)
        res.append(self.int_deg)
        res.append(self.learn_size)
        return res

    def print(self):
        print("Параметры генератора углов (L3):")
        print("\tarr_frq = ", self.arr_frq)
        print("\tsig_deg = ", self.sig_deg)
        print("\tint_deg = ", self.int_deg)
        print("\tlearn_size = ", self.learn_size)

    def get_vec(self, vec_time, id_deg, is_int):
        # вычисление вектора изменения углов
        deg, vec_mod = [], []
        # выбор режима
        if id_deg == 0:
            # статический режим - исходный угол
            deg = self.get_par(is_int)
            vec_mod = np.ones(shape=[deg.shape[0], vec_time.shape[0]])
        elif id_deg == 1:
            # время - линейное изменение угла
            deg = np.array([90])
            vec_mod = self.deg_line(deg.shape[0], vec_time.shape[0])
        elif id_deg == 2:
            # время - выборка случайной одиночной помехи
            deg = np.array([90])
            vec_mod = self.deg_rand(deg.shape[0], vec_time.shape[0])
        elif id_deg == 3:
            # время - выборка случайной мерцающей помехи
            deg = np.array([75, 75])
            vec_mod = self.deg_2rand(deg.shape[0], vec_time.shape[0])
        elif id_deg == 4:
            # время - выборка шумовой помехи с накоплением
            deg = np.array([75])
            vec_mod = self.deg_noisegen(vec_time.shape[0])
        elif id_deg == 5:
            # время - выборка импульсной помехи с накоплением
            deg = np.array([75])
            vec_mod = self.deg_pulsegen(vec_time.shape[0])
        elif id_deg == 6:
            # время - выборка мерцающей помехи с накоплением
            deg = np.array([75, 75])
            vec_mod = self.deg_blinkgen(deg.shape[0], vec_time.shape[0])
        # вектора после модуляции
        vec_deg = cl.ones_modul(vec_mod, deg)
        return vec_deg

    def deg_line(self, len_deg, len_time):
        # линейная зависимость от -1 до 1
        self.check_deg(len_deg, 1)
        vec_mod = np.zeros(shape=[len_deg, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_deg):
                vec_mod[j][i] = (2 * i / (len_time-1)) - 1
        return vec_mod

    def deg_rand(self, len_deg, len_time):
        # случайные значения с равномерным распределением от -1 до 1
        self.check_deg(len_deg, 1)
        vec_mod = np.zeros(shape=[len_deg, len_time])
        # цикл по времени
        for i in range(len_time):
            # цикл по сигналам
            for j in range(len_deg):
                vec_mod[j][i] = np.random.uniform(-1, 1)
        return vec_mod

    def deg_2rand(self, len_deg, len_time):
        # случайные значения с равномерным распределением от -1 до 1
        self.check_deg(len_deg, 2)
        vec_mod = np.zeros(shape=[len_deg, len_time])
        diff_deg = np.zeros(shape=[len_time])
        diff_deg_var = 0
        # цикл по времени
        for i in range(len_time):
            # нормальное распределение для разности углов, среднее = ок. 25 град., СКО = ок. 9 град.
            flag = 0
            while flag == 0:
                diff_deg_var = abs(np.random.normal(loc=(2.0/7), scale=(2.0/20)))
                # проверка на допустимое значение [0,180] град
                if diff_deg_var < 2.0:
                    flag = 1
            # равномерное распределение для 1-й из 2-х помех
            vec_mod[0][i] = np.random.uniform(-1, 1-diff_deg_var)
            vec_mod[1][i] = vec_mod[0][i] + diff_deg_var
            diff_deg[i] = diff_deg_var
        print('diff_deg.mean = ', diff_deg.mean() * 90)
        return vec_mod

    def deg_noisegen(self, len_time):
        # случайные значения с накоплением и линейным сдвигом
        vec_mod = np.zeros(shape=[1, len_time])
        last_seq, new_seq, new_deg, new_sft = 0, 0, 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            new_seq = np.int(np.floor(i / self.learn_size) + 1)
            # условие смены случайного угла и смещения
            if new_seq != last_seq:
                # угол и смещение с равномерным распределением от -1 до 1
                new_deg = np.random.uniform(-1, 1)
                new_sft = np.random.uniform(-1, 1)
            # линейное смещение угла до 10 град.
            new_deg = new_deg + new_sft * 1/90
            # присвоение значений
            vec_mod[0][i] = new_deg
            last_seq = new_seq
        return vec_mod

    def deg_pulsegen(self, len_time):
        # случайные значения с накоплением
        vec_mod = np.zeros(shape=[1, len_time])
        last_seq, new_seq, new_deg = 0, 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            new_seq = np.int(np.floor(i / self.learn_size) + 1)
            # условие смены случайного угла
            if new_seq != last_seq:
                # угол с равномерным распределением от -1 до 1
                new_deg = np.random.uniform(-1, 1)
            # присвоение значений
            vec_mod[0][i] = new_deg
            last_seq = new_seq
        return vec_mod

    def deg_blinkgen(self, len_deg, len_time):
        # случайные значения с равномерным распределением от -1 до 1
        self.check_deg(len_deg, 2)
        vec_mod = np.zeros(shape=[len_deg, len_time])
        diff_deg = np.zeros(shape=[len_time])
        last_seq, new_seq = 0, 0
        new_deg1, new_deg2, diff_deg_var = 0, 0, 0
        # цикл по времени
        for i in range(len_time):
            # проверка пакета
            new_seq = np.int(np.floor(i/self.learn_size) + 1)
            # срабатывание переключателя модуляции
            if new_seq != last_seq:
                # нормальное распределение для разности углов, среднее = ок. 25 град., СКО = ок. 9 град.
                flag = 0
                while flag == 0:
                    diff_deg_var = abs(np.random.normal(loc=(2.0/7), scale=(2.0/20)))
                    # проверка на допустимое значение [0,180] град
                    if diff_deg_var < 2.0:
                        flag = 1
                # равномерное распределение для 1-й из 2-х помех
                new_deg1 = np.random.uniform(-1, 1-diff_deg_var)
                new_deg2 = new_deg1 + diff_deg_var
            # присвоение значений
            vec_mod[0][i] = new_deg1
            vec_mod[1][i] = new_deg2
            diff_deg[i] = diff_deg_var
            last_seq = new_seq
        print('diff_deg.mean = ', diff_deg.mean() * 90)
        return vec_mod

    def get_par(self, is_int):
        # сигнал или помеха
        deg = []
        if is_int == 0:
            # сигнал
            deg = self.sig_deg
        elif is_int == 1:
            # помеха
            deg = self.int_deg
        return deg

    def check_deg(self, len_deg, req_deg):
        # проверка размерности углов
        if len_deg != req_deg:
            print("Ошибка, размерность углов не равна " + str(req_deg))
            exit()
