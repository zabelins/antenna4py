import pack_model
from pack_model import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль динамической модели ААР (L1)")
    print("Модуль использует пакет:", pack_model.NAME)

class Model_AAA:
    """Класс динамического моделирования адаптивной антенны"""

    def __init__(self):
        self.f_cen = []
        self.list_settings = pack_model.settings.Model(1)
        self.list_env = pack_model.env.Env(1)
        self.list_array = pack_model.array.Array(1)
        self.list_proc = pack_model.proc.Proc(1)
        self.list_syntnet = pack_model.syntnet.Syntnet(1)
        self.list_train = pack_model.train.Train(1)
        self.list_test = pack_model.test.Test(1)
        self.list_file = pack_model.file_io.File_IO(1)
        self.out_set = []
        self.out_env = []
        self.out_array = []
        self.out_proc = []
        self.out_syntnet = []
        self.vec_meanindepth = []
        self.vec_meaninatten = []
        self.vec_meaninsnir = []
        self.vec_meanoutdepth = []
        self.vec_meanoutatten = []
        self.vec_meanoutsnir = []

    def set(self, obj_set):
        # инициализация параметров модели уровня L1
        par_array = obj_set.list_pararray.get()
        self.f_cen = par_array[1]
        # инициализация параметров уровня L2
        self.list_settings.set(obj_set.list_setmodel.get())
        self.list_env.set(obj_set.list_parenv.get())
        self.list_array.set(obj_set.list_pararray.get())
        self.list_proc.set(obj_set.list_paradapt.get())
        self.list_syntnet.set(obj_set.list_paradapt.get())
        self.list_train.set(obj_set.list_settrain.get())
        self.list_test.set(obj_set.list_settest.get())
        # инициализация параметров уровня L3
        self.list_array.list_factor.set(obj_set.list_pararray.get())
        self.list_array.list_element.set(obj_set.list_pararray.get())
        self.list_proc.list_trad.set(obj_set.list_paradapt.get())
        self.list_proc.list_neuro.set(obj_set.list_paradapt.get())
        self.list_proc.list_kalman.set(obj_set.list_paradapt.get())

    def get(self):
        res = []
        res.append(self.f_cen)
        return res

    def print(self):
        print(" --- ПАРАМЕТРЫ ДИНАМИЧЕСКОЙ МОДЕЛИ ААР (L1) --- ")
        print("f_cen = ", self.f_cen)
        self.list_settings.print_short()
        self.list_env.print_short()
        self.list_array.print_short()
        self.list_proc.print_short()
        self.list_syntnet.print_short()
        self.list_train.print_short()
        self.list_test.print_short()
        self.list_file.print_short()

    def calc_out(self, id_script):
        # создание векторов изменения параметров
        self.list_settings.calc_out(id_script)
        self.out_set = self.list_settings.get_out()
        # запускаем цикл по параметрам
        len_var = self.out_set[2].shape[0]
        for i in range(len_var):
            # вычисление параметра
            if (id_script == 6):
                var_par = self.out_set[2][i]
                par_band = self.f_cen * var_par
                print("var_par = ", var_par)
            else:
                var_par = 0.1
                par_band = self.f_cen * var_par
                if (id_script == 4):
                    print("var_par = ", var_par)
            # создание векторов изменения сигналов и помех от времени
            self.list_env.calc_out(self.out_set, self.f_cen, par_band, id_script)
            self.out_env = self.list_env.get_out()
            # инициализация векторов усреднённых характеристик
            len_sig, len_int = self.out_env[0].shape[1], self.out_env[3].shape[1]
            if (i == 0):
                self.vec_meanindepth = np.zeros(shape=[len_var, len_int])
                self.vec_meaninatten = np.zeros(shape=[len_var, len_sig])
                self.vec_meaninsnir = np.zeros(shape=[len_var])
                self.vec_meanoutdepth = np.zeros(shape=[len_var, len_int])
                self.vec_meanoutatten = np.zeros(shape=[len_var, len_sig])
                self.vec_meanoutsnir = np.zeros(shape=[len_var])
            # вычисление сигналов с антенной решётки
            self.list_array.calc_out(self.out_set, self.out_env)
            self.out_array = self.list_array.get_out()
            # вычисление векторов ВК
            self.list_proc.calc_out(self.out_array)
            self.out_proc = self.list_proc.get_out()
            # вычисление ДН и характеристик
            self.list_syntnet.calc_out(self.out_set, self.out_env, self.out_array, self.out_proc)
            self.out_syntnet = self.list_syntnet.get_out()
            # сохранение усреднённых параметров
            self.vec_meanindepth[i] = self.out_syntnet[6]
            self.vec_meaninatten[i] = self.out_syntnet[7]
            self.vec_meaninsnir[i] = self.out_proc[4]
            self.vec_meanoutdepth[i] = self.out_syntnet[8]
            self.vec_meanoutatten[i] = self.out_syntnet[9]
            self.vec_meanoutsnir[i] = self.out_proc[5]
            #self.vec_meanindepth.append(self.out_syntnet[6])
            #self.vec_meaninatten.append(self.out_syntnet[7])
            #self.vec_meaninsnir.append(self.out_proc[4])
            #self.vec_meanoutdepth.append(self.out_syntnet[8])
            #self.vec_meanoutatten.append(self.out_syntnet[9])
            #self.vec_meanoutsnir.append(self.out_proc[5])

    def get_out(self):
        # формирование выходных векторов
        out_model = []
        out_model.append(self.vec_meanindepth)
        out_model.append(self.vec_meaninatten)
        out_model.append(self.vec_meaninsnir)
        out_model.append(self.vec_meanoutdepth)
        out_model.append(self.vec_meanoutatten)
        out_model.append(self.vec_meanoutsnir)
        return [self.out_set, self.out_env, self.out_array, self.out_proc, self.out_syntnet, out_model]

    def print_out(self):
        # вывод информации о ходе вычислений
        self.list_settings.print_out()
        self.list_env.print_out()
        self.list_array.print_out()
        self.list_proc.print_out()
        self.list_syntnet.print_out()