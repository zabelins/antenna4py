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
        self.str_axis = ["band", "depth, дБ", "atten, дБ"]
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
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.2, 1.2, 1.2, 1.2, 1.2]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.2, 1.2, 1.2, 0.1, 0.1]

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

    def draw_graph(self, x_int, y_int, x_sig, y_sig, int_strleg, sig_strleg, app):
        self.approx = app
        # приведение типа к float
        x_int, y_int, x_sig, y_sig = self.get_float(x_int, y_int, x_sig, y_sig)
        # нормировка графиков
        y_int = self.get_norm(x_int, y_int)
        y_sig = self.get_norm(x_sig, y_sig)
        # приведение к децибеллам
        y_int = self.get_db(x_int, y_int)
        y_sig = self.get_db(x_sig, y_sig)
        # границы отрисовки графика
        vec_axisint = self.get_axes(x_int, y_int)
        vec_axissig = self.get_axes(x_sig, y_sig)
        # выбор стиля графиков
        vec_col, vec_lst, vec_lwd = self.get_style()
        # создаём окно с областями
        fig = plt.figure(figsize=(12, 5))
        ax_1 = fig.add_subplot(1, 2, 1)
        ax_2 = fig.add_subplot(1, 2, 2)
        ax_1.set(title='Подавление помех', xlabel=self.str_axis[0], ylabel=self.str_axis[1])
        ax_2.set(title='Ослабление сигнала', xlabel=self.str_axis[0], ylabel=self.str_axis[2])
        # аппроксимация МНК 1
        is_approx = 0
        if (self.approx != []) and (self.approx > 0):
            is_approx = 1
            for i in range(len(x_int)):
                ax_1.scatter(x_int[i], y_int[i], color=vec_col[i])
                x_i_new, y_i_new = self.get_approx(x_int[i], y_int[i])
                ax_1.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=int_strleg[i])
        # аппроксимация МНК 2
        is_approx = 0
        if (self.approx != []) and (self.approx > 0):
            is_approx = 1
            for i in range(len(x_sig)):
                ax_2.scatter(x_sig[i], y_sig[i], color=vec_col[i])
                x_i_new, y_i_new = self.get_approx(x_sig[i], y_sig[i])
                ax_2.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=sig_strleg[i])
        # отрисовка графика 1
        for i in range(len(x_int)):
            if is_approx != 1:
                ax_1.plot(x_int[i], y_int[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=int_strleg[i])
            else:
                ax_1.plot(x_int[i], y_int[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.adapt_mean == 1:
                ax_1.hlines(np.mean(y_int[i]), -90, 90, color=vec_col[i], linestyle='--', lw=0.6)
        # отрисовка графика 2
        for i in range(len(x_sig)):
            if is_approx != 1:
                ax_2.plot(x_sig[i], y_sig[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=sig_strleg[i])
            else:
                ax_2.plot(x_sig[i], y_sig[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.adapt_mean == 1:
                ax_2.hlines(np.mean(y_sig[i]), -90, 90, color=vec_col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.adapt_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axisint)
        ax_2.axis(vec_axissig)
        ax_1.grid()
        ax_2.grid()
        plt.show()

    def get_float(self, x1, y_int, x2, y_sig):
        # преобразование типа к float
        x1 = np.array(x1, dtype='float64')
        y_int = np.array(y_int, dtype='float64')
        x2 = np.array(x2, dtype='float64')
        y_sig = np.array(y_sig, dtype='float64')
        return [x1, y_int, x2, y_sig]

    def get_style(self):
        # выбор стиля графиков
        if self.adapt_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        return [vec_col, vec_lst, vec_lwd]

    def get_norm(self, x, y):
        # нормировка графика
        max_y = y.max()
        if self.adapt_norm == 1:
            for i in range(len(x)):
                y[i] = y[i] / max_y
        return y

    def get_db(self, x, y):
        # перевод шкалы y к децибеллам
        if self.adapt_db == 1:
            for i in range(len(x)):
                y[i] = 20 * np.log10(abs(y[i]))
        return y

    def get_axes(self, x, y):
        max_x, min_x = x.max(), x.min()
        max_y, min_y = y.max(), y.min()
        # определение границ графика
        if self.adapt_db == 1:
            vec_axis = [min_x, max_x, -70, max_y]
        else:
            # максимальная граница по y
            if (max_y < 0):
                max_y = 0
            else:
                max_y = max_y * 1.5
            vec_axis = [min_x, max_x, min_y * 1.2, max_y]
        return vec_axis

    def get_approx(self, x, y):
        x_i, y_i = [x, y]
        step = (x_i[1] - x_i[0]) / 10
        x_i_new = np.arange(min(x_i), max(x_i) + step, step)
        # аппроксимация
        y_i_new = cl.approx(5, x_i_new, x_i, y_i)
        # интерполяция
        # coef = np.polyfit(x_i, y_i, self.approx)
        # y_i_new = np.polyval(coef, x_i_new)
        return [x_i_new, y_i_new]