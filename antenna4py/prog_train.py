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
        # характеристики модулей обучения
        self.out_data = []
        self.out_samples = []

    def set(self, list_set):
        # инициализация параметров уровня L2
        self.obj_file.set(list_set[5])
        self.obj_network.set(list_set[4], list_set[5])

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры модели обучения НС (L1):")
        print("\t-")
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