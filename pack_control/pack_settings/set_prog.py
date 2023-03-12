import math

if __name__ == "__main__":
    print("Вы запустили модуль настроек вывода информации (L3)")

class Set_prog:
    """Класс настроек вывода информации для пользователя"""

    def __init__(self):
        # ОБЩИЕ НАСТРОЙКИ ГРАФИКИ
        # стиль отрисовки (0=цветной, 1=чб), легенда (0=нет, 1=да)
        self.graph_style = 0
        self.graph_legend = 1
        # ОТОБРАЖЕНИЕ
        # диаграмма нпаравленности (0=нет, 1=да), сигналы (0=нет, 1=да), помехи (0=нет, 1=да),
        # адаптация (0=нет, 1=да), выход (0=нет, 1=да), параметр (0=нет, 1=да)
        self.view_ptn = 1
        self.view_sig = 1
        self.view_int = 1
        self.view_cpl = 1
        self.view_adp = 1
        self.view_out = 1
        self.view_par = 1
        # СРЕДНИЙ УРОВЕНЬ
        # диаграмма нпаравленности (0=нет, 1=да), сигналы (0=нет, 1=да), помехи (0=нет, 1=да),
        # адаптация (0=нет, 1=да), выход (0=нет, 1=да)
        self.mean_ptn = 0
        self.mean_sig = 0
        self.mean_int = 0
        self.mean_cpl = 0
        self.mean_adp = 1
        self.mean_out = 0
        self.mean_par = 0
        # ДИАГРАММА НАРПАВЛЕННОСТИ
        # нормировка (0=нет, 1=да), дБ (0=нет, 1=да)
        self.ptn_norm = 1
        self.ptn_db = 1
        # ГРАФИКИ СИГНАЛОВ
        # множитель (flt)
        self.amp_coef = 1 * math.pow(10, -6)
        # ГРАФИКИ ПАРАМЕТРОВ
        # аппроксимация (int)
        self.par_aprx = 5
        # ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
        # сохранение (0=нет, 1=да), вывод (0=нет, 1=да)
        self.calc_save = 0
        self.calc_info = 1
        # СОХРАНЕНИЕ ФАЙЛОВ
        self.dir_data = 'dir_data'
        self.dir_net = 'dir_net'
        self.dir_set = 'dir_set'

    def set(self, init):
        self.graph_style = init[0]
        self.graph_legend = init[1]
        self.view_ptn = init[2]
        self.view_sig = init[3]
        self.view_int = init[4]
        self.view_cpl = init[5]
        self.view_adp = init[6]
        self.view_out = init[7]
        self.view_par = init[8]
        self.mean_ptn = init[9]
        self.mean_sig = init[10]
        self.mean_int = init[11]
        self.mean_cpl = init[12]
        self.mean_adp = init[13]
        self.mean_out = init[14]
        self.mean_par = init[15]
        self.ptn_norm = init[16]
        self.ptn_db = init[17]
        self.amp_coef = init[18]
        self.par_aprx = init[19]
        self.calc_save = init[20]
        self.calc_info = init[21]
        self.dir_data = init[22]
        self.dir_net = init[23]
        self.dir_set = init[24]

    def get(self):
        res = []
        res.append(self.graph_style)
        res.append(self.graph_legend)
        res.append(self.view_ptn)
        res.append(self.view_sig)
        res.append(self.view_int)
        res.append(self.view_cpl)
        res.append(self.view_adp)
        res.append(self.view_out)
        res.append(self.view_par)
        res.append(self.mean_ptn)
        res.append(self.mean_sig)
        res.append(self.mean_int)
        res.append(self.mean_cpl)
        res.append(self.mean_adp)
        res.append(self.mean_out)
        res.append(self.mean_par)
        res.append(self.ptn_norm)
        res.append(self.ptn_db)
        res.append(self.amp_coef)
        res.append(self.par_aprx)
        res.append(self.calc_save)
        res.append(self.calc_info)
        res.append(self.dir_data)
        res.append(self.dir_net)
        res.append(self.dir_set)
        return res

    def print(self):
        print("Настройки вывода информации (L3):")
        print("\tgraph_style = ", self.graph_style)
        print("\tgraph_legend = ", self.graph_legend)
        print("\tview_ptn = ", self.view_ptn)
        print("\tview_sig = ", self.view_sig)
        print("\tview_int = ", self.view_int)
        print("\tview_cpl = ", self.view_cpl)
        print("\tview_adp = ", self.view_adp)
        print("\tview_out = ", self.view_out)
        print("\tview_par = ", self.view_par)
        print("\tmean_ptn = ", self.mean_ptn)
        print("\tmean_sig = ", self.mean_sig)
        print("\tmean_int = ", self.mean_int)
        print("\tmean_cpl = ", self.mean_cpl)
        print("\tmean_adp = ", self.mean_adp)
        print("\tmean_out = ", self.mean_out)
        print("\tmean_par = ", self.mean_par)
        print("\tptn_norm = ", self.ptn_norm)
        print("\tptn_db = ", self.ptn_db)
        print("\tamp_coef = ", self.amp_coef)
        print("\tpar_aprx = ", self.par_aprx)
        print("\tcalc_save = ", self.calc_save)
        print("\tcalc_info = ", self.calc_info)
        print("\tdir_data = ", self.dir_data)
        print("\tdir_net = ", self.dir_net)
        print("\tdir_set = ", self.dir_set)

