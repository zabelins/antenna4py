import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль отображения ДН (L3)")

class Pattern:
    """Класс вывода графика диаграммы направленности антенны"""

    def __init__(self, id):
        self.id = id
        self.pattern_style = []
        self.pattern_norm = []
        self.pattern_mean = []
        self.pattern_db = []
        self.pattern_legend = []
        self.pattern_strleg = []
        self.str_y = "F(Θ)"
        self.str_x = "Θ, град."
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.pattern_style = init[1]
        self.pattern_norm = init[2]
        self.pattern_mean = init[3]
        self.pattern_db = init[4]
        self.pattern_legend = init[5]
        self.pattern_strleg = init[6]
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '--', '-.']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 1.0, 1.0]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.pattern_style)
        res.append(self.pattern_norm)
        res.append(self.pattern_mean)
        res.append(self.pattern_db)
        res.append(self.pattern_legend)
        res.append(self.pattern_strleg)
        res.append(self.str_y)
        res.append(self.str_x)
        return res

    def print(self):
        print(" --- Параметры отображения ДН (L3) --- ")
        print("id = ", self.id)
        print("pattern_style = ", self.pattern_style)
        print("pattern_norm = ", self.pattern_norm)
        print("pattern_mean = ", self.pattern_mean)
        print("pattern_db = ", self.pattern_db)
        print("pattern_legend = ", self.pattern_legend)
        print("pattern_strleg = ", self.pattern_strleg)
        print("str_y = ", self.str_y)
        print("str_x = ", self.str_x)

    def print_short(self):
        print(" --- Параметры отображения ДН (L3) --- ")
        print("pattern = ", self.get())

    def draw_pattern(self, x, y, deg_int):
        plt.title("Диаграмма направленности ААР")
        # приведение типа к double
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        # подписи графика
        plt.xlabel(self.str_x)
        plt.ylabel(self.str_y)
        # стиль графика
        if self.pattern_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        # нормировка и единицы измерения графика
        max_y = y[0].max()
        for i in range(len(x)):
            if self.pattern_norm == 1:
                y[i] = y[i] / max_y
            if self.pattern_db == 1:
                y[i] = 20 * np.log10(abs(y[i]))
        max_y = y[0].max()
        # границы отрисовки графика
        if self.pattern_db == 1:
            vec_axis = [-90, 90, -70, max_y]
        else:
            vec_axis = [-90, 90, 0, max_y]
        # отрисовка графика
        for i in range(len(x)):
            plt.plot(x[i], y[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=self.pattern_strleg[i])
            if self.pattern_mean == 1:
                plt.hlines(np.mean(y[i]), vec_axis[0], vec_axis[1], color='#666666', linestyle='--', lw=0.6)
        # отображение помех
        if (len(deg_int) >= 1) and (self.pattern_db == 1) and (self.pattern_norm == 1):
            for i in range(len(deg_int)):
                plt.arrow(deg_int[i], -2, 0, -4, color='k', width=0.5, head_width=1.3)
                plt.vlines(deg_int[i], vec_axis[2], vec_axis[3], color='#666666', linestyle='--', lw=0.6)
        # отображение легенды
        if self.pattern_legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()