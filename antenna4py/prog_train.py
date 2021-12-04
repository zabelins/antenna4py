import pack_train
from pack_train import *
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль модели обучения НС (L1)")
    print("Модуль использует пакет:", pack_train.NAME)

class Model_train:
    """Класс обучения НС"""

    def __init__(self):
        self.list_sampling = pack_train.sampling.Sampling(1)
        self.list_network = pack_train.network.Network(1)
        self.list_file = pack_train.file_io.File_IO(2)
        # параметры нейронной сети
        self.net_type = []
        self.net_layers = []
        self.net_nodes = []
        # параметры обучения
        self.learn_type = []
        self.learn_epoch = []
        # выборки
        self.matrix_learn = []
        self.matrix_test = []

    def set(self, obj_set):
        # формирование векторов параметров и настроек
        par_train = obj_set.list_partrain.get()
        set_prog = obj_set.list_setprog.get()
        # инициализация параметров модели уровня L1
        self.net_type = par_train[0]
        self.net_layers = par_train[1]
        self.net_nodes = par_train[2]
        self.learn_type = par_train[3]
        self.learn_epoch = par_train[4]
        # инициализация параметров уровня L2
        self.list_file.set(set_prog)

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_layers)
        res.append(self.net_nodes)
        res.append(self.learn_type)
        res.append(self.learn_epoch)
        return res

    def print(self):
        print("Параметры модели обучения НС (L1):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_layers = ", self.net_layers)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_type = ", self.learn_type)
        print("\tlearn_epoch = ", self.learn_epoch)
        self.list_sampling.print()
        self.list_network.print()
        self.list_file.print()

    def calc_out(self):
        # загрузка файлов с обучающими выборками
        out_data = self.list_file.load_files()
        # проверка исходных данных
        if len(out_data) == 0:
            return []
        # формирование обучающих выборок
        self.list_sampling.calc_out(out_data)
        out_sampling = self.list_sampling.get_out()
        # обучение НС
        print("инициализация НС...")
        self.list_network.calc_out(out_sampling)