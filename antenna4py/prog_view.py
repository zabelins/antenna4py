import pack_view
from pack_view import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода информации (L1)")
    print("Модуль использует пакет:", pack_view.NAME)

class View:
    """Класс вывода информации для пользователя"""

    def __init__(self, controller, model, train):
        # основные модули программы
        self.controller = controller
        self.model = model
        self.train = train
        # модули вывода информации
        self.obj_graph = pack_view.graph.Graph(1)
        self.obj_client = pack_view.client.Client(1)
        self.obj_report = pack_view.report.Report(1)
        # выходные данные модели ААР
        self.out_data = []

    def set(self):
        # инициализация модуля управления (L1)
        self.controller.set()
        list_set = self.controller.obj_set.get()
        # инициализация модулей вывода информации (L2)
        self.obj_graph.set(list_set[5])
        self.obj_client.set(list_set[5])
        self.obj_report.set(list_set[5])
        # инициализация модулей вывода информации (L3)
        self.obj_graph.obj_pattern.set(list_set[5])
        self.obj_graph.obj_signals.set(list_set[5])
        self.obj_graph.obj_output.set(list_set[5])
        self.obj_graph.obj_adapt.set(list_set[5])

    def print(self):
        print("Параметры модуля представления (L1):")
        self.obj_graph.print()
        self.obj_client.print()
        self.obj_report.print()

    def start_prog(self):
        # инициализируем числовую модель
        self.set()
        # выбор режима расчёта
        input_buf = self.obj_client.input_mode()
        self.obj_client.print_namemode(input_buf)
        # запуск выбранного режима
        if input_buf == 1:
            # расчёт диаграммы направленности
            self.mode_static()
        elif input_buf == 2:
            # расчёт временных характеристик
            self.mode_dynamic1nd()
        elif input_buf == 3:
            # расчёт усреднённых характеристик
            self.mode_dynamic2nd()
        elif input_buf == 4:
            # обучение нейронной сети
            self.mode_train()
        elif input_buf == 5:
            # просмотр исходных настроек программы
            self.controller.mode_print(1)
        elif input_buf == 6:
            # просмотр параметров модели
            self.controller.mode_print(2)
        elif input_buf == 7:
            # просмотр параметров графиков
            self.obj_graph.print()

    def mode_static(self):
        # режим расчёта диаграммы направленности
        self.controller.mode_static(0)
        # синхронизация с моделью
        self.sync_model()
        # вывод информации о ДН
        self.info_pattern()
        # вывод графика ДН
        self.show_pattern()

    def mode_dynamic1nd(self):
        # режим расчёта временных характеристик ААР (1 параметр)
        # выбор сценария моделирования
        id_script = self.obj_client.input_script()
        # расчёт модели
        self.controller.mode_dynamic1nd(id_script)
        # синхронизация с моделью
        self.sync_model()
        # вывод информации о ДН
        self.info_pattern()
        # вывод информации об адаптации
        self.info_adapt()
        # вывод графика ДН
        self.show_pattern()
        # вывод графика характеристик сигналов и помех
        self.show_signals()
        # вывод графика характеристик адаптации
        self.show_adapt()
        # вывод графика характеристик выходного сигнала
        self.show_output()

    def mode_dynamic2nd(self):
        # режим расчёта временных характеристик ААР (N параметров)
        self.controller.mode_dynamic2nd(8)
        # синхронизация с моделью
        self.sync_model()
        # вывод информации о ДН
        self.info_pattern()
        # вывод информации об адаптации
        self.info_adapt()
        # вывод информации об адаптации
        self.info_mean()
        # вывод графика ДН
        self.show_pattern()
        # вывод графика характеристик сигналов и помех
        self.show_signals()
        # вывод графика характеристик адаптации
        self.show_adapt()
        # вывод графика характеристик выходного сигнала
        self.show_output()
        # вывод графика усреднённых характеристик адаптации
        self.show_mean()

    def mode_train(self):
        # обучение нейронной сети
        self.controller.mode_samples()
        # выбор сценария моделирования
        id_train = self.obj_client.input_train()
        # обучение нейронной сети
        self.controller.mode_train(id_train)

    def sync_model(self):
        # синхронизация с моделью
        self.out_data = self.model.get_data()

    def show_pattern(self):
        # вывод графика диаграммы направленности
        vec = self.get_vecpattern()
        self.obj_graph.draw_pattern(vec, 0)

    def show_signals(self):
        # вывод графиков временных характеристик сигналов
        vec = self.get_vecsignals()
        self.obj_graph.draw_signals(vec)

    def show_adapt(self):
        # вывод графиков временных характеристик адаптации
        vec = self.get_vecadapt()
        self.obj_graph.draw_adapt(vec)

    def show_output(self):
        # вывод графиков характеристик выходного сигнала
        vec = self.get_vecoutput()
        self.obj_graph.draw_output(vec)

    def show_mean(self):
        # вывод графиков усреднённых характеристик адаптации
        vec = self.get_vecmean()
        self.obj_graph.draw_mean(vec)

    def info_pattern(self):
        # вывод информации о диаграмме направленности
        vec_adapt = self.get_vecadapt()
        self.obj_report.info_pattern(vec_adapt, 0)

    def info_adapt(self):
        # вывод информации об адаптации
        vec_mean = self.get_vecmean()
        self.obj_report.info_adapt(vec_mean)

    def info_mean(self):
        # вывод информации об адаптации
        vec_mean = self.get_vecmean()
        self.obj_report.info_mean(vec_mean)

    def get_vecpattern(self):
        # получить вектора для диаграммы направленности
        res = []
        res.append(self.out_data[0][0])
        res.append(self.out_data[1][0])
        res.append(self.out_data[1][3])
        res.append(self.out_data[2][1])
        res.append(self.out_data[2][2])
        res.append(self.out_data[4][0])
        res.append(self.out_data[4][4])
        return res

    def get_vecsignals(self):
        # получить вектора для временных характеристик сигналов
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[1][0])
        res.append(self.out_data[1][1])
        res.append(self.out_data[1][2])
        res.append(self.out_data[1][3])
        res.append(self.out_data[1][4])
        res.append(self.out_data[1][5])
        res.append(self.out_data[2][1])
        res.append(self.out_data[2][2])
        return res

    def get_vecadapt(self):
        # получить вектора для временных характеристик адаптации
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[4][1])
        res.append(self.out_data[4][2])
        res.append(self.out_data[3][3])
        res.append(self.out_data[4][5])
        res.append(self.out_data[4][6])
        res.append(self.out_data[3][4])
        res.append(self.out_data[2][3])
        return res

    def get_vecoutput(self):
        # получить вектора для характеристик выходного сигнала
        res = []
        res.append(self.out_data[0][1])
        res.append(self.out_data[4][3])
        res.append(self.out_data[4][7])
        return res

    def get_vecmean(self):
        # получить вектора для усреднённых характеристик адаптации
        res = []
        res.append(self.out_data[0][2])
        res.append(self.out_data[5][1])
        res.append(self.out_data[5][2])
        res.append(self.out_data[5][3])
        res.append(self.out_data[5][4])
        res.append(self.out_data[5][5])
        res.append(self.out_data[5][6])
        res.append(self.out_data[5][0])
        return res





