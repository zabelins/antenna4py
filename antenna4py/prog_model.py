import pack_model
from pack_model import *
import math
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль динамической модели ААР (L1)")
    print("Модуль использует пакет:", pack_model.NAME)


class Model_antenna:
    """Класс динамического моделирования адаптивной антенны"""

    def __init__(self):
        # модули адаптивной антенны
        self.obj_set = pack_model.settings.Model(1)
        self.obj_env = pack_model.env.Env(1)
        self.obj_array = pack_model.array.Array(1)
        self.obj_proc = pack_model.proc.Proc(1)
        self.obj_syntnet = pack_model.syntnet.Syntnet(1)
        self.obj_file = pack_model.file_io.File_IO(1)
        self.obj_test = pack_model.test.Test(1)
        # параметры моделирования
        self.f_cen = []
        self.id_script = []
        self.par_script = []
        # характеристики модулей ААР
        self.out_set = []
        self.out_env = []
        self.out_array = []
        self.out_proc = []
        self.out_syntnet = []
        self.out_model = []
        # результаты моделирования
        self.vec_meansnir = []
        self.vec_meanindepth = []
        self.vec_meaninatten = []
        self.vec_meaninsnir = []
        self.vec_meanoutdepth = []
        self.vec_meanoutatten = []
        self.vec_meanoutsnir = []

    def set(self, list_set):
        # инициализация параметров модели уровня L1
        self.f_cen = list_set[2][0]
        # инициализация параметров уровня L2
        self.obj_set.set(list_set[0])
        self.obj_env.set(list_set[1])
        self.obj_array.set(list_set[2])
        self.obj_proc.set(list_set[3])
        self.obj_syntnet.set(list_set[3])
        self.obj_file.set(list_set[5])
        self.obj_test.set(list_set[6])
        # инициализация параметров уровня L3
        self.obj_array.obj_factor.set(list_set[2])
        self.obj_array.obj_element.set(list_set[2])
        self.obj_proc.obj_trad.set(list_set[3])
        self.obj_proc.obj_neuro.set(list_set[4], list_set[5])
        self.obj_proc.obj_kalman.set(list_set[3])

    def get(self):
        res = []
        res.append(self.f_cen)
        return res

    def print(self):
        print("Параметры динамической модели (L1):")
        print("\tf_cen = ", self.f_cen)
        self.obj_set.print()
        self.obj_env.print()
        self.obj_array.print()
        self.obj_proc.print()
        self.obj_syntnet.print()
        self.obj_test.print()
        self.obj_file.print()

    def calc_out(self, id_script):
        # динамическое моделирование ААР
        self.id_script = id_script
        # получение параметров для создания сетки
        self.get_parscript()
        # получение параметров динамического моделирования
        self.obj_set.calc_out(self.par_script)
        self.out_set = self.obj_set.get_out()
        # запускаем цикл по параметру (частотной полосе)
        len_par = self.out_set[2].shape[0]
        for par in range(len_par):
            # получение параметров для генератора сигналов
            self.get_parscript(par)
            # создание векторов изменения сигналов и помех от времени
            self.obj_env.calc_out(self.out_set, self.par_script)
            self.out_env = self.obj_env.get_out()
            # вычисление сигналов с антенной решётки
            self.obj_array.calc_out(self.out_set, self.out_env)
            self.out_array = self.obj_array.get_out()
            # вычисление векторов ВК
            self.obj_proc.calc_out(self.out_array)
            self.out_proc = self.obj_proc.get_out()
            # вычисление ДН и характеристик
            self.obj_syntnet.calc_out(self.out_set, self.out_env, self.out_array, self.out_proc)
            self.out_syntnet = self.obj_syntnet.get_out()
            # инициализация векторов усреднённых характеристик
            if par == 0:
                len_sig, len_int = self.out_env[0].shape[1], self.out_env[3].shape[1]
                self.init_vecmean(len_par, len_sig, len_int)
            # сохранение усреднённых параметров
            self.vec_meansnir[par] = self.out_array[4]
            self.vec_meanindepth[par] = self.out_syntnet[8]
            self.vec_meaninatten[par] = self.out_syntnet[9]
            self.vec_meaninsnir[par] = self.out_proc[5]
            self.vec_meanoutdepth[par] = self.out_syntnet[10]
            self.vec_meanoutatten[par] = self.out_syntnet[11]
            self.vec_meanoutsnir[par] = self.out_proc[6]

    def get_out(self):
        # список усреднённых характеристик от параметра
        self.out_model = []
        self.out_model.append(self.vec_meansnir)
        self.out_model.append(self.vec_meanindepth)
        self.out_model.append(self.vec_meaninatten)
        self.out_model.append(self.vec_meaninsnir)
        self.out_model.append(self.vec_meanoutdepth)
        self.out_model.append(self.vec_meanoutatten)
        self.out_model.append(self.vec_meanoutsnir)

    def get_data(self):
        # список всех характеристик модели
        self.get_out()
        out_data = []
        out_data.append(self.out_set)
        out_data.append(self.out_env)
        out_data.append(self.out_array)
        out_data.append(self.out_proc)
        out_data.append(self.out_syntnet)
        out_data.append(self.out_model)
        return out_data

    def print_out(self):
        # проверка типа векторов на ndarray
        condit_1 = cl.is_ndarray([self.vec_meansnir, self.vec_meanindepth, self.vec_meaninatten, self.vec_meaninsnir])
        condit_2 = cl.is_ndarray([self.vec_meanoutdepth, self.vec_meanoutatten, self.vec_meanoutsnir])
        # вывод размерностей векторов
        if condit_1 and condit_2:
            print("Размерности векторов модели ААР:")
            print("\tvec_meansnir.shape = ", self.vec_meansnir.shape)
            print("\tvec_meanindepth.shape = ", self.vec_meanindepth.shape)
            print("\tvec_meaninatten.shape = ", self.vec_meaninatten.shape)
            print("\tvec_meaninsnir.shape = ", self.vec_meaninsnir.shape)
            print("\tvec_meanoutdepth.shape = ", self.vec_meanoutdepth.shape)
            print("\tvec_meanoutatten.shape = ", self.vec_meanoutatten.shape)
            print("\tvec_meanoutsnir.shape = ", self.vec_meanoutsnir.shape)

    def print_calc(self):
        # вывод информации о ходе вычислений
        self.obj_set.print_out()
        self.obj_env.print_out()
        self.obj_array.print_out()
        self.obj_proc.print_out()
        self.obj_syntnet.print_out()
        self.print_out()

    def save_learn(self, list_set):
        # сохранение обучающей выборки
        out_data = self.get_data()
        self.obj_file.save_file(list_set, out_data, self.id_script)

    def init_vecmean(self, len_var, len_sig, len_int):
        # инициализация усреднённых векторов
        self.vec_meanindepth = np.zeros(shape=[len_var, len_int])
        self.vec_meaninatten = np.zeros(shape=[len_var, len_sig])
        self.vec_meaninsnir = np.zeros(shape=[len_var])
        self.vec_meanoutdepth = np.zeros(shape=[len_var, len_int])
        self.vec_meanoutatten = np.zeros(shape=[len_var, len_sig])
        self.vec_meanoutsnir = np.zeros(shape=[len_var])
        self.vec_meansnir = np.zeros(shape=[len_var])

    def get_parscript(self, item=-1):
        # выдать значения параметров для скрипта
        id_set, id_deg, id_amp, id_band, int_deg, int_amp, int_band, int_mfreq = 0, 0, 0, 0, 0, 0, 0, 0
        if self.id_script == 0:
            # статический режим ДН
            id_set, id_deg, id_amp, id_band = [0, 0, 0, 0]
            int_deg, int_amp, int_band, int_mfreq = [0, 0, 0, 0]
        elif self.id_script == 1:
            # амплитуды - симуляция синусоидальных помех
            id_set, id_deg, id_amp, id_band = [1, 0, 1, 0]
            int_deg, int_amp, int_band, int_mfreq = [0, 0, 0, 1 * math.pow(10, 3)]
        elif self.id_script == 2:
            # амплитуды - симуляция меандровых помех
            id_set, id_deg, id_amp, id_band = [1, 0, 2, 0]
            int_deg, int_amp, int_band, int_mfreq = [0, 0, 0, 1 * math.pow(10, 3)]
        elif self.id_script == 3:
            # амплитуды - симуляция импульсных помех
            id_set, id_deg, id_amp, id_band = [1, 0, 3, 0]
            int_deg, int_amp, int_band, int_mfreq = [0, 0, 0, 1 * math.pow(10, 3)]
        elif self.id_script == 4:
            # углы - линейное изменение углов для одной помехи
            id_set, id_deg, id_amp, id_band = [1, 1, 0, 0]
            int_deg, int_amp, int_band, int_mfreq = [np.array([90]), np.array([1]), np.array([self.f_cen * 0.1]), 0]
        elif self.id_script == 5:
            # рандом - генерирование случайных параметров для одной помехи
            id_set, id_deg, id_amp, id_band = [1, 2, 4, 1]
            int_deg, int_amp, int_band, int_mfreq = [np.array([90]), np.array([1]), np.array([self.f_cen * 0.1]), 0]
        elif self.id_script == 6:
            # рандом - генерирование случайных параметров для мерцающей помехи
            id_set, id_deg, id_amp, id_band = [1, 3, 5, 2]
            int_deg, int_amp, int_band, int_mfreq = [np.array([90, 90]), np.array([1, 1]),
                                                     np.array([self.f_cen * 0.1, self.f_cen * 0.1]), 0]
        elif self.id_script == 7:
            # параметрический режим ДН
            id_set, id_deg, id_amp, id_band = [2, 1, 0, 0]
            int_deg, int_amp, int_mfreq = [np.array([90]), np.array([1]), 0]
            if item == -1:
                int_band = 0
            else:
                int_band = np.array([self.f_cen * self.out_set[2][item]])
                print("var_band = ", self.out_set[2][item])
        # формат: режим для сетки, полоса частот, режим изменения углов,
        # режим изменения амплитуд, режим изменения полос, частота модуляции
        self.par_script = [id_set, id_deg, id_amp, id_band, int_deg, int_amp, int_band, int_mfreq]
