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
        self.int_deg = [17, 44]
        self.int_amp = [1/2, 1/2]
        self.int_band = [3 * math.pow(10, 8), 3 * math.pow(10, 8)] # [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)]
        # параметры модуляции
        self.shift_dynamic = [math.pi / 4]
        self.shift_static = [-math.pi / 4 + math.pi / 4]

    def set(self, init):
        self.sig_deg = init[0]
        self.sig_amp = init[1]
        self.sig_band = init[2]
        self.int_deg = init[3]
        self.int_amp = init[4]
        self.int_band = init[5]
        self.shift_dynamic = init[6]
        self.shift_static = init[7]

    def get(self):
        res = []
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_band)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_band)
        res.append(self.shift_dynamic)
        res.append(self.shift_static)
        return res

    def print(self):
        print("Параметры сигнально-помеховой обстановки (L3):")
        print("\tsig_deg = ", self.sig_deg)
        print("\tsig_amp = ", self.sig_amp)
        print("\tsig_band = ", self.sig_band)
        print("\tint_deg = ", self.int_deg)
        print("\tint_amp = ", self.int_amp)
        print("\tint_band = ", self.int_band)
        print("\tshift_dynamic = ", self.shift_dynamic)
        print("\tshift_static = ", self.shift_static)

