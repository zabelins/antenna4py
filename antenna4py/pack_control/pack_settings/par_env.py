# модуль параметров сигналов и помех

import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров сигналов и помех (L3)")

class Par_env:
    def __init__(self, id):
        self.id = id
        self.id_config = 1
        self.mod_sig = 1
        self.mod_int = 1
        self.deg_sig = [0]
        self.deg_int = [70, 80]
        self.am_sig = [1]
        self.am_int = [1, 1]
        self.am_nois = [1]
        self.fband_sig = [0]
        self.fband_int = [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)]
    def set(self, init):
        self.id_config = init[0]
        self.mod_sig = init[1]
        self.mod_int = init[2]
        self.deg_sig = init[3]
        self.deg_int = init[4]
        self.am_sig = init[5]
        self.am_int = init[6]
        self.am_nois = init[7]
        self.fband_sig = init[8]
        self.fband_int = init[9]
    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_config)
        res.append(self.mod_sig)
        res.append(self.mod_int)
        res.append(self.deg_sig)
        res.append(self.deg_int)
        res.append(self.am_sig)
        res.append(self.am_int)
        res.append(self.am_nois)
        res.append(self.fband_sig)
        res.append(self.fband_int)
        return res
    def print(self):
        print(" --- Значения параметров сигналов и помех (L3) --- ")
        print("id = ", self.id)
        print("id_config = ", self.id_config)
        print("mod_sig = ", self.mod_sig)
        print("mod_int = ", self.mod_int)
        print("deg_sig = ", self.deg_sig)
        print("deg_int = ", self.deg_int)
        print("am_sig = ", self.am_sig)
        print("am_int = ", self.am_int)
        print("am_nois = ", self.am_nois)
        print("fband_sig = ", self.fband_sig)
        print("fband_int = ", self.fband_int)
    def print_short(self):
        print(" --- Значения параметров сигналов и помех (L3) --- ")
        print("parameters_env = ", self.get())
