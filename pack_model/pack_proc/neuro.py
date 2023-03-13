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

    def __init__(self):
        # параметры работы с файлами
        self.dir_net = ''
        self.name_net = 'NN'
        self.is_swith = 1
        # параметры выборки
        self.learn_size = 5
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
        # параметры нормировки
        self.x_real_mean = -6.936583902531577e-07
        self.x_real_dev = 5.895636508536925e-05
        self.x_imag_mean = 2.5648447580986522e-08
        self.x_imag_dev = 5.6396658544314275e-05
        self.y_real_mean = 0.9513155216941713
        self.y_real_dev = 1.1448185294741398
        self.y_imag_mean = -0.00036983829047969064
        self.y_imag_dev = 0.82881380379252

    def set(self, init0, init1, init2):
        self.learn_size = np.array(init0[16])
        self.net_type = init1[0]
        self.net_nodes = init1[1]
        self.learn_batch = init1[2]
        self.learn_epoch = init1[3]
        self.dir_net = init2[23]

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_nodes)
        res.append(self.learn_batch)
        res.append(self.learn_epoch)
        res.append(self.dir_net)
        res.append(self.learn_size)
        return res

    def print(self):
        print("Параметры модели НС алгоритма (L3):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_batch = ", self.learn_batch)
        print("\tlearn_epoch = ", self.learn_epoch)
        print("\tdir_net = ", self.dir_net)
        print("\tlearn_size = ", self.learn_size)

    def get_weights(self, vec_in):
        # вычисление с помощью НС
        net_loaded = self.load_network()
        # преобразование входных векторов во входы НС
        if self.is_swith == 0:
            self.create_in(vec_in)
        elif self.is_swith == 1:
            self.create_switchin(vec_in)
        len_array = self.x_predict.shape[0]
        # вычисление ВВК
        for sample in range(len_array):
            x = np.expand_dims(self.x_predict[sample], axis=0)
            self.y_predict[sample] = net_loaded.predict(x)
        # обратное преобразование в ВК ААР
        if self.is_swith == 0:
            self.create_out()
        elif self.is_swith == 1:
            len_time_real = vec_in.shape[0]
            self.create_switchout(len_time_real)
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

    def create_switchin(self, vec_in):
        # преобразование входных векторов во входы НС
        self.get_format(vec_in)
        self.get_norm()
        # объединение векторов
        len_time, len_num = self.x_real.shape[0], self.x_real.shape[1]
        len_batch = np.int(self.learn_size)
        len_array = len_time - (len_batch-1)
        print("len_array = ", len_array)
        self.x_predict = np.zeros(shape=[len_array, len_batch-1, len_num * 2])
        self.y_predict = np.zeros(shape=[len_array, len_num * 2])
        # собираем единые вектора обучающей выборки
        for batch in range(len_array):
            for column in range(len_num):
                for sample in range(len_batch - 1):
                    time_in = batch + sample
                    self.x_predict[batch][sample][column] = self.x_real[time_in][column]
                    self.x_predict[batch][sample][column + len_num] = self.x_imag[time_in][column]

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

    def create_switchout(self, len_time_real):
        # преобразование выходов НС в ВК ААР
        len_array, len_num = self.y_predict.shape[0], self.y_predict.shape[1]
        # преобразование во временную шкалу
        len_batch = np.int(self.learn_size)
        self.y_real = np.ones(shape=[len_time_real, round(len_num/2)])
        self.y_imag = np.zeros(shape=[len_time_real, round(len_num/2)])
        # разбиваем на вектора действительных и мнимых составляющих
        for batch in range(len_array):
            for column in range(round(len_num/2)):
                time_out = batch + (len_batch-1)
                if time_out < len_time_real:
                    self.y_real[time_out][column] = self.y_predict[batch][column]
                    self.y_imag[time_out][column] = self.y_predict[batch][column + round(len_num / 2)]
        # денормировка
        self.get_denorm()
        # коррекция первого пакета (единичные ВК)
        for sample in range(len_batch-1):
            for column in range(round(len_num / 2)):
                self.y_real[sample][column] = 1.0
                self.y_imag[sample][column] = 0.0
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
        self.x_real = (self.x_real - self.x_real_mean) / (self.x_real_dev * 2) + 0.5
        self.x_imag = (self.x_imag - self.x_imag_mean) / (self.x_imag_dev * 2) + 0.5

    def get_denorm(self):
        # возврат реальных значений (для конкретной обучающей выборки)
        self.y_real = (self.y_real - 0.5) * (self.y_real_dev * 2) + self.y_real_mean
        self.y_imag = (self.y_imag - 0.5) * (self.y_imag_dev * 2) + self.y_imag_mean

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

