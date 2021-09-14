import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик сигналов и помех (L3)")

class TimeFreq:
    """Класс вывода графика характеристик сигналов и помех для пользователя"""

    def __init__(self, id):
        self.id = id
        self.timefreq_style = []
        self.timefreq_norm = []
        self.timefreq_mean = []
        self.timefreq_db = []
        self.timefreq_legend = []
        self.timefreq_strleg = []
        self.str_y = "T"
        self.str_x = "Amp"
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.timefreq_style = init[13]
        self.timefreq_norm = init[14]
        self.timefreq_mean = init[15]
        self.timefreq_db = init[16]
        self.timefreq_legend = init[17]
        self.timefreq_strleg = init[18]
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.timefreq_style)
        res.append(self.timefreq_norm)
        res.append(self.timefreq_mean)
        res.append(self.timefreq_db)
        res.append(self.timefreq_legend)
        res.append(self.timefreq_strleg)
        res.append(self.str_y)
        res.append(self.str_x)
        return res

    def print(self):
        print(" --- Параметры отображения характеристик сигналов и помех (L3) --- ")
        print("id = ", self.id)
        print("timefreq_style = ", self.timefreq_style)
        print("timefreq_norm = ", self.timefreq_norm)
        print("timefreq_mean = ", self.timefreq_mean)
        print("timefreq_db = ", self.timefreq_db)
        print("timefreq_legend = ", self.timefreq_legend)
        print("timefreq_strleg = ", self.timefreq_strleg)
        print("str_y = ", self.str_y)
        print("str_x = ", self.str_x)

    def print_short(self):
        print(" --- Параметры отображения характеристик сигналов и помех (L3) --- ")
        print("timefreq = ", self.get())

    def draw_time(self, x, y, str):
        plt.title("Изменяемый параметр")
        # приведение типа к double
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        # подписи графика
        if len(str) != 2:
            plt.ylabel(self.str_y)
            plt.xlabel(self.str_x)
        else:
            plt.ylabel(str[0])
            plt.xlabel(str[1])
        # стиль графика
        if self.timefreq_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        # нормировка и единицы измерения графика
        # max_y = np.amax(y)
        # for i in range(len(x)):
        #    if self.timefreq_norm == 1:
        #        y[i] = y[i] / max_y
        #    if self.timefreq_db == 1:
        #        y[i] = 20 * np.log10(abs(y[i]))
        max_y = np.amax(y)
        # границы отрисовки графика
        if self.timefreq_db == 1:
            vec_axis = [x[0].min(), x[0].max(), -70, max_y]
        else:
            vec_axis = [x[0].min(), x[0].max(), 0, max_y * 1.1]
        # отрисовка графика
        for i in range(len(x)):
            plt.plot(x[i], y[i], color=vec_col[i], linestyle='-', lw=0.7, label=self.timefreq_strleg[i])
            if self.timefreq_mean == 1:
                plt.hlines(np.mean(y[i]), -90, 90, color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if self.timefreq_legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()

    def draw_freq(self):
        pass