import os
import numpy as np
import time
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist

if __name__ == "__main__":
    print("Вы запустили модуль модели НС алгоритма (L3)")

class Neuro_alg:
    """Класс моделирования НС алгоритмов"""

    def __init__(self, id):
        self.id = id
        # параметры работы с файлами
        self.dir_net = ''
        self.name_net = 'NN'
        # параметры нейронной сети
        self.net_type = []
        self.net_nodes = []
        # параметры обучения
        self.learn_type = []
        self.learn_epoch = []
        # промежуточные вектора
        self.x_amp = []
        self.x_sin = []
        self.x_cos = []
        self.x_test = []
        self.y_amp = []
        self.y_sin = []
        self.y_cos = []
        self.y_test = []
        self.vec_outweight = []

    def set(self, init0, init1):
        self.net_type = init0[0]
        self.net_nodes = init0[1]
        self.learn_type = init0[2]
        self.learn_epoch = init0[3]
        self.dir_net = init1[13]

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_nodes)
        res.append(self.learn_type)
        res.append(self.learn_epoch)
        res.append(self.dir_net)
        return res

    def print(self):
        print("Параметры модели НС алгоритма (L3):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_type = ", self.learn_type)
        print("\tlearn_epoch = ", self.learn_epoch)
        print("\tdir_net = ", self.dir_net)

    def calc_out(self, vec_in):
        # вычисление с помощью НС
        net_loaded = self.load_network()
        # преобразование входных векторов во входы НС
        self.create_in(vec_in)
        len_time = self.x_test.shape[0]
        # вычисление ВВК
        for i in range(len_time):
            x = np.expand_dims(self.x_test[i], axis=0)
            self.y_test[i] = net_loaded.predict(x)
        # обратное преобразование в ВК ААР
        self.create_out()
        # возврат вектора ВК ААР
        return self.vec_outweight

    def create_in(self, vec_in):
        # преобразование входных векторов во входы НС
        self.get_format(vec_in)
        self.get_norm()
        # объединение векторов
        len_time, len_num = self.x_amp.shape[0], self.x_amp.shape[1]
        self.x_test = np.zeros(shape=[len_time, len_num * 3])
        self.y_test = np.zeros(shape=[len_time, len_num * 3])
        # собираем единые вектора обучающей выборки
        for i in range(len_time):
            for j in range(len_num):
                self.x_test[i][j] = self.x_amp[i][j]
                self.x_test[i][j + len_num] = self.x_sin[i][j]
                self.x_test[i][j + 2 * len_num] = self.x_cos[i][j]
        # преобразование векторов для свёрточной НС
        if self.net_type == 2:
            self.x_test = np.reshape(self.x_test, (len_time, 3, 10, 1))

    def create_out(self):
        # преобразование выходов НС в ВК ААР
        len_time, len_num = self.y_test.shape[0], self.y_test.shape[1]
        self.y_amp = np.zeros(shape=[len_time, round(len_num/3)])
        self.y_sin = np.zeros(shape=[len_time, round(len_num/3)])
        self.y_cos = np.zeros(shape=[len_time, round(len_num/3)])
        # разбиваем на вектора амплитуд и фаз
        for i in range(len_time):
            for j in range(round(len_num/3)):
                self.y_amp[i][j] = self.y_test[i][j]
                self.y_sin[i][j] = self.y_test[i][j + round(len_num/3)]
                self.y_cos[i][j] = self.y_test[i][j + 2 * round(len_num/3)]
        # денормировка
        self.get_denorm()
        # сборка комплексных векторов
        self.get_complex()

    def get_vecin(self, vec_sig, vec_int, vec_nois):
        # суммарный входной вектор на ААР в заданный момент времени
        len_num = vec_sig.shape[1]
        vec_in = np.zeros(shape=[len_num], dtype=complex)
        vec_in = vec_in + np.sum(vec_sig, axis=0)
        vec_in = vec_in + np.sum(vec_int, axis=0)
        #vec_in = vec_in + np.sum(vec_nois, axis=0)
        return vec_in

    def get_format(self, vec):
        # разделение на амплитуды, фазовые синусы и косинусы
        self.x_amp = np.abs(vec)
        self.x_sin = np.sin(np.angle(vec))
        self.x_cos = np.cos(np.angle(vec))

    def get_norm(self):
        # нормировка входных значений
        self.x_amp = self.x_amp / 4
        self.x_sin = self.x_sin / 2 + 0.5
        self.x_cos = self.x_cos / 2 + 0.5

    def get_denorm(self):
        # возврат реальных значений
        self.y_amp = self.y_amp * 4
        self.y_sin = (self.y_sin - 0.5) * 2
        self.y_cos = (self.y_cos - 0.5) * 2

    def get_complex(self):
        # разделение на амплитудную и фазовую составляющую
        # фазы - угол относительно оси Re
        self.vec_outweight = abs(self.y_amp) * (self.y_cos + 1j * self.y_sin)
        #self.vec_outweight = self.y_amp * np.exp(1j * self.vec_outphi)

    def load_network(self):
        # начало фиксации времени
        start_time = time.time()
        name_file = self.get_namefile()
        if os.path.exists(self.dir_net + '/' + name_file):
            # отключение предупреждений
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            # загрузка НС
            print("Загрузка НС")
            net_loaded = keras.models.load_model(self.dir_net + '/' + name_file)
            print(net_loaded.summary())
        else:
            print("Сохранённая НС не обнаружена")
            quit()
        # конец фиксации времени
        print("\ntime_load = ", time.time() - start_time)
        return net_loaded

    def get_namefile(self):
        name_file = self.name_net + '_TYP' + str(int(self.net_type))
        return name_file

