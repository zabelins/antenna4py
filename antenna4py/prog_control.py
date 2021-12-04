import pack_control
from pack_control import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль управления программой (L1)")
    print("Модуль использует пакет:", pack_control.NAME)

class Control:
    """Класс управления программой"""

    def __init__(self, model_antenna, model_train):
        self.model_antenna = model_antenna
        self.model_train = model_train
        self.list_set = pack_control.settings.All_settings(1)
        self.list_file = file_io.File_IO(1)
        # вывод и сохранение результатов
        self.calc_save = []
        self.calc_info = []

    def set(self):
        # формирование векторов параметров и настроек
        set_prog = self.list_set.list_setprog.get()
        # инициализация параметров модели уровня L1
        self.model_antenna.set(self.list_set)
        self.model_train.set(self.list_set)
        self.calc_save = set_prog[9]
        self.calc_info = set_prog[10]
        # инициализация параметров уровня L2
        self.list_file.set(set_prog)

    def print(self):
        print("Параметры модуля управления (L1):")
        self.list_set.print()
        self.list_file.print()

    def mode_static(self, id_script):
        # расчёт диаграммы направленности
        self.model_antenna.calc_out(id_script)
        self.print_calc()

    def mode_dynamic1nd(self, id_script):
        # расчёт временных характеристик
        self.model_antenna.calc_out(id_script)
        self.print_calc()
        self.save_learn()

    def mode_dynamic2nd(self, id_script):
        # расчёт усреднённых характеристик
        self.model_antenna.calc_out(id_script)
        self.print_calc()

    def mode_train(self):
        # обучение нейронной сети
        self.model_train.calc_out()

    def mode_print(self, id_set):
        # просмотр настроек и параметров
        if id_set == 1:
            # просмотр настроек программы
            self.list_set.print()
        if id_set == 2:
            # просмотр параметров модели
            self.model_antenna.print()
            self.model_train.print()

    def print_calc(self):
        # вывод служебной информации для графика
        if self.calc_info == 1:
            self.model_antenna.print_calc()

    def save_learn(self):
        # сохранение обучающей выборки
        if self.calc_save == 1:
            self.model_antenna.save_learn()





