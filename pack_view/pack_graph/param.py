import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик параметра (L3)")

class Parameter:
    """Класс вывода графика характеристик адаптации для пользователя"""

    def __init__(self):
        # общие настройки графики
        self.graph_style = []
        self.graph_legend = []
        # параметры
        self.mean_par = []
        self.par_aprx = []
        self.str_axis = ["band", "amp [%]", "depth [dB]", "atten [dB]", "snir [dB]", "ber"]
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_mrk1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []
        self.vec_mrk2 = []

    def set(self, init):
        self.graph_style = init[0]
        self.graph_legend = init[1]
        self.mean_par = init[15]
        self.par_aprx = init[19]
        self.vec_col1 = ['#000000', '#d1281f', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.2, 1.2, 1.2, 1.2, 1.2]
        self.vec_mrk1 = ['o', 'v', 'D', 'S', 'P']
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.0, 1.2, 1.2, 1.2, 0.1]
        self.vec_mrk2 = ['o', 'v', 'D', 'S', 'P']

    def get(self):
        res = []
        res.append(self.graph_style)
        res.append(self.graph_legend)
        res.append(self.mean_par)
        res.append(self.par_aprx)
        res.append(self.str_axis)
        return res

    def print(self):
        print("Параметры отображения характеристик параметра (L3):")
        print("\tgraph_style = ", self.graph_style)
        print("\tgraph_legend = ", self.graph_legend)
        print("\tmean_par = ", self.mean_par)
        print("\tpar_aprx = ", self.par_aprx)
        print("\tstr_axis = ", self.str_axis)

    def draw_graph(self, x_par0, y_dpt, x_par1, y_atn, x_par2, y_snir, str_mean, str_snir, id_script):
        # приведение типа к float
        x_par0, y_dpt = self.get_float(x_par0, y_dpt)
        x_par1, y_atn = self.get_float(x_par1, y_atn)
        x_par2, y_snir = self.get_float(x_par2, y_snir)
        # инициализация оси x
        if id_script == 6:
            str_buf = self.str_axis[0]
        else:
            str_buf = self.str_axis[1]
        # границы отрисовки графика
        vec_axis_depth = self.get_axes(x_par0, y_dpt)
        vec_axis_atten = self.get_axes(x_par1, y_atn)
        vec_axis_snir = self.get_axes(x_par2, y_snir)
        # выбор стиля графиков
        col, stl, wdt, mrk = self.get_style()
        # создаём окно с областями
        fig = plt.figure("Parametric modeling", figsize=(19, 5.5))
        fig.suptitle("Параметрическое моделирование", fontsize=14, fontweight='bold')
        ax_1 = fig.add_subplot(1, 3, 1)
        ax_2 = fig.add_subplot(1, 3, 2)
        ax_3 = fig.add_subplot(1, 3, 3)
        ax_1.set(title='Подавление помех', xlabel=str_buf, ylabel=self.str_axis[2])
        ax_2.set(title='Ослабление сигнала', xlabel=str_buf, ylabel=self.str_axis[3])
        ax_3.set(title='ОСШП', xlabel=str_buf, ylabel=self.str_axis[4])
        # график 1
        for i in range(len(x_par0)):
            # аппроксимация
            x_i_new, y_i_new = self.get_approx_gr(x_par0[i], y_dpt[i])
            ax_1.plot(x_i_new, y_i_new, color=col[i], linestyle=stl[i], lw=wdt[i], label=str_mean[i],
                      markersize=6, marker=mrk[i])
            # реальный сигнал
            # ax_1.scatter(x_par0[i], y_dpt[i], s=20, color=col[i])
            # ax_1.plot(x_par0[i], y_dpt[i], color=col[i], linestyle='--', lw=0.7)
            if self.mean_par == 1:
                ax_1.hlines(np.mean(y_dpt[i]), vec_axis_depth[0], vec_axis_depth[1], color=col[i], linestyle='--',
                            lw=0.6)
        # график 2
        for i in range(len(x_par1)):
            # аппроксимация
            x_i_new, y_i_new = self.get_approx_gr(x_par1[i], y_atn[i])
            ax_2.plot(x_i_new, y_i_new, color=col[i], linestyle=stl[i], lw=wdt[i], label=str_mean[i],
                      markersize=6, marker=mrk[i])
            # реальный сигнал
            # ax_2.scatter(x_par1[i], y_atn[i], s=20, color=col[i])
            # ax_2.plot(x_par1[i], y_atn[i], color=col[i], linestyle='--', lw=0.7)
            if self.mean_par == 1:
                ax_2.hlines(np.mean(y_atn[i]), vec_axis_atten[0], vec_axis_atten[1], color=col[i], linestyle='--', lw=0.6)
        # график 3
        for i in range(len(x_par2)):
            # аппроксимация
            x_i_new, y_i_new = self.get_approx_gr(x_par2[i], y_snir[i])
            ax_3.plot(x_i_new, y_i_new, color=col[i], linestyle=stl[i], lw=wdt[i], label=str_snir[i],
                      markersize=6, marker=mrk[i])
            # реальный сигнал
            # ax_3.scatter(x_par2[i], y_snir[i], s=20, color=col[i])
            # ax_3.plot(x_par2[i], y_snir[i], color=col[i], linestyle='--', lw=0.7)
            if self.mean_par == 1:
                ax_2.hlines(np.mean(y_snir[i]), vec_axis_snir[0], vec_axis_snir[1], color=col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax_1.legend(loc='lower right')
            ax_2.legend(loc='lower right')
            ax_3.legend(loc='lower right')
        # отображение графика
        ax_1.axis(vec_axis_depth)
        ax_2.axis(vec_axis_atten)
        ax_3.axis(vec_axis_snir)
        ax_1.grid()
        ax_2.grid()
        ax_3.grid()
        plt.show()

    def draw_ber(self, x_par, y_ber, str_snir, id_script):
        # приведение типа к float
        x_par, y_ber = self.get_float(x_par, y_ber)
        # границы отрисовки графика
        vec_axis_ber = self.get_axes(x_par, y_ber)
        # выбор стиля графиков
        col, stl, wdt, mrk = self.get_style()
        # создаём окно с областями
        fig = plt.figure("Parametric modeling", figsize=(5.7, 5.5))
        fig.suptitle("Параметрическое моделирование", fontsize=14, fontweight='bold')
        ax_1 = fig.add_subplot(1, 1, 1)
        ax_1.set(title='Частота битовых ошибок', xlabel=self.str_axis[4], ylabel=self.str_axis[5])
        # график
        for i in range(len(x_par)):
            # аппроксимация
            x_i_new, y_i_new = self.get_approx_ber(x_par[i], y_ber[i])
            ax_1.plot(x_i_new, y_i_new, color=col[i], linestyle=stl[i], lw=wdt[i], label=str_snir[i],
                      markersize=6, marker=mrk[i])
            # реальный сигнал
            # ax_1.scatter(x_par[i], y_ber[i], s=20, color=col[i])
            # ax_1.plot(x_par[i], y_ber[i], color=col[i], linestyle=stl[i], lw=wdt[i], label=str_snir[i])
            if self.mean_par == 1:
                ax_1.hlines(np.mean(y_ber[i]), vec_axis_ber[0], vec_axis_ber[1], color=col[i], linestyle='--', lw=0.6)
        # отображение легенды
        if self.graph_legend == 1:
            ax_1.legend(loc='lower left')
        # отображение графика
        vec_axis_ber[0] = vec_axis_ber[0] - np.abs(vec_axis_ber[1]) * 0.1
        vec_axis_ber[1] = vec_axis_ber[1] + np.abs(vec_axis_ber[1]) * 0.1
        vec_axis_ber[2], vec_axis_ber[3] = 0.001, 1
        ax_1.axis(vec_axis_ber)
        ax_1.semilogy()
        ax_1.grid()
        plt.show()

    def get_float(self, x, y):
        # преобразование типа к float
        x = np.array(x, dtype='float64')
        y = np.array(y, dtype='float64')
        return [x, y]

    def get_style(self):
        # выбор стиля графиков
        if self.graph_style == 0:
            vec_col, vec_lst, vec_lwd, vec_mrk = [self.vec_col1, self.vec_lst1, self.vec_lwd1, self.vec_mrk1]
        else:
            vec_col, vec_lst, vec_lwd, vec_mrk = [self.vec_col2, self.vec_lst2, self.vec_lwd2, self.vec_mrk2]
        return [vec_col, vec_lst, vec_lwd, vec_mrk]

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

    def get_approx_gr(self, x, y):
        x_i, y_i = [x, y]
        step = (x_i[1] - x_i[0]) / 2
        x_i_new = np.arange(min(x_i), max(x_i) + step, step)
        # аппроксимация
        y_i_new = cl.approx(self.par_aprx, x_i_new, x_i, y_i)
        # интерполяция
        # coef = np.polyfit(x_i, y_i, self.approx)
        # y_i_new = np.polyval(coef, x_i_new)
        return [x_i_new, y_i_new]

    def get_approx_ber(self, x, y):
        x_i, y_i = [x, y]
        step = (x_i[1] - x_i[0]) / 4
        x_i_new = np.arange(min(x_i), max(x_i) + step, step)
        # аппроксимация
        y_i_new = cl.approx(self.par_aprx, x_i_new, x_i, y_i)
        # интерполяция
        # coef = np.polyfit(x_i, y_i, self.approx)
        # y_i_new = np.polyval(coef, x_i_new)
        return [x_i_new, y_i_new]