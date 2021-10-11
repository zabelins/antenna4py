if __name__ == "__main__":
    print("Вы запустили модуль настроек вывода информации (L3)")

class Set_view:
    """Класс настроек вывода информации для пользователя"""

    def __init__(self, id):
        self.id = id
        # настройки графика диаграммы направленности
        self.pattern_style = 1
        self.pattern_mean = 0
        self.pattern_norm = 1
        self.pattern_db = 1
        self.pattern_legend = 1
        # настройки графика сигналов
        self.signals_style = 1
        self.signals_mean = 0
        self.signals_legend = 1
        # настройки графика сигналов
        self.output_style = 1
        self.output_mean = 0
        self.output_legend = 1
        # настройки графика адаптации
        self.adapt_style = 1
        self.adapt_mean = 1
        self.adapt_legend = 1
        # дополнительные настройки графики
        self.approx = 5
        self.animation = 0

    def set(self, init):
        self.pattern_style = init[0]
        self.pattern_mean = init[1]
        self.pattern_norm = init[2]
        self.pattern_db = init[3]
        self.pattern_legend = init[4]
        self.signals_style = init[5]
        self.signals_mean = init[6]
        self.signals_legend = init[7]
        self.output_style = init[8]
        self.output_mean = init[9]
        self.output_legend = init[10]
        self.adapt_style = init[11]
        self.adapt_mean = init[12]
        self.adapt_legend = init[13]
        self.approx = init[14]
        self.animation = init[15]
    def get(self):
        res = []
        res.append(self.pattern_style)
        res.append(self.pattern_mean)
        res.append(self.pattern_norm)
        res.append(self.pattern_db)
        res.append(self.pattern_legend)
        res.append(self.signals_style)
        res.append(self.signals_mean)
        res.append(self.signals_legend)
        res.append(self.output_style)
        res.append(self.output_mean)
        res.append(self.output_legend)
        res.append(self.adapt_style)
        res.append(self.adapt_mean)
        res.append(self.adapt_legend)
        res.append(self.approx)
        res.append(self.animation)
        return res

    def print(self):
        print("Настройки вывода информации (L3):")
        print("\tpattern_style = ", self.pattern_style)
        print("\tpattern_mean = ", self.pattern_mean)
        print("\tpattern_norm = ", self.pattern_norm)
        print("\tpattern_db = ", self.pattern_db)
        print("\tpattern_legend = ", self.pattern_legend)
        print("\tsignals_style = ", self.signals_style)
        print("\tsignals_mean = ", self.signals_mean)
        print("\tsignals_legend = ", self.signals_legend)
        print("\tadapt_style = ", self.adapt_style)
        print("\tadapt_mean = ", self.adapt_mean)
        print("\tadapt_legend = ", self.adapt_legend)
        print("\tapprox = ", self.approx)
        print("\tanimation = ", self.animation)

