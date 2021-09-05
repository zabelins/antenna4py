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
    def calc_out(self, out_array, out_weight):
        len_num = out_weight[2].shape[0]
        S1_test = out_array[0].T
        Wk_test = out_weight[2].reshape((len_num,1))
        self.vec_inpattern = abs(np.dot(S1_test, Wk_test))
        #print(self.vec_inpattern.shape)
        #print(self.vec_inpattern)
        self.vec_outpattern = []
        self.vec_outdeph = []
        self.vec_outatten = []
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