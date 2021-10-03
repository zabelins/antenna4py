import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist

if __name__ == "__main__":
    print("Вы запустили модуль обучения НС (L3)")


class Network:
    """Класс модуль обучения НС"""

    def __init__(self, id):
        self.id = id
        # вектора обучающей выборки
        self.x_train = []
        self.y_train = []
        # вектора тестовой выборки
        self.x_test = []
        self.y_test = []
        # имя сохранения НС
        self.name_net = 'NN_1'

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры модуля обучения НС (L3):")
        print("\t-")

    def calc_out(self, out_sampling):
        # распаковка исходных данных
        vec_inamp, vec_inphi = out_sampling[0], out_sampling[1]
        vec_outamp, vec_outphi = out_sampling[2], out_sampling[3]
        matrix_inamp, matrix_inphi = out_sampling[4], out_sampling[5]
        self.calc_xy(vec_inamp, vec_inphi, vec_outamp, vec_outphi)
        self.start_train()

    def print_out(self):
        pass

    def start_train(self):
        # эксперименты с НС
        print("Тестовое обучение НС")
        # отключение предупреждений
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        # загрузка данных
        x_train, y_train = self.x_train, self.y_train
        x_test, y_test = self.x_test, self.y_test
        print("x_train", x_train.shape)
        print("y_train", y_train.shape)
        # создаём модель НС
        net_model = keras.Sequential()
        # создаём слои
        net_model.add(Dense(units=20, input_shape=(20,), activation='sigmoid'))
        net_model.add(Dense(26, activation='sigmoid'))
        net_model.add(Dense(20, activation='linear'))
        # компиляция НС с оптимизацией Adam
        net_model.compile(optimizer='adam',
                          loss='mean_squared_error',
                          metrics=['accuracy'])
        # вывод информации о НС
        print(net_model.summary())
        # запуск процесса обучения
        net_model.fit(x_train, y_train, batch_size=2, epochs=300, validation_split=0.2)
        # проверка на тестовой выборке
        print("Проверка обученной НС")
        net_model.evaluate(x_test, y_test)
        # сохранение НС
        print("Сохранение НС")
        net_model.save(self.name_net)
        # загрузка НС
        print("Загрузка НС")
        net_loaded = keras.models.load_model(self.name_net)
        print("Проверка сохранённой НС")
        net_loaded.evaluate(x_test, y_test)
        # проверка 1 значения
        n = 1
        x = np.expand_dims(x_test[n], axis=0)
        res = net_loaded.predict(x)
        print(res)
        print(np.argmax(res))

    def calc_xy(self, vec_inamp, vec_inphi, vec_outamp, vec_outphi):
        # преобразование в сигналы для входа
        len_time, len_num = vec_inamp.shape[0], vec_inamp.shape[1]
        len_train, len_test = round(len_time * 0.8), round(len_time * 0.2)
        # инициализация векторов выборки
        self.x_train = np.zeros(shape=[len_train, len_num * 2])
        self.y_train = np.zeros(shape=[len_train, len_num * 2])
        self.x_test = np.zeros(shape=[len_test, len_num * 2])
        self.y_test = np.zeros(shape=[len_test, len_num * 2])
        # собираем единые вектора обучающей выборки
        for i in range(len_train):
            for j in range(len_num):
                self.x_train[i][j] = vec_inamp[i][j]
                self.y_train[i][j] = vec_outamp[i][j]
                self.x_train[i][j+len_num] = vec_inphi[i][j]
                self.y_train[i][j+len_num] = vec_outphi[i][j]
        # собираем единые вектора тестовой выборки
        for i in range(len_test):
            for j in range(len_num):
                self.x_test[i][j] = vec_inamp[i][j]
                self.y_test[i][j] = vec_outamp[i][j]
                self.x_test[i][j+len_num] = vec_inphi[i][j]
                self.y_test[i][j+len_num] = vec_outphi[i][j]

