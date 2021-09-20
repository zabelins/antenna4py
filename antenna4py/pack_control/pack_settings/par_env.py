import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров сигналов и помех (L3)")

class Par_env:
    """Класс исходных параметров сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.id = id
        # параметры сигналов
        self.sig_deg = [0]
        self.sig_amp = [1]
        self.sig_band = [0]
        # параметры помех
        self.int_deg = [6, 20]
        self.int_amp = [1, 1]
        self.int_band = [5 * math.pow(10, 8), 5 * math.pow(10, 8)] # [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)]
        # параметры шума
        self.nois_amp = [1]

    def set(self, init):
        self.sig_deg = init[0]
        self.sig_amp = init[1]
        self.sig_band = init[2]
        self.int_deg = init[3]
        self.int_amp = init[4]
        self.int_band = init[5]
        self.nois_amp = init[6]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_band)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_band)
        res.append(self.nois_amp)
        return res

    def print(self):
        print(" --- Параметры сигнально-помеховой обстановки (L3) --- ")
        print("id = ", self.id)
        print("sig_deg = ", self.sig_deg)
        print("sig_amp = ", self.sig_amp)
        print("sig_band = ", self.sig_band)
        print("int_deg = ", self.int_deg)
        print("int_amp = ", self.int_amp)
        print("int_band = ", self.int_band)
        print("nois_amp = ", self.nois_amp)

    def print_short(self):
        print(" --- Параметры сигнально-помеховой обстановки (L3) --- ")
        print("par_env = ", self.get())
