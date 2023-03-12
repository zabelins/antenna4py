import numpy as np

MSG_RES = "\nРЕЗУЛЬТАТЫ РАСЧЁТА"
MSG_STATIC = "Для диаграммы направленности:"
MSG_TIME = "Для временных характеристик:"
MSG_PARAM = "Для параметрических характеристик:"

if __name__ == "__main__":
    print("Вы запустили модуль отчётов о работе программы (L2)")

class Report:
    """Класс отчётов о работе программы"""

    def __init__(self):
        self.is_title = 0

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры отчётов о работе программы (L2):")
        print("\t-")

    def info_ptn(self, vec, time):
        # распаковка исходных данных
        vec_snir, vec_insnir, vec_outsnir = vec[1], vec[2], vec[3]
        vec_indpt, vec_inatn, vec_outdpt, vec_outatn = vec[4], vec[5], vec[6], vec[7]
        # инициализация параметров
        len_int, len_sig = vec_indpt.shape[1], vec_inatn.shape[1]
        dpt_int, dpt_sum = np.zeros(shape=[len_int]), 0
        atn_sig, atn_sum = np.zeros(shape=[len_sig]), 0
        # расчёт глубины подавления
        for i in range(len_int):
            dpt_int[i] = self.get_ras(vec_indpt[time][i], vec_outdpt[time][i])
            dpt_sum = dpt_sum + dpt_int[i]
        # расчёт ослабления сигнала
        for i in range(len_sig):
            atn_sig[i] = self.get_ras(vec_inatn[time][i], vec_outatn[time][i])
            atn_sum = atn_sum + atn_sig[i]
        # расчёт осшп
        snirio = np.array([vec_snir[time][0], vec_insnir[time][0], vec_outsnir[time][0]])
        snirdif = snirio[2] - snirio[0]
        # округление до сотых
        dpt_int = self.get_round(dpt_int)
        dpt_sum = self.get_round(dpt_sum)
        atn_sig = self.get_round(atn_sig)
        atn_sum = self.get_round(atn_sum)
        snirio = self.get_round(snirio)
        snirdif = self.get_round(snirdif)
        # вывод результатов
        if self.is_title == 0:
            print(MSG_RES)
            self.is_title = 1
        print(MSG_STATIC)
        print("\tpattern_dptint = ", dpt_int)
        print("\tpattern_dptsum = ", dpt_sum)
        print("\tpattern_atnsig = ", atn_sig)
        print("\tpattern_atnsum = ", atn_sum)
        print("\tpattern_snirio = ", snirio)
        print("\tpattern_snirdif = ", snirdif)

    def info_time(self, vec):
        id_par = -1
        # распаковка исходных данных
        seq_intime, seq_indiscr, seq_inbits = vec[1], vec[2], vec[3]
        vec_meansnir, vec_meanindpt, vec_meaninatn, vec_meaninber, vec_meaninsnir = vec[4], vec[5], vec[6], vec[7], vec[8]
        vec_meanoutdpt, vec_meanoutatn, vec_meanoutber, vec_meanoutsnir = vec[9], vec[10], vec[11], vec[12]
        # инициализация параметров
        len_int, len_sig = vec_meanindpt.shape[1], vec_meaninatn.shape[1]
        dpt_int, dpt_sum = np.zeros(shape=[len_int]), 0
        atn_sig, atn_sum = np.zeros(shape=[len_sig]), 0
        # расчёт глубины подавления
        for i in range(len_int):
            dpt_int[i] = self.get_ras(vec_meanindpt[id_par][i], vec_meanoutdpt[id_par][i])
            dpt_sum = dpt_sum + dpt_int[i]
        # расчёт ослабления сигнала
        for i in range(len_sig):
            atn_sig[i] = self.get_ras(vec_meaninatn[id_par][i], vec_meanoutatn[id_par][i])
            atn_sum = atn_sum + atn_sig[i]
        # расчёт осшп
        snir_io = np.array([vec_meansnir[id_par], vec_meaninsnir[id_par], vec_meanoutsnir[id_par]])
        snir_dif = snir_io[2] - snir_io[0]
        # характеристики битового потока
        ber_io = np.array([vec_meaninber[id_par], vec_meanoutber[id_par]])
        # округление до сотых
        dpt_int = self.get_round(dpt_int)
        dpt_sum = self.get_round(dpt_sum)
        atn_sig = self.get_round(atn_sig)
        atn_sum = self.get_round(atn_sum)
        snir_io = self.get_round(snir_io)
        snir_dif = self.get_round(snir_dif)
        # вывод результатов
        if self.is_title == 0:
            print(MSG_RES)
            self.is_title = 1
        print(MSG_TIME)
        print("\ttime_dptint = ", dpt_int)
        print("\ttime_dptsum = ", dpt_sum)
        print("\ttime_atnsig = ", atn_sig)
        print("\ttime_atnsum = ", atn_sum)
        print("\ttime_snirio = ", snir_io)
        print("\ttime_snirdif = ", snir_dif)
        print("\ttime_berio = ", ber_io)
        print("\ttime_bertime = ", seq_intime)
        print("\ttime_berdscr = ", seq_indiscr)
        print("\ttime_berbits = ", seq_inbits)

    def info_par(self, vec):
        # распаковка исходных данных
        vec_meansnir, vec_meanindpt, vec_meaninatn, vec_meaninber, vec_meaninsnir = vec[4], vec[5], vec[6], vec[7], vec[8]
        vec_meanoutdpt, vec_meanoutatn, vec_meanoutber, vec_meanoutsnir = vec[9], vec[10], vec[11], vec[12]
        # инициализация параметров
        len_int, len_sig = vec_meanindpt.shape[1], vec_meaninatn.shape[1]
        dpt_int, dpt_sum = np.zeros(shape=[len_int]), 0
        atn_sig, atn_sum = np.zeros(shape=[len_sig]), 0
        # расчёт глубины подавления
        for i in range(len_int):
            buf1, buf2 = vec_meanindpt.T, vec_meanoutdpt.T
            dpt_int[i] = self.get_ras(np.mean(buf1[i]), np.mean(buf2[i]))
            dpt_sum = dpt_sum + dpt_int[i]
        # расчёт ослабления сигнала
        for i in range(len_sig):
            buf1, buf2 = vec_meaninatn.T, vec_meanoutatn.T
            atn_sig[i] = self.get_ras(np.mean(buf1[i]), np.mean(buf2[i]))
            atn_sum = atn_sum + atn_sig[i]
        # расчёт осшп
        snirio = np.array([np.mean(vec_meansnir), np.mean(vec_meaninsnir), np.mean(vec_meanoutsnir)])
        snirdif = snirio[2] - snirio[0]
        # округление до сотых
        dpt_int = self.get_round(dpt_int)
        dpt_sum = self.get_round(dpt_sum)
        atn_sig = self.get_round(atn_sig)
        atn_sum = self.get_round(atn_sum)
        snirio = self.get_round(snirio)
        snirdif = self.get_round(snirdif)
        # вывод результатов
        if self.is_title == 0:
            print(MSG_RES)
            self.is_title = 1
        print(MSG_PARAM)
        print("\tpar_dptint = ", dpt_int)
        print("\tpar_dptsum = ", dpt_sum)
        print("\tpar_atnsig = ", atn_sig)
        print("\tpar_atnsum = ", atn_sum)
        print("\tpar_snirio = ", snirio)
        print("\tpar_snirdif = ", snirdif)
        print("\tpar_berin = ", vec_meaninber)
        print("\tpar_berout = ", vec_meanoutber)

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

