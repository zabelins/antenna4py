import numpy as np
import pack_calc.calc_list as cl
import os

if __name__ == "__main__":
    print("Вы запустили модуль формирования обучающей выборки (L2)")

class Sampling:
    """Класс формирования обучающей выборки"""

    def __init__(self, id):
        self.id = id
        # обучающая выборка
        self.x_amp = []
        self.x_sin = []
        self.x_cos = []
        self.y_amp = []
        self.y_sin = []
        self.y_cos = []
        # вектора обучающей выборки
        self.x_train = []
        self.y_train = []
        # вектора тестовой выборки
        self.x_test = []
        self.y_test = []

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры формирования обучающей выборки (L3):")
        print("\t-")

    def calc_out(self, out_data):
        # цикл склейки обучающей выборки по файлам
        for i in range(len(out_data)):
            if i == 0:
                vec_in = out_data[i][9]
                vec_out = out_data[i][10]
            else:
                if vec_in.shape[1] == (out_data[i][9]).shape[1]:
                    vec_in = np.concatenate((vec_in, out_data[i][9]), axis=0)
                    vec_out = np.concatenate((vec_out, out_data[i][10]), axis=0)
                else:
                    print("Ошибка размерности обучающей выборки")
        # разделение на амплитуды, синусы и косинусы
        self.x_amp, self.x_sin, self.x_cos = self.get_format(vec_in)
        self.y_amp, self.y_sin, self.y_cos = self.get_format(vec_out)
        # нормировка векторов
        self.get_norm()
        # формирование обучающей и тестовой выборок
        self.get_array()

    def get_out(self):
        out_samples = []
        out_samples.append(self.x_train)
        out_samples.append(self.y_train)
        out_samples.append(self.x_test)
        out_samples.append(self.y_test)
        return out_samples

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res = cl.is_ndarray([self.x_train, self.y_train, self.x_test, self.y_test])
        # вывод размерностей векторов
        if bool_res:
            print("Размерности векторов обучающей выборки:")
            print("\tx_train.shape = ", self.x_train.shape)
            print("\ty_train.shape = ", self.y_train.shape)
            print("\tx_test.shape = ", self.x_test.shape)
            print("\ty_test.shape = ", self.y_test.shape)
        else:
            print("Ошибка проверки типа векторов обучающей выборки")

    def get_format(self, vec):
        # разделение на амплитуды, фазовые синусы и косинусы
        vec_amp = np.abs(vec)
        vec_sin = np.sin(np.angle(vec))
        vec_cos = np.cos(np.angle(vec))
        return [vec_amp, vec_sin, vec_cos]

    def get_norm(self):
        # нормировка выборки
        # запас по амплитуде = 10%
        self.x_amp = self.x_amp / 4
        self.y_amp = self.y_amp / 4
        self.x_sin = self.x_sin / 2 + 0.5
        self.y_sin = self.y_sin / 2 + 0.5
        self.x_cos = self.x_cos / 2 + 0.5
        self.y_cos = self.y_cos / 2 + 0.5
        #self.vec_inphi = (self.vec_inphi + np.pi) / (2 * np.pi)
        #self.vec_outphi = (self.vec_outphi + np.pi) / (2 * np.pi)

    def get_array(self):
        # преобразование в сигналы для входа
        len_time, len_num = self.x_amp.shape[0], self.x_amp.shape[1]
        len_train, len_test = round(len_time * 0.8), round(len_time * 0.2)
        # инициализация векторов выборки
        self.x_train = np.zeros(shape=[len_train, len_num * 3])
        self.y_train = np.zeros(shape=[len_train, len_num * 3])
        self.x_test = np.zeros(shape=[len_test, len_num * 3])
        self.y_test = np.zeros(shape=[len_test, len_num * 3])
        # собираем единые вектора обучающей выборки
        for i in range(len_train):
            for j in range(len_num):
                self.x_train[i][j] = self.x_amp[i][j]
                self.y_train[i][j] = self.y_amp[i][j]
                self.x_train[i][j + len_num] = self.x_sin[i][j]
                self.y_train[i][j + len_num] = self.y_sin[i][j]
                self.x_train[i][j + 2 * len_num] = self.x_cos[i][j]
                self.y_train[i][j + 2 * len_num] = self.y_cos[i][j]
        # собираем единые вектора тестовой выборки
        for i in range(len_test):
            for j in range(len_num):
                self.x_test[i][j] = self.x_amp[len_train + i][j]
                self.y_test[i][j] = self.y_amp[len_train + i][j]
                self.x_test[i][j + len_num] = self.x_sin[len_train + i][j]
                self.y_test[i][j + len_num] = self.y_sin[len_train + i][j]
                self.x_test[i][j + 2 * len_num] = self.x_cos[len_train + i][j]
                self.y_test[i][j + 2 * len_num] = self.y_cos[len_train + i][j]