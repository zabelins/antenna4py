# модуль отображения ДН

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль отображения ДН (L3)")

class Pattern:
    """Класс вывода графика диаграммы направленности антенны"""

    def __init__(self, id):
        self.id = id
        self.str_y = "F(Θ)"
        self.str_x = "Θ, град."
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '--', '-.']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 1.0, 1.0]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.str_y)
        res.append(self.str_x)
        return res

    def print(self):
        print(" --- Параметры отображения ДН (L3) --- ")
        print("id = ", self.id)
        print("str_y = ", self.str_y)
        print("str_x = ", self.str_x)

    def print_short(self):
        print(" --- Параметры отображения ДН (L3) --- ")
        print("pattern = ", self.get())

    def draw_pattern(self, x, y, vec_par, deg_int):
        style, norm, mean, db, legend, strleg = [vec_par[1], vec_par[2], vec_par[3], vec_par[4], vec_par[5], vec_par[6]]
        plt.title("Диаграмма направленности ААР")
        # приведение типа к double
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        # подписи графика
        plt.xlabel(self.str_x)
        plt.ylabel(self.str_y)
        # стиль графика
        if style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        # нормировка и единицы измерения графика
        max_y = y[0].max()
        for i in range(len(x)):
            if norm == 1:
                y[i] = y[i] / max_y
            if db == 1:
                y[i] = 20 * np.log10(abs(y[i]))
        max_y = y[0].max()
        # границы отрисовки графика
        if db == 1:
            vec_axis = [-90, 90, -70, max_y]
        else:
            vec_axis = [-90, 90, 0, max_y]
        # отрисовка графика
        for i in range(len(x)):
            plt.plot(x[i], y[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=strleg[i])
            if mean == 1:
                plt.hlines(np.mean(y[i]), vec_axis[0], vec_axis[1], color='#666666', linestyle='--', lw=0.6)
        # отображение помех
        if (len(deg_int) >= 1) and (db == 1) and (norm == 1):
            for i in range(len(deg_int)):
                plt.arrow(deg_int[i], -2, 0, -4, color='k', width=0.5, head_width=1.3)
                plt.vlines(deg_int[i], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
        # отображение легенды
        if legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()