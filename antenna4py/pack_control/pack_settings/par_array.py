import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров антенной решётки (L3)")

class Par_array:
    """Класс исходных параметров антенной решётки"""

    def __init__(self, id):
        self.id = id
        self.N = 10
        self.beta = 1
        self.f_cen = 5 * math.pow(10, 9)
        self.noise_phimax = 0 * math.pi
        self.noise_ampmax = 0
        self.noise_phidist = 1
        self.noise_ampdist = 1
        self.id_dist = 1
        self.id_elem = 1
        self.id_effect = 1

    def set(self, init):
        self.N = init[0]
        self.beta = init[1]
        self.f_cen = init[2]
        self.noise_phimax = init[3]
        self.noise_ampmax = init[4]
        self.noise_phidist = init[5]
        self.noise_ampdist = init[6]
        self.id_dist = init[7]
        self.id_elem = init[8]
        self.id_effect = init[9]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.N)
        res.append(self.beta)
        res.append(self.f_cen)
        res.append(self.noise_phimax)
        res.append(self.noise_ampmax)
        res.append(self.noise_phidist)
        res.append(self.noise_ampdist)
        res.append(self.id_dist)
        res.append(self.id_elem)
        res.append(self.id_effect)
        return res

    def print(self):
        print(" --- Значения параметров антенной решётки (L3) --- ")
        print("id = ", self.id)
        print("N = ", self.N)
        print("beta = ", self.beta)
        print("f_cen = ", self.f_cen)
        print("noise_phimax = ", self.noise_phimax)
        print("noise_ampmax = ", self.noise_ampmax)
        print("noise_phidist = ", self.noise_phidist)
        print("noise_ampdist = ", self.noise_ampdist)
        print("id_dist = ", self.id_dist)
        print("id_elem = ", self.id_elem)
        print("id_effect = ", self.id_effect)

    def print_short(self):
        print(" --- Значения параметров антенной решётки (L3) --- ")
        print("par_array = ", self.get())