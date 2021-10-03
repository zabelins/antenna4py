import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense

if __name__ == "__main__":
    print("Вы запустили модуль обучения НС (L3)")


class Network:
    """Класс модуль обучения НС"""

    def __init__(self, id):
        self.id = id

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
        #vec_inamp, vec_inphi = out_sampling[0], out_sampling[1]
        #vec_outamp, vec_outphi = out_sampling[2], out_sampling[3]
        #matrix_inamp, matrix_inphi = out_sampling[4], out_sampling[5]
        #print("pp vec_inamp.shape", vec_inamp.shape)
        print("Тестовое обучение НС")
        # отключение предупреждений
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        # эксперименты с НС
        vec_in = np.array([-40, -10, 0, 8, 15, 22, 38])
        vec_out = np.array([-40, 14, 32, 46, 59, 72, 100])
        # модель многослойной НС
        net_model = keras.Sequential()
        # создаём слой
        # units - кол-во нейронов, input - кол-во входов
        net_model.add(Dense(units=1, input_shape=(1,), activation='linear'))
        # метод обучения
        # adam - градиентный спуск, 0.1 - шаг сходимости
        net_model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(0.1))
        # запуск обучения
        log = net_model.fit(vec_in, vec_out, epochs=500, verbose=0)
        print("Обучение завершено")
        # вывод информации
        plt.plot(log.history['loss'])
        plt.grid(True)
        plt.show()
        # проверка работы НС
        vec_test = [100]
        print(net_model.predict(vec_test))
        # проверка весов НС
        print(net_model.get_weights())


    def print_out(self):
        pass
