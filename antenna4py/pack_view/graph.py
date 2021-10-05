import pack_view.pack_graph as pg
from pack_view.pack_graph import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода графика (L2)")
    print("Модуль использует пакет:", pg.NAME)

class Graph:
    """Класс вывода графиков для пользователя"""

    def __init__(self, id):
        self.id = id
        self.list_pattern = pg.pattern.Pattern(1)
        self.list_signals = pg.signals.Signals(1)
        self.list_adapt = pg.adapt.Adapt(1)
        self.animation = []

    def set(self, init):
        self.animation = init[12]

    def get(self):
        res = []
        res.append(self.animation)
        return res

    def print(self):
        print("Параметры вывода графика (L2):")
        print("\tanimation = ", self.animation)
        self.list_pattern.print()
        self.list_signals.print()
        self.list_adapt.print()

    def draw_pattern(self, vec, time):
        # распаковка исходных данных
        vec_pattern, vec_sigdeg, vec_intdeg = vec[0], vec[1], vec[2]
        vec_eqdegsig, vec_eqdegint = vec[3], vec[4]
        vec_inpattern, vec_outpattern = vec[5], vec[6]
        # формируем вектора x и y
        x = np.array([vec_pattern, vec_pattern])
        y = np.array([vec_inpattern[time], vec_outpattern[time]])
        # подписи графиков
        str_legend = ["исходная ДН", "оптимальная ДН"]
        # отрисовка графиков
        self.list_pattern.draw_graph(x, y, vec_sigdeg[time], vec_intdeg[time], vec_eqdegsig[time], vec_eqdegint[time], str_legend)

    def draw_signals(self, vec):
        # распаковка исходных данных
        vec_time, vec_sigdeg, vec_sigamp, vec_sigband = vec[0], vec[1].T, vec[2].T, vec[3].T
        vec_intdeg, vec_intamp, vec_intband = vec[4].T, vec[5].T, vec[6].T
        vec_eqdegsig, vec_eqdegint = vec[7], vec[8]
        # инициализируем вектора
        len_int, len_sig = vec_intamp.shape[0], vec_sigamp.shape[0]
        x1, y1_amp, y1_deg, y1_band = [], [], [], []
        x2, y2_amp, y2_deg, y2_band = [], [], [], []
        # формируем вектора x и y для помех
        for i in range(len_int):
            x1.append(vec_time)
            y1_amp.append(vec_intamp[i])
            y1_deg.append(vec_intdeg[i])
            y1_band.append(vec_intband[i])
        # формируем вектора x и y для сигналов
        for i in range(len_sig):
            x2.append(vec_time)
            y2_amp.append(vec_sigamp[i])
            y2_deg.append(vec_sigdeg[i])
            y2_band.append(vec_sigband[i])
        # подписи графиков
        signals_strleg = ["сигнал 1", "сигнал 2", "сигнал 3", "сигнал 4", "сигнал 5"]
        # отрисовка графиков
        self.list_signals.draw_graph(x1, y1_amp, y1_deg, y1_band, signals_strleg)
        #self.list_signals.draw_graph(x2, y2_amp, y2_deg, y2_band, signals_strleg)

    def draw_adapt(self, vec):
        # распаковка исходных данных
        vec_time, vec_indepth, vec_inatten, vec_insnir = vec[0], vec[1].T, vec[2].T, vec[3]
        vec_outdepth, vec_outatten, vec_outsnir, vec_snir = vec[4].T, vec[5].T, vec[6], vec[7]
        # инициализируем вектора
        len_sig, len_int = vec_inatten.shape[0], vec_indepth.shape[0]
        x1, y_depth, x2, y_atten, x3, y_snir = [], [], [], [], [], []
        # формируем вектора x и y для глубины подавления
        for i in range(len_int):
            x1.append(vec_time)
            y_depth.append(vec_outdepth[i] - vec_indepth[i])
        # формируем вектора x и y для ослабления сигнала
        for i in range(len_sig):
            x2.append(vec_time)
            y_atten.append(vec_outatten[i] - vec_inatten[i])
        # формируем вектора x и y для осшп
        x3 = [vec_time, vec_time]
        y_snir = [vec_insnir, vec_outsnir]
        # подписи графиков
        leg_depth = ["помеха 1", "помеха 2", "помеха 3", "помеха 4", "помеха 5"]
        leg_atten = ["сигнал 1", "сигнал 2", "сигнал 3", "сигнал 4", "сигнал 5"]
        leg_snir = ["осшп исх.", "осшп опт."]
        # отрисовка графиков
        self.list_adapt.draw_graph(x1, y_depth, x2, y_atten, x3, y_snir, leg_depth, leg_atten, leg_snir, 0)

    def draw_mean(self, vec):
        # распаковка исходных данных
        vec_var, vec_meanindepth, vec_meaninatten, vec_meaninsnir = vec[0], vec[1], vec[2], vec[3]
        vec_meanoutdepth, vec_meanoutatten, vec_meanoutsnir = vec[4], vec[5], vec[6]
        # подавление помехи
        x1 = [vec_var]
        y_depth = vec_meanoutdepth - vec_meanindepth
        # ослабление сигнала
        x2 = [vec_var]
        y_atten = vec_meanoutatten - vec_meaninatten
        # осшп
        x3 = [vec_var, vec_var]
        y_snir = [vec_meaninsnir, vec_meanoutsnir]
        # коррекция
        y_depth = y_depth.T
        y_atten = y_atten.T
        # подписи графиков
        leg_depth = ["помеха 1", "помеха 2", "помеха 3", "помеха 4", "помеха 5"]
        leg_atten = ["сигнал 1", "сигнал 2", "сигнал 3", "сигнал 4", "сигнал 5"]
        leg_snir = ["осшп исх.", "осшп опт."]
        # отрисовка графиков
        self.list_adapt.draw_graph(x1, y_depth, x2, y_atten, x3, y_snir, leg_depth, leg_atten, leg_snir, 1)

    def get_amp2db(self, num):
        # перевод амплитуды в децибеллы
        return 20 * np.log10(abs(num))

    def get_pow2db(self, num):
        # перевод мощности в децибеллы
        return 10 * np.log10(abs(num))

