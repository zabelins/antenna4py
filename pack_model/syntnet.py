import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль модели ДОС (L2)")

class Syntnet:
    """Класс моделирования схемы диаграммообразования"""

    def __init__(self):
        # дискретность управления
        self.ctl_stepphi = 0
        self.ctl_stepamp = 0
        # параметры сигналов
        self.msg_code = np.array([])
        # временные характеристики адаптации
        self.vec_inptn = np.array([])
        self.vec_indpt = np.array([])
        self.vec_inatn = np.array([])
        self.vec_insig = np.array([])
        self.vec_outptn = np.array([])
        self.vec_outdpt = np.array([])
        self.vec_outatn = np.array([])
        self.vec_outsig = np.array([])
        # усреднённые характеристики адаптации
        self.mean_indpt = np.array([])
        self.mean_inatn = np.array([])
        self.mean_inber = np.array([])
        self.mean_outdpt = np.array([])
        self.mean_outatn = np.array([])
        self.mean_outber = np.array([])
        # характеристики битового потока
        self.seq_intime = 0
        self.seq_indiscr = 0
        self.seq_inbits = 0
        self.seq_inber = 0
        self.seq_outtime = 0
        self.seq_outdiscr = 0
        self.seq_outbits = 0
        self.seq_outber = 0


    def set(self, init0, init1):
        self.ctl_stepphi = init1[5]
        self.ctl_stepamp = init1[6]
        self.msg_code = init0[12]

    def get(self):
        res = []
        res.append(self.ctl_stepphi)
        res.append(self.ctl_stepamp)
        res.append(self.msg_code)
        return res

    def print(self):
        print("Параметры модели ДОС (L2):")
        print("\tctl_stepphi = ", self.ctl_stepphi)
        print("\tctl_stepamp = ", self.ctl_stepamp)
        print("\tmsg_code = ", self.msg_code)

    def calc_out(self, out_set, out_env, out_array, out_proc):
        # распаковка исходных данных
        vec_deg, vec_time, vec_inweight, vec_outweight = out_set[0], out_set[1], out_proc[0], out_proc[1]
        vec_sigdeg, vec_intdeg, flag_mod, vec_code = out_env[0], out_env[3], out_env[6], out_env[7]
        vec_test, vec_eqdegsig, vec_eqdegint, vec_sum = out_array[3].T, out_array[4], out_array[5], out_array[11]
        # инициализируем размеры векторов
        self.init_vecmean(vec_time.shape[0], vec_deg.shape[0], vec_sigdeg.shape[1], vec_intdeg.shape[1])
        # диаграмма направленности системы
        self.calc_ptn(vec_test, vec_inweight, vec_outweight)
        # выходные сигналы системы
        self.calc_outsig(vec_sum, vec_inweight, vec_outweight)
        # глубина подавления помех
        self.calc_dpt(vec_deg, vec_intdeg, vec_eqdegint)
        # ослабление сигнала
        self.calc_atn(vec_deg, vec_sigdeg, vec_eqdegsig)
        # частота битовых ошибок
        self.calc_ber(flag_mod, vec_code)
        # усреднённые характеристики
        self.calc_mean()

    def get_out(self):
        out_syntnet = []
        out_syntnet.append(self.vec_inptn)
        out_syntnet.append(self.vec_indpt)
        out_syntnet.append(self.vec_inatn)
        out_syntnet.append(self.vec_insig)
        out_syntnet.append(self.vec_outptn)
        out_syntnet.append(self.vec_outdpt)
        out_syntnet.append(self.vec_outatn)
        out_syntnet.append(self.vec_outsig)
        out_syntnet.append(self.mean_indpt)
        out_syntnet.append(self.mean_inatn)
        out_syntnet.append(self.mean_inber)
        out_syntnet.append(self.mean_outdpt)
        out_syntnet.append(self.mean_outatn)
        out_syntnet.append(self.mean_outber)
        out_syntnet.append(self.seq_intime)
        out_syntnet.append(self.seq_indiscr)
        out_syntnet.append(self.seq_inbits)
        out_syntnet.append(self.seq_inber)
        out_syntnet.append(self.seq_outtime)
        out_syntnet.append(self.seq_outdiscr)
        out_syntnet.append(self.seq_outbits)
        out_syntnet.append(self.seq_outber)
        return out_syntnet

    def print_out(self):
        # проверка типа векторов на ndarray
        condit_1 = cl.is_ndarray([self.vec_inptn, self.vec_indpt, self.vec_inatn, self.vec_insig])
        condit_2 = cl.is_ndarray([self.vec_outptn, self.vec_outdpt, self.vec_outatn, self.vec_outsig])
        condit_3 = cl.is_ndarray([self.mean_indpt, self.mean_inatn, self.mean_outdpt, self.mean_outatn])
        condit_4 = cl.is_ndarray([self.mean_inber, self.mean_outber])
        # вывод размерностей векторов
        if condit_1 and condit_2 and condit_3 and condit_4:
            print("Диаграммо-образующая схема:")
            print("\tvec_inptn.shape = ", self.vec_inptn.shape)
            print("\tvec_indpt.shape = ", self.vec_indpt.shape)
            print("\tvec_inatn.shape = ", self.vec_inatn.shape)
            print("\tvec_insig.shape = ", self.vec_insig.shape)
            print("\tvec_outptn.shape = ", self.vec_outptn.shape)
            print("\tvec_outdpt.shape = ", self.vec_outdpt.shape)
            print("\tvec_outatn.shape = ", self.vec_outatn.shape)
            print("\tvec_outsig.shape = ", self.vec_outsig.shape)
            print("\tmean_indpt.shape = ", self.mean_indpt.shape)
            print("\tmean_inatn.shape = ", self.mean_inatn.shape)
            print("\tmean_inber.shape = ", self.mean_inber.shape)
            print("\tmean_outdpt.shape = ", self.mean_outdpt.shape)
            print("\tmean_outatn.shape = ", self.mean_outatn.shape)
            print("\tmean_outber.shape = ", self.mean_outber.shape)
        else:
            print("Ошибка проверки векторов ДОС")

    def calc_ptn(self, vec_test, vec_inweight, vec_outweight):
        # диаграммы направленности системы от времени
        for i in range(vec_outweight.shape[0]):
            self.vec_inptn[i] = abs(np.dot(vec_test, vec_inweight))
            self.vec_outptn[i] = abs(np.dot(vec_test, vec_outweight[i]))

    def calc_outsig(self, vec_sum, vec_inweight, vec_outweight):
        # выходные сигналы системы от времени
        for i in range(vec_outweight.shape[0]):
            self.vec_insig[i][0] = np.dot(vec_sum[0][i], vec_inweight)
            self.vec_outsig[i][0] = np.dot(vec_sum[0][i], vec_outweight[i])
        # усреднённые характеристики

    def calc_dpt(self, vec_deg, vec_intdeg, vec_eqdegint):
        # глубина подавления помехи от времени
        for i in range(vec_intdeg.shape[0]):
            self.vec_indpt[i] = self.calc_gain(vec_deg, vec_intdeg[i], vec_eqdegint[i], i, 1)
            self.vec_outdpt[i] = self.calc_gain(vec_deg, vec_intdeg[i], vec_eqdegint[i], i, 2)

    def calc_atn(self, vec_deg, vec_sigdeg, vec_eqdegsig):
        # ослабление сигнала от времени
        for i in range(vec_sigdeg.shape[0]):
            self.vec_inatn[i] = self.calc_gain(vec_deg, vec_sigdeg[i], vec_eqdegsig[i], i, 1)
            self.vec_outatn[i] = self.calc_gain(vec_deg, vec_sigdeg[i], vec_eqdegsig[i], i, 2)

    def calc_ber(self, flag_mod, vec_code):
        # частота битовых ошибок от времени
        if flag_mod == 1 and vec_code != []:
            vec_inbits, self.seq_intime, self.seq_indiscr, self.seq_inbits = self.detector_bpsk(self.vec_insig)
            vec_outbits, self.seq_outtime, self.seq_outdiscr, self.seq_outbits = self.detector_bpsk(self.vec_outsig)
            init_bits = vec_code[:-1]
            # проверка
            print("init_bits = ", init_bits)
            print("vec_inbits = ", vec_inbits)
            print("vec_outbits = ", vec_outbits)
            self.seq_inber = self.get_errfrq(init_bits, vec_inbits)
            self.seq_outber = self.get_errfrq(init_bits, vec_outbits)

    def calc_mean(self):
        # усреднённые характеристики
        self.mean_indpt = np.mean(self.vec_indpt, axis=0)
        self.mean_inatn = np.mean(self.vec_inatn, axis=0)
        self.mean_inber = np.array([self.seq_inber])
        self.mean_outdpt = np.mean(self.vec_outdpt, axis=0)
        self.mean_outatn = np.mean(self.vec_outatn, axis=0)
        self.mean_outber = np.array([self.seq_outber])

    def calc_gain(self, vec_deg, vec_sigdeg, vec_eqsigdeg, var_time, id_inout):
        # вычисление нормированного усиления по N реальным углам в 1 момент времени
        len_deg = vec_sigdeg.shape[0]
        out_gain = np.zeros(shape=[len_deg], dtype='float64')
        # номер учёта эквивалентных углов (1=реал, 2=экв)
        id_eq = 1
        # цикл по сигналам
        for i in range(len_deg):
            out_gain[i] = self.calc_meangain(vec_deg, vec_sigdeg[i], vec_eqsigdeg[i], var_time, id_inout, id_eq)
        return out_gain

    def calc_meangain(self, vec_deg, var_sigdeg, var_eqsigdeg, var_time, id_inout, id_eq):
        # вычисление нормированного усиления по 1 реальному углу в 1 момент времени
        deg_step = abs(vec_deg[1] - vec_deg[0])
        max_inptn = self.vec_inptn[var_time].max()
        vec_inout, id_sig = [], []
        # выбор ДН
        if id_inout == 1:
            # для исходной ДН
            vec_inout = self.vec_inptn
        if id_inout == 2:
            # для оптимальной ДН
            vec_inout = self.vec_outptn
        # выбор способа расчёта
        if id_eq == 1:
            # усиление по реальным сигналам
            ind_sig = self.get_deg2ind(var_sigdeg, vec_deg, deg_step)
            res = self.get_amp2db(vec_inout[var_time][ind_sig] / max_inptn)
        if id_eq == 2:
            # среднее усиление по эквивалентным сигналам
            len_eqdeg = var_eqsigdeg.shape[0]
            res, div = 0, len_eqdeg
            # цикл по эквивалентным помехам
            for i in range(len_eqdeg):
                if var_eqsigdeg[i] != 361:
                    ind_sig = self.get_deg2ind(var_eqsigdeg[i], vec_deg, deg_step)
                    res = res + self.get_amp2db(vec_inout[var_time][ind_sig] / max_inptn)
                else:
                    div = div - 1
            res = res / div
        return res

    def detector_bpsk(self, lowpass_out):
        # демодулятор bpsk
        len_time, len_amp = lowpass_out.shape[0], lowpass_out.shape[1]
        # выборочная оценка
        num_bit = self.msg_code - 1
        out_bits = np.zeros(shape=[num_bit], dtype=np.int)
        len_discr = int(round(len_time/num_bit))
        # оценка битов
        for i in range(num_bit):
            tempF = 0
            for j in range(len_discr):
                tempF = tempF + lowpass_out[i * len_discr + j][0]
            if tempF > 0:
                out_bits[i] = 1
            else:
                out_bits[i] = 0
        # формирование последовательности
        #out_stream = np.zeros(shape=[len_time, len_amp])
        #for i in range(num_bit):
        #    if out_bits[i] == 0:
        #        for j in range(len_discr):
        #            out_stream[i * len_discr + j][0] = 0
        #    else:
        #        for j in range(len_discr):
        #            out_stream[i * len_discr + j][0] = 1
        return [out_bits, len_time, len_discr, num_bit]

    def get_errfrq(self, init_bits, fact_bits):
        # вычисление частоты битовых ошибок
        len_init, count = len(init_bits), 0
        # цикл по элементам
        for i in range(len_init):
            if init_bits[i] != fact_bits[i]:
                count = count + 1
        err_rate = count / len_init
        return err_rate

    def init_vecmean(self, len_time, len_pattern, len_sig, len_int):
        # инициализируем вектора и средние величины
        self.vec_inptn = np.zeros(shape=[len_time, len_pattern])
        self.vec_indpt = np.zeros(shape=[len_time, len_int])
        self.vec_inatn = np.zeros(shape=[len_time, len_sig])
        self.vec_insig = np.zeros(shape=[len_time, 1], dtype=complex)
        self.vec_outptn = np.zeros(shape=[len_time, len_pattern])
        self.vec_outdpt = np.zeros(shape=[len_time, len_int])
        self.vec_outatn = np.zeros(shape=[len_time, len_sig])
        self.vec_outsig = np.zeros(shape=[len_time, 1], dtype=complex)

    def get_deg2ind(self, deg, vec_deg, deg_step):
        # перевод индексов для угла заданного сигнала
        deg = round(deg / deg_step) * deg_step
        return np.where(vec_deg == deg)

    def get_amp2db(self, num):
        # перевод амплитуды в дБ
        return 20 * np.log10(abs(num))
