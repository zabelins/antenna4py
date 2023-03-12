import pack_model
from pack_model import *
import math
import numpy as np
import pack_calc.calc_list as cl

if __name__ == "__main__":
    print("Вы запустили модуль динамической модели ААР (L1)")
    print("Модуль использует пакет:", pack_model.NAME)

class Antenna:
    """Класс динамического моделирования адаптивной антенны"""

    def __init__(self):
        # модули адаптивной антенны
        self.obj_set = pack_model.settings.Model()
        self.obj_env = pack_model.env.Env()
        self.obj_array = pack_model.array.Array()
        self.obj_proc = pack_model.proc.Proc()
        self.obj_syntnet = pack_model.syntnet.Syntnet()
        self.obj_file = pack_model.file_save.File_save()
        self.obj_test = pack_model.test.Test()
        # параметры моделирования
        self.id_script = 0
        self.var_par = 0
        # характеристики модулей ААР
        self.out_set = np.array([])
        self.out_env = np.array([])
        self.out_array = np.array([])
        self.out_proc = np.array([])
        self.out_syntnet = np.array([])
        self.out_model = np.array([])
        # результаты моделирования
        self.vec_meansnir = np.array([])
        self.vec_meanindpt = np.array([])
        self.vec_meaninatn = np.array([])
        self.vec_meaninber = np.array([])
        self.vec_meaninsnir = np.array([])
        self.vec_meanoutdpt = np.array([])
        self.vec_meanoutatn = np.array([])
        self.vec_meanoutber = np.array([])
        self.vec_meanoutsnir = np.array([])

    def set(self, list_set):
        # инициализация параметров уровня L2
        self.obj_set.set(list_set[0])
        self.obj_array.set(list_set[2])
        self.obj_proc.set(list_set[3])
        self.obj_syntnet.set(list_set[1], list_set[3])
        self.obj_file.set(list_set[5])
        self.obj_test.set(list_set[6])
        # инициализация параметров уровня L3
        self.obj_env.obj_gendeg.set(list_set[1], list_set[2])
        self.obj_env.obj_genmod.set(list_set[1], list_set[2])
        self.obj_env.obj_genbnd.set(list_set[1], list_set[2])
        self.obj_array.obj_elem.set(list_set[2])
        self.obj_array.obj_factor.set(list_set[0], list_set[1], list_set[2])
        self.obj_proc.obj_trad.set(list_set[3])
        self.obj_proc.obj_neuro.set(list_set[1], list_set[4], list_set[5])
        self.obj_proc.obj_kalman.set(list_set[3])

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры динамической модели (L1):")
        print("\t-")
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
        # параметры динамического моделирования
        self.obj_set.calc_out(id_script)
        self.out_set = self.obj_set.get_out()
        # цикл по параметру
        len_par = self.out_set[2].shape[0]
        for item in range(len_par):
            # получение параметров для генератора сигналов
            self.get_varpar(item)
            # создание векторов изменения сигналов и помех от времени
            self.obj_env.calc_out(self.out_set, id_script, self.var_par)
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
            if item == 0:
                len_sig, len_int = self.out_env[0].shape[1], self.out_env[3].shape[1]
                self.init_vecmean(len_par, len_sig, len_int)
            # сохранение усреднённых параметров
            self.vec_meansnir[item] = self.out_array[7]
            self.vec_meanindpt[item] = self.out_syntnet[8]
            self.vec_meaninatn[item] = self.out_syntnet[9]
            self.vec_meaninber[item] = self.out_syntnet[10]
            self.vec_meaninsnir[item] = self.out_proc[4]
            self.vec_meanoutdpt[item] = self.out_syntnet[11]
            self.vec_meanoutatn[item] = self.out_syntnet[12]
            self.vec_meanoutber[item] = self.out_syntnet[13]
            self.vec_meanoutsnir[item] = self.out_proc[5]

    def get_out(self):
        # список усреднённых характеристик от параметра
        self.out_model = []
        self.out_model.append(self.vec_meansnir)
        self.out_model.append(self.vec_meanindpt)
        self.out_model.append(self.vec_meaninatn)
        self.out_model.append(self.vec_meaninber)
        self.out_model.append(self.vec_meaninsnir)
        self.out_model.append(self.vec_meanoutdpt)
        self.out_model.append(self.vec_meanoutatn)
        self.out_model.append(self.vec_meanoutber)
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
        condit_1 = cl.is_ndarray([self.vec_meansnir, self.vec_meanindpt, self.vec_meaninatn, self.vec_meaninsnir])
        condit_2 = cl.is_ndarray([self.vec_meanoutdpt, self.vec_meanoutatn, self.vec_meanoutsnir])
        condit_3 = cl.is_ndarray([self.vec_meaninber, self.vec_meanoutber])
        # вывод размерностей векторов
        if condit_1 and condit_2 and condit_3:
            print("Модель ААР:")
            print("\tvec_meansnir.shape = ", self.vec_meansnir.shape)
            print("\tvec_meanindpt.shape = ", self.vec_meanindpt.shape)
            print("\tvec_meaninatn.shape = ", self.vec_meaninatn.shape)
            print("\tvec_meaninber.shape = ", self.vec_meaninber.shape)
            print("\tvec_meaninsnir.shape = ", self.vec_meaninsnir.shape)
            print("\tvec_meanoutdpt.shape = ", self.vec_meanoutdpt.shape)
            print("\tvec_meanoutatn.shape = ", self.vec_meanoutatn.shape)
            print("\tvec_meanoutber.shape = ", self.vec_meanoutber.shape)
            print("\tvec_meanoutsnir.shape = ", self.vec_meanoutsnir.shape)

    def print_calc(self):
        # вывод информации о ходе вычислений
        print("\nРАЗМЕРНОСТИ ВЕКТОРОВ")
        self.obj_set.print_out()
        self.obj_env.print_out()
        self.obj_array.print_out()
        self.obj_proc.print_out()
        self.obj_syntnet.print_out()
        self.print_out()

    def save_learn(self, list_set):
        # сохранение обучающей выборки
        out_data = self.get_data()
        self.obj_file.save_data(list_set, out_data, self.id_script)

    def init_vecmean(self, len_var, len_sig, len_int):
        # инициализация усреднённых векторов
        self.vec_meanindpt = np.zeros(shape=[len_var, len_int])
        self.vec_meaninatn = np.zeros(shape=[len_var, len_sig])
        self.vec_meaninber = np.zeros(shape=[len_var])
        self.vec_meaninsnir = np.zeros(shape=[len_var])
        self.vec_meanoutdpt = np.zeros(shape=[len_var, len_int])
        self.vec_meanoutatn = np.zeros(shape=[len_var, len_sig])
        self.vec_meanoutber = np.zeros(shape=[len_var])
        self.vec_meanoutsnir = np.zeros(shape=[len_var])
        self.vec_meansnir = np.zeros(shape=[len_var])

    def get_varpar(self, item=-1):
        # выдать значения параметров для скрипта
        var_par = []
        if item != -1:
            # если отсчёт начался
            if self.id_script == 8:
                # изменение полосы
                var_par = np.array([self.out_set[2][item]])
                print("var_bnd = ", np.round(var_par[0]*100)/100)
            if self.id_script == 9:
                # изменение амплитуды
                var_par = np.array([self.out_set[2][item]])
                print("var_amp = ", np.round(var_par[0]*100)/100)
        self.var_par = var_par
