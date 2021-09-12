import pack_view
from pack_view import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода информации (L1)")
    print("Модуль использует пакет:", pack_view.NAME)

class View:
    """Класс вывода информации для пользователя"""

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.list_graph = pack_view.graph.Graph(1)
        self.list_console = pack_view.console.Console(1)
        self.list_table = pack_view.table.Table(1)
        self.vec_pattern = []
        self.vec_time = []
        self.vec_patternin = []
        self.vec_patternout = []
        self.vec_depthout = []
        self.vec_attenout = []
        self.vec_degsig = []
        self.vec_degint = []
        self.vec_eqdegsig = []
        self.vec_eqdegint = []

    def start_prog(self):
        # инициализируем числовую модель
        self.set()
        # синхронизация с моделью
        self.sync_model()
        # вывод служебной информации для графика
        self.model.print_out()
        # вывод графика ДН
        self.show_pattern()
        # вывод графика характеристик адаптации
        self.show_charact()
        # вывод графика характеристик сигналов и помех
        #self.show_timefreq()

    def set(self):
        # инициализация контроллера и модели
        self.controller.set()
        setview = self.controller.list_set.list_setview.get()
        # инициализация параметров интерфейса уровня L2
        self.list_graph.set(setview)
        self.list_console.set(setview)
        self.list_table.set(setview)
        # инициализация параметров интерфейса уровня L3
        self.list_graph.list_pattern.set(setview)
        self.list_graph.list_charact.set(setview)
        self.list_graph.list_timefreq.set(setview)

    def show_settings(self):
        # вывод настроек программы
        self.controller.list_set.print()

    def sync_model(self):
        # синхронизация с моделью
        self.controller.calc_model()
        out_model = self.model.get()
        self.vec_pattern = out_model[1]
        self.vec_time = out_model[2]
        self.vec_patternin = out_model[0][0]
        self.vec_patternout = out_model[0][1]
        self.vec_depthout = out_model[0][2].T
        self.vec_attenout = out_model[0][3].T
        self.vec_degsig = out_model[3]
        self.vec_degint = out_model[4]
        self.vec_eqdegsig = out_model[5]
        self.vec_eqdegint = out_model[6]

    def show_pattern(self):
        # вывод графика ДН
        time = 1
        x = np.array([self.vec_pattern, self.vec_pattern])
        y = np.array([self.vec_patternin[time], self.vec_patternout[time]])
        self.list_graph.draw_pattern(x, y, self.vec_degint[time])

    def show_charact(self):
        # вывод графика характеристик
        x = np.array([self.vec_time, self.vec_time, self.vec_time])
        y = np.array([self.vec_attenout[0], self.vec_depthout[0], self.vec_depthout[1]])
        self.list_graph.draw_charact(x, y, ['dp', 'time'])

    def show_timefreq(self):
        x = np.array([self.vec_time, self.vec_time])
        y = np.array([self.vec_attenout[0], self.vec_depthout[1]])
        self.list_graph.draw_timefreq(x, y, ['ampt', 'time'])

    def print(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ ВЫВОДА ИНФОРМАЦИИ (L1) --- ")
        self.list_graph.print_short()
        self.list_console.print_short()
        self.list_table.print_short()
        self.controller.print()
        self.model.print()



