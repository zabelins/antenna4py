import pack_model.pack_environment as pe
from pack_model.pack_environment import *
import pack_calc.calc_list as cl
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели сигналов и помех (L2)")
    print("Модуль использует пакет:", pe.NAME)

class Env:
    """Класс моделирования сигнально-помеховой обстановки"""

    def __init__(self, id):
        self.id = id
        self.id_config = []
        self.mod_sig = []
        self.mod_int = []
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
        self.id_config = np.array(init[1])
        self.mod_sig = np.array(init[2])
        self.mod_int = np.array(init[6])
        self.deg_sig = np.array(init[3])
        self.deg_int = np.array(init[7])
        self.amp_sig = np.array(init[4])
        self.amp_int = np.array(init[8])
        self.amp_nois = np.array(init[10])
        self.fband_sig = np.array(init[5])
        self.fband_int = np.array(init[9])

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_config)
        res.append(self.mod_sig)
        res.append(self.mod_int)
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
        print("id_config = ", self.id_config)
        print("mod_sig = ", self.mod_sig)
        print("mod_int = ", self.mod_int)
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
        print("environment = ", self.get())

    def calc_dynamic(self, out_set):
        # распаковка исходных данных
        vec_time, len_time = [out_set[1], out_set[1].shape[0]]
        # нужно добавить амплитудную и частотную модуляцию
        # нужно добавить возможность изменения по углам
        # создаём вектора изменения сигналов и помех от времени
        self.vec_degsig = self.list_gen.get_vecdeg(len_time, self.deg_sig, 0)
        self.vec_degint = self.list_gen.get_vecdeg(len_time, self.deg_int, 0)
        self.vec_ampsig = self.list_gen.get_vecamp(len_time, self.amp_sig, self.mod_sig)
        self.vec_ampint = self.list_gen.get_vecamp(len_time, self.amp_int, self.mod_int)
        self.vec_ampnois = self.list_gen.get_vecamp(len_time, self.amp_nois, 0)
        self.vec_fbandsig = self.list_gen.get_vecband(len_time, self.fband_sig, 0)
        self.vec_fbandint = self.list_gen.get_vecband(len_time, self.fband_int, 0)
        # нужно добавить разные типы расстановки помех
        print("vec_time = ", vec_time)
        print("self.vec_degint = ", self.vec_degint)
        print("self.vec_ampint = ", self.vec_ampint)

    def calc_static(self, out_set):
        pass

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
        print("Размерности векторов сигналов и помех от времени:")
        print("vec_degsig.shape = ", self.vec_degsig.shape)
        print("vec_degint.shape = ", self.vec_degint.shape)
        print("vec_ampsig.shape = ", self.vec_ampsig.shape)
        print("vec_ampint.shape = ", self.vec_ampint.shape)
        print("vec_ampnois.shape = ", self.vec_ampnois.shape)
        print("vec_fbandsig.shape = ", self.vec_fbandsig.shape)
        print("vec_fbandint.shape = ", self.vec_fbandint.shape)

