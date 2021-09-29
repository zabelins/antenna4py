import numpy as np
import pack_calc.calc_list as cl
import pack_model.pack_neuro as pn
from pack_model.pack_neuro import *

if __name__ == "__main__":
    print("Вы запустили модуль формирования обучающей выборки (L2)")


class Train:
    """Класс формирования обучающей выборки"""

    def __init__(self, id):
        self.list_sampling = pn.sampling.Sampling(1)
        self.id = id
        self.id_nn = []
        self.id_learn = []
        self.num_epoch = []
        self.num_layers = []
        self.num_neurons = []
        self.matrix_learn = []
        self.matrix_test = []

    def set(self, init):
        self.id_nn = init[0]
        self.id_learn = init[1]
        self.num_epoch = init[2]
        self.num_layers = init[3]
        self.num_neurons = init[4]

    def get(self):
        res = []
        res.append(self.id_nn)
        res.append(self.id_learn)
        res.append(self.num_epoch)
        res.append(self.num_layers)
        res.append(self.num_neurons)
        return res

    def print(self):
        print("Параметры обучения НС (L2):")
        print("\tid_nn = ", self.id_nn)
        print("\tid_learn = ", self.id_learn)
        print("\tnum_epoch = ", self.num_epoch)
        print("\tnum_layers = ", self.num_layers)
        print("\tnum_neurons = ", self.num_neurons)

    def calc_out(self, out_data):
        # проверка исходных данных
        if len(out_data) == 0:
            return []
        # формирование обучающих выборок
        self.list_sampling.calc_out(out_data)
        out_sampling = self.list_sampling.get_out()
        # печать результатов
        print("инициализация НС...")
        print(len(out_sampling))

    def print_out(self):
        pass
