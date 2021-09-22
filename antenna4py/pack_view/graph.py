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
        self.animation = init[16]

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

    def draw_pattern(self, vec):
        # распаковка исходных данных
        vec_pattern, vec_sigdeg, vec_intdeg = vec[0], vec[1], vec[2]
        vec_eqdegsig, vec_eqdegint = vec[3], vec[4]
        vec_inpattern, vec_outpattern = vec[5], vec[6]
        # формируем вектора x и y
        t = 0
        x = np.array([vec_pattern, vec_pattern])
        y = np.array([vec_inpattern[t], vec_outpattern[t]])
        # подписи графиков
        str_legend = ["исходная ДН", "оптимальная ДН"]
        # отрисовка графиков
        self.list_pattern.draw_pattern(x, y, vec_sigdeg[t], vec_intdeg[t], vec_eqdegsig[t], vec_eqdegint[t], str_legend)

    def draw_signals(self, vec):
        # распаковка исходных данных
        vec_time, vec_sigdeg, vec_sigamp, vec_sigband = vec[0], vec[1].T, vec[2].T, vec[3].T
        vec_intdeg, vec_intamp, vec_intband = vec[4].T, vec[5].T, vec[6].T
        vec_eqdegsig, vec_eqdegint = vec[7], vec[8]
        # формируем вектора x и y
        len_int, len_sig = vec_intamp.shape[0], vec_sigamp.shape[0]
        x1, y1_amp, y1_deg, y1_band = [], [], [], []
        x2, y2_amp, y2_deg, y2_band = [], [], [], []
        for i in range(len_int):
            x1.append(vec_time)
            y1_amp.append(vec_intamp[i])
            y1_deg.append(vec_intdeg[i])
            y1_band.append(vec_intband[i])
        for i in range(len_sig):
            x2.append(vec_time)
            y2_amp.append(vec_sigamp[i])
            y2_deg.append(vec_sigdeg[i])
            y2_band.append(vec_sigband[i])
        # подписи графиков
        signals_strleg = ["сигнал 1", "сигнал 2", "сигнал 3", "сигнал 4", "сигнал 5"]
        # отрисовка графиков
        self.list_signals.draw_time(x1, y1_amp, y1_deg, y1_band, signals_strleg)
        self.list_signals.draw_time(x2, y2_amp, y2_deg, y2_band, signals_strleg)

    def draw_adapt(self, vec):
        # распаковка исходных данных
        vec_time, vec_indepth, vec_inatten, vec_insnir = vec[0], vec[1], vec[2], vec[3]
        vec_outdepth, vec_outatten, vec_outsnir = vec[4], vec[5], vec[6]
        # вывод графика характеристик адаптации
        len_sig, len_int, x1, y1, x2, y2 = vec_inatten.shape[0], vec_indepth.shape[0], [], [], [], []
        for i in range(len_int):
            x1.append(vec_time)
            db_outdepth = 20 * np.log10(abs(vec_outdepth[i]))
            db_indepth = 20 * np.log10(abs(vec_indepth[i]))
            y1.append(db_outdepth - db_indepth)
        for i in range(len_sig):
            x2.append(vec_time)
            db_outatten = 20 * np.log10(abs(vec_outatten[i]))
            db_inatten = 20 * np.log10(abs(vec_inatten[i]))
            y2.append(db_outatten - db_inatten)
        # подписи графиков
        adapt_strleg = ["c1", "c2", "c3", "c4", "c5"]
        # отрисовка графиков
        self.list_adapt.draw_charact(x1, y1, x2, y2, ['dp', 'time'], adapt_strleg)

    def draw_mean(self, vec):
        # распаковка исходных данных
        vec_var, vec_meanindepth, vec_meaninatten, vec_meaninsnir = vec[0], vec[1], vec[2], vec[3]
        vec_meanoutdepth, vec_meanoutatten, vec_meanoutsnir = vec[4], vec[5], vec[6]
        # вывод графика характеристик адаптации
        x1, y1, x2, y2 = [], [], [], []
        # подавление помехи
        x1.append(vec_var)
        db_outdepth = 20 * np.log10(vec_meanoutdepth)
        db_indepth = 20 * np.log10(vec_meanindepth)
        y1.append(db_outdepth - db_indepth)
        # ослабление сигнала
        x2.append(vec_var)
        db_outatten = 20 * np.log10(vec_meanoutatten)
        db_inatten = 20 * np.log10(vec_meaninatten)
        y2.append(db_outatten - db_inatten)
        # подписи графиков
        adapt_strleg = ["c1", "c2", "c3", "c4", "c5"]
        # отрисовка графиков
        self.list_adapt.draw_charact(x1, y1, x2, y2, ['dp', 'par'], adapt_strleg)

