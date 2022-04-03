import numpy as np
import pack_calc.calc_list as cl
import os

if __name__ == "__main__":
    print("Вы запустили модуль формирования обучающей выборки (L2)")

class Sampling:
    """Класс формирования обучающей выборки"""

    def __init__(self, id):
        self.id = id
        # данные для фильтрации
        self.x_complex = []
        self.y_complex = []
        self.outsnir = []
        # обучающая выборка
        self.x_real = []
        self.x_imag = []
        self.y_real = []
        self.y_imag = []
        # вектора обучающей выборки
        self.x_train = []
        self.y_train = []
        # вектора тестовой выборки
        self.x_test = []
        self.y_test = []

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры формирования обучающей выборки (L3):")
        print("\t-")

    def calc_out(self, out_data):
        # цикл склейки обучающей выборки по файлам
        for file in range(len(out_data)):
            if file == 0:
                self.outsnir = out_data[file][2]
                self.x_complex = out_data[file][3]
                self.y_complex = out_data[file][4]
            else:
                # проверка размерности входов и выходов обучающей выборки
                condit_1 = (self.x_complex.shape[1] == (out_data[file][3]).shape[1])
                condit_2 = (self.y_complex.shape[1] == (out_data[file][4]).shape[1])
                if condit_1 and condit_2:
                    self.outsnir = np.concatenate((self.outsnir, out_data[file][2]), axis=0)
                    self.x_complex = np.concatenate((self.x_complex, out_data[file][3]), axis=0)
                    self.y_complex = np.concatenate((self.y_complex, out_data[file][4]), axis=0)
                else:
                    print("Ошибка размерности обучающей выборки")
        # результаты фильтрации
        print("Выборка до фильтрации:")
        print("\tx_complex.shape = ", self.x_complex.shape)
        print("\ty_complex.shape = ", self.y_complex.shape)
        # цикл фильтрации
        self.calc_filter()
        # разделение на амплитуды, синусы и косинусы
        self.calc_format()
        # нормировка векторов
        self.calc_norm()
        # формирование обучающей и тестовой выборок
        self.get_array()

    def get_out(self):
        out_samples = []
        out_samples.append(self.x_train)
        out_samples.append(self.y_train)
        out_samples.append(self.x_test)
        out_samples.append(self.y_test)
        return out_samples

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res = cl.is_ndarray([self.x_train, self.y_train, self.x_test, self.y_test])
        # вывод размерностей векторов
        if bool_res:
            print("Размерности векторов обучающей выборки:")
            print("\tx_train.shape = ", self.x_train.shape)
            print("\ty_train.shape = ", self.y_train.shape)
            print("\tx_test.shape = ", self.x_test.shape)
            print("\ty_test.shape = ", self.y_test.shape)
        else:
            print("Ошибка проверки типа векторов обучающей выборки")

    def calc_filter(self):
        # фильтрация обучающей выборки по критерию
        len_array, sample = self.outsnir.shape[0], 0
        while sample < len_array:
            # порог по выходному ОСШП
            if self.outsnir[sample][0] < 12.0:
                self.x_complex = np.delete(self.x_complex, sample, axis=0)
                self.y_complex = np.delete(self.y_complex, sample, axis=0)
                self.outsnir = np.delete(self.outsnir, sample, axis=0)
                len_array = len_array - 1
                sample = sample - 1
            sample = sample + 1
        # результаты фильтрации
        print("Выборка после фильтрации:")
        print("\tx_complex.shape = ", self.x_complex.shape)
        print("\ty_complex.shape = ", self.y_complex.shape)

    def calc_format(self):
        # разделение на действительную и мнимую составляющую
        self.x_real = np.real(self.x_complex)
        self.x_imag = np.imag(self.x_complex)
        self.y_real = np.real(self.y_complex)
        self.y_imag = np.imag(self.y_complex)

    def calc_norm(self):
        # нормировка выборки
        print("x_real")
        [x_real_mean, x_real_dev] = self.calc_statistic(self.x_real, 1)
        print("x_imag")
        [x_imag_mean, x_imag_dev] = self.calc_statistic(self.x_imag, 1)
        print("y_real")
        [y_real_mean, y_real_dev] = self.calc_statistic(self.y_real, 1)
        print("y_imag")
        [y_imag_mean, y_imag_dev] = self.calc_statistic(self.y_imag, 1)
        # нормируем, чтобы попадало в интервал [0,1]
        self.x_real = (self.x_real - x_real_mean) / (x_real_dev * 2) + 0.5
        self.x_imag = (self.x_imag - x_imag_mean) / (x_imag_dev * 2) + 0.5
        self.y_real = (self.y_real - y_real_mean) / (y_real_dev * 2) + 0.5
        self.y_imag = (self.y_imag - y_imag_mean) / (y_imag_dev * 2) + 0.5

    def calc_statistic(self, vec, info):
        if info == 1:
            #print("\tmax = ", np.max(vec))
            #print("\tmin = ", np.min(vec))
            #print("\tmax_3msd = ", np.mean(vec) + (np.std(vec) * 3))
            #print("\tmin_3msd = ", np.mean(vec) - (np.std(vec) * 3))
            print("\tmean = ", np.mean(vec))
            print("\tdev = ", np.max([np.max(vec)-np.mean(vec), np.mean(vec)-np.min(vec)]))
        return [np.mean(vec), np.max([np.max(vec)-np.mean(vec), np.mean(vec)-np.min(vec)])]

    def get_array(self):
        # преобразование в сигналы для входа
        len_time, len_num = self.x_real.shape[0], self.x_real.shape[1]
        len_train, len_test = round(len_time * 0.8), round(len_time * 0.2)
        # инициализация векторов выборки
        self.x_train = np.zeros(shape=[len_train, len_num * 2])
        self.y_train = np.zeros(shape=[len_train, len_num * 2])
        self.x_test = np.zeros(shape=[len_test, len_num * 2])
        self.y_test = np.zeros(shape=[len_test, len_num * 2])
        # собираем единые вектора обучающей выборки
        for sample in range(len_train):
            for column in range(len_num):
                self.x_train[sample][column] = self.x_real[sample][column]
                self.y_train[sample][column] = self.y_real[sample][column]
                self.x_train[sample][column + len_num] = self.x_imag[sample][column]
                self.y_train[sample][column + len_num] = self.y_imag[sample][column]
        # собираем единые вектора тестовой выборки
        for sample in range(len_test):
            for column in range(len_num):
                self.x_test[sample][column] = self.x_real[sample + len_train][column]
                self.y_test[sample][column] = self.y_real[sample + len_train][column]
                self.x_test[sample][column + len_num] = self.x_imag[sample + len_train][column]
                self.y_test[sample][column + len_num] = self.y_imag[sample + len_train][column]
