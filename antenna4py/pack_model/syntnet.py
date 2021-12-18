import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль модели ДОС (L2)")

class Syntnet:
    """Класс моделирования схемы диаграммообразования"""

    def __init__(self, id):
        self.id = id
        # дискретность управления
        self.control_stepphi = []
        self.control_stepamp = []
        # временные характеристики адаптации
        self.vec_inpattern = []
        self.vec_indeph = []
        self.vec_inatten = []
        self.vec_insignal = []
        self.vec_outpattern = []
        self.vec_outdeph = []
        self.vec_outatten = []
        self.vec_outsignal = []
        # усреднённые характеристики адаптации
        self.mean_indeph = []
        self.mean_inatten = []
        self.mean_outdeph = []
        self.mean_outatten = []

    def set(self, init):
        self.control_stepphi = init[5]
        self.control_stepamp = init[6]

    def get(self):
        res = []
        res.append(self.control_stepphi)
        res.append(self.control_stepamp)
        return res

    def print(self):
        print("Параметры модели ДОС (L2):")
        print("\tcontrol_stepphi = ", self.control_stepphi)
        print("\tcontrol_stepamp = ", self.control_stepamp)

    def calc_out(self, out_set, out_env, out_array, out_proc):
        # распаковка исходных данных
        vec_pattern, vec_time = out_set[0], out_set[1]
        vec_degsig, vec_degint = out_env[0], out_env[3]
        vec_test, vec_eqdegsig, vec_eqdegint = out_array[0].T, out_array[1], out_array[2]
        vec_in, vec_inweight, vec_outweight = out_proc[0], out_proc[1], out_proc[2]
        # вычисляем размерности
        len_time, len_pattern = vec_time.shape[0], vec_pattern.shape[0]
        len_sig, len_int = vec_degsig.shape[1], vec_degint.shape[1]
        # инициализируем размеры векторов
        self.init_vecmean(len_time, len_pattern, len_sig, len_int)
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление диаграмм направленности ААР
            self.vec_inpattern[i] = abs(np.dot(vec_test, vec_inweight))
            self.vec_outpattern[i] = abs(np.dot(vec_test, vec_outweight[i]))
            # вычисление выходных сигналов с ААР
            self.vec_insignal[i][0] = np.dot(vec_in[i], vec_inweight)
            self.vec_outsignal[i][0] = np.dot(vec_in[i], vec_outweight[i])
            # вычисление глубины подавления помехи и ослабления сигнала
            self.vec_indeph[i] = self.calc_gain(vec_pattern, vec_degint[i], vec_eqdegint[i], i, 1)
            self.vec_inatten[i] = self.calc_gain(vec_pattern, vec_degsig[i], vec_eqdegsig[i], i, 1)
            self.vec_outdeph[i] = self.calc_gain(vec_pattern, vec_degint[i], vec_eqdegint[i], i, 2)
            self.vec_outatten[i] = self.calc_gain(vec_pattern, vec_degsig[i], vec_eqdegsig[i], i, 2)
        # вычисление усреднённых характеристик адаптации
        self.mean_indeph = np.mean(self.vec_indeph, axis=0)
        self.mean_inatten = np.mean(self.vec_inatten, axis=0)
        self.mean_outdeph = np.mean(self.vec_outdeph, axis=0)
        self.mean_outatten = np.mean(self.vec_outatten, axis=0)

    def get_out(self):
        out_syntnet = []
        out_syntnet.append(self.vec_inpattern)
        out_syntnet.append(self.vec_indeph)
        out_syntnet.append(self.vec_inatten)
        out_syntnet.append(self.vec_insignal)
        out_syntnet.append(self.vec_outpattern)
        out_syntnet.append(self.vec_outdeph)
        out_syntnet.append(self.vec_outatten)
        out_syntnet.append(self.vec_outsignal)
        out_syntnet.append(self.mean_indeph)
        out_syntnet.append(self.mean_inatten)
        out_syntnet.append(self.mean_outdeph)
        out_syntnet.append(self.mean_outatten)
        return out_syntnet

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_inpattern, self.vec_indeph, self.vec_inatten, self.vec_insignal])
        bool_res2 = cl.is_ndarray([self.vec_outpattern, self.vec_outdeph, self.vec_outatten, self.vec_outsignal])
        bool_res3 = cl.is_ndarray([self.mean_indeph, self.mean_inatten, self.mean_outdeph, self.mean_outatten])
        # вывод размерностей векторов
        if bool_res1 == True and bool_res2 == True and bool_res3 == True:
            print("Размерности векторов ДОС:")
            print("\tvec_inpattern.shape = ", self.vec_inpattern.shape)
            print("\tvec_indeph.shape = ", self.vec_indeph.shape)
            print("\tvec_inatten.shape = ", self.vec_inatten.shape)
            print("\tvec_insignal.shape = ", self.vec_insignal.shape)
            print("\tvec_outpattern.shape = ", self.vec_outpattern.shape)
            print("\tvec_outdeph.shape = ", self.vec_outdeph.shape)
            print("\tvec_outatten.shape = ", self.vec_outatten.shape)
            print("\tvec_outsignal.shape = ", self.vec_outsignal.shape)
            print("\tmean_indeph.shape = ", self.mean_indeph.shape)
            print("\tmean_inatten.shape = ", self.mean_inatten.shape)
            print("\tmean_outdeph.shape = ", self.mean_outdeph.shape)
            print("\tmean_outatten.shape = ", self.mean_outatten.shape)
        else:
            print("Ошибка проверки типа векторов ДОС")

    def calc_gain(self, vec_pattern, vec_deg, vec_eqdeg, var_time, id_inout):
        # вычисление нормированного усиления по N реальным углам в 1 момент времени
        len_deg = vec_deg.shape[0]
        # инициализируем размер вектора
        out_gain = np.zeros(shape=[len_deg], dtype='float64')
        # номер учёта эквивалентных углов (1=реал, 2=экв)
        id_eq = 1
        # цикл по сигналам
        for i in range(len_deg):
            out_gain[i] = self.calc_meangain(vec_pattern, vec_deg[i], vec_eqdeg[i], var_time, id_inout, id_eq)
        return out_gain

    def calc_meangain(self, vec_pattern, var_deg, var_eqdeg, var_time, id_inout, id_eq):
        # вычисление нормированного усиления по 1 реальному углу в 1 момент времени
        pattern_step = abs(vec_pattern[1] - vec_pattern[0])
        max_inpattern = self.vec_inpattern[var_time].max()
        vec_inout, id_sig = [], []
        # выбор ДН
        if id_inout == 1:
            # для исходной ДН
            vec_inout = self.vec_inpattern
        if id_inout == 2:
            # для оптимальной ДН
            vec_inout = self.vec_outpattern
        # выбор способа расчёта
        if id_eq == 1:
            # усиление по реальным сигналам
            ind_sig = self.get_deg2ind(var_deg, vec_pattern, pattern_step)
            res = self.get_one2db(vec_inout[var_time][ind_sig] / max_inpattern)
        if id_eq == 2:
            # среднее усиление по эквивалентным сигналам
            len_eqdeg = var_eqdeg.shape[0]
            res, div = 0, len_eqdeg
            # цикл по эквивалентным помехам
            for i in range(len_eqdeg):
                if var_eqdeg[i] != 361:
                    ind_sig = self.get_deg2ind(var_eqdeg[i], vec_pattern, pattern_step)
                    res = res + self.get_one2db(vec_inout[var_time][ind_sig] / max_inpattern)
                else:
                    div = div - 1
            res = res / div
        return res

    def get_deg2ind(self, var_deg, vec_pattern, pattern_step):
        # перевод индексов для угла заданного сигнала
        var_deg = round(var_deg / pattern_step) * pattern_step
        return np.where(vec_pattern == var_deg)

    def get_one2db(self, num):
        # перевод числа в дБ
        return 20 * np.log10(abs(num))

    def init_vecmean(self, len_time, len_pattern, len_sig, len_int):
        # инициализируем вектора и средние величины
        self.vec_inpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_indeph = np.zeros(shape=[len_time, len_int])
        self.vec_inatten = np.zeros(shape=[len_time, len_sig])
        self.vec_insignal = np.zeros(shape=[len_time, 1], dtype=complex)
        self.vec_outpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_outdeph = np.zeros(shape=[len_time, len_int])
        self.vec_outatten = np.zeros(shape=[len_time, len_sig])
        self.vec_outsignal = np.zeros(shape=[len_time, 1], dtype=complex)
        self.mean_indeph = np.zeros(shape=[len_int])
        self.mean_inatten = np.zeros(shape=[len_sig])
        self.mean_outdeph = np.zeros(shape=[len_int])
        self.mean_outatten = np.zeros(shape=[len_sig])