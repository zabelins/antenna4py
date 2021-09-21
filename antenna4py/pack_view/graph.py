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
        self.animation = []
        self.list_pattern = pg.pattern.Pattern(1)
        self.list_timefreq = pg.timefreq.TimeFreq(1)
        self.list_charact = pg.charact.Charact(1)

    def set(self, init):
        self.animation = init[19]

    def get(self):
        res = []
        res.append(self.animation)
        return res

    def print(self):
        print("Параметры вывода графика (L2):")
        print("\tanimation = ", self.animation)
        self.list_pattern.print()
        self.list_charact.print()
        self.list_timefreq.print()

    def draw_pattern(self, vec):
        # распаковка исходных данных
        vec_pattern, vec_sigdeg, vec_intdeg = vec[0], vec[1], vec[2]
        vec_eqdegsig, vec_eqdegint = vec[3], vec[4]
        vec_inpattern, vec_outpattern = vec[5], vec[6]
        # отобразить диаграмму направленности
        time = 0
        deg = vec_intdeg.T
        x = np.array([vec_pattern, vec_pattern])
        y = np.array([vec_inpattern[time], vec_outpattern[time]])
        self.list_pattern.draw_pattern(x, y, deg[time])

    def draw_signals(self, vec):
        # распаковка исходных данных
        vec_time, vec_sigdeg, vec_sigamp, vec_sigband = vec[0], vec[1], vec[2], vec[3]
        vec_intdeg, vec_intamp, vec_intband = vec[4], vec[5], vec[6]
        vec_eqdegsig, vec_eqdegint = vec[7], vec[8]
        # вывод графика характеристик сигналов и помех
        len_intamp, x, y = vec_intamp.shape[0], [], []
        for i in range(len_intamp):
            x.append(vec_time)
            y.append(vec_intamp[i])
        self.list_timefreq.draw_time(x, y, ['amp', 'time'])
        # вывод графика характеристик сигналов и помех
        len_intdeg, x, y = vec_intdeg.shape[0], [], []
        for i in range(len_intdeg):
            x.append(vec_time)
            y.append(vec_intdeg[i])
        self.list_timefreq.draw_time(x, y, ['deg', 'time'])
        # вывод графика характеристик сигналов и помех
        len_intband, x, y = vec_intband.shape[0], [], []
        for i in range(len_intband):
            x.append(vec_time)
            y.append(vec_intband[i])
        self.list_timefreq.draw_time(x, y, ['band', 'time'])

    def draw_adapt(self, vec):
        # распаковка исходных данных
        vec_time, vec_indepth, vec_inatten, vec_insnir = vec[0], vec[1], vec[2], vec[3]
        vec_outdepth, vec_outatten, vec_outsnir = vec[4], vec[5], vec[6]
        # вывод графика характеристик адаптации
        len_sig, len_int, x, y = vec_inatten.shape[0], vec_indepth.shape[0], [], []
        for i in range(len_sig):
            x.append(vec_time)
            db_outatten = 20 * np.log10(abs(vec_outatten[i]))
            db_inatten = 20 * np.log10(abs(vec_inatten[i]))
            y.append(db_outatten - db_inatten)
        for i in range(len_int):
            x.append(vec_time)
            db_outdepth = 20 * np.log10(abs(vec_outdepth[i]))
            db_indepth = 20 * np.log10(abs(vec_indepth[i]))
            y.append(db_outdepth - db_indepth)
        self.list_charact.draw_charact(x, y, ['dp', 'time'])

    def draw_mean(self, vec):
        # распаковка исходных данных
        vec_var, vec_meanindepth, vec_meaninatten, vec_meaninsnir = vec[0], vec[1], vec[2], vec[3]
        vec_meanoutdepth, vec_meanoutatten, vec_meanoutsnir = vec[4], vec[5], vec[6]
        # вывод графика характеристик адаптации
        x, y = [], []
        # ослабление сигнала
        x.append(vec_var)
        db_outatten = 20 * np.log10(vec_meanoutatten)
        db_inatten = 20 * np.log10(vec_meaninatten)
        y.append(db_outatten - db_inatten)
        # подавление помехи
        x.append(vec_var)
        db_outdepth = 20 * np.log10(vec_meanoutdepth)
        db_indepth = 20 * np.log10(vec_meanindepth)
        y.append(db_outdepth - db_indepth)
        self.list_charact.draw_charact(x, y, ['dp', 'par'])

