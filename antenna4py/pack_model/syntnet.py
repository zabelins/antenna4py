import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели ДОС (L2)")

class Syntnet:
    """Класс моделирования схемы диаграммообразования"""

    def __init__(self, id):
        self.id = id
        self.control_stepphi = []
        self.control_stepamp = []
        # временные характеристики адаптации
        self.vec_inpattern = []
        self.vec_indeph = []
        self.vec_inatten = []
        self.vec_insnir = []
        self.vec_outpattern = []
        self.vec_outdeph = []
        self.vec_outatten = []
        self.vec_outsnir = []
        # усреднённые характеристики адаптации
        self.mean_rasdeph = []
        self.mean_rasatten = []
        self.mean_rassnir = []

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
        vec_inweight, vec_outweight = out_proc[0], out_proc[1]
        # вычисляем размерности
        len_time, len_pattern = vec_time.shape[0], vec_pattern.shape[0]
        len_sig, len_int = vec_degsig.shape[1], vec_degint.shape[1]
        # инициализируем размеры векторов
        self.vec_inpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_inatten = np.zeros(shape=[len_time, len_sig])
        self.vec_indeph = np.zeros(shape=[len_time, len_int])
        self.vec_insnir = np.zeros(shape=[len_time])
        self.vec_outpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_outatten = np.zeros(shape=[len_time, len_sig])
        self.vec_outdeph = np.zeros(shape=[len_time, len_int])
        self.vec_outsnir = np.zeros(shape=[len_time])
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление диаграмм направленности
            self.vec_inpattern[i] = abs(np.dot(vec_test, vec_inweight))
            self.vec_outpattern[i] = abs(np.dot(vec_test, vec_outweight[i]))
            # вычисление глубины подавления помехи и ослабления сигнала
            self.vec_indeph[i] = self.calc_charact(vec_pattern, vec_degint[i], vec_eqdegint[i], i, 1)
            self.vec_inatten[i] = self.calc_charact(vec_pattern, vec_degsig[i], vec_eqdegsig[i], i, 1)
            self.vec_outdeph[i] = self.calc_charact(vec_pattern, vec_degint[i], vec_eqdegint[i], i, 2)
            self.vec_outatten[i] = self.calc_charact(vec_pattern, vec_degsig[i], vec_eqdegsig[i], i, 2)

    def get_out(self):
        res = []
        res.append(self.vec_inpattern)
        res.append(self.vec_indeph)
        res.append(self.vec_inatten)
        res.append(self.vec_insnir)
        res.append(self.vec_outpattern)
        res.append(self.vec_outdeph)
        res.append(self.vec_outatten)
        res.append(self.vec_outsnir)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_buf1 = isinstance(self.vec_inpattern, np.ndarray)
        bool_buf2 = isinstance(self.vec_indeph, np.ndarray)
        bool_buf3 = isinstance(self.vec_inatten, np.ndarray)
        bool_buf4 = isinstance(self.vec_insnir, np.ndarray)
        bool_buf5 = isinstance(self.vec_outpattern, np.ndarray)
        bool_buf6 = isinstance(self.vec_outdeph, np.ndarray)
        bool_buf7 = isinstance(self.vec_outatten, np.ndarray)
        bool_buf8 = isinstance(self.vec_outsnir, np.ndarray)
        bool_res1 = (bool_buf1 == True) and (bool_buf2 == True) and (bool_buf3 == True)
        bool_res2 = (bool_buf4 == True) and (bool_buf5 == True) and (bool_buf6 == True)
        bool_res3 = (bool_buf7 == True) and (bool_buf8 == True)
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True) and (bool_res3 == True):
            print("Размерности векторов ДОС:")
            print("vec_inpattern.shape = ", self.vec_inpattern.shape)
            print("vec_indeph.shape = ", self.vec_indeph.shape)
            print("vec_inatten.shape = ", self.vec_inatten.shape)
            print("vec_insnir.shape = ", self.vec_insnir.shape)
            print("vec_outpattern.shape = ", self.vec_outpattern.shape)
            print("vec_outdeph.shape = ", self.vec_outdeph.shape)
            print("vec_outatten.shape = ", self.vec_outatten.shape)
            print("vec_outsnir.shape = ", self.vec_outsnir.shape)
        else:
            print("Ошибка проверки типа векторов ДОС")

    def calc_charact(self, vec_pattern, vec_deg, vec_eqdeg, var_time, id_inout):
        # вычисление разности искодной и оптимальной ДН по заданным углам
        pattern_step = abs(vec_pattern[1] - vec_pattern[0])
        len_sig = vec_deg.shape[0]
        max_inpattern = self.vec_inpattern[var_time].max()
        # инициализируем размер вектора
        out_vec = np.zeros(shape=[len_sig], dtype='float64')
        # цикл по сигналам
        for i in range(len_sig):
            # вычисление индексов для угла заданного сигнала
            vec_deg[i] = round(vec_deg[i]/pattern_step) * pattern_step
            id_sig = np.where(vec_pattern == vec_deg[i])
            # вычисление нормированной ДН по заданным углам
            if (id_inout == 1):
                # для исходной ДН
                norm_inpattern = self.vec_inpattern[var_time][id_sig] / max_inpattern
                out_vec[i] = norm_inpattern
            if (id_inout == 2):
                # для оптимальной ДН
                norm_outpattern = self.vec_outpattern[var_time][id_sig] / max_inpattern
                out_vec[i] = norm_outpattern
        return out_vec