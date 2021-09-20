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
        self.vec_outpattern = []
        self.vec_outdeph = []
        self.vec_outatten = []
        # усреднённые характеристики адаптации
        self.mean_indeph = []
        self.mean_inatten = []
        self.mean_outdeph = []
        self.mean_outatten = []

    def set(self, init):
        self.control_stepphi = init[6]
        self.control_stepamp = init[7]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.control_stepphi)
        res.append(self.control_stepamp)
        return res

    def print(self):
        print(" --- Параметры модели ДОС (L2) --- ")
        print("id = ", self.id)
        print("control_stepphi = ", self.control_stepphi)
        print("control_stepamp = ", self.control_stepamp)

    def print_short(self):
        print(" --- Параметры модели ДОС (L2) --- ")
        print("syntnet = ", self.get())

    def calc_out(self, out_set, out_env, out_array, out_proc):
        # распаковка исходных данных
        vec_pattern, vec_time = out_set[0], out_set[1]
        vec_degsig, vec_degint = out_env[0], out_env[3]
        vec_test, vec_eqdegsig, vec_eqdegint = out_array[0].T, out_array[7], out_array[8]
        vec_inweight, vec_outweight = out_proc[0], out_proc[2]
        # вычисляем размерности
        len_time, len_pattern = vec_time.shape[0], vec_pattern.shape[0]
        len_sig, len_int = vec_degsig.shape[1], vec_degint.shape[1]
        # инициализируем размеры векторов
        self.vec_inpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_indeph = np.zeros(shape=[len_time, len_int])
        self.vec_inatten = np.zeros(shape=[len_time, len_sig])
        self.vec_outpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_outdeph = np.zeros(shape=[len_time, len_int])
        self.vec_outatten = np.zeros(shape=[len_time, len_sig])
        self.mean_indeph = np.zeros(shape=[len_int])
        self.mean_inatten = np.zeros(shape=[len_sig])
        self.mean_outdeph = np.zeros(shape=[len_int])
        self.mean_outatten = np.zeros(shape=[len_sig])
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление диаграмм направленности
            self.vec_inpattern[i] = abs(np.dot(vec_test, vec_inweight))
            self.vec_outpattern[i] = abs(np.dot(vec_test, vec_outweight[i]))
            # вычисление глубины подавления помехи и ослабления сигнала
            self.vec_indeph[i] = self.calc_gain(vec_pattern, vec_degint[i], vec_eqdegint[i], i, 1)
            self.vec_inatten[i] = self.calc_gain(vec_pattern, vec_degsig[i], vec_eqdegsig[i], i, 1)
            self.vec_outdeph[i] = self.calc_gain(vec_pattern, vec_degint[i], vec_eqdegint[i], i, 2)
            self.vec_outatten[i] = self.calc_gain(vec_pattern, vec_degsig[i], vec_eqdegsig[i], i, 2)
            # вычисление усреднённых характеристик адаптации
            self.mean_indeph = self.mean_indeph + self.vec_indeph[i]
            self.mean_inatten = self.mean_inatten + self.vec_inatten[i]
            self.mean_outdeph = self.mean_outdeph + self.vec_outdeph[i]
            self.mean_outatten = self.mean_outatten + self.vec_outatten[i]
        # деление на общее количество
        self.mean_indeph = self.mean_indeph / len_time
        self.mean_inatten = self.mean_inatten / len_time
        self.mean_outdeph = self.mean_outdeph / len_time
        self.mean_outatten = self.mean_outatten / len_time

    def get_out(self):
        res = []
        res.append(self.vec_inpattern)
        res.append(self.vec_indeph)
        res.append(self.vec_inatten)
        res.append(self.vec_outpattern)
        res.append(self.vec_outdeph)
        res.append(self.vec_outatten)
        res.append(self.mean_indeph)
        res.append(self.mean_inatten)
        res.append(self.mean_outdeph)
        res.append(self.mean_outatten)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_inpattern, self.vec_indeph, self.vec_inatten])
        bool_res2 = cl.is_ndarray([self.vec_outpattern, self.vec_outdeph, self.vec_outatten])
        bool_res3 = cl.is_ndarray([self.mean_indeph, self.mean_inatten, self.mean_outdeph, self.mean_outatten])
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True) and (bool_res3 == True):
            print("Размерности векторов ДОС:")
            print("\tvec_inpattern.shape = ", self.vec_inpattern.shape)
            print("\tvec_indeph.shape = ", self.vec_indeph.shape)
            print("\tvec_inatten.shape = ", self.vec_inatten.shape)
            print("\tvec_outpattern.shape = ", self.vec_outpattern.shape)
            print("\tvec_outdeph.shape = ", self.vec_outdeph.shape)
            print("\tvec_outatten.shape = ", self.vec_outatten.shape)
            print("\tmean_indeph.shape = ", self.mean_indeph.shape)
            print("\tmean_inatten.shape = ", self.mean_inatten.shape)
            print("\tmean_outdeph.shape = ", self.mean_outdeph.shape)
            print("\tmean_outatten.shape = ", self.mean_outatten.shape)
        else:
            print("Ошибка проверки типа векторов ДОС")

    def calc_gain(self, vec_pattern, vec_deg, vec_eqdeg, var_time, id_inout):
        # вычисление нормированного усиления по N реальным углам в 1 момент времени
        max_inpattern = self.vec_inpattern[var_time].max()
        len_deg = vec_deg.shape[0]
        # инициализируем размер вектора
        out_gain = np.zeros(shape=[len_deg], dtype='float64')
        # номер учёта эквивалентных углов (1=реал, 2=экв)
        id_eq = 1
        # цикл по сигналам
        for i in range(len_deg):
            out_gain[i] = self.calc_meangain(vec_pattern, vec_deg[i], vec_eqdeg[i], var_time, id_inout, id_eq)
            out_gain[i] = out_gain[i] / max_inpattern
        return out_gain

    def calc_meangain(self, vec_pattern, var_deg, var_eqdeg, var_time, id_inout, id_eq):
        # вычисление нормированного усиления по 1 реальному углу в 1 момент времени
        pattern_step = abs(vec_pattern[1] - vec_pattern[0])
        vec_inout, id_sig = [], []
        # выбор ДН
        if (id_inout == 1):
            # для исходной ДН
            vec_inout = self.vec_inpattern
        if (id_inout == 2):
            # для оптимальной ДН
            vec_inout = self.vec_outpattern
        # выбор способа расчёта
        if (id_eq == 1):
            # усиление по реальным сигналам
            id_sig = self.calc_deg2ind(var_deg, vec_pattern, pattern_step)
            res = vec_inout[var_time][id_sig]
        if (id_eq == 2):
            # среднее усиление по эквивалентным сигналам
            len_eqdeg = var_eqdeg.shape[0]
            res = 0
            # цикл по эквивалентным помехам
            for i in range(len_eqdeg):
                if (var_eqdeg[i] != 361):
                    id_sig = self.calc_deg2ind(var_eqdeg[i], vec_pattern, pattern_step)
                    res = res + vec_inout[var_time][id_sig]
            res = res / len_eqdeg
        return res

    def calc_deg2ind(self, var_deg, vec_pattern, pattern_step):
        # вычисление индексов для угла заданного сигнала
        var_deg = round(var_deg / pattern_step) * pattern_step
        return np.where(vec_pattern == var_deg)