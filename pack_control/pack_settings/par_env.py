import math

if __name__ == "__main__":
    print("Вы запустили модуль параметров сигналов и помех (L3)")

class Par_env:
    """Класс исходных параметров сигнально-помеховой обстановки"""

    def __init__(self):
        # ПОЛЕЗНЫЙ СИГНАЛ
        # угол (flt), амплитуда (flt), полоса (flt), частота модуляции (flt),
        # модуляция (0=нет, 1=ФМ), информация (0=const, 1=меандр, 2=имп, 3=син, 4=биты, 5=фаз.шум)
        self.sig_deg = [0]
        self.sig_amp = [1 * math.pow(10, -6)]
        self.sig_bnd = [0]
        self.sig_frq = 1 * math.pow(10, 3)
        self.sig_mod = 1
        self.sig_inf = 4
        # НЕЖЕЛАТЕЛЬНЫЕ ПОМЕХИ
        # углы (flt), амплитуды (flt), полосы (flt), частота модуляции (flt),
        # модуляция (0=нет, 1=ФМ), информация (0=const, 1=имп, 2=меандр, 3=син, 4=биты, 5=фаз.шум)
        self.int_deg = [10.25]
        self.int_amp = [3.1623 * math.pow(10, -5)]
        self.int_bnd = [0] # [5 * math.pow(10, 8), 2.5 * math.pow(10, 8)]
        self.int_frq = 1 * math.pow(10, 3)
        self.int_mod = 1
        self.int_inf = 5
        # ПАРАМЕТРЫ МОДУЛЯЦИИ
        # длина кода (int), несущая частота (flt), фазовые сдвиги (flt)
        self.msg_code = 100
        self.msg_carr = 2 * math.pow(10, 3)
        self.shift_dynamic = [math.pi / 4]
        self.shift_static = [0]
        # ПАРАМЕТРЫ ОБУЧАЮЩЕЙ ВЫБОРКИ
        # накопление (int)
        self.learn_size = 10

    def set(self, init):
        self.sig_deg = init[0]
        self.sig_amp = init[1]
        self.sig_bnd = init[2]
        self.sig_frq = init[3]
        self.sig_mod = init[4]
        self.sig_inf = init[5]
        self.int_deg = init[6]
        self.int_amp = init[7]
        self.int_bnd = init[8]
        self.int_frq = init[9]
        self.int_mod = init[10]
        self.int_inf = init[11]
        self.msg_code = init[12]
        self.msg_carr = init[13]
        self.shift_dynamic = init[14]
        self.shift_static = init[15]
        self.learn_size = init[16]

    def get(self):
        res = []
        res.append(self.sig_deg)
        res.append(self.sig_amp)
        res.append(self.sig_bnd)
        res.append(self.sig_frq)
        res.append(self.sig_mod)
        res.append(self.sig_inf)
        res.append(self.int_deg)
        res.append(self.int_amp)
        res.append(self.int_bnd)
        res.append(self.int_frq)
        res.append(self.int_mod)
        res.append(self.int_inf)
        res.append(self.msg_code)
        res.append(self.msg_carr)
        res.append(self.shift_dynamic)
        res.append(self.shift_static)
        res.append(self.learn_size)
        return res

    def print(self):
        print("Параметры сигнально-помеховой обстановки (L3):")
        print("\tsig_deg = ", self.sig_deg)
        print("\tsig_amp = ", self.sig_amp)
        print("\tsig_bnd = ", self.sig_bnd)
        print("\tsig_frq = ", self.sig_frq)
        print("\tsig_mod = ", self.sig_mod)
        print("\tsig_inf = ", self.sig_inf)
        print("\tint_deg = ", self.int_deg)
        print("\tint_amp = ", self.int_amp)
        print("\tint_bnd = ", self.int_bnd)
        print("\tint_frq = ", self.int_frq)
        print("\tint_mod = ", self.int_mod)
        print("\tint_inf = ", self.int_inf)
        print("\tmsg_code = ", self.msg_code)
        print("\tmsg_carr = ", self.msg_carr)
        print("\tshift_dynamic = ", self.shift_dynamic)
        print("\tshift_static = ", self.shift_static)
        print("\tlearn_size = ", self.learn_size)

