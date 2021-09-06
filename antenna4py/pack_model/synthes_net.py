# модуль модели ДОС

import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели ДОС (L2)")

class Synt_net:
    def __init__(self, id):
        self.id = id
        self.control_phistep = []
        self.control_ampstep = []
        self.vec_inpattern = []
        self.vec_outpattern = []
        self.vec_outdeph = []
        self.vec_outatten = []
        self.vec_outsnir = []
        self.vec_outsnr = []
        self.vec_outinr = []
        self.vec_outsignal = []
    def set(self, init):
        self.control_phistep = init[6]
        self.control_ampstep = init[7]
    def get(self):
        res = []
        res.append(self.id)
        res.append(self.control_phistep)
        res.append(self.control_ampstep)
        return res
    def print(self):
        print(" --- Параметры модели ДОС (L2) --- ")
        print("id = ", self.id)
        print("control_phistep = ", self.control_phistep)
        print("control_ampstep = ", self.control_ampstep)
    def print_short(self):
        print(" --- Параметры модели ДОС (L2) --- ")
        print("syntnet = ", self.get())
    def calc_out(self, out_set, out_env, out_array, out_weight):
        # распаковка исходных данных
        vec_pattern = out_set[0]
        deg_sig = out_env[0][0]
        deg_int = out_env[1][0]
        vec_test = out_array[0].T
        vec_weight1 = out_weight[2]
        vec_weight2 = out_weight[5]
        # вычисление ДН
        self.vec_inpattern = abs(np.dot(vec_test, vec_weight1))
        self.vec_outpattern = abs(np.dot(vec_test, vec_weight2))
        # вычисление глубины подавления помехи и ослабления сигнала
        len_sig, len_deg = [deg_sig.shape[0], deg_int.shape[0]]
        out_atten = np.zeros(shape=[len_sig], dtype='float64')
        out_depth = np.zeros(shape=[len_deg], dtype='float64')
        max_inpattern = self.vec_inpattern.max()
        for i in range(len_sig):
            # вычисление индексов для угла заданного сигнала
            id_sig = np.where(vec_pattern == deg_sig[i])
            # вычисление в дБ разности ДН по заданным углам
            norm_inpattern = self.vec_inpattern[id_sig] / max_inpattern
            norm_outpattern = self.vec_outpattern[id_sig] / max_inpattern
            db_inpattern = 20 * np.log10(abs(norm_inpattern))
            db_outpattern = 20 * np.log10(abs(norm_outpattern))
            out_atten[i] = db_inpattern - db_outpattern
            print(vec_pattern[id_sig])
            print(db_inpattern)
        for i in range(len_deg):
            # вычисление индексов для угла заданной помехи
            id_int = np.where(vec_pattern == deg_int[i])
            # вычисление в дБ разности ДН по заданным углам
            norm_inpattern = self.vec_inpattern[id_int] / max_inpattern
            norm_outpattern = self.vec_outpattern[id_int] / max_inpattern
            db_inpattern = 20 * np.log10(abs(norm_inpattern))
            db_outpattern = 20 * np.log10(abs(norm_outpattern))
            out_depth[i] = db_inpattern - db_outpattern
            print(vec_pattern[id_int])
        # вывод параметров
        self.vec_outdeph = out_depth
        self.vec_outatten = out_atten
        print("vec_outdeph = ", self.vec_outdeph)
        print("vec_outatten = ", self.vec_outatten)
        self.vec_outsnir = []
        self.vec_outsnr = []
        self.vec_outinr = []
        self.vec_outsignal = []
    def get_out(self):
        res = []
        res.append(self.vec_inpattern)
        res.append(self.vec_outpattern)
        res.append(self.vec_outdeph)
        res.append(self.vec_outatten)
        res.append(self.vec_outsnir)
        res.append(self.vec_outsnr)
        res.append(self.vec_outinr)
        res.append(self.vec_outsignal)
        return res