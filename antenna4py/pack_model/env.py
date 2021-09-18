import pack_model.pack_environment as pe
from pack_model.pack_environment import *
import pack_calc.calc_list as cl
import numpy as np
import math

if __name__ == "__main__":
    print("Вы запустили модуль модели сигналов и помех (L2)")
    print("Модуль использует пакет:", pe.NAME)

class Env:
    """Класс моделирования сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.id = id
        self.deg_sig = []
        self.deg_int = []
        self.amp_sig = []
        self.amp_int = []
        self.amp_nois = []
        self.fband_sig = []
        self.fband_int = []
        self.vec_degsig = []
        self.vec_degint = []
        self.vec_ampsig = []
        self.vec_ampint = []
        self.vec_ampnois = []
        self.vec_fbandsig = []
        self.vec_fbandint = []
        self.list_gen = pe.signal_generator.Generator(1)

    def set(self, init):
        self.deg_sig = np.array(init[1])
        self.deg_int = np.array(init[4])
        self.amp_sig = np.array(init[2])
        self.amp_int = np.array(init[5])
        self.amp_nois = np.array(init[7])
        self.fband_sig = np.array(init[3])
        self.fband_int = np.array(init[6])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.deg_sig)
        res.append(self.deg_int)
        res.append(self.amp_sig)
        res.append(self.amp_int)
        res.append(self.amp_nois)
        res.append(self.fband_sig)
        res.append(self.fband_int)
        return res

    def print(self):
        print(" --- Параметры модели сигналов и помех (L2) --- ")
        print("id = ", self.id)
        print("deg_sig = ", self.deg_sig)
        print("deg_int = ", self.deg_int)
        print("amp_sig = ", self.amp_sig)
        print("amp_int = ", self.amp_int)
        print("amp_nois = ", self.amp_nois)
        print("fband_sig = ", self.fband_sig)
        print("fband_int = ", self.fband_int)
        self.list_gen.print_short()

    def print_short(self):
        print(" --- Параметры модели сигналов и помех (L2) --- ")
        print("env = ", self.get())

    def calc_out(self, out_set, id_script):
        # распаковка исходных данных
        vec_time = out_set[1]
        # частота модуляции сигналов
        var_freq = 10 * math.pow(10, 6)
        # определение необходимой модуляции для заданного динамического сценария
        id_ampint, id_degint, id_bandint = 0, 0, 0
        if (id_script >= 1) and (id_script <= 3):
            # если амплитудная модуляция
            id_ampint = id_script
        if (id_script == 4):
            # если изменение углов
            id_degint = 1
            self.deg_int, self.amp_int, self.fband_int = np.array([-90]), np.array([1]), np.array([5 * math.pow(10, 8)])
        if (id_script == 5):
            # если рандомные помехи
            pp = 0
        # создаём вектора изменения сигналов и помех от времени
        self.vec_degsig = self.list_gen.get_vecdeg(vec_time, self.deg_sig, 0)
        self.vec_degint = self.list_gen.get_vecdeg(vec_time, self.deg_int, id_degint)
        self.vec_ampsig = self.list_gen.get_vecamp(vec_time, self.amp_sig, var_freq, 0)
        self.vec_ampint = self.list_gen.get_vecamp(vec_time, self.amp_int, var_freq, id_ampint)
        self.vec_ampnois = self.list_gen.get_vecamp(vec_time, self.amp_nois, var_freq, 0)
        self.vec_fbandsig = self.list_gen.get_vecband(vec_time, self.fband_sig, 0)
        self.vec_fbandint = self.list_gen.get_vecband(vec_time, self.fband_int, id_bandint)
        #print("vec_time = ", vec_time)
        #print("self.vec_degint = ", self.vec_degint)
        #print("self.vec_ampint = ", self.vec_ampint)

    def get_out(self):
        res = []
        res.append(self.vec_degsig)
        res.append(self.vec_degint)
        res.append(self.vec_ampsig)
        res.append(self.vec_ampint)
        res.append(self.vec_ampnois)
        res.append(self.vec_fbandsig)
        res.append(self.vec_fbandint)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_buf1 = isinstance(self.vec_degsig, np.ndarray)
        bool_buf2 = isinstance(self.vec_degint, np.ndarray)
        bool_buf3 = isinstance(self.vec_ampsig, np.ndarray)
        bool_buf4 = isinstance(self.vec_ampint, np.ndarray)
        bool_buf5 = isinstance(self.vec_ampnois, np.ndarray)
        bool_buf6 = isinstance(self.vec_fbandsig, np.ndarray)
        bool_buf7 = isinstance(self.vec_fbandint, np.ndarray)
        bool_res1 = (bool_buf1 == True) and (bool_buf2 == True) and (bool_buf3 == True)
        bool_res2 = (bool_buf4 == True) and (bool_buf5 == True) and (bool_buf6 == True)
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True) and (bool_buf7 == True):
            print("Размерности векторов сигналов и помех от времени:")
            print("vec_degsig.shape = ", self.vec_degsig.shape)
            print("vec_degint.shape = ", self.vec_degint.shape)
            print("vec_ampsig.shape = ", self.vec_ampsig.shape)
            print("vec_ampint.shape = ", self.vec_ampint.shape)
            print("vec_ampnois.shape = ", self.vec_ampnois.shape)
            print("vec_fbandsig.shape = ", self.vec_fbandsig.shape)
            print("vec_fbandint.shape = ", self.vec_fbandint.shape)
        else:
            print("Ошибка проверки типа векторов сигналов и помех от времени")


