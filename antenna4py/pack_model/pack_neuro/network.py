import numpy as np
import tensorflow as tf

if __name__ == "__main__":
    print("Вы запустили модуль обучения НС (L3)")


class Network:
    """Класс модуль обучения НС"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры модуля обучения НС (L3):")
        print("\t-")

    def calc_out(self, out_sampling):
        # распаковка исходных данных
        vec_inamp, vec_inphi = out_sampling[0], out_sampling[1]
        vec_outamp, vec_outphi = out_sampling[2], out_sampling[3]
        matrix_inamp, matrix_inphi = out_sampling[4], out_sampling[5]
        #print("pp vec_inamp.shape", vec_inamp.shape)

    def print_out(self):
        pass
