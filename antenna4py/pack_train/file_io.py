import sys

import pack_calc.calc_list as cl
import numpy as np
import pandas as pd
import os

if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_IO:
    """Класс работы с сохранёнными файлами"""

    def __init__(self, id):
        self.id = id
        # параметры работы с файлами
        self.dir_data = ''
        self.name_file = 'DF'
        # параметры
        self.sig_deg = []
        self.sig_amp = []
        self.sig_band = []
        self.int_deg = []
        self.int_amp = []
        self.int_band = []
        self.depth = []
        self.atten = []
        self.outsnir = []
        self.vec_sum = []
        self.outweight = []
        # список данных от файлов
        self.out_data = []

    def set(self, init):
        self.dir_data = init[12]

    def get(self):
        res = []
        res.append(self.dir_data)
        res.append(self.name_file)
        return res

    def print(self):
        print("Настройки работы с файлами (L2):")
        print("\tdir_data = ", self.dir_data)
        print("\tname_file = ", self.name_file)

    def load_files(self):
        # проверка списка доступных файлов
        if os.path.exists(self.dir_data + '/'):
            file_list = os.listdir(self.dir_data + '/')
        else:
            print("Файлы с обучающими выборками не найдены")
            return []
        # вывод числа доступных файлов
        len_files = len(file_list)
        print("Найдено файлов с обучающими выборками:", len_files)
        # запуск цикла по файлам
        for i in range(len_files):
            # чтение csv
            data_file = pd.read_csv(self.dir_data + '/' + file_list[i], delimiter=',')
            # инициализация массивов
            self.init_vec(data_file)
            # заполнение массивов
            for j in range(data_file.shape[0]):
                self.depth[j] = self.get_flarray(data_file.at[j, 'depth'])
                self.atten[j] = self.get_flarray(data_file.at[j, 'atten'])
                self.outsnir[j] = self.get_flarray(data_file.at[j, 'outsnir'])
                self.vec_sum[j] = self.get_cparray(data_file.at[j, 'vec_sum'])
                self.outweight[j] = self.get_cparray(data_file.at[j, 'outweight'])
            # формирование выходных данных
            out_file = [self.depth, self.atten, self.outsnir, self.vec_sum, self.outweight]
            self.out_data.append(out_file)
            self.print_calc(i)
            # очистка векторов
            self.depth, self.atten, self.outsnir = [], [], []
            self.vec_sum, self.outweight = [], []
        # возврат данных
        return self.out_data

    def print_calc(self, id_file):
        # проверка типа векторов на ndarray
        condit = cl.is_ndarray([self.depth, self.atten, self.outsnir, self.vec_sum, self.outweight])
        # вывод размерностей векторов
        if condit:
            print("Файл ", id_file+1, ", размерности векторов:")
            print("\tdepth = ", self.depth.shape)
            print("\tatten = ", self.atten.shape)
            print("\toutsnir = ", self.outsnir.shape)
            print("\tvec_sum = ", self.vec_sum.shape)
            print("\toutweight = ", self.outweight.shape)
        else:
            print("Ошибка проверки типа векторов и матриц от антенной решётки")

    def get_cparray(self, str):
        str = str.replace(' ', '')
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.replace('(', '')
        str = str.replace(')', '')
        str = str.split(',')
        my_list = [complex(x) for x in str]
        my_list = np.array(my_list)
        return my_list

    def get_flarray(self, str):
        str = str.replace(' ', '')
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.replace('(', '')
        str = str.replace(')', '')
        str = str.split(',')
        my_list = [float(x) for x in str]
        my_list = np.array(my_list)
        return my_list

    def init_vec(self, data_file):
        # инициализация векторов
        len_time = data_file.shape[0]
        self.depth = np.zeros(shape=[len_time, (self.get_flarray(data_file.at[0, 'depth'])).shape[0]])
        self.atten = np.zeros(shape=[len_time, (self.get_flarray(data_file.at[0, 'atten'])).shape[0]])
        self.outsnir = np.zeros(shape=[len_time, (self.get_flarray(data_file.at[0, 'outsnir'])).shape[0]])
        self.vec_sum = np.zeros(shape=[len_time, (self.get_cparray(data_file.at[0, 'vec_sum'])).shape[0]],
                                dtype=complex)
        self.outweight = np.zeros(shape=[len_time, (self.get_cparray(data_file.at[0, 'outweight'])).shape[0]],
                                  dtype=complex)
