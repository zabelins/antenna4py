import pack_model
from pack_model import *
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль динамической модели ААР (L1)")
    print("Модуль использует пакет:", pack_model.NAME)

class Model_AAA:
    """Класс динамического моделирования адаптивной антенны"""

    def __init__(self):
        self.list_settings = pack_model.settings.Model(1)
        self.list_env = pack_model.env.Env(1)
        self.list_array = pack_model.array.Array(1)
        self.list_proc = pack_model.proc.Proc(1)
        self.list_syntnet = pack_model.syntnet.Syntnet(1)
        self.list_train = pack_model.train.Train(1)
        self.list_test = pack_model.test.Test(1)
        self.list_file = pack_model.file_io.File_IO(1)
        self.f_cen = []
        self.id_script = []
        self.out_set = []
        self.out_env = []
        self.out_array1nd = []
        self.out_array2nd = []
        self.out_proc1nd = []
        self.out_proc2nd = []
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
        self.f_cen = par_array[0]
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
        print("Параметры динамической модели (L1):")
        print("\tf_cen = ", self.f_cen)
        self.list_settings.print()
        self.list_env.print()
        self.list_array.print()
        self.list_proc.print()
        self.list_syntnet.print()
        self.list_train.print()
        self.list_test.print()
        self.list_file.print()

    def calc_out(self, id_script):
        self.id_script = id_script
        # создание векторов изменения параметров
        self.list_settings.calc_out(id_script)
        self.out_set = self.list_settings.get_out()
        # запускаем цикл по параметру (частотной полосе)
        len_var = self.out_set[2].shape[0]
        for i in range(len_var):
            # вычисление параметра
            if id_script == 6:
                var_band = self.out_set[2][i]
                print("var_band = ", var_band)
            elif id_script == 4:
                var_band = 0.1
            else:
                var_band = 0
            par_band = self.f_cen * var_band
            # создание векторов изменения сигналов и помех от времени
            self.list_env.calc_out(self.out_set, self.f_cen, par_band, id_script)
            self.out_env = self.list_env.get_out()
            # вычисление сигналов с антенной решётки
            self.list_array.calc_out(self.out_set, self.out_env)
            self.out_array1nd = self.list_array.get_out1nd()
            self.out_array2nd = self.list_array.get_out2nd()
            # вычисление векторов ВК
            self.list_proc.calc_out(self.out_array2nd)
            self.out_proc1nd = self.list_proc.get_out1nd()
            self.out_proc2nd = self.list_proc.get_out2nd()
            # вычисление ДН и характеристик
            self.list_syntnet.calc_out(self.out_set, self.out_env, self.out_array1nd, self.out_proc2nd)
            self.out_syntnet = self.list_syntnet.get_out()
            # инициализация векторов усреднённых характеристик
            if i == 0:
                len_sig, len_int = self.out_env[0].shape[1], self.out_env[3].shape[1]
                self.init_vecmean(len_var, len_sig, len_int)
            # сохранение усреднённых параметров
            self.vec_meanindepth[i] = self.out_syntnet[6]
            self.vec_meaninatten[i] = self.out_syntnet[7]
            self.vec_meaninsnir[i] = self.out_proc1nd[2]
            self.vec_meanoutdepth[i] = self.out_syntnet[8]
            self.vec_meanoutatten[i] = self.out_syntnet[9]
            self.vec_meanoutsnir[i] = self.out_proc1nd[3]

    def get_out(self):
        # получить усреднённые характеристики
        res = []
        res.append(self.vec_meanindepth)
        res.append(self.vec_meaninatten)
        res.append(self.vec_meaninsnir)
        res.append(self.vec_meanoutdepth)
        res.append(self.vec_meanoutatten)
        res.append(self.vec_meanoutsnir)
        return res

    def print_out(self):
        # проверка типа векторов на ndarray
        bool_res1 = cl.is_ndarray([self.vec_meanindepth, self.vec_meaninatten, self.vec_meaninsnir])
        bool_res2 = cl.is_ndarray([self.vec_meanoutdepth, self.vec_meanoutatten, self.vec_meanoutsnir])
        # вывод размерностей векторов
        if (bool_res1 == True) and (bool_res2 == True):
            print("Размерности векторов модели ААР:")
            print("\tvec_meanindepth.shape = ", self.vec_meanindepth.shape)
            print("\tvec_meaninatten.shape = ", self.vec_meaninatten.shape)
            print("\tvec_meaninsnir.shape = ", self.vec_meaninsnir.shape)
            print("\tvec_meanoutdepth.shape = ", self.vec_meanoutdepth.shape)
            print("\tvec_meanoutatten.shape = ", self.vec_meanoutatten.shape)
            print("\tvec_meanoutsnir.shape = ", self.vec_meanoutsnir.shape)

    def print_calc(self):
        # вывод информации о ходе вычислений
        self.list_settings.print_out()
        self.list_env.print_out()
        self.list_array.print_out()
        self.list_proc.print_out()
        self.list_syntnet.print_out()
        self.print_out()

    def get_out1nd(self):
        # получить вектора для представления
        out_model = self.get_out()
        return [self.out_set, self.out_env, self.out_array1nd, self.out_proc1nd, self.out_syntnet, out_model]

    def get_out2nd(self):
        # получить вектора для обучения НС
        out_model = self.get_info()
        return [self.out_array2nd, self.out_proc2nd, out_model]

    def get_info(self):
        # получить параметры ААР
        res = []
        res.append(self.list_array.array_N)
        res.append(self.list_proc.alg_type)
        res.append(self.list_proc.control_type)
        res.append(self.id_script)
        buf1 = self.vec_meanoutdepth.mean(axis=0) - self.vec_meanindepth.mean(axis=0)
        buf2 = self.vec_meanoutatten.mean(axis=0) - self.vec_meaninatten.mean(axis=0)
        res.append(buf1.sum())
        res.append(buf2.sum())
        res.append(self.vec_meanoutsnir.mean())
        return res

    def calc_train(self):
        # обучение нейронной сети
        var_data = self.list_file.load_files()
        self.list_train.calc_out(var_data)

    def save_learn(self):
        # сохранение обучающей выборки
        vec_data = self.get_out2nd()
        self.list_file.save_file(vec_data)

    def init_vecmean(self, len_var, len_sig, len_int):
        self.vec_meanindepth = np.zeros(shape=[len_var, len_int])
        self.vec_meaninatten = np.zeros(shape=[len_var, len_sig])
        self.vec_meaninsnir = np.zeros(shape=[len_var])
        self.vec_meanoutdepth = np.zeros(shape=[len_var, len_int])
        self.vec_meanoutatten = np.zeros(shape=[len_var, len_sig])
        self.vec_meanoutsnir = np.zeros(shape=[len_var])