import sys

import pack_calc.calc_list as cl
import numpy as np
import pandas as pd
import os

if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_load:
    """Класс работы с сохранёнными файлами"""

    def __init__(self):
        # параметры работы с файлами
        self.str_dir = ''
        self.str_name = 'DATA'
        # параметры
        self.sig_deg = np.array([])
        self.sig_amp = np.array([])
        self.sig_band = np.array([])
        self.int_deg = np.array([])
        self.int_amp = np.array([])
        self.int_band = np.array([])
        self.nois_amp = np.array([])
        self.dpt = np.array([])
        self.atn = np.array([])
        self.snir = np.array([])
        self.vec_sum = np.array([])
        self.vec_weight = np.array([])
        # список данных от файлов
        self.out_data = []

    def set(self, init):
        self.str_dir = init[22]

    def get(self):
        res = []
        res.append(self.str_dir)
        res.append(self.str_name)
        return res

    def print(self):
        print("Настройки работы с файлами (L2):")
        print("\tstr_dir = ", self.str_dir)
        print("\tstr_name = ", self.str_name)

    def calc_out(self):
        # проверка доступных файлов
        list_file = self.check_dir()
        # чтение файлов
        self.read_file(list_file)

    def get_out(self):
        return self.out_data

    def print_out(self, id_file):
        # проверка типа векторов на ndarray
        condit = cl.is_ndarray([self.dpt, self.atn, self.snir, self.vec_sum, self.vec_weight])
        # вывод размерностей векторов
        if condit:
            print("Файл ", id_file+1, ", размерности векторов:")
            print("\tdpt = ", self.dpt.shape)
            print("\tatn = ", self.atn.shape)
            print("\tsnir = ", self.snir.shape)
            print("\tvec_sum = ", self.vec_sum.shape)
            print("\tvec_weight = ", self.vec_weight.shape)
        else:
            print("Ошибка проверки типа векторов и матриц от антенной решётки")

    def read_file(self, list_file):
        # цикл по файлам
        for i in range(len(list_file)):
            # чтение csv
            var_file = pd.read_csv(self.str_dir + '/' + list_file[i], delimiter=',')
            # инициализация массивов
            self.init_vec(var_file)
            # цикл по времени
            for j in range(var_file.shape[0]):
                self.dpt[j] = self.get_flarray(var_file.at[j, 'depth'])
                self.atn[j] = self.get_flarray(var_file.at[j, 'atten'])
                self.snir[j] = self.get_flarray(var_file.at[j, 'outsnir'])
                self.vec_sum[j] = self.get_cparray(var_file.at[j, 'vec_sum'])
                self.vec_weight[j] = self.get_cparray(var_file.at[j, 'outweight'])
            # формирование выходных данных
            out_file = [self.dpt, self.atn, self.snir, self.vec_sum, self.vec_weight]
            self.out_data.append(out_file)
            self.print_out(i)
            # очистка векторов
            self.dpt, self.atn, self.snir, self.vec_sum, self.vec_weight = [], [], [], [], []

    def init_vec(self, data_file):
        # инициализация векторов
        len_time = data_file.shape[0]
        self.dpt = np.zeros(shape=[len_time, (self.get_flarray(data_file.at[0, 'depth'])).shape[0]])
        self.atn = np.zeros(shape=[len_time, (self.get_flarray(data_file.at[0, 'atten'])).shape[0]])
        self.snir = np.zeros(shape=[len_time, (self.get_flarray(data_file.at[0, 'outsnir'])).shape[0]])
        self.vec_sum = np.zeros(shape=[len_time, (self.get_cparray(data_file.at[0, 'vec_sum'])).shape[0]], dtype=complex)
        self.vec_weight = np.zeros(shape=[len_time, (self.get_cparray(data_file.at[0, 'outweight'])).shape[0]], dtype=complex)

    def check_dir(self):
        # проверка доступных файлов
        list_file = []
        if os.path.exists(self.str_dir + '/'):
            list_file = os.listdir(self.str_dir + '/')
            print("Найдено файлов с обучающими выборками:", len(list_file))
        else:
            print("Файлы с обучающими выборками не найдены")
        return list_file

    def get_cparray(self, str):
        str = str.replace(' ', '')
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.replace('(', '')
        str = str.replace(')', '')
        str = str.split(',')
        my_list = np.array([complex(x) for x in str])
        return my_list

    def get_flarray(self, str):
        str = str.replace(' ', '')
        str = str.replace('[', '')
        str = str.replace(']', '')
        str = str.replace('(', '')
        str = str.replace(')', '')
        str = str.split(',')
        my_list = np.array([float(x) for x in str])
        return my_list

