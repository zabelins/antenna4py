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
        self.learn_batch = []
        self.learn_epoch = []
        # промежуточные вектора
        self.x_predict = []
        self.y_predict = []
        self.x_real = []
        self.x_imag = []
        self.y_real = []
        self.y_imag = []
        self.vec_outweight = []

    def set(self, init0, init1):
        self.net_type = init0[0]
        self.net_nodes = init0[1]
        self.learn_batch = init0[2]
        self.learn_epoch = init0[3]
        self.dir_net = init1[13]

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_nodes)
        res.append(self.learn_batch)
        res.append(self.learn_epoch)
        res.append(self.dir_net)
        return res

    def print(self):
        print("Параметры модели НС алгоритма (L3):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_batch = ", self.learn_batch)
        print("\tlearn_epoch = ", self.learn_epoch)
        print("\tdir_net = ", self.dir_net)

    def calc_out(self, vec_in):
        # вычисление с помощью НС
        net_loaded = self.load_network()
        # преобразование входных векторов во входы НС
        self.create_in(vec_in)
        len_time = self.x_predict.shape[0]
        # вычисление ВВК
        for sample in range(len_time):
            x = np.expand_dims(self.x_predict[sample], axis=0)
            self.y_predict[sample] = net_loaded.predict(x)
        # обратное преобразование в ВК ААР
        self.create_out()
        # возврат вектора ВК ААР
        return self.vec_outweight

    def create_in(self, vec_in):
        # преобразование входных векторов во входы НС
        self.get_format(vec_in)
        self.get_norm()
        # объединение векторов
        len_time, len_num = self.x_real.shape[0], self.x_real.shape[1]
        self.x_predict = np.zeros(shape=[len_time, len_num * 2])
        self.y_predict = np.zeros(shape=[len_time, len_num * 2])
        # собираем единые вектора обучающей выборки
        for sample in range(len_time):
            for column in range(len_num):
                self.x_predict[sample][column] = self.x_real[sample][column]
                self.x_predict[sample][column + len_num] = self.x_imag[sample][column]
        # преобразование векторов для свёрточной НС
        if self.net_type == 2:
            self.x_predict = np.reshape(self.x_predict, (len_time, 2, 10, 1))

    def create_out(self):
        # преобразование выходов НС в ВК ААР
        len_time, len_num = self.y_predict.shape[0], self.y_predict.shape[1]
        self.y_real = np.zeros(shape=[len_time, round(len_num/2)])
        self.y_imag = np.zeros(shape=[len_time, round(len_num/2)])
        # разбиваем на вектора действительных и мнимых составляющих
        for sample in range(len_time):
            for column in range(round(len_num/2)):
                self.y_real[sample][column] = self.y_predict[sample][column]
                self.y_imag[sample][column] = self.y_predict[sample][column + round(len_num/2)]
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
        # разделение на действительный и мнимый вектор
        self.x_real = np.real(vec)
        self.x_imag = np.imag(vec)

    def get_norm(self):
        # нормировка входных значений (для конкретной обучающей выборки)
        x_real_mean, x_real_dev = 1.021384186653149, 0.7023038356201823
        x_imag_mean, x_imag_dev = -0.0003262891390589179, 0.6621864827314143
        self.x_real = (self.x_real - x_real_mean) / (x_real_dev * 2) + 0.5
        self.x_imag = (self.x_imag - x_imag_mean) / (x_imag_dev * 2) + 0.5

    def get_denorm(self):
        # возврат реальных значений (для конкретной обучающей выборки)
        y_real_mean, y_real_dev = 0.9062356566326484, 1.0097079374005649
        y_imag_mean, y_imag_dev = -5.280159566427528e-20, 0.7526434005875411
        self.y_real = (self.y_real - 0.5) * (y_real_dev * 2) + y_real_mean
        self.y_imag = (self.y_imag - 0.5) * (y_imag_dev * 2) + y_imag_mean

    def get_complex(self):
        # собираем комплексный вектор ВК
        self.vec_outweight = self.y_real + 1j * self.y_imag

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

