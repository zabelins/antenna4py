import pack_view.pack_graph as pg
from pack_view.pack_graph import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода графика (L2)")
    print("Модуль использует пакет:", pg.NAME)

class Graph:
    """Класс вывода графиков для пользователя"""

    def __init__(self):
        self.obj_ptn = pg.pattern.Pattern()
        self.obj_sig = pg.signals.Signals()
        self.obj_par = pg.param.Parameter()

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры вывода графика (L2):")
        print("\t-")
        self.obj_ptn.print()
        self.obj_sig.print()
        self.obj_par.print()

    def draw_ptn(self, data, time):
        # распаковка исходных данных
        vec_deg, vec_sigdeg, vec_intdeg = data[0][0], data[0][1][time], data[0][2][time]
        vec_eqsigdeg, vec_eqintdeg = data[0][3][time], data[0][4][time]
        # инициализация векторов
        x_deg = np.ones(shape=[len(data) + 1, vec_deg.shape[0]])
        y_pow = np.ones(shape=[len(data) + 1, vec_deg.shape[0]])
        # цикл по моделированиям
        for item in range(len(data)):
            vec_inptn, vec_outptn = data[0][5][time], data[item][6][time]
            x_deg[0], x_deg[item+1] = vec_deg, vec_deg
            y_pow[0], y_pow[item+1] = vec_inptn, vec_outptn
        # подписи графиков
        str_pattern = ["init", "alg 1", "alg 2", "alg 3", "alg 4", "alg 5"]
        # отрисовка графиков
        self.obj_ptn.draw_graph(x_deg, y_pow, vec_sigdeg, vec_intdeg, vec_eqsigdeg, vec_eqintdeg, str_pattern)

    def draw_input(self, data, type_graph):
        # распаковка исходных данных
        vec_time, x_time, y_amp, y_deg, y_band = data[0][0], [], [], [], []
        # цикл по моделированиям
        for item in range(len(data)):
            # распаковка исходных данных
            vec_deg, vec_amp = data[item][1].T, data[item][2].T
            vec_band, vec_eqdeg = data[item][3].T, data[item][4]
            # цикл по количеству сигналов
            for i in range(vec_amp.shape[0]):
                x_time.append(vec_time)
                y_amp.append(vec_amp[i])
                y_deg.append(vec_deg[i])
                y_band.append(vec_band[i])
        # подписи графиков
        if type_graph == 0:
            str_input = ["sig 1", "sig 2", "sig 3", "sig 4", "sig 5", "sig 6", "sig 7", "sig 8", "sig 9", "sig 10"]
        elif type_graph == 1:
            str_input = ["int 1", "int 2", "int 3", "int 4", "int 5", "int 6", "int 7", "int 8", "int 9", "int 10"]
        # отрисовка графиков
        self.obj_sig.draw_graph_in(x_time, y_amp, y_deg, y_band, str_input, type_graph)

    def draw_cpl(self, data):
        # распаковка исходных данных
        vec_time, x_time0, y_sig, x_time1, y_int, x_time2, y_sum = data[0][0], [], [], [], [], [], []
        # цикл по моделированиям
        for item in range(len(data)):
            # распаковка исходных данных
            vec_sig, vec_int, vec_sum = data[item][1].T, data[item][2].T, data[item][3].T
            # цикл по количеству сигналов
            for i in range(vec_sig.shape[0]):
                x_time0.append(vec_time)
                y_sig.append(np.real(vec_sig[i]))
            for i in range(vec_int.shape[0]):
                x_time1.append(vec_time)
                y_int.append(np.real(vec_int[i]))
            for i in range(vec_sum.shape[0]):
                x_time2.append(vec_time)
                y_sum.append(np.real(vec_sum[i]))
        # подписи графиков
        str_sig = ["sig 1", "sig 2", "sig 3", "sig 4", "sig 5", "sig 6", "sig 7", "sig 8", "sig 9", "sig 10", "sig 11"]
        str_int = ["int 1", "int 2", "int 3", "int 4", "int 5", "int 6", "int 7", "int 8", "int 9", "int 10", "int 11"]
        str_sum = ["sum 1", "sum 2", "sum 3", "sum 4", "sum 5", "sum 6", "sum 7", "sum 8", "sum 9", "sum 10", "sum 11"]
        # отрисовка графиков
        self.obj_sig.draw_graph_cpl(x_time0, y_sig, x_time1, y_int, x_time2, y_sum, str_sig, str_int, str_sum)

    def draw_adp(self, data):
        # распаковка исходных данных
        vec_time, vec_snir, vec_insnir = data[0][0], data[0][1], data[0][2]
        x_time0, y_dpt, x_time1, y_atn, x_time2, y_snir = [], [], [], [], [vec_time], [vec_insnir]
        # цикл по моделированиям
        for item in range(len(data)):
            # распаковка исходных данных
            vec_insnir, vec_indpt, vec_inatn = data[item][2], data[item][4].T, data[item][5].T
            vec_outsnir, vec_outdpt, vec_outatn = data[item][3], data[item][6].T, data[item][7].T
            # цикл по количеству помех
            for i in range(vec_indpt.shape[0]):
                x_time0.append(vec_time)
                y_dpt.append(vec_outdpt[i] - vec_indpt[i])
            # цикл по количеству сигналов
            for i in range(vec_inatn.shape[0]):
                x_time1.append(vec_time)
                y_atn.append(vec_outatn[i] - vec_inatn[i])
            x_time2.append(vec_time)
            y_snir.append(vec_outsnir)
        # подписи графиков
        str_depth = ["int 1", "int 2", "int 3", "int 4", "int 5", "int 6", "int 7", "int 8", "int 9", "int 10"]
        str_atten = ["sig 1", "sig 2", "sig 3", "sig 4", "sig 5", "sig 6", "sig 7", "sig 8", "sig 9", "sig 10"]
        str_snir = ["init", "alg 1", "alg 2", "alg 3", "alg 4", "alg 5"]
        # отрисовка графиков
        self.obj_sig.draw_graph_adp(x_time0, y_dpt, x_time1, y_atn, x_time2, y_snir, str_depth, str_atten, str_snir)

    def draw_out(self, data):
        # распаковка исходных данных
        vec_time, vec_insignal = data[0][0], data[0][1].T
        x_time, y_out = [vec_time], [np.real(vec_insignal[0])]
        # цикл по моделированиям
        for item in range(len(data)):
            # распаковка исходных данных
            vec_outsignal = data[item][2].T
            # выходные сигналы
            x_time.append(vec_time)
            y_out.append(np.real(vec_outsignal[0]))
        # подписи графиков
        str_output = ["init", "SMI", "LSTM", "alg 3", "alg 4", "alg 5"]
        # отрисовка графиков
        self.obj_sig.draw_graph_out(x_time, y_out, str_output)

    def draw_par(self, data, id_script):
        # распаковка исходных данных
        vec_par, vec_inber, vec_insnir = data[0][0], data[0][7], data[0][8]
        x_par0, y_dpt, x_par1, y_atn, x_par2, y_snir, x_par3, y_ber = [], [], [], [], [vec_par], [vec_insnir], [vec_par], [vec_inber]
        x_snir = [vec_insnir]
        # цикл по моделированиям
        for item in range(len(data)):
            # распаковка исходных данных
            vec_indpt, vec_inatn, vec_insnir = data[item][5].T, data[item][6].T, data[item][8]
            vec_outdpt, vec_outatn, vec_outber, vec_outsnir = data[item][9].T, data[item][10].T, data[item][11], data[item][12]
            # подавление помехи
            x_par0.append(vec_par)
            y_dpt.append(vec_outdpt[0] - vec_indpt[0])
            # ослабление сигнала
            x_par1.append(vec_par)
            y_atn.append(vec_outatn[0] - vec_inatn[0])
            # осшп
            x_par2.append(vec_par)
            y_snir.append(vec_outsnir)
            # битовая ошибка
            x_par3.append(vec_par)
            x_snir.append(vec_insnir)
            y_ber.append(vec_outber)
        # подписи графиков
        str_mean = ["SMI", "LSTM", "alg 3", "alg 4", "alg 5", "alg 6"]
        str_snir = ["init", "SMI", "LSTM", "alg 3", "alg 4", "alg 5"]
        # отрисовка графиков
        self.obj_par.draw_graph(x_par0, y_dpt, x_par1, y_atn, x_par2, y_snir, str_mean, str_snir, id_script)
        self.obj_par.draw_ber(x_snir, y_ber, str_snir, id_script)

    def get_amp2db(self, num):
        # перевод амплитуды в децибеллы
        return 20 * np.log10(abs(num))

    def get_pow2db(self, num):
        # перевод мощности в децибеллы
        return 10 * np.log10(abs(num))

