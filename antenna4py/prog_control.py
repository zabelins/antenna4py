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
        self.list_set = pack_control.settings.All_settings(1)
        self.list_file = file_io.File_IO(1)
        self.id_print = []
        self.id_save = []

    def set(self, id_print, id_save):
        self.model.set(self.list_set)
        self.id_print = id_print
        self.id_save = id_save

    def print(self):
        print("Параметры модуля управления (L1):")
        self.list_set.print()
        self.list_file.print()

    def mode_static(self):
        # расчёт диаграммы направленности
        self.model.calc_out(0)
        self.print_calc()

    def mode_dynamic1nd(self, id_script):
        # расчёт временных характеристик
        self.model.calc_out(id_script)
        self.print_calc()
        self.save_learn()

    def mode_dynamic2nd(self):
        # расчёт усреднённых характеристик
        self.model.calc_out(6)
        self.print_calc()

    def mode_train(self):
        # обучение нейронной сети
        pass

    def mode_print(self, id_set):
        # просмотр настроек и параметров
        if id_set == 1:
            # просмотр настроек программы
            self.list_set.print()
        if id_set == 2:
            # просмотр параметров модели
            self.model.print()

    def print_calc(self):
        # вывод служебной информации для графика
        if self.id_print == 1:
            self.model.print_calc()

    def save_learn(self):
        # сохранение обучающей выборки
        if self.id_save == 1:
            self.model.save_learn()





