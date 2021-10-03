import pack_train.pack_neuro as pn
from pack_train.pack_neuro import *

if __name__ == "__main__":
    print("Вы запустили модуль формирования обучающей выборки (L2)")

class Train:
    """Класс формирования обучающей выборки"""

    def __init__(self, id):
        self.list_sampling = pn.sampling.Sampling(1)
        self.list_network = pn.network.Network(1)
        self.id = id
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

    def set(self, init):
        self.net_type = init[0]
        self.net_layers = init[1]
        self.net_nodes = init[2]
        self.learn_type = init[3]
        self.learn_epoch = init[4]

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_layers)
        res.append(self.net_nodes)
        res.append(self.learn_type)
        res.append(self.learn_epoch)
        return res

    def print(self):
        print("Параметры обучения НС (L2):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_layers = ", self.net_layers)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_type = ", self.learn_type)
        print("\tlearn_epoch = ", self.learn_epoch)

    def calc_out(self, out_data):
        # проверка исходных данных
        if len(out_data) == 0:
            return []
        # формирование обучающих выборок
        self.list_sampling.calc_out(out_data)
        out_sampling = self.list_sampling.get_out()
        # обучение НС
        print("инициализация НС...")
        self.list_network.calc_out(out_sampling)

    def print_out(self):
        pass
