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
        self.name_file = 'DF'

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
        # проверка и создание директории файла
        self.check_dir()
        # создание и сохранение файла
        name_file = self.get_namefile(list_set, out_data, id_script)
        # сохранение файла
        buf_report = self.save_data(name_file, out_data)
        # результат сохранения
        print(buf_report)

    def get_namefile(self, list_set, out_data, id_script):
        # получить название файла
        array_N, alg_type, control_type = list_set[2][1], list_set[3][1], list_set[3][5]
        mean_indepth, mean_inatten = out_data[4][8], out_data[4][9]
        mean_outdepth, mean_outatten = out_data[4][10], out_data[4][11]
        mean_outsnir = out_data[3][6]
        # вычисления
        mean_depth = (mean_outdepth - mean_indepth).sum()
        mean_atten = (mean_outatten - mean_inatten).sum()
        # формируем название
        name_file = self.name_file + '_N' + str(int(array_N))
        name_file = name_file + '_ALG' + str(int(alg_type))
        name_file = name_file + '_CON' + str(int(control_type))
        name_file = name_file + '_SCR' + str(int(id_script))
        name_file = name_file + '_DPT' + str(self.get_round(mean_depth))
        name_file = name_file + '_ATT' + str(self.get_round(mean_atten))
        name_file = name_file + '_SNIR' + str(self.get_round(mean_outsnir))
        return name_file

    def save_data(self, name_file, out_data):
        # распаковка данных для обучения
        out_env, out_array, out_proc, out_syntnet = out_data[1], out_data[2], out_data[3], out_data[4]
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = out_array[5], out_array[6], out_array[7]
        matrix_sig, matrix_int, matrix_nois = out_array[8], out_array[9], out_array[10]
        vec_sum, vec_inweight, vec_outweight = out_proc[0], out_proc[1], out_proc[2]
        # проверка типа на ndarray
        res = self.check_type(vec_sig, vec_int, vec_nois, matrix_sig,
                              matrix_int, matrix_nois, vec_inweight, vec_outweight)
        if res != True:
            return "Ошибка проверки типа данных"
        # сохранение csv
        data_file = pd.DataFrame(columns=['sig_deg', 'sig_amp', 'sig_band', 'int_deg', 'int_amp', 'int_band',
                                          'depth', 'atten', 'outsnir', 'vec_sum', 'outweight'])
        for i in range(len(out_array[5])):
            data_file.at[i, 'sig_deg'] = out_env[0][i].tolist()
            data_file.at[i, 'sig_amp'] = out_env[1][i].tolist()
            data_file.at[i, 'sig_band'] = out_env[2][i].tolist()
            data_file.at[i, 'int_deg'] = out_env[3][i].tolist()
            data_file.at[i, 'int_amp'] = out_env[4][i].tolist()
            data_file.at[i, 'int_band'] = out_env[5][i].tolist()
            data_file.at[i, 'depth'] = (out_syntnet[5][i] - out_syntnet[1][i]).tolist()
            data_file.at[i, 'atten'] = (out_syntnet[6][i] - out_syntnet[2][i]).tolist()
            data_file.at[i, 'outsnir'] = out_proc[4][i].tolist()
            data_file.at[i, 'vec_sum'] = out_proc[0][i].tolist()
            data_file.at[i, 'outweight'] = out_proc[2][i].tolist()
        data_file.to_csv(self.dir_data + '/' + name_file + '.csv')
        return "Файл успешно сохранен:\n" + self.dir_data + '/' + name_file + ".csv"

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
        # округление числа до тысячных
        return np.round(num*100)/100
