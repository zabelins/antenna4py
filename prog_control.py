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
        self.obj_set = pack_control.settings.All_settings()
        self.obj_file = file_set.File_set()
        # вывод и сохранение результатов
        self.calc_save = []
        self.calc_info = []
        # выходные данные модели ААР
        self.out_data = []

    def set(self):
        # инициализация модуля управления (L1)
        list_set = self.obj_set.get()
        # инициализация основных модулей (L1)
        self.model.set(list_set)
        self.train.set(list_set)
        # инициализация модулей управления (L2)
        self.obj_file.set(list_set[5])
        # инициализация параметров
        self.calc_save = list_set[5][20]
        self.calc_info = list_set[5][21]

    def print(self):
        print("Параметры модуля управления (L1):")
        self.obj_set.print()
        self.obj_file.print()

    def mode_static(self, id_script):
        # диаграмма направленности
        self.model.calc_out(id_script)
        self.print_modelcalc()

    def mode_time(self, id_script):
        # временные характеристики
        self.model.calc_out(id_script)
        self.print_modelcalc()
        self.save_learn()

    def mode_param(self, id_script):
        # усреднённые характеристики
        self.model.calc_out(id_script)
        self.print_modelcalc()

    def mode_compar(self, id_script):
        # сравнение алгоритмов
        self.model.calc_out(id_script)
        self.print_modelcalc()

    def sync_model(self):
        # синхронизация с моделью
        self.out_data = self.model.get_data()

    def mode_samples(self):
        # подготовка обучающей выборки
        self.train.calc_out(0)
        self.print_traincalc()

    def mode_train(self, id_train):
        # обучение нейронной сети
        self.train.calc_out(1, id_train)

    def mode_print(self, id_set):
        # просмотр настроек и параметров
        if id_set == 1:
            # просмотр настроек программы
            self.obj_set.print()
        if id_set == 2:
            # просмотр параметров моделей
            self.model.print()
            self.train.print()

    def print_modelcalc(self):
        # вывод служебной информации для графика
        if self.calc_info == 1:
            self.model.print_calc()

    def print_traincalc(self):
        # вывод служебной информации для графика
        if self.calc_info == 1:
            self.train.print_calc()

    def save_learn(self):
        # сохранение обучающей выборки
        if self.calc_save == 1:
            self.model.save_learn(self.obj_set.get())

    def get_vecptn(self):
        # данные для диаграммы направленности
        res = []
        res.append(self.out_data[0][0])
        res.append(self.out_data[1][0])
        res.append(self.out_data[1][3])
        res.append(self.out_data[2][4])
        res.append(self.out_data[2][5])
        res.append(self.out_data[4][0])
        res.append(self.out_data[4][4])
        return res

    def get_vecsig(self):
        # данные для временных характеристик сигналов
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[1][0])
        res.append(self.out_data[1][1])
        res.append(self.out_data[1][2])
        res.append(self.out_data[2][4])
        return res

    def get_vecint(self):
        # данные для временных характеристик помех
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[1][3])
        res.append(self.out_data[1][4])
        res.append(self.out_data[1][5])
        res.append(self.out_data[2][5])
        return res

    def get_veccpl(self):
        # данные для временных характеристик огибающей
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[2][0])
        res.append(self.out_data[2][1])
        res.append(self.out_data[2][2])
        return res

    def get_vecadp(self):
        # данные для временных характеристик адаптации
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[2][6])
        res.append(self.out_data[3][2])
        res.append(self.out_data[3][3])
        res.append(self.out_data[4][1])
        res.append(self.out_data[4][2])
        res.append(self.out_data[4][5])
        res.append(self.out_data[4][6])
        return res

    def get_vecout(self):
        # данные для характеристик выходного сигнала
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[4][3])
        res.append(self.out_data[4][7])
        return res

    def get_vecpar(self):
        # данные для усреднённых характеристик адаптации
        res = []
        res.append(self.out_data[0][2])
        res.append(self.out_data[4][14])
        res.append(self.out_data[4][15])
        res.append(self.out_data[4][16])
        res.append(self.out_data[5][0])
        res.append(self.out_data[5][1])
        res.append(self.out_data[5][2])
        res.append(self.out_data[5][3])
        res.append(self.out_data[5][4])
        res.append(self.out_data[5][5])
        res.append(self.out_data[5][6])
        res.append(self.out_data[5][7])
        res.append(self.out_data[5][8])
        return res





