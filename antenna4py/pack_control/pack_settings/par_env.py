import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров сигналов и помех (L3)")

class Par_env:
    """Класс исходных параметров сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.id = id
        self.sig_deg = [0]
        self.sig_amp = [1]
        self.sig_fband = [0]
        self.int_deg = [20, 30]
        self.int_amp = [1, 1]
        self.int_fband = [5 * math.pow(10, 8), 5 * math.pow(10, 8)] # [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)]
        self.nois_amp = [1]

    def set(self, init):
        self.sig_deg = init[0]
        self.sig_amp = init[1]
        self.sig_fband = init[2]
        self.int_deg = init[3]
        self.int_amp = init[4]
        self.int_fband = init[5]
        self.nois_amp = init[6]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_fband)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_fband)
        res.append(self.nois_amp)
        return res

    def print(self):
        print(" --- Параметры сигнально-помеховой обстановки (L3) --- ")
        print("id = ", self.id)
        print("sig_deg = ", self.sig_deg)
        print("sig_amp = ", self.sig_amp)
        print("sig_fband = ", self.sig_fband)
        print("int_deg = ", self.int_deg)
        print("int_amp = ", self.int_amp)
        print("int_fband = ", self.int_fband)
        print("fband_int = ", self.nois_amp)

    def print_short(self):
        print(" --- Параметры сигнально-помеховой обстановки (L3) --- ")
        print("par_env = ", self.get())
