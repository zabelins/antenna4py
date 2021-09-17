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
        self.list_client = pack_view.client.Client(1)
        self.list_report = pack_view.report.Report(1)
        self.vec_pattern = []
        self.vec_time = []
        self.vec_patternin = []
        self.vec_patternout = []
        self.vec_depthout = []
        self.vec_attenout = []
        self.vec_degsig = []
        self.vec_degint = []
        self.vec_ampsig = []
        self.vec_ampint = []
        self.vec_eqdegsig = []
        self.vec_eqdegint = []

    def start_prog(self):
        # инициализируем числовую модель
        self.set()
        # выбор режима расчёта
        input_buf = self.list_client.input_mode()
        self.list_client.print_namemode(input_buf)
        # запуск выбранного режима
        if input_buf == 1:
            self.static_mode()
        if input_buf == 2:
            self.dynamic_mode1nd()
        if input_buf == 3:
            self.dynamic_mode2nd()
        if input_buf == 4:
            self.train_mode()
        if input_buf == 5:
            self.settings_mode()

    def set(self):
        # инициализация контроллера и модели
        self.controller.set()
        setview = self.controller.list_set.list_setview.get()
        # инициализация параметров интерфейса уровня L2
        self.list_graph.set(setview)
        self.list_client.set(setview)
        self.list_report.set(setview)
        # инициализация параметров интерфейса уровня L3
        self.list_graph.list_pattern.set(setview)
        self.list_graph.list_charact.set(setview)
        self.list_graph.list_timefreq.set(setview)

    def static_mode(self):
        # режим расчёта диаграммы направленности
        # расчёт модели
        self.controller.calc_static()
        # синхронизация с моделью
        self.sync_model()
        # вывод служебной информации для графика
        self.model.print_out()
        # вывод графика ДН
        self.show_pattern()

    def dynamic_mode1nd(self):
        # режим расчёта временных характеристик ААР (1 параметр)
        # выбор сценария моделирования
        id_script = self.list_client.input_script()
        print("ss = ", id_script)
        # расчёт модели
        self.controller.calc_dynamic1nd(id_script)
        # синхронизация с моделью
        self.sync_model()
        # вывод служебной информации для графика
        self.model.print_out()
        # вывод графика ДН
        self.show_pattern()
        # вывод графика характеристик сигналов и помех
        self.show_timefreq()
        # вывод графика характеристик адаптации
        self.show_charact()

    def dynamic_mode2nd(self):
        # режим расчёта временных характеристик ААР (N параметров)
        print("\tрежим в разработке :(")

    def train_mode(self):
        print("\tрежим в разработке :(")

    def settings_mode(self):
        # режим просмотра настроек программы
        self.controller.list_set.print()

    def sync_model(self):
        # синхронизация с моделью
        out_model = self.model.get()
        self.vec_pattern = out_model[0]
        self.vec_time = out_model[1]
        self.vec_patternin = out_model[2][0]
        self.vec_patternout = out_model[2][1]
        self.vec_depthout = out_model[2][2].T
        self.vec_attenout = out_model[2][3].T
        self.vec_degsig = out_model[3][0]
        self.vec_degint = out_model[3][1]
        self.vec_ampsig = out_model[3][2].T
        self.vec_ampint = out_model[3][3].T
        self.vec_eqdegsig = out_model[4]
        self.vec_eqdegint = out_model[5]
        #print("self.vec_time = ", self.vec_time)
        #print("self.vec_degint = ", self.vec_degint)
        #print("self.vec_attenout = ", self.vec_attenout)
        #print("self.vec_depthout = ", self.vec_depthout)
        #print("self.vec_ampint = ", self.vec_ampint)

    def show_pattern(self):
        # вывод графика ДН
        time = 0
        x = np.array([self.vec_pattern, self.vec_pattern])
        y = np.array([self.vec_patternin[time], self.vec_patternout[time]])
        self.list_graph.draw_pattern(x, y, self.vec_degint[time])

    def show_charact(self):
        # вывод графика характеристик адаптации
        len_ampsig, len_ampint, x, y = self.vec_ampsig.shape[0], self.vec_ampint.shape[0], [], []
        for i in range(len_ampsig):
            x.append(self.vec_time)
            y.append(self.vec_attenout[i])
        for i in range(len_ampint):
            x.append(self.vec_time)
            y.append(self.vec_depthout[i])
        self.list_graph.draw_charact(x, y, ['dp', 'time'])

    def show_timefreq(self):
        # вывод графика характеристик сигналов и помех
        len_ampint, x, y = self.vec_ampint.shape[0], [], []
        for i in range(len_ampint):
            x.append(self.vec_time)
            y.append(self.vec_ampint[i])
        self.list_graph.draw_timefreq(x, y, ['ampt', 'time'])

    def print(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ ВЫВОДА ИНФОРМАЦИИ (L1) --- ")
        self.list_graph.print_short()
        self.list_client.print_short()
        self.list_report.print_short()
        self.controller.print()
        self.model.print()



