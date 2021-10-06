import os
import numpy as np
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
        # номер критерия адаптации
        self.alg_crit = []
        # тип управления
        self.control_type = []
        # адрес сохранённой НС
        self.name_dir = 'NN_1'
        # промежуточные вектора
        self.vec_inamp = []
        self.vec_inphi = []
        self.x_in = []
        self.y_out = []
        self.vec_outamp = []
        self.vec_outphi = []
        self.vec_outweight = []


    def set(self, init):
        self.alg_crit = init[0]
        self.control_type = init[5]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.control_type)
        return res

    def print(self):
        print("Параметры модели НС алгоритма (L3):")
        print("\talg_crit = ", self.alg_crit)
        print("\tcontrol_type = ", self.control_type)

    def calc_out(self, vec_in):
        # вычисление с помощью НС
        if os.path.exists(self.name_dir):
            # отключение предупреждений
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            # загрузка НС
            print("Загрузка НС")
            net_loaded = keras.models.load_model(self.name_dir)
        else:
            print("Сохранённая НС не обнаружена")
            len_time, len_num = [vec_in.shape[0], vec_in.shape[2]]
            return np.ones(shape=[len_time, len_num], dtype=complex)
        # преобразование входных векторов во входы НС
        self.create_in(vec_in)
        # проверка значений
        len_time, len_num = self.x_in.shape[0], self.x_in.shape[1]
        self.y_out = np.zeros(shape=[len_time, len_num])
        for i in range(len_time):
            x = np.expand_dims(self.x_in[i], axis=0)
            self.y_out[i] = net_loaded.predict(x)
        print("y_out = ", self.y_out)
        # обратное преобразование в ВК ААР
        self.create_out()
        # возврат вектора ВК ААР
        return self.vec_outweight

    def create_in(self, vec_in):
        # преобразование входных векторов во входы НС
        # разбиение на амплитуды и фазы
        self.calc_ampphi(vec_in)
        # нормировка
        self.calc_norm()
        # сбор единых векторов
        self.calc_x()

    def create_out(self):
        # преобразование выходов НС в ВК ААР
        len_time, len_num = self.y_out.shape[0], self.y_out.shape[1]
        print(round(len_num/2))
        self.vec_outamp = np.zeros(shape=[len_time, round(len_num/2)])
        self.vec_outphi = np.zeros(shape=[len_time, round(len_num/2)])
        # разбиваем на вектора амплитуд и фаз
        for i in range(len_time):
            for j in range(round(len_num/2)):
                self.vec_outamp[i][j] = self.y_out[i][j]
                self.vec_outphi[i][j] = self.y_out[i][j+round(len_num/2)]
        # денормировка
        self.calc_denorm()
        # сборка комплексных векторов
        self.calc_complex()

    def get_vecin(self, vec_sig, vec_int, vec_nois):
        # суммарный входной вектор на ААР в заданный момент времени
        len_num = vec_sig.shape[1]
        vec_in = np.zeros(shape=[len_num], dtype=complex)
        vec_in = vec_in + np.sum(vec_sig, axis=0)
        vec_in = vec_in + np.sum(vec_int, axis=0)
        #vec_in = vec_in + np.sum(vec_nois, axis=0)
        return vec_in

    def calc_ampphi(self, vec):
        # разделение на амплитудную и фазовую составляющую
        # фазы - угол относительно оси Re
        self.vec_inamp = np.abs(vec)
        self.vec_inphi = np.angle(vec)

    def calc_norm(self):
        # нормировка входных значений
        self.vec_inamp = self.vec_inamp / 4
        self.vec_inphi = (self.vec_inphi + np.pi) / (2 * np.pi)

    def calc_x(self):
        # объединение векторов
        len_time, len_num = self.vec_inamp.shape[0], self.vec_inamp.shape[1]
        self.x_in = np.zeros(shape=[len_time, len_num * 2])
        # собираем единые вектора обучающей выборки
        for i in range(len_time):
            for j in range(len_num):
                self.x_in[i][j] = self.vec_inamp[i][j]
            for j in range(len_num):
                self.x_in[i][j + 10] = self.vec_inphi[i][j]

    def calc_denorm(self):
        # возврат реальных значений
        self.vec_outamp = self.vec_outamp * 4
        self.vec_outphi = self.vec_outphi * (2 * np.pi) - np.pi

    def calc_complex(self):
        # разделение на амплитудную и фазовую составляющую
        # фазы - угол относительно оси Re
        self.vec_outweight = self.vec_outamp * np.exp(1j * self.vec_outphi)

