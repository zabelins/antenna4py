# модуль настроек обучения НС

if __name__ == "__main__":
    print("Вы запустили модуль настроек обучения НС (L3)")

class Set_nn:
    """Класс настроек НС"""

    def __init__(self, id):
        self.id = id
        self.id_nn = 1
        self.id_learn = 1
        self.num_epoch = 100
        self.num_layers = 3
        self.num_neurons = 1

    def set(self, init):
        self.id_nn = init[0]
        self.id_learn = init[1]
        self.num_epoch = init[2]
        self.num_layers = init[3]
        self.num_neurons = init[4]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_nn)
        res.append(self.id_learn)
        res.append(self.num_epoch)
        res.append(self.num_layers)
        res.append(self.num_neurons)
        return res

    def print(self):
        print(" --- Значения настроек обучения НС (L3) --- ")
        print("id = ", self.id)
        print("id_alg = ", self.id_nn)
        print("id_alg = ", self.id_learn)
        print("num_epoch = ", self.num_epoch)
        print("num_layers = ", self.num_layers)
        print("num_neurons = ", self.num_neurons)

    def print_short(self):
        print(" --- Значения настроек обучения НС (L3) --- ")
        print("settings_nn = ", self.get())
