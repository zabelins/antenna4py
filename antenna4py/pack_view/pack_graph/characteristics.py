import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик адаптации (L3)")

class Characteristics:
    """Класс вывода графика характеристик адаптации для пользователя"""

    def __init__(self, id):
        self.id = id
        self.charact_style = []
        self.charact_norm = []
        self.charact_mean = []
        self.charact_db = []
        self.charact_legend = []
        self.charact_strleg = []
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
        self.charact_style = init[7]
        self.charact_norm = init[8]
        self.charact_mean = init[9]
        self.charact_db = init[10]
        self.charact_legend = init[11]
        self.charact_strleg = init[12]
        self.approx = init[19]
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.charact_style)
        res.append(self.charact_norm)
        res.append(self.charact_mean)
        res.append(self.charact_db)
        res.append(self.charact_legend)
        res.append(self.charact_strleg)
        res.append(self.str_y)
        res.append(self.str_x)
        res.append(self.approx)
        return res

    def print(self):
        print(" --- Параметры отображения характеристик адаптации (L3) --- ")
        print("id = ", self.id)
        print("charact_style = ", self.charact_style)
        print("charact_norm = ", self.charact_norm)
        print("charact_mean = ", self.charact_mean)
        print("charact_db = ", self.charact_db)
        print("charact_legend = ", self.charact_legend)
        print("charact_strleg = ", self.charact_strleg)
        print("str_y = ", self.str_y)
        print("str_x = ", self.str_x)
        print("approx = ", self.approx)

    def print_short(self):
        print(" --- Параметры отображения характеристик адаптации (L3) --- ")
        print("characteristics = ", self.get())

    def draw_charact(self, x, y, str):
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
        if self.charact_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        # нормировка и единицы измерения графика
        #max_y = np.amax(y)
        #for i in range(len(x)):
        #    if self.charact_norm == 1:
        #        y[i] = y[i] / max_y
        #    if self.charact_db == 1:
        #        y[i] = 20 * np.log10(abs(y[i]))
        max_y = np.amax(y)
        # границы отрисовки графика
        if self.charact_db == 1:
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
                plt.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=self.charact_strleg[i])
        # отрисовка графика
        for i in range(len(x)):
            plt.scatter(x[i], y[i], color=vec_col[i])
            if is_approx != 1:
                plt.plot(x[i], y[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=self.charact_strleg[i])
            else:
                plt.plot(x[i], y[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.charact_mean == 1:
                plt.hlines(np.mean(y[i]), -90, 90, color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if self.charact_legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()