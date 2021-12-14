import pack_control
from pack_control import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль управления программой (L1)")
    print("Модуль использует пакет:", pack_control.NAME)

class Control:
    """Класс управления программой"""

    def __init__(self, model, train):
        # основные модули программы
        self.model = model
        self.train = train
        # модули управления программой
        self.obj_set = pack_control.settings.All_settings(1)
        self.obj_file = file_io.File_IO(1)
        # вывод и сохранение результатов
        self.calc_save = []
        self.calc_info = []

    def set(self):
        # инициализация модуля управления (L1)
        list_set = self.obj_set.get()
        self.calc_save = list_set[5][9]
        self.calc_info = list_set[5][10]
        # инициализация основных модулей (L1)
        self.model.set(list_set)
        self.train.set(list_set)
        # инициализация модулей управления (L2)
        self.obj_file.set(list_set[5])

    def print(self):
        print("Параметры модуля управления (L1):")
        self.obj_set.print()
        self.obj_file.print()

    def mode_static(self, id_script):
        # расчёт диаграммы направленности
        self.model.calc_out(id_script)
        self.print_calc()

    def mode_dynamic1nd(self, id_script):
        # расчёт временных характеристик
        self.model.calc_out(id_script)
        self.print_calc()
        self.save_learn()

    def mode_dynamic2nd(self, id_script):
        # расчёт усреднённых характеристик
        self.model.calc_out(id_script)
        self.print_calc()

    def mode_train(self):
        # обучение нейронной сети
        self.train.calc_out()

    def mode_print(self, id_set):
        # просмотр настроек и параметров
        if id_set == 1:
            # просмотр настроек программы
            self.obj_set.print()
        if id_set == 2:
            # просмотр параметров моделей
            self.model.print()
            self.train.print()

    def print_calc(self):
        # вывод служебной информации для графика
        if self.calc_info == 1:
            self.model.print_calc()

    def save_learn(self):
        # сохранение обучающей выборки
        if self.calc_save == 1:
            self.model.save_learn(self.obj_set.get())





