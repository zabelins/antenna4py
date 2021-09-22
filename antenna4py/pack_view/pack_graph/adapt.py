import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик адаптации (L3)")

class Adapt:
    """Класс вывода графика характеристик адаптации для пользователя"""

    def __init__(self, id):
        self.id = id
        self.adapt_style = []
        self.adapt_mean = []
        self.adapt_norm = []
        self.adapt_db = []
        self.adapt_legend = []
        self.str_axis = ["F(par)", "par"]
        self.approx = []
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.adapt_style = init[10]
        self.adapt_mean = init[11]
        self.adapt_norm = init[12]
        self.adapt_db = init[13]
        self.adapt_legend = init[14]
        self.approx = init[15]
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.adapt_style)
        res.append(self.adapt_mean)
        res.append(self.adapt_norm)
        res.append(self.adapt_db)
        res.append(self.adapt_legend)
        res.append(self.str_axis)
        res.append(self.approx)
        return res

    def print(self):
        print("Параметры отображения характеристик адаптации (L3):")
        print("\tadapt_style = ", self.adapt_style)
        print("\tadapt_mean = ", self.adapt_mean)
        print("\tadapt_norm = ", self.adapt_norm)
        print("\tadapt_db = ", self.adapt_db)
        print("\tadapt_legend = ", self.adapt_legend)
        print("\tstr_axis = ", self.str_axis)
        print("\tapprox = ", self.approx)

    def draw_charact(self, x1, y1, x2, y2, str, adapt_strleg):
        plt.title("Характеристики адаптации")
        # приведение типа к double
        x = np.array(x1, dtype='float64')
        y = np.array(y1, dtype='float64')
        # подписи графика
        if len(str)!=2:
            plt.ylabel(self.str_axis[0])
            plt.xlabel(self.str_axis[1])
        else:
            plt.ylabel(str[0])
            plt.xlabel(str[1])
        # стиль графика
        if self.adapt_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        # нормировка и единицы измерения графика
        max_y = np.amax(y)
        for i in range(len(x)):
            if self.adapt_norm == 1:
                y[i] = y[i] / max_y
            if self.adapt_db == 1:
                y[i] = 20 * np.log10(abs(y[i]))
        max_y = np.amax(y)
        min_y = np.amin(y)
        # границы отрисовки графика
        if self.adapt_db == 1:
            vec_axis = [x[0].min(), x[0].max(), -70, max_y]
        else:
            vec_axis = [x[0].min(), x[0].max(), -70, max_y]
        # аппроксимация МНК
        is_approx = 0
        if (self.approx != []) and (self.approx > 0):
            is_approx = 1
            for i in range(len(x)):
                x_i, y_i = [x[i], y[i]]
                step = (x_i[1] - x_i[0]) / 10
                x_i_new = np.arange(min(x_i), max(x_i) + step, step)
                # аппроксимация
                y_i_new = cl.approx(self.approx, x_i_new, x_i, y_i)
                # интерполяция
                # coef = np.polyfit(x_i, y_i, self.approx)
                # y_i_new = np.polyval(coef, x_i_new)
                plt.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=adapt_strleg[i])
        # отрисовка графика
        for i in range(len(x)):
            plt.scatter(x[i], y[i], color=vec_col[i])
            if is_approx != 1:
                plt.plot(x[i], y[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=adapt_strleg[i])
            else:
                plt.plot(x[i], y[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.adapt_mean == 1:
                plt.hlines(np.mean(y[i]), -90, 90, color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if self.adapt_legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()