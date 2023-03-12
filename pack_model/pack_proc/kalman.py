import math

import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели фильтра Калмана (L3)")

class Kalman:
    """Класс моделирования фильтра Калмана"""

    def __init__(self):
        # параметры фильтра Калмана
        self.klm_type = 0
        self.klm_sigma = 0
        # фильтруемые параметры
        self.matrix_sig = np.array([])
        self.matrix_int = np.array([])
        self.matrix_nois = np.array([])

    def set(self, init):
        self.klm_type = init[3]
        self.klm_sigma = init[4]

    def get(self):
        res = []
        res.append(self.klm_type)
        res.append(self.klm_sigma)
        return res

    def print(self):
        print("Параметры модели фильтра Калмана (L3):")
        print("\tklm_type = ", self.klm_type)
        print("\tklm_sigma = ", self.klm_sigma)

    def get_matrix(self, matrix_sig, matrix_int, matrix_nois):
        # фильтр Калмана для матриц
        self.matrix_sig, self.matrix_int, self.matrix_nois = matrix_sig, matrix_int, matrix_nois
        # рабочий режим фильтра Калмана
        if self.klm_type == 1:
            x_sig = self.matrix_sig
            x_int = self.filtering(self.matrix_int)
            x_nois = self.matrix_nois
            self.matrix_sig, self.matrix_int, self.matrix_nois = x_sig, x_int, x_nois
        return [self.matrix_sig, self.matrix_int, self.matrix_nois]

    def filtering(self, matrix):
        # рабочий режим фильтра Калмана
        dispers_model, dispers_measure, ex_control = 1, 0, 0
        # инициализация параметров
        len_time, len_matrix = matrix.shape[0], matrix.shape[1]
        x_opt = np.zeros(shape=[len_time, len_matrix, len_matrix], dtype=complex)
        e_opt = np.ones(shape=[len_time, len_matrix, len_matrix])
        kalman_coef = np.ones(shape=[len_time, len_matrix, len_matrix])
        # цикл по времени
        for i in range(len_time):
            if i == 0:
                x_opt[i] = matrix[i]
                e_opt[i] = e_opt[i] * dispers_model
            else:
                squareEta = dispers_model ** 2
                squarePsi = dispers_measure ** 2
                e_opt[i] = np.sqrt(squareEta * (e_opt[i-1] ** 2 + squarePsi) / (squareEta + e_opt[i-1] ** 2 + squarePsi))
                kalman_coef[i] = (e_opt[i] ** 2) / squareEta
                x_opt[i] = kalman_coef[i] * self.matrix_int[i] + (1 - kalman_coef[i]) * (x_opt[i-1] + ex_control * (i-1))
        return x_opt