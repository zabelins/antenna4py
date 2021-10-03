import pack_train
from pack_train import *
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль модели обучения НС (L1)")
    print("Модуль использует пакет:", pack_train.NAME)

class Model_train:
    """Класс динамического моделирования адаптивной антенны"""

    def __init__(self):
        self.list_train = pack_train.train.Train(1)
        self.list_file = pack_train.file_io.File_IO(2)

    def set(self, obj_set):
        # инициализация параметров обучения НС уровня L2
        self.list_train.set(obj_set.list_settrain.get())

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры динамической модели (L1):")
        print("\t-")
        self.list_train.print()
        self.list_file.print()

    def calc_out(self):
        # загрузка файлов с обучающими выборками
        out_data = self.list_file.load_files()
        # запуск обучения нейронной сети
        self.list_train.calc_out(out_data)