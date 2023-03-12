import math
import numpy as np
import time
import cmath

if __name__ == "__main__":
    print("Вы запустили модуль модели традиционного алгоритма (L3)")

class Trad_alg:
    """Класс моделирования традиционный алгоритмов"""

    def __init__(self):
        # номер критерия адаптации
        self.alg_crit = 0
        # тип управления
        self.ctl_type = 0

    def set(self, init):
        self.alg_crit = init[0]
        self.ctl_type = init[5]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.ctl_type)
        return res

    def print(self):
        print("Параметры модели традиционного алгоритма (L3):")
        print("\talg_crit = ", self.alg_crit)
        print("\tctl_type = ", self.ctl_type)

    def get_weights(self, vec_sig, matrix_sig, matrix_int, matrix_nois):
        # алгоритм прямого обращения матрицы
        len_time, len_num = [vec_sig.shape[1], vec_sig.shape[2]]
        vec_outweight = np.zeros(shape=[len_time, len_num], dtype=complex)
        if self.alg_crit == 0:
            # критерий максимума ОСШП
            for i in range(len_time):
                matrix_in = matrix_int[i] + matrix_nois[i]
                vec_ref = vec_sig[0][i] / np.real(vec_sig[0][i][0])
                vec_cj = np.conj(vec_ref)
                vec_outweight[i] = np.dot(np.dot(np.linalg.inv(matrix_in), matrix_nois[i]), vec_cj)
        if self.alg_crit == 1:
            # критерий минимума помех и шумов
            for i in range(len_time):
                matrix_in = matrix_int[i] + matrix_nois[i]
                vec_ref = vec_sig[0][i] / np.real(vec_sig[0][i][0])
                vec_cj = np.conj(vec_ref)
                const = np.dot(vec_ref.T, vec_ref) / self.get_power(vec_ref, np.linalg.inv(matrix_in))
                vec_outweight[i] = const * np.dot(np.linalg.inv(matrix_in), vec_cj)
        return vec_outweight

    def get_power(self, vec_in, matrix_in):
        # вычисление мощности для 1 момента времени
        vec_cj = np.conj(vec_in)
        res = np.dot(np.dot(vec_cj, matrix_in), vec_in)
        return res