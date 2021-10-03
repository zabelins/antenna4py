import math
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели традиционного алгоритма (L3)")

class Trad_alg:
    """Класс моделирования традиционный алгоритмов"""

    def __init__(self, id):
        self.id = id
        # номер критерия адаптации
        self.alg_crit = []
        # тип управления
        self.control_type = []

    def set(self, init):
        self.alg_crit = init[0]
        self.control_type = init[5]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.control_type)
        return res

    def print(self):
        print("Параметры модели традиционного алгоритма (L3):")
        print("\talg_crit = ", self.alg_crit)
        print("\tcontrol_type = ", self.control_type)

    def calc_out(self, vec_sig, matrix_sig, matrix_int, matrix_nois):
        # алгоритм прямого обращения матрицы
        len_time, len_num = [vec_sig.shape[0], vec_sig.shape[2]]
        res = np.zeros(shape=[len_time, len_num], dtype=complex)
        if (self.alg_crit == 1):
            # критерий адаптации без ограничений
            for i in range(len_time):
                mu = abs(matrix_nois[i][0][0])
                matrix_in = np.linalg.inv(matrix_int[i] + matrix_nois[i])
                vector_in = np.array(vec_sig[i][0])
                vector_cj = np.conj(vector_in)
                res[i] = mu * matrix_in.dot(vector_cj)
        if (self.alg_crit == 2):
            # критерий с ограничениями
            for i in range(len_time):
                mu = abs(len_num * matrix_sig[i][0][0])
                matrix_in = np.linalg.inv(matrix_int[i] + matrix_nois[i])
                vector_in = np.array(vec_sig[i][0])
                vector_cj = np.conj(vector_in)
                buf = self.calc_power(vector_in, matrix_in)
                res[i] = mu * matrix_in.dot(vector_cj) / buf
        return res

    def calc_power(self, vector_in, matrix):
        # вычисление мощности для 1 момента времени
        vector_cj = np.conj(vector_in)
        matrix_in = matrix
        matrix_buf = vector_cj.dot(matrix_in)
        res = matrix_buf.dot(vector_in)
        return res