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
        # модули обучения нейронной сети
        self.obj_sampling = pack_train.sampling.Sampling(1)
        self.obj_network = pack_train.network.Network(1)
        self.obj_file = pack_train.file_io.File_IO(2)
        # параметры нейронной сети
        self.net_type = []
        self.net_layers = []
        self.net_nodes = []
        # параметры обучения
        self.learn_type = []
        self.learn_epoch = []
        # характеристики модулей обучения
        self.out_data = []
        self.out_samples = []
        self.out_net = []

    def set(self, list_set):
        # инициализация параметров модели уровня L1
        self.net_type = list_set[4][0]
        self.net_layers = list_set[4][1]
        self.net_nodes = list_set[4][2]
        self.learn_type = list_set[4][3]
        self.learn_epoch = list_set[4][4]
        # инициализация параметров уровня L2
        self.obj_file.set(list_set[5])

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
        self.obj_sampling.print()
        self.obj_network.print()
        self.obj_file.print()

    def calc_samples(self):
        # загрузка файлов с обучающими выборками
        self.out_data = self.obj_file.load_files()
        # проверка исходных данных
        if len(self.out_data) == 0:
            return []
        # формирование обучающих выборок
        self.obj_sampling.calc_out(self.out_data)
        self.out_samples = self.obj_sampling.get_out()

    def calc_out(self, id_train):
        # обучение НС
        self.obj_network.calc_out(self.out_samples, id_train)

    def print_calc(self):
        # вывод информации о ходе вычислений
        self.obj_sampling.print_out()