# модуль управления программой

import pack_control
from pack_control import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль управления программой (L1)")
    print("Модуль использует пакет:", pack_control.NAME)

class Control:
    """Класс загрузки исходных данных и управления программой"""

    def __init__(self, id_control, id_view, id_model, mode):
        self.id_control = id_control
        self.id_view = id_view
        self.id_model = id_model
        self.mode = mode
        self.list_set = pack_control.settings.Settings_list(1)
        self.list_file = file_io.File_IO(1)

    def get(self):
        res = []
        res.append(self.id_control)
        res.append(self.id_view)
        res.append(self.id_model)
        res.append(self.mode)
        return res

    def print(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ УПРАВЛЕНИЯ (L1) --- ")
        print("id_control = ", self.id_control)
        print("id_view = ", self.id_view)
        print("id_model = ", self.id_model)
        print("mode = ", self.mode)
        self.list_set.print_short()
        self.list_file.print_short()

    def print_short(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ УПРАВЛЕНИЯ (L1) --- ")
        print("prog_control = ", self.get())



