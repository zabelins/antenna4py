import pack_control
from pack_control import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль управления программой (L1)")
    print("Модуль использует пакет:", pack_control.NAME)

class Control:
    """Класс загрузки исходных данных и управления программой"""

    def __init__(self, model):
        self.model = model
        self.list_set = pack_control.settings.Settings_list(1)
        self.list_file = file_io.File_IO(1)

    def set(self):
        self.model.set(self.list_set)

    def print(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ УПРАВЛЕНИЯ (L1) --- ")
        self.list_set.print_short()
        self.list_file.print_short()

    def calc_static(self):
        # вычисление статической модели адаптации
        self.model.calc_out(0)

    def calc_dynamic1nd(self, id_script):
        # вычисление динамической модели адаптации
        self.model.calc_out(id_script)

    def calc_dynamic2nd(self):
        # вычисление динамической модели адаптации
        pass

    def calc_train(self):
        # запуск обучения НС
        pass





