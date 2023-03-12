import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль отображения ДН (L3)")

class Pattern:
    """Класс вывода графика диаграммы направленности антенны"""

    def __init__(self):
        # общие настройки графики
        self.graph_style = []
        self.graph_legend = []
        # параметры диаграммы направленности
        self.mean_ptn = []
        self.ptn_norm = []
        self.ptn_db = []
        # скрытые настройки графики
        self.str_axis = ["Θ [deg]", "G [dB]"]
        self.show_eqint = 1
        # вектора стилей
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['--', '-', '-', '-', '-']
        self.vec_lwd1 = [1.4, 1.6, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['--', '-', '-.', '--', '-.']
        self.vec_lwd2 = [1.0, 1.2, 1.0, 1.0, 1.0]
        plt.rcParams['font.size'] = '12'

    def set(self, init):
        self.graph_style = init[0]
        self.graph_legend = init[1]
        self.mean_ptn = init[9]
        self.ptn_norm = init[16]
        self.ptn_db = init[17]

    def get(self):
        res = []
        res.append(self.graph_style)
        res.append(self.graph_legend)
        res.append(self.mean_ptn)
        res.append(self.ptn_norm)
        res.append(self.ptn_db)
        res.append(self.show_eqint)
        res.append(self.str_axis)
        return res

    def print(self):
        print("Параметры отображения ДН (L3):")
        print("\tgraph_style = ", self.graph_style)
        print("\tgraph_legend = ", self.graph_legend)
        print("\tmean_ptn = ", self.mean_ptn)
        print("\tptn_norm = ", self.ptn_norm)
        print("\tptn_db = ", self.ptn_db)
        print("\tshow_eqint = ", self.show_eqint)
        print("\tstr_axis = ", self.str_axis)

    def draw_graph(self, x, y, deg_sig, deg_int, eqdeg_sig, eqdeg_int, str_legend):
        # приведение типа к float, нормировка и перевод в дБ
        x, y = self.get_float(x, y)
        y = self.get_norm(x, y)
        y = self.get_amp2db(x, y)
        # границы отрисовки графика
        vec_axis = self.get_axes(x, y)
        # выбор стиля графиков
        col, stl, wdt = self.get_style()
        # создаём окно
        fig = plt.figure("Диаграмма направленности ААР", figsize=(8, 7))
        ax = fig.add_subplot(1, 1, 1)
        ax.set(xlabel=self.str_axis[0], ylabel=self.str_axis[1])
        # отрисовка графика
        for i in range(len(x)):
            ax.plot(x[i], y[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_legend[i])
            # отрисовка среднего уровня
            if self.mean_ptn == 1:
                ax.hlines(np.mean(y[i]), vec_axis[0], vec_axis[1], color=col[i], linestyle='--', lw=0.6)
        # настройки отображения помех
        vec_mark = self.get_mark(vec_axis)
        # отображение помех
        if (len(deg_int) > 0) and (self.ptn_norm == 1) and (self.ptn_db == 1):
            # цикл по реальным помехам
            for i in range(len(deg_int)):
                if self.show_eqint == 1:
                    # эквивалентные помехи
                    for j in range(len(eqdeg_int[i])):
                        if (eqdeg_int[i][j] >= vec_axis[0]) and (eqdeg_int[i][j] <= vec_axis[1]):
                            if j == 0:
                                ax.arrow(deg_int[i], vec_mark[0], 0, vec_mark[1], color=col[i], width=0.5, head_width=1.3)
                                ax.vlines(deg_int[i], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
                            else:
                                ax.arrow(eqdeg_int[i][j], vec_mark[2], 0, vec_mark[3], color=col[i], width=0.3, head_width=1.0)
                                ax.vlines(eqdeg_int[i][j], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
                else:
                    # реальные помехи
                    ax.arrow(deg_int[i], vec_mark[0], 0, vec_mark[1], color=col[i], width=0.5, head_width=1.3)
                    ax.vlines(deg_int[i], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax.legend(loc='lower left')
        # отображение графика
        ax.axis(vec_axis)
        ax.grid()
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

    def get_norm(self, x, y):
        # нормировка графика
        max_y = y[0].max()
        if self.ptn_norm == 1:
            for i in range(len(x)):
                y[i] = y[i] / max_y
        return y

    def get_amp2db(self, x, y):
        # перевод шкалы y к децибеллам
        if self.ptn_db == 1:
            for i in range(len(x)):
                # для амплитудной ДН
                y[i] = 20 * np.log10(abs(y[i]))
        return y

    def get_axes(self, x, y):
        # определение границ графика
        max_x, min_x = x.max(), x.min()
        max_y, min_y = y.max(), y.min()
        if self.ptn_db == 1:
            vec_axis = [min_x, max_x, -100, max_y]
        else:
            vec_axis = [min_x, max_x, 0, max_y]
        return vec_axis

    def get_mark(self, vec_axis):
        # определение границ графика
        y_min, y_max = vec_axis[2], vec_axis[3]
        dif = abs(y_max - y_min)
        # положение стрелок в нормированном диапазоне
        y_minint, y_maxint = 0.92, 0.98
        y_mineqint, y_maxeqint = 0.94, 0.97
        # преобразование в реальный диапазон
        y_minint, y_maxint = (y_minint * dif) + y_min, (y_maxint * dif) + y_min
        y_mineqint, y_maxeqint = (y_mineqint * dif) + y_min, (y_maxeqint * dif) + y_min
        # преобразование в относительную величину
        dif_int = round((y_maxint - y_minint) * 100) / (-100)
        dif_eqint = round((y_maxeqint - y_mineqint) * 100) / (-100)
        # округление
        y_maxint = round(y_maxint * 100) / 100
        y_maxeqint = round(y_maxeqint * 100) / 100
        return [y_maxint, dif_int, y_maxeqint, dif_eqint]
