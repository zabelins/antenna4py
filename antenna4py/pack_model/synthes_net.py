import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль модели ДОС (L2)")

class Synt_net:
    """Класс моделирования схемы диаграммообразования"""

    def __init__(self, id):
        self.id = id
        self.control_phistep = []
        self.control_ampstep = []
        self.vec_inpattern = []
        self.vec_outpattern = []
        self.vec_outdeph = []
        self.vec_outatten = []
        self.vec_outsnir = []
        self.vec_outsnr = []
        self.vec_outinr = []
        self.vec_outsignal = []

    def set(self, init):
        self.control_phistep = init[6]
        self.control_ampstep = init[7]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.control_phistep)
        res.append(self.control_ampstep)
        return res

    def print(self):
        print(" --- Параметры модели ДОС (L2) --- ")
        print("id = ", self.id)
        print("control_phistep = ", self.control_phistep)
        print("control_ampstep = ", self.control_ampstep)

    def print_short(self):
        print(" --- Параметры модели ДОС (L2) --- ")
        print("syntnet = ", self.get())

    def calc_out(self, out_set, out_env, out_array, out_weight):
        # распаковка исходных данных
        vec_pattern, vec_time = out_set[0], out_set[1]
        vec_test = out_array[0].T
        vec_degsig, vec_degint = out_env[0], out_env[1]
        vec_eqdegsig, vec_eqdegint = out_array[7], out_array[8]
        vec_weight1, vec_weight2 = out_weight[2], out_weight[5]
        print("vec_time = ", vec_time)
        print("vec_degint = ", vec_degint)
        print("vec_eqdegint = ", vec_eqdegint)
        # инициализируем размеры векторов
        len_time, len_pattern = vec_time.shape[0], vec_pattern.shape[0]
        len_sig, len_int = vec_degsig.shape[1], vec_degint.shape[1]
        self.vec_inpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_outpattern = np.zeros(shape=[len_time, len_pattern])
        self.vec_outatten = np.zeros(shape=[len_time, len_sig])
        self.vec_outdeph = np.zeros(shape=[len_time, len_int])
        # запускаем цикл по времени
        for i in range(len_time):
            # вычисление ДН
            self.vec_inpattern[i] = abs(np.dot(vec_test, vec_weight1))
            self.vec_outpattern[i] = abs(np.dot(vec_test, vec_weight2[i]))
            # вычисление глубины подавления помехи и ослабления сигнала
            self.vec_outatten[i] = self.calc_difference(vec_pattern, vec_degsig[i], i)
            self.vec_outdeph[i] = self.calc_difference(vec_pattern, vec_degint[i], i)
            # вывод информации
            print("vec_outdeph = ", self.vec_outdeph[i])
            print("vec_outatten = ", self.vec_outatten[i])

        self.vec_outsnir = []
        self.vec_outsnr = []
        self.vec_outinr = []
        self.vec_outsignal = []

    def get_out(self):
        res = []
        res.append(self.vec_inpattern)
        res.append(self.vec_outpattern)
        res.append(self.vec_outdeph)
        res.append(self.vec_outatten)
        res.append(self.vec_outsnir)
        res.append(self.vec_outsnr)
        res.append(self.vec_outinr)
        res.append(self.vec_outsignal)
        return res

    def print_out(self):
        print("Размерности векторов ДОС:")
        print("vec_inpattern.shape = ", self.vec_inpattern.shape)
        print("vec_outpattern.shape = ", self.vec_outpattern.shape)
        print("vec_outdeph.shape = ", self.vec_outdeph.shape)
        print("vec_outatten.shape = ", self.vec_outatten.shape)
        #print("vec_outsnir.shape = ", self.vec_outsnir.shape)
        #print("vec_outsnr.shape = ", self.vec_outsnr.shape)
        #print("vec_outinr.shape = ", self.vec_outinr.shape)
        #print("vec_outsignal.shape = ", self.vec_outsignal.shape)

    def calc_difference(self, vec_pattern, vec_deg, index):
        # вычисление разности искодной и оптимальной ДН по заданным углам
        len_sig = vec_deg.shape[0]
        out_diff = np.zeros(shape=[len_sig], dtype='float64')
        max_inpattern = self.vec_inpattern[index].max()
        for i in range(len_sig):
            # вычисление индексов для угла заданного сигнала
            id_sig = np.where(vec_pattern == vec_deg[i])
            # вычисление в дБ разности ДН по заданным углам
            norm_inpattern = self.vec_inpattern[index][id_sig] / max_inpattern
            norm_outpattern = self.vec_outpattern[index][id_sig] / max_inpattern
            db_inpattern = 20 * np.log10(abs(norm_inpattern))
            db_outpattern = 20 * np.log10(abs(norm_outpattern))
            out_diff[i] = db_outpattern - db_inpattern
        return out_diff