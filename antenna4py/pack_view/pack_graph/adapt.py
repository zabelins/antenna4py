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
        self.adapt_legend = []
        self.str_axis = ["time, мс", "band, ед.", "depth, дБ", "atten, дБ", "snir, ед."]
        self.approx = []
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.adapt_style = init[8]
        self.adapt_mean = init[9]
        self.adapt_legend = init[10]
        self.approx = init[11]
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
        res.append(self.adapt_legend)
        res.append(self.str_axis)
        res.append(self.approx)
        return res

    def print(self):
        print("Параметры отображения характеристик адаптации (L3):")
        print("\tadapt_style = ", self.adapt_style)
        print("\tadapt_mean = ", self.adapt_mean)
        print("\tadapt_legend = ", self.adapt_legend)
        print("\tstr_axis = ", self.str_axis)
        print("\tapprox = ", self.approx)

    def draw_graph(self, x_depth, y_depth, x_atten, y_atten, x_snir, y_snir, leg_depth, leg_atten, leg_snir, mode):
        # приведение типа к float
        x_depth, y_depth = self.get_float(x_depth, y_depth)
        x_atten, y_atten = self.get_float(x_atten, y_atten)
        x_snir, y_snir = self.get_float(x_snir, y_snir)
        # границы отрисовки графика
        vec_axisdepth = self.get_axes(x_depth, y_depth)
        vec_axisatten = self.get_axes(x_atten, y_atten)
        vec_axissnir = self.get_axes(x_snir, y_snir)
        # выбор стиля графиков
        vec_col, vec_lst, vec_lwd = self.get_style()
        # выбор подписи оси x
        if mode == 0:
            str_buf = self.str_axis[0]
        else:
            str_buf = self.str_axis[1]
        # создаём окно с областями
        fig = plt.figure(figsize=(17, 5))
        ax_1 = fig.add_subplot(1, 3, 1)
        ax_2 = fig.add_subplot(1, 3, 2)
        ax_3 = fig.add_subplot(1, 3, 3)
        ax_1.set(title='Подавление помех', xlabel=str_buf, ylabel=self.str_axis[2])
        ax_2.set(title='Ослабление сигнала', xlabel=str_buf, ylabel=self.str_axis[3])
        ax_3.set(title='ОСШП', xlabel=str_buf, ylabel=self.str_axis[4])
        # аппроксимация МНК 1
        is_approx1 = 0
        if mode == 1:
            is_approx1 = 1
            for i in range(len(x_depth)):
                ax_1.scatter(x_depth[i], y_depth[i], color=vec_col[i])
                x_i_new, y_i_new = self.get_approx(x_depth[i], y_depth[i])
                ax_1.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=leg_depth[i])
        # аппроксимация МНК 2
        is_approx2 = 0
        if mode == 1:
            is_approx2 = 1
            for i in range(len(x_atten)):
                ax_2.scatter(x_atten[i], y_atten[i], color=vec_col[i])
                x_i_new, y_i_new = self.get_approx(x_atten[i], y_atten[i])
                ax_2.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=leg_atten[i])
        # аппроксимация МНК 3
        is_approx3 = 0
        if mode == 1:
            is_approx3 = 1
            for i in range(len(x_snir)):
                ax_3.scatter(x_snir[i], y_snir[i], color=vec_col[i])
                x_i_new, y_i_new = self.get_approx(x_snir[i], y_snir[i])
                ax_3.plot(x_i_new, y_i_new, color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=leg_snir[i])
        # отрисовка графика 1
        for i in range(len(x_depth)):
            if is_approx1 != 1:
                ax_1.plot(x_depth[i], y_depth[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=leg_depth[i])
            else:
                ax_1.plot(x_depth[i], y_depth[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.adapt_mean == 1:
                ax_1.hlines(np.mean(y_depth[i]), vec_axisdepth[0], vec_axisdepth[1], color=vec_col[i], linestyle='--', lw=0.6)
        # отрисовка графика 2
        for i in range(len(x_atten)):
            if is_approx2 != 1:
                ax_2.plot(x_atten[i], y_atten[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=leg_atten[i])
            else:
                ax_2.plot(x_atten[i], y_atten[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.adapt_mean == 1:
                ax_2.hlines(np.mean(y_atten[i]), vec_axisatten[0], vec_axisatten[1], color=vec_col[i], linestyle='--', lw=0.6)
        # отрисовка графика 3
        for i in range(len(x_snir)):
            if is_approx3 != 1:
                ax_3.plot(x_snir[i], y_snir[i], color=vec_col[i], linestyle=vec_lst[i], lw=vec_lwd[i], label=leg_snir[i])
            else:
                ax_3.plot(x_snir[i], y_snir[i], color=vec_col[i], linestyle='--', lw=0.7)
            if self.adapt_mean == 1:
                ax_3.hlines(np.mean(y_snir[i]), vec_axissnir[0], vec_axissnir[1], color=vec_col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.adapt_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
            ax_3.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axisdepth)
        ax_2.axis(vec_axisatten)
        ax_3.axis(vec_axissnir)
        ax_1.grid()
        ax_2.grid()
        ax_3.grid()
        plt.show()

    def get_float(self, x, y):
        # преобразование типа к float
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        return [x, y]

    def get_style(self):
        # выбор стиля графиков
        if self.adapt_style == 1:
            vec_col, vec_lst, vec_lwd = [self.vec_col1, self.vec_lst1, self.vec_lwd1]
        else:
            vec_col, vec_lst, vec_lwd = [self.vec_col2, self.vec_lst2, self.vec_lwd2]
        return [vec_col, vec_lst, vec_lwd]

    def get_axes(self, x, y):
        # определение границ графика
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
        vec_axis = [min_x, max_x, min_y, max_y]
        return vec_axis

    def get_approx(self, x, y):
        x_i, y_i = [x, y]
        step = (x_i[1] - x_i[0]) / 10
        x_i_new = np.arange(min(x_i), max(x_i) + step, step)
        # аппроксимация
        y_i_new = cl.approx(self.approx, x_i_new, x_i, y_i)
        # интерполяция
        # coef = np.polyfit(x_i, y_i, self.approx)
        # y_i_new = np.polyval(coef, x_i_new)
        return [x_i_new, y_i_new]