import math
import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик выходного сигнала (L3)")

class Output:
    """Класс вывода графика характеристик выходного сигнала для пользователя"""

    def __init__(self, id):
        self.id = id
        self.output_style = []
        self.output_mean = []
        self.output_legend = []
        self.str_axis = ["time [ms]", "freq [Hz]", "power [W]"]
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.output_style = init[8]
        self.output_mean = init[9]
        self.output_legend = init[10]
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.2, 1.2, 1.2, 1.2, 1.2]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.2, 1.2, 1.2, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.output_style)
        res.append(self.output_mean)
        res.append(self.output_legend)
        res.append(self.str_axis)
        return res

    def print(self):
        print("Параметры отображения характеристик выходного сигнала (L3):")
        print("\toutput_style = ", self.output_style)
        print("\toutput_mean = ", self.output_mean)
        print("\toutput_legend = ", self.output_legend)
        print("\tstr_axis = ", self.str_axis)

    def draw_graph(self, x_1, y_1, output_strleg):
        # приведение типа к float
        x_1, y_1 = self.get_float(x_1, y_1)
        # вычисление преобразования фурье
        x_2, y_2 = self.get_fourier(x_1, y_1)
        # приведение типа к float
        x_2, y_2 = self.get_float(x_2, y_2)
        # границы отрисовки графика
        vec_axis1 = self.get_axes(x_1, y_1)
        vec_axis2 = self.get_axes(x_2, y_2)
        # выбор стиля графиков
        vec_col, vec_lst, vec_lwd = self.get_style()
        # создаём окно с областями
        fig = plt.figure(figsize=(12, 5))
        ax_1 = fig.add_subplot(1, 2, 1)
        ax_2 = fig.add_subplot(1, 2, 2)
        ax_1.set(title='Выходной сигнал с ААР', xlabel=self.str_axis[0], ylabel=self.str_axis[2])
        ax_2.set(title='Спектр выходного сигнала с ААР', xlabel=self.str_axis[1], ylabel=self.str_axis[2])
        # отрисовка графика 1
        for i in range(len(x_1)):
            ax_1.plot(x_1[i], y_1[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=output_strleg[i])
            if self.output_mean == 1:
                ax_1.hlines(np.mean(y_1[i]), vec_axis1[0], vec_axis1[1], color='#666666', linestyle='-', lw=0.6)
        # отрисовка графика 2
        for i in range(len(x_2)):
            #ax_2.scatter(x_2[i], y_2[i], color=vec_col[i])
            ax_2.plot(x_2[i], y_2[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=output_strleg[i])
            if self.output_mean == 1:
                ax_2.hlines(np.mean(y_2[i]), vec_axis2[0], vec_axis2[1], color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if self.output_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='upper right')
        # отображение графика
        ax_1.axis(vec_axis1)
        ax_2.axis(vec_axis2)
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
        if self.output_style == 1:
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
            max_y = max_y * 1.1
        # коррекция нижней границы
        if min_y >= 0:
            min_y = -0.001
        else:
            min_y = min_y * 1.1
        # определение границ графика
        vec_axis = [min_x, max_x, min_y, max_y * 1.1]
        return vec_axis

    def get_fourier(self, time, signal):
        # преобразование фурье
        len_signal = signal.shape[0]
        # 1 ед = 1 мс
        time = time * math.pow(10, -3)
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