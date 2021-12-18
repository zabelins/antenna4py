import numpy as np
import pack_calc.calc_list as cl
import os

if __name__ == "__main__":
    print("Вы запустили модуль формирования обучающей выборки (L2)")

class Sampling:
    """Класс формирования обучающей выборки"""

    def __init__(self, id):
        self.id = id
        # обучающая выборка
        self.vec_inamp = []
        self.vec_inphi = []
        self.vec_outamp = []
        self.vec_outphi = []

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

    def get_out(self):
        out_samples = []
        out_samples.append(self.vec_inamp)
        out_samples.append(self.vec_inphi)
        out_samples.append(self.vec_outamp)
        out_samples.append(self.vec_outphi)
        return out_samples

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res = cl.is_ndarray([self.vec_inamp, self.vec_inphi, self.vec_outamp, self.vec_outphi])
        # вывод размерностей векторов
        if bool_res:
            print("Размерности векторов обучающей выборки:")
            print("\tvec_inamp.shape = ", self.vec_inamp.shape)
            print("\tvec_inphi.shape = ", self.vec_inphi.shape)
            print("\tvec_outamp.shape = ", self.vec_outamp.shape)
            print("\tvec_outphi.shape = ", self.vec_outphi.shape)
        else:
            print("Ошибка проверки типа векторов обучающей выборки")

    def get_learnarray(self, out_data):
        # цикл склейки обучающей выборки по файлам
        for i in range(len(out_data)):
            if i == 0:
                vec_in = out_data[i][9]
                vec_out = out_data[i][10]
            else:
                if vec_in.shape[1] == (out_data[i][9]).shape[1]:
                    vec_in = np.concatenate((vec_in, out_data[i][9]), axis=0)
                    vec_out = np.concatenate((vec_out, out_data[i][10]), axis=0)
                else:
                    print("Ошибка размерности обучающей выборки")
        # разделение на амплитуды и фазы
        self.vec_inamp, self.vec_inphi = self.get_ampphi(vec_in)
        self.vec_outamp, self.vec_outphi = self.get_ampphi(vec_out)

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

