import matplotlib.pyplot as plt
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль отображения характеристик сигналов и помех (L3)")

class Signals:
    """Класс вывода графика характеристик сигналов и помех для пользователя"""

    def __init__(self, id):
        self.id = id
        self.signals_style = []
        self.signals_mean = []
        self.signals_norm = []
        self.signals_db = []
        self.signals_legend = []
        self.str_axis = ["T", "Amp"]
        self.vec_col1 = []
        self.vec_lst1 = []
        self.vec_lwd1 = []
        self.vec_col2 = []
        self.vec_lst2 = []
        self.vec_lwd2 = []

    def set(self, init):
        self.signals_style = init[5]
        self.signals_mean = init[6]
        self.signals_norm = init[7]
        self.signals_db = init[8]
        self.signals_legend = init[9]
        self.vec_col1 = ['#000000', '#b22222', '#00008b', '#336600', '#996600']
        self.vec_lst1 = ['-', '-', '-', '-', '-']
        self.vec_lwd1 = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.vec_col2 = ['#000000', '#000000', '#000000', '#000000', '#000000']
        self.vec_lst2 = ['-', '--', '-.', '-', '--']
        self.vec_lwd2 = [1.0, 1.0, 1.0, 0.1, 0.1]

    def get(self):
        res = []
        res.append(self.signals_style)
        res.append(self.signals_mean)
        res.append(self.signals_norm)
        res.append(self.signals_db)
        res.append(self.signals_legend)
        res.append(self.str_axis)
        return res

    def print(self):
        print("Параметры отображения характеристик сигналов и помех (L3):")
        print("\tsignals_style = ", self.signals_style)
        print("\tsignals_mean = ", self.signals_mean)
        print("\tsignals_norm = ", self.signals_norm)
        print("\tsignals_db = ", self.signals_db)
        print("\tsignals_legend = ", self.signals_legend)
        print("\tstr_axis = ", self.str_axis)

    def draw_time(self, x, y_amp, y_deg, y_band, signals_strleg):
        plt.title("Графики сигналов и помех")
        str = ["par", "deg"]
        # приведение типа к float
        x, y_amp, y_deg, y_band = self.get_float(x, y_amp, y_deg, y_band)
        y = y_amp
        # подписи графика
        plt.ylabel(str[0])
        plt.xlabel(str[1])
        # выбор стиля графиков
        vec_col, vec_lst = self.get_style()
        # нормировка и единицы измерения графика
        # max_y = np.amax(y)
        # for i in range(len(x)):
        #    if self.timefreq_norm == 1:
        #        y[i] = y[i] / max_y
        #    if self.timefreq_db == 1:
        #        y[i] = 20 * np.log10(abs(y[i]))
        max_y = np.amax(y)
        # границы отрисовки графика
        if self.signals_db == 1:
            vec_axis = [x[0].min(), x[0].max(), -70, max_y]
        else:
            vec_axis = [x[0].min(), x[0].max(), 0, max_y * 1.1]
        # отрисовка графика
        for i in range(len(x)):
            plt.plot(x[i], y[i], color=vec_col[i], linestyle='-', lw=0.7, label=signals_strleg[i])
            if self.signals_mean == 1:
                plt.hlines(np.mean(y[i]), -90, 90, color='#666666', linestyle='-', lw=0.6)
        # отображение легенды
        if self.signals_legend == 1:
            plt.legend(loc='lower right')
        # отображение графика
        plt.axis(vec_axis)
        plt.grid()
        plt.show()

    def get_float(self, x, y_amp, y_deg, y_band):
        # преобразование типа к float
        x = np.array(x, dtype='float64')
        y_amp = np.array(y_amp, dtype='float64')
        y_deg = np.array(y_deg, dtype='float64')
        y_band = np.array(y_band, dtype='float64')
        return [x, y_amp, y_deg, y_band]

    def get_style(self):
        # выбор стиля графиков
        if self.signals_style == 1:
            vec_col, vec_lst = [self.vec_col1, self.vec_lst1]
        else:
            vec_col, vec_lst = [self.vec_col2, self.vec_lst2]
        return [vec_col, vec_lst]