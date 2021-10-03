import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль формирования обучающей выборки (L3)")

class Sampling:
    """Класс формирования обучающей выборки"""

    def __init__(self, id):
        self.id = id
        self.matrix_learn = []
        self.matrix_test = []
        # обучающая выборка
        self.vec_inamp = []
        self.vec_inphi = []
        self.vec_outamp = []
        self.vec_outphi = []
        self.matrix_inamp = []
        self.matrix_inphi = []

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры формирования обучающей выборки (L3):")
        print("\t-")

    def calc_out(self, out_data):
        # подготовка обучающей выборки
        self.get_learnarray(out_data)
        self.get_norm()
        # вывод информации
        self.print_out()

    def get_out(self):
        res = []
        res.append(self.vec_inamp)
        res.append(self.vec_inphi)
        res.append(self.vec_outamp)
        res.append(self.vec_outphi)
        res.append(self.matrix_inamp)
        res.append(self.matrix_inphi)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_inamp, self.vec_inphi, self.vec_outamp, self.vec_outphi])
        bool_res2 = cl.is_ndarray([self.matrix_inamp, self.matrix_inphi])
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True):
            print("Размерности векторов обучающей выборки:")
            print("\tvec_inamp.shape = ", self.vec_inamp.shape)
            print("\tvec_inphi.shape = ", self.vec_inphi.shape)
            print("\tvec_outamp.shape = ", self.vec_outamp.shape)
            print("\tvec_outphi.shape = ", self.vec_outphi.shape)
            print("\tmatrix_inamp.shape = ", self.matrix_inamp.shape)
            print("\tmatrix_inphi.shape = ", self.matrix_inphi.shape)
        else:
            print("Ошибка проверки типа векторов обучающей выборки")

    def get_learnarray(self, out_data):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = out_data[0], out_data[1], out_data[2]
        matrix_sig, matrix_int, matrix_nois = out_data[3], out_data[4], out_data[5]
        vec_inweight, vec_outweight = out_data[6], out_data[7]
        # инициализация векторов
        len_sumtime, len_arrayn = self.get_sumtime(vec_sig), vec_sig[0].shape[2]
        vec_in = np.zeros(shape=[len_sumtime, len_arrayn], dtype=complex)
        vec_out = np.zeros(shape=[len_sumtime, len_arrayn], dtype=complex)
        matrix_in = np.zeros(shape=[len_sumtime, len_arrayn, len_arrayn], dtype=complex)
        # формирование обучающей выборки
        len_data, id_buf = len(vec_sig), 0
        # запускаем цикл по файлам
        for i in range(len_data):
            len_time = vec_sig[i].shape[0]
            # запускаем цикл по времени
            for j in range(len_time):
                vec_in[id_buf] = self.get_vecin(vec_sig[i][j], vec_int[i][j], vec_nois[i][j])
                vec_out[id_buf] = vec_outweight[i][j]
                matrix_in[id_buf] = self.get_matrixin(matrix_sig[i][j], matrix_int[i][j], matrix_nois[i][j])
                id_buf = id_buf + 1
        # разделение на амплитуды и фазы
        self.vec_inamp, self.vec_inphi = self.get_ampphi(vec_in)
        self.vec_outamp, self.vec_outphi = self.get_ampphi(vec_out)
        self.matrix_inamp, self.matrix_inphi = self.get_ampphi(matrix_in)

    def get_sumtime(self, vec):
        # вычисление общего размера обучающей выборки
        len_data = len(vec)
        len_time = 0
        for i in range(len_data):
            len_time = len_time + vec[i].shape[0]
        return len_time

    def get_vecin(self, vec_sig, vec_int, vec_nois):
        # суммарный входной вектор на ААР в заданный момент времени
        len_N = vec_sig.shape[1]
        vec_in = np.zeros(shape=[len_N], dtype=complex)
        vec_in = vec_in + np.sum(vec_sig, axis=0)
        vec_in = vec_in + np.sum(vec_int, axis=0)
        #vec_in = vec_in + np.sum(vec_nois, axis=0)
        return vec_in

    def get_matrixin(self, matrix_sig, matrix_int, matrix_nois):
        # суммарная входная матрица на ААР в заданный момент времени
        len_N = matrix_sig.shape[1]
        matrix_in = np.zeros(shape=[len_N, len_N], dtype=complex)
        matrix_in = matrix_in + matrix_sig
        matrix_in = matrix_in + matrix_int
        matrix_in = matrix_in + matrix_nois
        return matrix_in

    def get_ampphi(self, vec):
        # разделение на амплитудную и фазовую составляющую
        # фазы - угол относительно оси Re
        vec_amp = np.abs(vec)
        vec_phi = np.angle(vec)
        return [vec_amp, vec_phi]

    def get_norm(self):
        # нормировка выборки
        self.vec_inamp = self.vec_inamp / 4
        self.vec_outamp = self.vec_outamp / 4
        self.vec_inphi = (self.vec_inphi + np.pi) / (2 * np.pi)
        self.vec_outphi = (self.vec_outphi + np.pi) / (2 * np.pi)

