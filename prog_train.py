import pack_train
from pack_train import *
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль модели обучения НС (L1)")
    print("Модуль использует пакет:", pack_train.NAME)

class Train:
    """Класс обучения НС"""

    def __init__(self):
        # модули обучения нейросети
        self.obj_sampling = pack_train.sampling.Sampling()
        self.obj_network = pack_train.network.Network()
        self.obj_file = pack_train.file_load.File_load()
        # характеристики модулей
        self.out_data = []
        self.out_samples = []

    def set(self, list_set):
        # инициализация параметров уровня L2
        self.obj_sampling.set(list_set[1])
        self.obj_network.set(list_set[1], list_set[4], list_set[5])
        self.obj_file.set(list_set[5])

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры модели обучения НС (L1):")
        print("\t-")
        self.obj_sampling.print()
        self.obj_network.print()
        self.obj_file.print()

    def calc_out(self, id_step, id_train=-1):
        # обучение НС
        if id_step == 0:
            # подготовка выборки
            self.calc_samples()
        elif id_step == 1:
            # обучение нейросети
            self.calc_net(id_train)

    def calc_samples(self):
        # загрузка исходных данных
        self.obj_file.calc_out()
        self.out_data = self.obj_file.get_out()
        # формирование обучающих выборок
        self.obj_sampling.calc_out(self.out_data)
        self.out_samples = self.obj_sampling.get_out()

    def calc_net(self, id_train):
        # обучение нейросети
        self.obj_network.calc_out(self.out_samples, id_train)

    def print_calc(self):
        # вывод информации о ходе вычислений
        self.obj_sampling.print_out()
