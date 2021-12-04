if __name__ == "__main__":
    print("Вы запустили модуль настроек обучения НС (L3)")

class Par_train:
    """Класс параметров НС"""

    def __init__(self, id):
        self.id = id
        # параметры нейронной сети
        self.net_type = 1
        self.net_layers = 3
        self.net_nodes = [20, 18, 20]
        # параметры обучения
        self.learn_type = 1
        self.learn_epoch = 100

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
        print("Параметры обучения НС (L3):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_layers = ", self.net_layers)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_type = ", self.learn_type)
        print("\tlearn_epoch = ", self.learn_epoch)

