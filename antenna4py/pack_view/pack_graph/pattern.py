import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль отображения ДН (L3)")

class Pattern:
    """Класс вывода графика диаграммы направленности антенны"""

    def __init__(self, id):
        self.id = id
        # пользовательские настройки графики
        self.pattern_style = []
        self.pattern_mean = []
        self.pattern_norm = []
        self.pattern_db = []
        self.pattern_legend = []
        # скрытые настройки графики
        self.str_axis = ["Θ, град.", "F(Θ)"]
        self.show_eqint = 1
        # вектора стилей
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.pattern_style = init[0]
        self.pattern_mean = init[1]
        self.pattern_norm = init[2]
        self.pattern_db = init[3]
        self.pattern_legend = init[4]
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.2, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '--', '-.']
        self.vec_lwd2 = [1.0, 1.2, 1.0, 1.0, 1.0]

    def get(self):
        res = []
        res.append(self.pattern_style)
        res.append(self.pattern_mean)
        res.append(self.pattern_norm)
        res.append(self.pattern_db)
        res.append(self.pattern_legend)
        res.append(self.show_eqint)
        res.append(self.str_axis)
        return res

    def print(self):
        print("Параметры отображения ДН (L3):")
        print("\tpattern_style = ", self.pattern_style)
        print("\tpattern_mean = ", self.pattern_mean)
        print("\tpattern_norm = ", self.pattern_norm)
        print("\tpattern_db = ", self.pattern_db)
        print("\tpattern_legend = ", self.pattern_legend)
        print("\tshow_eqint = ", self.show_eqint)
        print("\tstr_axis = ", self.str_axis)

    def draw_pattern(self, x, y, deg_sig, deg_int, eqdeg_sig, eqdeg_int, str_legend):
        # приведение типа к float
        x, y = self.get_float(x, y)
        # нормировка и приведение графиков к децибеллам
        y = self.get_norm(x, y)
        y = self.get_db(x, y)
        # границы отрисовки графика
        vec_axis = self.get_axes(x, y)
        # выбор стиля графиков
        vec_col, vec_lst, vec_lwd = self.get_style()
        # создаём окно
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.set(title='Диаграмма направленности ААР', xlabel=self.str_axis[0], ylabel=self.str_axis[1])
        # отрисовка графика
        for i in range(len(x)):
            ax.plot(x[i], y[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=str_legend[i])
            # отрисовка среднего уровня
            if self.pattern_mean == 1:
                ax.hlines(np.mean(y[i]), vec_axis[0], vec_axis[1], color=vec_col[i], linestyle='--', lw=0.6)
        # настройки отображения помех
        vec_mark = self.get_mark(vec_axis)
        # отображение помех
        if (len(deg_int) > 0) and (self.pattern_norm == 1) and (self.pattern_db == 1):
            # цикл по реальным помехам
            for i in range(len(deg_int)):
                if self.show_eqint == 1:
                    # эквивалентные помехи
                    for j in range(len(eqdeg_int[i])):
                        if (eqdeg_int[i][j] >= vec_axis[0]) and (eqdeg_int[i][j] <= vec_axis[1]):
                            if j == 0:
                                ax.arrow(deg_int[i], vec_mark[0], 0, vec_mark[1], color='#000000', width=0.5, head_width=1.3)
                                ax.vlines(deg_int[i], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
                            else:
                                ax.arrow(eqdeg_int[i][j], vec_mark[2], 0, vec_mark[3], color='#000000', width=0.3, head_width=1.0)
                                ax.vlines(eqdeg_int[i][j], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
                else:
                    # реальные помехи
                    ax.arrow(deg_int[i], vec_mark[0], 0, vec_mark[1], color='#000000', width=0.5, head_width=1.3)
                    ax.vlines(deg_int[i], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
        # отображение легенды
        if self.pattern_legend == 1:
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
        if self.pattern_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        return [vec_col, vec_lst, vec_lwd]

    def get_norm(self, x, y):
        # нормировка графика
        max_y = y[0].max()
        if self.pattern_norm == 1:
            for i in range(len(x)):
                y[i] = y[i] / max_y
        return y

    def get_db(self, x, y):
        # перевод шкалы y к децибеллам
        if self.pattern_db == 1:
            for i in range(len(x)):
                y[i] = 20 * np.log10(abs(y[i]))
        return y

    def get_axes(self, x, y):
        # определение границ графика
        max_x, min_x = x.max(), x.min()
        max_y, min_y = y.max(), y.min()
        if self.pattern_db == 1:
            vec_axis = [min_x, max_x, -70, max_y]
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
