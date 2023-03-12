import pack_control.pack_settings as ps
from pack_control.pack_settings import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль списка настроек программы и модели (L2)")
    print("Модуль использует пакет:", ps.NAME)

class All_settings:
    """Класс исходных параметров и настроек программы, динамической модели и НС"""

    def __init__(self):
        self.obj_parmodel = ps.par_model.Par_model()
        self.obj_parenv = ps.par_env.Par_env()
        self.obj_pararray = ps.par_array.Par_array()
        self.obj_paradapt = ps.par_adapt.Par_adapt()
        self.obj_partrain = ps.par_train.Par_train()
        self.obj_setprog = ps.set_prog.Set_prog()
        self.obj_settest = ps.set_test.Set_test()

    def get(self):
        res = []
        res.append(self.obj_parmodel.get())
        res.append(self.obj_parenv.get())
        res.append(self.obj_pararray.get())
        res.append(self.obj_paradapt.get())
        res.append(self.obj_partrain.get())
        res.append(self.obj_setprog.get())
        res.append(self.obj_settest.get())
        return res

    def print(self):
        print("Настройки программы и модели (L2):")
        print("\t-")
        self.obj_parmodel.print()
        self.obj_parenv.print()
        self.obj_pararray.print()
        self.obj_paradapt.print()
        self.obj_partrain.print()
        self.obj_setprog.print()
        self.obj_settest.print()


