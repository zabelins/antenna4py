import pack_calc.calc_list as cl
import numpy as np
import pandas as pd
import os

if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_IO:
    """Класс работы с сохранёнными файлами"""

    def __init__(self, id):
        self.id = id
        # параметры работы с файлами
        self.dir_data = ''
        self.name_file = 'CL'
        # формирование обучающей выборки
        self.vec_sig = []
        self.vec_int = []
        self.vec_nois = []
        self.matrix_sig = []
        self.matrix_int = []
        self.matrix_nois = []
        self.vec_inweight = []
        self.vec_outweight = []

    def set(self, init):
        self.dir_data = init[12]

    def get(self):
        res = []
        res.append(self.dir_data)
        res.append(self.name_file)
        return res

    def print(self):
        print("Настройки работы с файлами (L2):")
        print("\tdir_data = ", self.dir_data)
        print("\tname_file = ", self.name_file)

    def save_file(self, list_set, out_data, id_script):
        # сохранить файл
        print("\nСОХРАНЕНИЕ ФАЙЛА")
        # распаковка данных для обучения
        out_array, out_proc = out_data[2], out_data[3]
        # распаковка служебных данных
        par_array, par_adapt = list_set[2], list_set[3]
        out_model = out_data[5]
        # проверка и создание директории файла
        self.check_dir()
        # создание и сохранение файла
        name_file = self.get_namefile(par_array, par_adapt, out_model, id_script)
        # сохранение файла
        buf_report = self.save_data(name_file, out_array, out_proc)
        # результат сохранения
        print(buf_report)

    def get_namefile(self, par_array, par_adapt, out_model, id_script):
        # получить название файла
        array_N, alg_type, control_type = par_array[1], par_adapt[1], par_adapt[5]
        vec_meanindepth, vec_meaninatten = out_model[1], out_model[2]
        vec_meanoutdepth, vec_meanoutatten = out_model[4], out_model[5]
        vec_meanoutsnir = out_model[6]
        # вычисления
        mean_depth = vec_meanoutdepth.mean(axis=0) - vec_meanindepth.mean(axis=0)
        mean_atten = vec_meanoutatten.mean(axis=0) - vec_meaninatten.mean(axis=0)
        mean_depth = mean_depth.sum()
        mean_atten = mean_atten.sum()
        mean_snir = vec_meanoutsnir.mean()
        # формируем название
        name_file = self.name_file + '_N' + str(int(array_N))
        name_file = name_file + '_A' + str(int(alg_type))
        name_file = name_file + '_C' + str(int(control_type))
        name_file = name_file + '_SCR' + str(int(id_script))
        name_file = name_file + '_DPT' + str(self.get_round(mean_depth))
        name_file = name_file + '_ATT' + str(self.get_round(mean_atten))
        name_file = name_file + '_SNIR' + str(self.get_round(mean_snir))
        return self.dir_data + '/' + name_file

    def save_data(self, name_file, out_array, out_proc):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = out_array[5], out_array[6], out_array[7]
        matrix_sig, matrix_int, matrix_nois = out_array[8], out_array[9], out_array[10]
        vec_inweight, vec_outweight = out_proc[1], out_proc[2]
        # проверка типа на ndarray
        res = self.check_type(vec_sig, vec_int, vec_nois, matrix_sig,
                              matrix_int, matrix_nois, vec_inweight, vec_outweight)
        if res != True:
            return "Ошибка проверки типа данных"
        # сохранение
        np.savez(name_file, vec_sig=vec_sig, vec_int=vec_int, vec_nois=vec_nois,
                 matrix_sig=matrix_sig, matrix_int=matrix_int, matrix_nois=matrix_nois,
                 vec_inweight=vec_inweight, vec_outweight=vec_outweight)
        return "Файл успешно сохранён:\n" + name_file + ".npz"

    def check_type(self, *args):
        # проверка типа на ndarray
        bool_res = cl.is_ndarray([*args])
        return bool_res

    def check_dir(self):
        # проверка и создание директории файла
        if os.path.exists(self.dir_data):
            pass
        else:
            os.mkdir(self.dir_data)

    def get_round(self, num):
        # округление числа
        return round(num * 100) / 100
