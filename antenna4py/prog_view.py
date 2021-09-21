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
        # вывод и сохранение результатов
        self.id_print = 1
        self.id_save = 1
        # координатная сетка для графиков
        self.vec_pattern = []
        self.vec_time = []
        self.vec_var = []
        # временные характеристики сигналов и помех
        self.vec_sigdeg = []
        self.vec_sigamp = []
        self.vec_sigband = []
        self.vec_intdeg = []
        self.vec_intamp = []
        self.vec_intband = []
        self.vec_eqdegsig = []
        self.vec_eqdegint = []
        # временные характеристики адаптации
        self.vec_inpattern = []
        self.vec_indepth = []
        self.vec_inatten = []
        self.vec_insnir = []
        self.vec_outpattern = []
        self.vec_outdepth = []
        self.vec_outatten = []
        self.vec_outsnir = []
        # параметрические характеристики адаптации
        self.vec_meanindepth = []
        self.vec_meaninatten = []
        self.vec_meaninsnir = []
        self.vec_meanoutdepth = []
        self.vec_meanoutatten = []
        self.vec_meanoutsnir = []

    def set(self):
        # инициализация контроллера и модели
        self.controller.set(self.id_print, self.id_save)
        vec_setview = self.controller.list_set.list_setview.get()
        # инициализация параметров интерфейса уровня L2
        self.list_graph.set(vec_setview)
        self.list_client.set(vec_setview)
        self.list_report.set(vec_setview)
        # инициализация параметров интерфейса уровня L3
        self.list_graph.list_pattern.set(vec_setview)
        self.list_graph.list_charact.set(vec_setview)
        self.list_graph.list_timefreq.set(vec_setview)

    def print(self):
        print("Параметры модуля представления (L1):")
        self.list_graph.print()
        self.list_client.print()
        self.list_report.print()

    def start_prog(self):
        # инициализируем числовую модель
        self.set()
        # выбор режима расчёта
        input_buf = self.list_client.input_mode()
        self.list_client.print_namemode(input_buf)
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
            self.list_graph.print()

    def mode_static(self):
        # режим расчёта диаграммы направленности
        self.controller.mode_static()
        # синхронизация с моделью
        self.sync_model()
        # вывод графика ДН
        self.show_pattern()

    def mode_dynamic1nd(self):
        # режим расчёта временных характеристик ААР (1 параметр)
        # выбор сценария моделирования
        id_script = self.list_client.input_script()
        # расчёт модели
        self.controller.mode_dynamic1nd(id_script)
        # синхронизация с моделью
        self.sync_model()
        # вывод графика ДН
        self.show_pattern()
        # вывод графика характеристик сигналов и помех
        self.show_timefreq()
        # вывод графика характеристик адаптации
        self.show_charact1nd()

    def mode_dynamic2nd(self):
        # режим расчёта временных характеристик ААР (N параметров)
        self.controller.mode_dynamic2nd()
        # синхронизация с моделью
        self.sync_model()
        # вывод графика ДН
        self.show_pattern()
        # вывод графика характеристик сигналов и помех
        self.show_timefreq()
        # вывод графика характеристик адаптации
        self.show_charact1nd()
        # вывод графика усреднённых характеристик адаптации
        self.show_charact2nd()

    def mode_train(self):
        print("\tрежим в разработке :(")

    def sync_model(self):
        # синхронизация с моделью
        out_model = self.model.get_out1nd()
        # координатные сетки
        self.vec_pattern = out_model[0][0]
        self.vec_time = out_model[0][1]
        self.vec_var = out_model[0][2]
        # временные характеристики сигналов и помех
        self.vec_sigdeg = out_model[1][0].T
        self.vec_sigamp = out_model[1][1].T
        self.vec_sigband = out_model[1][2].T
        self.vec_intdeg = out_model[1][3].T
        self.vec_intamp = out_model[1][4].T
        self.vec_intband = out_model[1][5].T
        self.vec_eqdegsig = out_model[2][1]
        self.vec_eqdegint = out_model[2][2]
        # временные характеристики адаптации
        self.vec_insnir = out_model[3][0]
        self.vec_outsnir = out_model[3][1]
        self.vec_inpattern = out_model[4][0]
        self.vec_indepth = out_model[4][1].T
        self.vec_inatten = out_model[4][2].T
        self.vec_outpattern = out_model[4][3]
        self.vec_outdepth = out_model[4][4].T
        self.vec_outatten = out_model[4][5].T
        # параметрические характеристики адаптации
        self.vec_meanindepth = out_model[5][0]
        self.vec_meaninatten = out_model[5][1]
        self.vec_meaninsnir = out_model[5][2]
        self.vec_meanoutdepth = out_model[5][3]
        self.vec_meanoutatten = out_model[5][4]
        self.vec_meanoutsnir = out_model[5][5]

    def show_pattern(self):
        # вывод графика ДН
        time = 0
        deg = self.vec_intdeg.T
        x = np.array([self.vec_pattern, self.vec_pattern])
        y = np.array([self.vec_inpattern[time], self.vec_outpattern[time]])
        self.list_graph.draw_pattern(x, y, deg[time])

    def show_timefreq(self):
        # вывод графика характеристик сигналов и помех
        len_intamp, x, y = self.vec_intamp.shape[0], [], []
        for i in range(len_intamp):
            x.append(self.vec_time)
            y.append(self.vec_intamp[i])
        self.list_graph.draw_timefreq(x, y, ['amp', 'time'])
        # вывод графика характеристик сигналов и помех
        len_intdeg, x, y = self.vec_intdeg.shape[0], [], []
        for i in range(len_intdeg):
            x.append(self.vec_time)
            y.append(self.vec_intdeg[i])
        self.list_graph.draw_timefreq(x, y, ['deg', 'time'])
        # вывод графика характеристик сигналов и помех
        len_intband, x, y = self.vec_intband.shape[0], [], []
        for i in range(len_intband):
            x.append(self.vec_time)
            y.append(self.vec_intband[i])
        self.list_graph.draw_timefreq(x, y, ['band', 'time'])

    def show_charact1nd(self):
        # вывод графика характеристик адаптации
        len_sigamp, len_intamp, x, y = self.vec_sigamp.shape[0], self.vec_intamp.shape[0], [], []
        for i in range(len_sigamp):
            x.append(self.vec_time)
            db_outatten = 20 * np.log10(abs(self.vec_outatten[i]))
            db_inatten = 20 * np.log10(abs(self.vec_inatten[i]))
            y.append(db_outatten - db_inatten)
        for i in range(len_intamp):
            x.append(self.vec_time)
            db_outdepth = 20 * np.log10(abs(self.vec_outdepth[i]))
            db_indepth = 20 * np.log10(abs(self.vec_indepth[i]))
            y.append(db_outdepth - db_indepth)
        self.list_graph.draw_charact(x, y, ['dp', 'time'])

    def show_charact2nd(self):
        # вывод графика характеристик адаптации
        x, y = [], []
        # ослабление сигнала
        x.append(self.vec_var)
        db_outatten = 20 * np.log10(self.vec_meanoutatten)
        db_inatten = 20 * np.log10(self.vec_meaninatten)
        y.append(db_outatten - db_inatten)
        # подавление помехи
        x.append(self.vec_var)
        db_outdepth = 20 * np.log10(self.vec_meanoutdepth)
        db_indepth = 20 * np.log10(self.vec_meanindepth)
        y.append(db_outdepth - db_indepth)
        self.list_graph.draw_charact(x, y, ['dp', 'par'])




