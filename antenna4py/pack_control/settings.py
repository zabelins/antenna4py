import pack_control.pack_settings as ps
from pack_control.pack_settings import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль списка настроек программы и модели (L2)")
    print("Модуль использует пакет:", ps.NAME)

class All_settings:
    """Класс исходных параметров и настроек программы, динамической модели и НС"""

    def __init__(self, id):
        self.id = id
        self.list_setmodel = ps.set_model.Set_model(1)
        self.list_parenv = ps.par_env.Par_env(1)
        self.list_pararray = ps.par_array.Par_array(1)
        self.list_paradapt = ps.par_adapt.Par_adapt(1)
        self.list_settrain = ps.set_train.Set_train(1)
        self.list_setview = ps.set_view.Set_view(1)
        self.list_settest = ps.set_test.Set_test(1)

    def get(self):
        res = []
        return res

    def print(self):
        print("Настройки программы и модели (L2):")
        print("\t-")
        self.list_parenv.print()
        self.list_pararray.print()
        self.list_paradapt.print()
        self.list_setmodel.print()
        self.list_settrain.print()
        self.list_setview.print()
        self.list_settest.print()


