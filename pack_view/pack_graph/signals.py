import math
import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик сигналов и помех (L3)")

class Signals:
    """Класс вывода графика характеристик сигналов и помех для пользователя"""

    def __init__(self):
        # общие настройки графики
        self.graph_style = []
        self.graph_legend = []
        # параметры сигналов
        self.mean_sig = []
        self.mean_int = []
        self.mean_cpl = []
        self.mean_adp = []
        self.mean_out = []
        self.amp_coef = []
        self.time_coef = []
        # скрытые настройки графики (ms, μs)
        self.str_axis_sig = ["time [ms]", "amp [μV]", "angle [deg]", "band [Hz]"]
        self.str_axis_adp = ["time [ms]", "depth [dB]", "atten [dB]", "snir [dB]"]
        self.str_axis_out = ["time [ms]", "freq [KHz]", "amp [μV]"]
        # вектора стилей
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600', '#996600', '#996600', '#996600', '#996600']
        #self.vec_col1 = ['#00008b', '#000000', '#00008b', '#336600', '#996600', '#996600', '#996600', '#996600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.2, 1.4, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--', '-', '-', '-', '-']
        self.vec_lwd2 = [1.2, 1.2, 1.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    def set(self, init0, init1):
        self.graph_style = init0[0]
        self.graph_legend = init0[1]
        self.mean_sig = init0[10]
        self.mean_int = init0[11]
        self.mean_cpl = init0[12]
        self.mean_adp = init0[13]
        self.mean_out = init0[14]
        self.amp_coef = init0[18]
        self.time_coef = init1[4]

    def get(self):
        res = []
        res.append(self.graph_style)
        res.append(self.graph_legend)
        res.append(self.mean_sig)
        res.append(self.mean_int)
        res.append(self.mean_cpl)
        res.append(self.mean_adp)
        res.append(self.mean_out)
        res.append(self.amp_coef)
        res.append(self.time_coef)
        res.append(self.str_axis_sig)
        res.append(self.str_axis_adp)
        res.append(self.str_axis_out)
        return res

    def print(self):
        print("Параметры отображения характеристик сигналов и помех (L3):")
        print("\tgraph_style = ", self.graph_style)
        print("\tgraph_legend = ", self.graph_legend)
        print("\tmean_sig = ", self.mean_sig)
        print("\tmean_int = ", self.mean_int)
        print("\tmean_cpl = ", self.mean_cpl)
        print("\tmean_adp = ", self.mean_adp)
        print("\tmean_out = ", self.mean_out)
        print("\tamp_coef = ", self.amp_coef)
        print("\ttime_coef = ", self.time_coef)
        print("\tstr_axis_sig = ", self.str_axis_sig)
        print("\tstr_axis_adp = ", self.str_axis_adp)
        print("\tstr_axis_out = ", self.str_axis_out)

    def draw_graph_in(self, x_time, y_amp, y_deg, y_bnd, str_leg, type_graph):
        # приведение типа к float
        x_time, y_amp = self.get_float(x_time, y_amp)
        y_deg, y_bnd = self.get_float(y_deg, y_bnd)
        # корректировка сетки времени
        x_time = x_time / self.time_coef
        y_amp = y_amp / self.amp_coef
        # границы отрисовки графика
        vec_axis_amp = self.get_axes(x_time, y_amp)
        vec_axis_deg = self.get_axes(x_time, y_deg)
        vec_axis_bnd = self.get_axes(x_time, y_bnd)
        # выбор стиля графиков
        col, stl, wdt = self.get_style()
        # создаём окно с областями
        fig = plt.figure("System input", figsize=(19, 5.5))
        if type_graph == 0:
            fig.suptitle("Сигналы на входе ААР", fontsize=14, fontweight='bold')
            mean_flag = self.mean_sig
        else:
            fig.suptitle("Помехи на входе ААР", fontsize=14, fontweight='bold')
            mean_flag = self.mean_int
        ax_1 = fig.add_subplot(1, 3, 1)
        ax_2 = fig.add_subplot(1, 3, 2)
        ax_3 = fig.add_subplot(1, 3, 3)
        ax_1.set(title='График амплитуд', xlabel=self.str_axis_sig[0], ylabel=self.str_axis_sig[1])
        ax_2.set(title='График углов', xlabel=self.str_axis_sig[0], ylabel=self.str_axis_sig[2])
        ax_3.set(title='График полос', xlabel=self.str_axis_sig[0], ylabel=self.str_axis_sig[3])
        # отрисовка графика
        for i in range(len(x_time)):
            ax_1.plot(x_time[i], y_amp[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_leg[i])
            ax_2.plot(x_time[i], y_deg[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_leg[i])
            ax_3.plot(x_time[i], y_bnd[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_leg[i])
            if mean_flag == 1:
                ax_1.hlines(np.mean(y_amp[i]), vec_axis_amp[0], vec_axis_amp[1], color=col[i], linestyle='--', lw=0.6)
                ax_2.hlines(np.mean(y_deg[i]), vec_axis_deg[0], vec_axis_deg[1], color=col[i], linestyle='--', lw=0.6)
                ax_3.hlines(np.mean(y_bnd[i]), vec_axis_bnd[0], vec_axis_bnd[1], color=col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
            ax_3.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axis_amp)
        ax_2.axis(vec_axis_deg)
        ax_3.axis(vec_axis_bnd)
        # отображение сетки
        ax_1.grid()
        ax_2.grid()
        ax_3.grid()
        # вывод графика
        plt.show()

    def draw_graph_cpl(self, x_time0, y_sig, x_time1, y_int, x_time2, y_sum, str_sig, str_int, str_sum):
        # приведение типа к float
        x_time0, y_sig = self.get_float(x_time0, y_sig)
        x_time1, y_int = self.get_float(x_time1, y_int)
        x_time2, y_sum = self.get_float(x_time2, y_sum)
        # корректировка сетки времени
        x_time0, x_time1, x_time2 = x_time0 / self.time_coef, x_time1 / self.time_coef, x_time2 / self.time_coef
        y_sig, y_int, y_sum = y_sig / self.amp_coef, y_int / self.amp_coef, y_sum / self.amp_coef
        # границы отрисовки графика
        vec_axis_sig = self.get_axes(x_time0, y_sig)
        vec_axis_int = self.get_axes(x_time1, y_int)
        vec_axis_sum = self.get_axes(x_time2, y_sum)
        # выбор стиля графиков
        col, stl, wdt = self.get_style()
        # создаём окно с областями
        fig = plt.figure("Complex envelope", figsize=(19, 5.5))
        fig.suptitle("Комплексная огибающая", fontsize=14, fontweight='bold')
        ax_1 = fig.add_subplot(1, 3, 1)
        ax_2 = fig.add_subplot(1, 3, 2)
        ax_3 = fig.add_subplot(1, 3, 3)
        ax_1.set(title='Огибающая сигнала', xlabel=self.str_axis_sig[0], ylabel=self.str_axis_sig[1])
        ax_2.set(title='Огибающая помехи', xlabel=self.str_axis_sig[0], ylabel=self.str_axis_sig[1])
        ax_3.set(title='Огибающая суммы', xlabel=self.str_axis_sig[0], ylabel=self.str_axis_sig[1])
        # отрисовка графика 1
        for i in range(len(x_time0)):
            ax_1.plot(x_time0[i], y_sig[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_sig[i])
            if self.mean_cpl == 1:
                ax_1.hlines(np.mean(y_sig[i]), vec_axis_sig[0], vec_axis_sig[1], color=col[i], linestyle='--', lw=0.6)
        # отрисовка графика 2
        for i in range(len(x_time1)):
            ax_2.plot(x_time1[i], y_int[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_int[i])
            if self.mean_cpl == 1:
                ax_2.hlines(np.mean(y_int[i]), vec_axis_int[0], vec_axis_int[1], color=col[i], linestyle='--', lw=0.6)
        # отрисовка графика 3
        for i in range(len(x_time2)):
            ax_3.plot(x_time2[i], y_sum[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_sum[i])
            if self.mean_cpl == 1:
                ax_3.hlines(np.mean(y_sum[i]), vec_axis_sum[0], vec_axis_sum[1], color=col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
            ax_3.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axis_sig)
        ax_2.axis(vec_axis_int)
        ax_3.axis(vec_axis_sum)
        ax_1.grid()
        ax_2.grid()
        ax_3.grid()
        plt.show()

    def draw_graph_adp(self, x_time0, y_dpt, x_time1, y_atn, x_time2, y_snir, str_dpt, str_atn, str_snir):
        # приведение типа к float
        x_time0, y_dpt = self.get_float(x_time0, y_dpt)
        x_time1, y_atn = self.get_float(x_time1, y_atn)
        x_time2, y_snir = self.get_float(x_time2, y_snir)
        # корректировка сетки времени
        x_time0, x_time1, x_time2 = x_time0 / self.time_coef, x_time1 / self.time_coef, x_time2 / self.time_coef
        # границы отрисовки графика
        vec_axis_dpt = self.get_axes(x_time0, y_dpt)
        vec_axis_atn = self.get_axes(x_time1, y_atn)
        vec_axis_snir = self.get_axes(x_time2, y_snir)
        # выбор стиля графиков
        col, stl, wdt = self.get_style()
        # создаём окно с областями
        fig = plt.figure("Adaptation characteristics", figsize=(19, 5.5))
        fig.suptitle("Характеристики адаптации", fontsize=14, fontweight='bold')
        ax_1 = fig.add_subplot(1, 3, 1)
        ax_2 = fig.add_subplot(1, 3, 2)
        ax_3 = fig.add_subplot(1, 3, 3)
        ax_1.set(title='Глубина подавления', xlabel=self.str_axis_adp[0], ylabel=self.str_axis_adp[1])
        ax_2.set(title='Ослабление сигнала', xlabel=self.str_axis_adp[0], ylabel=self.str_axis_adp[2])
        ax_3.set(title='ОСШП', xlabel=self.str_axis_adp[0], ylabel=self.str_axis_adp[3])
        # отрисовка графика 1
        for i in range(len(x_time0)):
            ax_1.plot(x_time0[i], y_dpt[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_dpt[i])
            if self.mean_adp == 1:
                ax_1.hlines(np.mean(y_dpt[i]), vec_axis_dpt[0], vec_axis_dpt[1], color=col[i], linestyle='--', lw=0.6)
        # отрисовка графика 2
        for i in range(len(x_time1)):
            ax_2.plot(x_time1[i], y_atn[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_atn[i])
            if self.mean_adp == 1:
                ax_2.hlines(np.mean(y_atn[i]), vec_axis_atn[0], vec_axis_atn[1], color=col[i], linestyle='--', lw=0.6)
        # отрисовка графика 3
        for i in range(len(x_time2)):
            ax_3.plot(x_time2[i], y_snir[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_snir[i])
            if self.mean_adp == 1:
                ax_3.hlines(np.mean(y_snir[i]), vec_axis_snir[0], vec_axis_snir[1], color=col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
            ax_3.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axis_dpt)
        ax_2.axis(vec_axis_atn)
        ax_3.axis(vec_axis_snir)
        ax_1.grid()
        ax_2.grid()
        ax_3.grid()
        plt.show()

    def draw_graph_out(self, x_time, y_out0, str_out):
        # приведение типа к float
        x_time, y_out0 = self.get_float(x_time, y_out0)
        # вычисление преобразования фурье
        x_frq, y_out1 = self.get_fourier(x_time, y_out0)
        # приведение типа к float
        x_frq, y_out1 = self.get_float(x_frq, y_out1)
        # корректировка сетки времени и частот
        x_time, x_frq = x_time / self.time_coef, x_frq * self.time_coef
        y_out0, y_out1 = y_out0 / self.amp_coef, y_out1 / self.amp_coef
        # границы отрисовки графика
        vec_axis1 = self.get_axes(x_time, y_out0)
        vec_axis2 = self.get_axes(x_frq, y_out1)
        # выбор стиля графиков
        col, stl, wdt = self.get_style()
        # создаём окно с областями
        fig = plt.figure("System output", figsize=(12.5, 5.5))
        fig.suptitle("Сигнал на выходе ААР", fontsize=14, fontweight='bold')
        ax_1 = fig.add_subplot(1, 2, 1)
        ax_2 = fig.add_subplot(1, 2, 2)
        ax_1.set(title='Выходной сигнал с ААР', xlabel=self.str_axis_out[0], ylabel=self.str_axis_out[2])
        ax_2.set(title='Спектр выходного сигнала с ААР', xlabel=self.str_axis_out[1], ylabel=self.str_axis_out[2])
        # отрисовка графика 1
        for i in range(len(x_time)):
            ax_1.plot(x_time[i], y_out0[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_out[i])
            if self.mean_out == 1:
                ax_1.hlines(np.mean(y_out0[i]), vec_axis1[0], vec_axis1[1], color=col[i], linestyle='--', lw=0.6)
        # отрисовка графика 1
        #ax_1.plot(x_time[0], y_out0[0], color=col[0], linestyle=stl[0], lw=wdt[0], label=str_out[0])
        # отрисовка графика 2
        for i in range(len(x_frq)):
            #ax_2.scatter(x_frq[i], y_out1[i], color=vec_col[i])
            ax_2.plot(x_frq[i], y_out1[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_out[i])
            if self.mean_out == 1:
                ax_2.hlines(np.mean(y_out1[i]), vec_axis2[0], vec_axis2[1], color=col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='upper right')
        # отображение графика
        ax_1.axis(vec_axis1)
        #ax_2.axis(vec_axis2)
        ax_2.semilogy()
        # отображение сетки
        ax_1.grid()
        ax_2.grid()
        # вывод графика
        plt.show()

    def get_float(self, x, y):
        # преобразование типа к float
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        return [x, y]

    def get_style(self):
        # выбор стиля графиков
        if self.graph_style == 0:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        return [vec_col, vec_lst, vec_lwd]

    def get_axes(self, x, y):
        max_x, min_x = x.max(), x.min()
        max_y, min_y = y.max(), y.min()
        # коррекция верхней границы
        if max_y <= 0:
            max_y = 0.001
        else:
            max_y = max_y * 1.2
        # коррекция нижней границы
        if min_y >= 0:
            min_y = -0.001
        else:
            min_y = min_y * 1.2
        # определение границ графика
        vec_axis = [min_x, max_x, min_y, max_y * 1.1]
        #vec_axis = [min_x, max_x, -25, 25]
        return vec_axis

    def get_fourier(self, time, signal):
        # преобразование фурье
        len_signal = signal.shape[0]
        # интервал выборки, с
        time_step = time[0][1] - time[0][0]
        # частота дискретизации, Гц
        freq_sample = 1 / time_step
        # чило выборок, ед
        num_sample = time.shape[1]
        # интервал частот, Гц
        freq_step = freq_sample / num_sample
        # инициализация векторов
        vec_freq, vec_specamp = [], []
        # цикл по сигналам
        for i in range(len_signal):
            # сетка частот
            vec_freq.append(np.arange(-freq_sample/2 + freq_step/2, freq_sample/2, freq_step))
            # преобразование Фурье
            vec_spec = np.fft.fft(signal[i])
            vec_spec = np.fft.fftshift(vec_spec)
            vec_specamp.append(np.abs(vec_spec) / num_sample)
        # вывод параметров Фурье
        id_print = 0
        if id_print == 1:
            print("time_step = ", time_step)
            print("num_sample = ", num_sample)
            print("freq_sample = ", freq_sample)
            print("freq_step = ", freq_step)
        # возврат значений
        return vec_freq, vec_specamp
