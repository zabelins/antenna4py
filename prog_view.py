import pack_view
from pack_view import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода информации (L1)")
    print("Модуль использует пакет:", pack_view.NAME)

class View:
    """Класс вывода информации для пользователя"""

    def __init__(self, controller):
        # основные модули программы
        self.controller = controller
        # модули вывода информации
        self.obj_graph = pack_view.graph.Graph()
        self.obj_client = pack_view.client.Client()
        self.obj_report = pack_view.report.Report()
        # параметры отображения
        self.view_ptn = []
        self.view_sig = []
        self.view_int = []
        self.view_cpl = []
        self.view_adp = []
        self.view_out = []
        self.view_par = []

    def set(self):
        # инициализация модуля управления (L1)
        self.controller.set()
        list_set = self.controller.obj_set.get()
        # инициализация модулей вывода информации (L2)
        self.obj_graph.set(list_set[5])
        self.obj_client.set(list_set[5])
        self.obj_report.set(list_set[5])
        # инициализация модулей вывода информации (L3)
        self.obj_graph.obj_ptn.set(list_set[5])
        self.obj_graph.obj_sig.set(list_set[5], list_set[0])
        self.obj_graph.obj_par.set(list_set[5])
        # инициализация параметров отображения
        self.view_ptn = list_set[5][2]
        self.view_sig = list_set[5][3]
        self.view_int = list_set[5][4]
        self.view_cpl = list_set[5][5]
        self.view_adp = list_set[5][6]
        self.view_out = list_set[5][7]
        self.view_par = list_set[5][8]

    def print(self):
        print("Параметры модуля представления (L1):")
        self.obj_graph.print()
        self.obj_client.print()
        self.obj_report.print()

    def start_prog(self):
        # инициализируем числовую модель
        self.set()
        # выбор режима расчёта
        input_buf = self.obj_client.menu_main()
        # запуск выбранного режима
        if input_buf == 1:
            # диаграмма направленности
            self.mode_static()
        elif input_buf == 2:
            # временные характеристики
            self.mode_time()
        elif input_buf == 3:
            # усреднённые характеристики
            self.mode_param()
        elif input_buf == 4:
            # сравнение алгоритмов
            self.mode_compar()
        elif input_buf == 5:
            # обучение нейросети
            self.mode_train()
        elif input_buf == 6:
            # настройки программы
            self.controller.mode_print(1)
        elif input_buf == 7:
            # параметры модели
            self.controller.mode_print(2)
        elif input_buf == 8:
            # параметры графиков
            self.obj_graph.print()

    def mode_static(self):
        # расчёт диаграммы направленности
        self.controller.mode_static(0)
        # синхронизация с моделью
        self.sync_model()
        # вывод информации о ДН
        self.info_ptn()
        # вывод графика ДН
        self.show_ptn()

    def mode_time(self):
        # расчёт временных характеристик ААР (1 параметр)
        # выбор сценария моделирования
        id_script = self.obj_client.menu_time()
        # расчёт модели
        self.controller.mode_time(id_script)
        # синхронизация с моделью
        self.sync_model()
        # вывод информации о ДН
        self.info_ptn()
        # вывод информации об адаптации
        self.info_adp()
        # вывод графика ДН
        self.show_ptn()
        # вывод графика входных сигналов
        self.show_sig()
        # вывод графика входных помех
        self.show_int()
        # вывод графика комплексной огибающей
        self.show_cpl()
        # вывод графика характеристик адаптации
        self.show_adp()
        # вывод графика характеристик выходного сигнала
        self.show_out()

    def mode_param(self):
        # расчёт временных характеристик ААР (N параметров)
        # выбор сценария моделирования
        id_script = self.obj_client.menu_par()
        # расчёт модели
        self.controller.mode_param(id_script)
        # синхронизация с моделью
        self.sync_model()
        # вывод информации о ДН
        self.info_ptn()
        # вывод информации об адаптации
        self.info_adp()
        # вывод информации об адаптации
        self.info_par()
        # вывод графика ДН
        self.show_ptn()
        # вывод графика характеристик сигналов
        self.show_sig()
        # вывод графика характеристик помех
        self.show_int()
        # вывод графика комплексной огибающей
        self.show_cpl()
        # вывод графика характеристик адаптации
        self.show_adp()
        # вывод графика характеристик выходного сигнала
        self.show_out()
        # вывод графика усреднённых характеристик адаптации
        self.show_par(id_script)

    def mode_compar(self):
        # сравнение алгоритмов
        id_mode = 2
        if id_mode == 0:
            # сравнение диаграмм направленности
            self.show_compar_ptn()
        if id_mode == 1:
            # сравнение временных графиков
            self.show_compar_time()
        if id_mode == 2:
            # сравнение параметрических графиков
            self.show_compar_par()

    def mode_train(self):
        # обучение нейронной сети
        self.controller.mode_samples()
        # выбор сценария моделирования
        id_train = self.obj_client.input_train()
        # обучение нейронной сети
        self.controller.mode_train(id_train)

    def sync_model(self):
        # синхронизация контроллера с моделью
        self.controller.sync_model()

    def show_ptn(self):
        # вывод графика диаграммы направленности
        if self.view_ptn == 1:
            vec = [self.controller.get_vecptn()]
            self.obj_graph.draw_ptn(vec, 0)

    def show_sig(self):
        # вывод графиков временных характеристик сигналов
        if self.view_sig == 1:
            vec = [self.controller.get_vecsig()]
            self.obj_graph.draw_input(vec, 0)

    def show_int(self):
        # вывод графиков временных характеристик помех
        if self.view_int == 1:
            vec = [self.controller.get_vecint()]
            self.obj_graph.draw_input(vec, 1)

    def show_cpl(self):
        # вывод графиков временных характеристик огибающей
        if self.view_cpl == 1:
            vec = [self.controller.get_veccpl()]
            self.obj_graph.draw_cpl(vec)

    def show_adp(self):
        # вывод графиков временных характеристик адаптации
        if self.view_adp == 1:
            vec = [self.controller.get_vecadp()]
            self.obj_graph.draw_adp(vec)

    def show_out(self):
        # вывод графиков характеристик выходного сигнала
        if self.view_out == 1:
            vec = [self.controller.get_vecout()]
            self.obj_graph.draw_out(vec)

    def show_par(self, id_script):
        # вывод графиков усреднённых характеристик адаптации
        if self.view_par == 1:
            vec = [self.controller.get_vecpar()]
            self.obj_graph.draw_par(vec, id_script)

    def show_compar_ptn(self):
        # сравнение диаграмм направленности
        # первый расчёт модели
        self.controller.mode_static(0)
        self.sync_model()
        vec = [self.controller.get_vecptn()]
        # изменение параметра
        self.controller.model.obj_proc.obj_trad.alg_crit = 1
        # второй расчёт модели
        self.controller.mode_static(0)
        self.sync_model()
        vec.append(self.controller.get_vecptn())
        # вывод графиков сравнения
        self.obj_graph.draw_ptn(vec, 0)

    def show_compar_time(self):
        # сравнение временных графиков
        # первый расчёт модели
        self.controller.mode_compar(1)
        self.sync_model()
        vec = [self.controller.get_vecadp()]
        # изменение параметра
        self.controller.model.obj_proc.obj_trad.alg_crit = 1
        # второй расчёт модели
        self.controller.mode_compar(1)
        self.sync_model()
        vec.append(self.controller.get_vecadp())
        # вывод графиков сравнения
        self.obj_graph.draw_adp(vec)

    def show_compar_par(self):
        # сравнение параметрических графиков
        # первый расчёт модели
        self.controller.mode_compar(7)
        self.sync_model()
        vec = [self.controller.get_vecpar()]
        # изменение параметра
        self.controller.model.obj_proc.alg_type = 1
        # второй расчёт модели
        self.controller.mode_compar(7)
        self.sync_model()
        vec.append(self.controller.get_vecpar())
        # вывод графиков сравнения
        self.obj_graph.draw_par(vec, 7)

    def info_ptn(self):
        # вывод информации о диаграмме направленности
        vec_adapt = self.controller.get_vecadp()
        self.obj_report.info_ptn(vec_adapt, 0)

    def info_adp(self):
        # вывод информации об адаптации
        vec_par = self.controller.get_vecpar()
        self.obj_report.info_time(vec_par)

    def info_par(self):
        # вывод информации об адаптации
        vec_par = self.controller.get_vecpar()
        self.obj_report.info_par(vec_par)







