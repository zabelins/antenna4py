if __name__ == "__main__":
    print("Вы запустили модуль настроек обучения НС (L3)")

class Par_train:
    """Класс параметров НС"""

    def __init__(self):
        # НЕЙРОННАЯ СЕТЬ
        # тип (0=mlp, 1=rbf, 2=cnn, 3=rnn), число нейронов (int)
        self.net_type = 3
        self.net_nodes = [20, 80, 20]
        # ОБУЧЕНИЕ
        # пакет (int), эпохи (int)
        self.learn_batch = 256
        self.learn_epoch = 200

    def set(self, init):
        self.net_type = init[0]
        self.net_nodes = init[1]
        self.learn_batch = init[2]
        self.learn_epoch = init[3]

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_nodes)
        res.append(self.learn_batch)
        res.append(self.learn_epoch)
        return res

    def print(self):
        print("Параметры обучения НС (L3):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_batch = ", self.learn_batch)
        print("\tlearn_epoch = ", self.learn_epoch)

