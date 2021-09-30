import math

import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели фильтра Калмана (L3)")

class Kalman:
    """Класс моделирования фильтра Калмана"""

    def __init__(self, id):
        self.id = id
        # параметры фильтра Калмана
        self.kalman_type = []
        self.kalman_coef = []
        # фильтруемые параметры
        self.matrix_sig = []
        self.matrix_int = []
        self.matrix_nois = []

    def set(self, init):
        self.kalman_type = init[3]
        self.kalman_coef = init[4]

    def get(self):
        res = []
        res.append(self.kalman_type)
        res.append(self.kalman_coef)
        return res

    def print(self):
        print("Параметры модели фильтра Калмана (L3):")
        print("\tkalman_type = ", self.kalman_type)
        print("\tcoef_kalman = ", self.kalman_coef)

    def calc_matrix(self, matrix_sig, matrix_int, matrix_nois):
        # фильтр Калмана для матриц
        self.matrix_sig, self.matrix_int, self.matrix_nois = matrix_sig, matrix_int, matrix_nois
        # рабочий режим фильтра Калмана
        if self.kalman_type == 1:
            x_sig = self.get_matrix(self.matrix_sig)
            x_int = self.get_matrix(self.matrix_int)
            x_nois = self.get_matrix(self.matrix_nois)
            self.matrix_sig, self.matrix_int, self.matrix_nois = x_sig, x_int, x_nois
        return [self.matrix_sig, self.matrix_int, self.matrix_nois]

    def get_matrix(self, matrix):
        # рабочий режим фильтра Калмана
        sigmaEta, sigmaPsi, a = 1, 0, 0
        # инициализация параметров
        len_time, len_matrix = matrix.shape[0], matrix.shape[1]
        x_opt = np.zeros(shape=[len_time, len_matrix, len_matrix], dtype=complex)
        e_opt = np.ones(shape=[len_time, len_matrix, len_matrix])
        Kk = np.ones(shape=[len_time, len_matrix, len_matrix])
        # цикл по времени
        for i in range(len_time):
            if i == 0:
                x_opt[i] = matrix[i]
                e_opt[i] = e_opt[i] * sigmaEta
            else:
                squareEta = sigmaEta ** 2
                squarePsi = sigmaPsi ** 2
                buf = squareEta * (e_opt[i - 1] ** 2 + squarePsi) / (squareEta + e_opt[i - 1] ** 2 + squarePsi)
                e_opt[i] = np.sqrt(buf)
                Kk[i] = (e_opt[i] ** 2) / squareEta
                x_opt[i] = Kk[i] * self.matrix_int[i] + (1 - Kk[i]) * (x_opt[i - 1] + a * (i - 1))
        return x_opt