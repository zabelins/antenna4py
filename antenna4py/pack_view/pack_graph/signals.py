import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик сигналов и помех (L3)")

class Signals:
    """Класс вывода графика характеристик сигналов и помех для пользователя"""

    def __init__(self, id):
        self.id = id
        self.signals_style = []
        self.signals_mean = []
        self.signals_legend = []
        self.str_axis = ["time [ms]", "amp [V]", "angle [deg]", "band [Hz]"]
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.signals_style = init[5]
        self.signals_mean = init[6]
        self.signals_legend = init[7]
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.2, 1.2, 1.2, 1.2, 1.2]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.2, 1.2, 1.2, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.signals_style)
        res.append(self.signals_mean)
        res.append(self.signals_legend)
        res.append(self.str_axis)
        return res

    def print(self):
        print("Параметры отображения характеристик сигналов и помех (L3):")
        print("\tsignals_style = ", self.signals_style)
        print("\tsignals_mean = ", self.signals_mean)
        print("\tsignals_legend = ", self.signals_legend)
        print("\tstr_axis = ", self.str_axis)

    def draw_graph(self, x, y_amp, y_deg, y_band, signals_strleg):
        # приведение типа к float
        x, y_amp, y_deg, y_band = self.get_float(x, y_amp, y_deg, y_band)
        # границы отрисовки графика
        vec_axisamp = self.get_axes(x, y_amp)
        vec_axisdeg = self.get_axes(x, y_deg)
        vec_axisband = self.get_axes(x, y_band)
        # выбор стиля графиков
        vec_col, vec_lst, vec_lwd = self.get_style()
        # создаём окно с областями
        fig = plt.figure(figsize=(17, 5))
        ax_1 = fig.add_subplot(1, 3, 1)
        ax_2 = fig.add_subplot(1, 3, 2)
        ax_3 = fig.add_subplot(1, 3, 3)
        ax_1.set(title='График амплитуд', xlabel=self.str_axis[0], ylabel=self.str_axis[1])
        ax_2.set(title='График углов', xlabel=self.str_axis[0], ylabel=self.str_axis[2])
        ax_3.set(title='График полос', xlabel=self.str_axis[0], ylabel=self.str_axis[3])
        # отрисовка графика
        for i in range(len(x)):
            ax_1.plot(x[i], y_amp[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=signals_strleg[i])
            ax_2.plot(x[i], y_deg[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=signals_strleg[i])
            ax_3.plot(x[i], y_band[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=signals_strleg[i])
            if self.signals_mean == 1:
                ax_1.hlines(np.mean(y_amp[i]), vec_axisamp[0], vec_axisamp[1], color='#666666', linestyle='-', lw=0.6)
                ax_2.hlines(np.mean(y_deg[i]), vec_axisdeg[0], vec_axisdeg[1], color='#666666', linestyle='-', lw=0.6)
                ax_3.hlines(np.mean(y_band[i]), vec_axisband[0], vec_axisband[1], color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if self.signals_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
            ax_3.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axisamp)
        ax_2.axis(vec_axisdeg)
        ax_3.axis(vec_axisband)
        # отображение сетки
        ax_1.grid()
        ax_2.grid()
        ax_3.grid()
        # вывод графика
        plt.show()

    def get_float(self, x, y_amp, y_deg, y_band):
        # преобразование типа к float
        x = np.array(x, dtype='float64')
        y_amp = np.array(y_amp, dtype='float64')
        y_deg = np.array(y_deg, dtype='float64')
        y_band = np.array(y_band, dtype='float64')
        return [x, y_amp, y_deg, y_band]

    def get_style(self):
        # выбор стиля графиков
        if self.signals_style == 1:
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
        return vec_axis