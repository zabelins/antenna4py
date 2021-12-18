import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль отчётов о работе программы (L2)")

class Report:
    """Класс отчётов о работе программы"""

    def __init__(self, id):
        self.id = id
        self.is_title = 0

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры отчётов о работе программы (L2):")
        print("\t-")

    def info_pattern(self, vec, time):
        # распаковка исходных данных
        vec_indepth, vec_inatten, vec_insnir = vec[1], vec[2], vec[3]
        vec_outdepth, vec_outatten, vec_outsnir, vec_snir = vec[4], vec[5], vec[6], vec[7]
        # инициализация параметров
        len_int, len_sig = vec_indepth.shape[1], vec_inatten.shape[1]
        pattern_depthint, pattern_depthsum = np.zeros(shape=[len_int]), 0
        pattern_attensig, pattern_attensum = np.zeros(shape=[len_sig]), 0
        # расчёт глубины подавления
        for i in range(len_int):
            pattern_depthint[i] = self.get_ras(vec_indepth[time][i], vec_outdepth[time][i])
            pattern_depthsum = pattern_depthsum + pattern_depthint[i]
        # расчёт ослабления сигнала
        for i in range(len_sig):
            pattern_attensig[i] = self.get_ras(vec_inatten[time][i], vec_outatten[time][i])
            pattern_attensum = pattern_attensum + pattern_attensig[i]
        # расчёт осшп
        pattern_snirio = np.array([vec_snir[time][0], vec_insnir[time][0], vec_outsnir[time][0]])
        pattern_snirdif = pattern_snirio[2] - pattern_snirio[0]
        # округление до сотых
        pattern_depthint = self.get_round(pattern_depthint)
        pattern_depthsum = self.get_round(pattern_depthsum)
        pattern_attensig = self.get_round(pattern_attensig)
        pattern_attensum = self.get_round(pattern_attensum)
        pattern_snirio = self.get_round(pattern_snirio)
        pattern_snirdif = self.get_round(pattern_snirdif)
        # вывод результатов
        if self.is_title == 0:
            print("\nРЕЗУЛЬТАТЫ РАСЧЁТА МОДЕЛИ ААР")
            self.is_title = 1
        print("Для диаграммы направленности:")
        print("\tpattern_depthint = ", pattern_depthint)
        print("\tpattern_depthsum = ", pattern_depthsum)
        print("\tpattern_attensig = ", pattern_attensig)
        print("\tpattern_attensum = ", pattern_attensum)
        print("\tpattern_snirio = ", pattern_snirio)
        print("\tpattern_snirdif = ", pattern_snirdif)

    def info_adapt(self, vec):
        id_par = -1
        # распаковка исходных данных
        vec_meanindepth, vec_meaninatten, vec_meaninsnir = vec[1], vec[2], vec[3]
        vec_meanoutdepth, vec_meanoutatten, vec_meanoutsnir, vec_meansnir = vec[4], vec[5], vec[6], vec[7]
        # инициализация параметров
        len_int, len_sig = vec_meanindepth.shape[1], vec_meaninatten.shape[1]
        time_depthint, time_depthsum = np.zeros(shape=[len_int]), 0
        time_attensig, time_attensum = np.zeros(shape=[len_sig]), 0
        # расчёт глубины подавления
        for i in range(len_int):
            time_depthint[i] = self.get_ras(vec_meanindepth[id_par][i], vec_meanoutdepth[id_par][i])
            time_depthsum = time_depthsum + time_depthint[i]
        # расчёт ослабления сигнала
        for i in range(len_sig):
            time_attensig[i] = self.get_ras(vec_meaninatten[id_par][i], vec_meanoutatten[id_par][i])
            time_attensum = time_attensum + time_attensig[i]
        # расчёт осшп
        time_snirio = np.array([vec_meansnir[id_par], vec_meaninsnir[id_par], vec_meanoutsnir[id_par]])
        time_snirdif = time_snirio[2] - time_snirio[0]
        # округление до сотых
        time_depthint = self.get_round(time_depthint)
        time_depthsum = self.get_round(time_depthsum)
        time_attensig = self.get_round(time_attensig)
        time_attensum = self.get_round(time_attensum)
        time_snirio = self.get_round(time_snirio)
        time_snirdif = self.get_round(time_snirdif)
        # вывод результатов
        if self.is_title == 0:
            print("\nРЕЗУЛЬТАТЫ РАСЧЁТА МОДЕЛИ ААР")
            self.is_title = 1
        print("Для временных характеристик адаптации:")
        print("\ttime_depthint = ", time_depthint)
        print("\ttime_depthsum = ", time_depthsum)
        print("\ttime_attensig = ", time_attensig)
        print("\ttime_attensum = ", time_attensum)
        print("\ttime_snirio = ", time_snirio)
        print("\ttime_snirdif = ", time_snirdif)

    def info_mean(self, vec):
        # распаковка исходных данных
        vec_meanindepth, vec_meaninatten, vec_meaninsnir = vec[1], vec[2], vec[3]
        vec_meanoutdepth, vec_meanoutatten, vec_meanoutsnir, vec_meansnir = vec[4], vec[5], vec[6], vec[7]
        # инициализация параметров
        len_int, len_sig = vec_meanindepth.shape[1], vec_meaninatten.shape[1]
        par_depthint, par_depthsum = np.zeros(shape=[len_int]), 0
        par_attensig, par_attensum = np.zeros(shape=[len_sig]), 0
        # расчёт глубины подавления
        for i in range(len_int):
            buf1, buf2 = vec_meanindepth.T, vec_meanoutdepth.T
            par_depthint[i] = self.get_ras(np.mean(buf1[i]), np.mean(buf2[i]))
            par_depthsum = par_depthsum + par_depthint[i]
        # расчёт ослабления сигнала
        for i in range(len_sig):
            buf1, buf2 = vec_meaninatten.T, vec_meanoutatten.T
            par_attensig[i] = self.get_ras(np.mean(buf1[i]), np.mean(buf2[i]))
            par_attensum = par_attensum + par_attensig[i]
        # расчёт осшп
        par_snirio = np.array([np.mean(vec_meansnir), np.mean(vec_meaninsnir), np.mean(vec_meanoutsnir)])
        par_snirdif = par_snirio[2] - par_snirio[0]
        # округление до сотых
        par_depthint = self.get_round(par_depthint)
        par_depthsum = self.get_round(par_depthsum)
        par_attensig = self.get_round(par_attensig)
        par_attensum = self.get_round(par_attensum)
        par_snirio = self.get_round(par_snirio)
        par_snirdif = self.get_round(par_snirdif)
        # вывод результатов
        if self.is_title == 0:
            print("\nРЕЗУЛЬТАТЫ РАСЧЁТА МОДЕЛИ ААР")
            self.is_title = 1
        print("Для параметрических характеристик адаптации:")
        print("\tpar_depthint = ", par_depthint)
        print("\tpar_depthsum = ", par_depthsum)
        print("\tpar_attensig = ", par_attensig)
        print("\tpar_attensum = ", par_attensum)
        print("\tpar_snirio = ", par_snirio)
        print("\tpar_snirdif = ", par_snirdif)


    def get_one2db(self, num):
        # перевод числа в дБ
        return 20 * np.log10(abs(num))

    def get_dbras(self, innum, outnum):
        # разность децибелльных параметров
        db_out = self.get_one2db(outnum)
        db_in = self.get_one2db(innum)
        return db_out - db_in

    def get_ras(self, innum, outnum):
        # разность параметров
        return outnum - innum

    def get_round(self, num):
        # округление до сотых
        return np.round(num * 100) / 100

