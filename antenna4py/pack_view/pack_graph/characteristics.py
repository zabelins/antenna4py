import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик (L3)")

class Characteristics:
    """Класс вывода графика характеристик для пользователя"""

    def __init__(self, id):
        self.id = id
        self.str_y = "F(par)"
        self.str_x = "par"
        self.approx = []
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.approx = init[7]
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.str_y)
        res.append(self.str_x)
        res.append(self.approx)
        return res

    def print(self):
        print(" --- Параметры отображения характеристик (L3) --- ")
        print("id = ", self.id)
        print("str_y = ", self.str_y)
        print("str_x = ", self.str_x)
        print("approx = ", self.approx)

    def print_short(self):
        print(" --- Параметры отображения характеристик (L3) --- ")
        print("characteristics = ", self.get())

    def draw_charact(self, x, y, vec_par, str):
        style, norm, mean, db, legend, strleg = [vec_par[1], vec_par[2], vec_par[3], vec_par[4], vec_par[5], vec_par[6]]
        plt.title("Характеристики ААР")
        # приведение типа к double
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        # подписи графика
        if len(str)!=2:
            plt.ylabel(self.str_y)
            plt.xlabel(self.str_x)
        else:
            plt.ylabel(str[0])
            plt.xlabel(str[1])
        # стиль графика
        if style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        # нормировка и единицы измерения графика
        #max_y = np.amax(y)
        #for i in range(len(x)):
        #    if norm == 1:
        #        y[i] = y[i] / max_y
        #    if db == 1:
        #        y[i] = 20 * np.log10(abs(y[i]))
        max_y = np.amax(y)
        # границы отрисовки графика
        if db == 1:
            vec_axis = [x[0].min(), x[0].max(), -70, max_y]
        else:
            vec_axis = [x[0].min(), x[0].max(), 0, max_y]
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
                plt.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=strleg[i])
        # отрисовка графика
        for i in range(len(x)):
            plt.scatter(x[i], y[i], color=vec_col[i])
            if is_approx != 1:
                plt.plot(x[i], y[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=strleg[i])
            else:
                plt.plot(x[i], y[i], color=vec_col[i], linestyle='--', lw=0.7)
            if mean == 1:
                plt.hlines(np.mean(y[i]), -90, 90, color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()