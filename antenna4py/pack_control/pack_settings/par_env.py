import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров сигналов и помех (L3)")

class Par_env:
    """Класс исходных параметров сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.id = id
        self.id_config = 1
        self.sig_mod = 0
        self.sig_deg = [0]
        self.sig_amp = [1]
        self.sig_fband = [0]
        self.int_mod = 0
        self.int_deg = [30, 80]
        self.int_amp = [1, 1]
        self.int_fband = [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)] # [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)]
        self.nois_amp = [1]

    def set(self, init):
        self.id_config = init[0]
        self.sig_mod = init[1]
        self.sig_deg = init[2]
        self.sig_amp = init[3]
        self.sig_fband = init[4]
        self.int_mod = init[5]
        self.int_deg = init[6]
        self.int_amp = init[7]
        self.int_fband = init[8]
        self.nois_amp = init[9]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_config)
        res.append(self.sig_mod)
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_fband)
        res.append(self.int_mod)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_fband)
        res.append(self.nois_amp)
        return res

    def print(self):
        print(" --- Значения параметров сигналов и помех (L3) --- ")
        print("id = ", self.id)
        print("id_config = ", self.id_config)
        print("sig_mod = ", self.sig_mod)
        print("sig_deg = ", self.sig_deg)
        print("sig_amp = ", self.sig_amp)
        print("sig_fband = ", self.sig_fband)
        print("int_mod = ", self.int_mod)
        print("int_deg = ", self.int_deg)
        print("int_amp = ", self.int_amp)
        print("int_fband = ", self.int_fband)
        print("fband_int = ", self.nois_amp)

    def print_short(self):
        print(" --- Значения параметров сигналов и помех (L3) --- ")
        print("parameters_env = ", self.get())
