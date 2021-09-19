import math
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели традиционного алгоритма (L3)")

class Trad_alg:
    """Класс моделирования традиционный алгоритмов"""

    def __init__(self, id):
        self.id = id
        self.adapt_type = []
        self.alg_crit = []

    def set(self, init):
        self.adapt_type = init[1]
        self.alg_crit = init[2]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.adapt_type)
        res.append(self.alg_crit)
        return res

    def print(self):
        print(" --- Параметры модели традиционного алгоритма (L3) --- ")
        print("id = ", self.id)
        print("adapt_type = ", self.adapt_type)
        print("alg_crit = ", self.alg_crit)

    def print_short(self):
        print(" --- Параметры модели традиционного алгоритма (L3) --- ")
        print("trad_alg = ", self.get())

    def get_invers(self, vec_sig, matrix_sig, matrix_int, matrix_nois):
        # алгоритм прямого обращения матрицы
        len_time, len_num = [vec_sig.shape[0], vec_sig.shape[2]]
        res = np.zeros(shape=[len_time, len_num], dtype=complex)
        if (self.alg_crit == 1):
            # критерий адаптации без ограничений
            for i in range(len_time):
                mu = abs(matrix_nois[i][0][0])
                matrix_M = np.linalg.inv(matrix_int[i] + matrix_nois[i])
                vector_in = np.array(vec_sig[i][0])
                vector_cj = np.conj(vector_in)
                res[i] = mu * matrix_M.dot(vector_cj)
        if (self.alg_crit == 2):
            # критерий с ограничениями
            for i in range(len_time):
                mu = abs(len_num * matrix_sig[i][0][0])
                matrix_M = np.linalg.inv(matrix_int[i] + matrix_nois[i])
                vector_in = np.array(vec_sig[i][0])
                vector_cj = np.conj(vector_in)
                matrix_buf1 = vector_cj.dot(matrix_M)
                matrix_buf2 = matrix_buf1.dot(vector_in)
                res[i] = mu * matrix_M.dot(vector_cj) / matrix_buf2
        return res