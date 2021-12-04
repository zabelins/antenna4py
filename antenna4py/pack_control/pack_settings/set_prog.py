if __name__ == "__main__":
    print("Вы запустили модуль настроек вывода информации (L3)")

class Set_prog:
    """Класс настроек вывода информации для пользователя"""

    def __init__(self, id):
        self.id = id
        # общие настройки графики
        self.graph_style = 0
        self.graph_legend = 1
        # настройки графика диаграммы направленности
        self.pattern_mean = 0
        self.pattern_norm = 1
        self.pattern_db = 1
        # настройки графика сигналов
        self.signals_mean = 0
        # настройки графика сигналов
        self.output_mean = 0
        # настройки графика адаптации
        self.adapt_mean = 1
        self.adapt_approx = 5
        # дополнительные настройки
        self.calc_save = 1
        self.calc_info = 1
        self.calc_anima = 0
        # сохранение файлов
        self.dir_data = 'dir_data'
        self.dir_net = 'dir_net'
        self.dir_set = 'dir_set'

    def set(self, init):
        self.graph_style = init[0]
        self.graph_legend = init[1]
        self.pattern_mean = init[2]
        self.pattern_norm = init[3]
        self.pattern_db = init[4]
        self.signals_mean = init[5]
        self.output_mean = init[6]
        self.adapt_mean = init[7]
        self.adapt_approx = init[8]
        self.calc_save = init[9]
        self.calc_info = init[10]
        self.calc_anima = init[11]
        self.dir_data = init[12]
        self.dir_net = init[13]
        self.dir_set = init[14]

    def get(self):
        res = []
        res.append(self.graph_style)
        res.append(self.graph_legend)
        res.append(self.pattern_mean)
        res.append(self.pattern_norm)
        res.append(self.pattern_db)
        res.append(self.signals_mean)
        res.append(self.output_mean)
        res.append(self.adapt_mean)
        res.append(self.adapt_approx)
        res.append(self.calc_save)
        res.append(self.calc_info)
        res.append(self.calc_anima)
        res.append(self.dir_data)
        res.append(self.dir_net)
        res.append(self.dir_set)
        return res

    def print(self):
        print("Настройки вывода информации (L3):")
        print("\tgraph_style = ", self.graph_style)
        print("\tgraph_legend = ", self.graph_legend)
        print("\tpattern_mean = ", self.pattern_mean)
        print("\tpattern_norm = ", self.pattern_norm)
        print("\tpattern_db = ", self.pattern_db)
        print("\tsignals_mean = ", self.signals_mean)
        print("\tadapt_mean = ", self.adapt_mean)
        print("\tadapt_approx = ", self.adapt_approx)
        print("\tcalc_save = ", self.calc_save)
        print("\tcalc_info = ", self.calc_info)
        print("\tcalc_anima = ", self.calc_anima)
        print("\tdir_data = ", self.dir_data)
        print("\tdir_net = ", self.dir_net)
        print("\tdir_set = ", self.dir_set)

