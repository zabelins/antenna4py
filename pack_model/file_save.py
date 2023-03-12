import pack_calc.calc_list as cl
import numpy as np
import pandas as pd
import os

if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_save:
    """Класс работы с сохранёнными файлами"""

    def __init__(self):
        # параметры работы с файлами
        self.str_dir = ''
        self.str_name = 'DATA'

    def set(self, init):
        self.str_dir = init[22]

    def get(self):
        res = []
        res.append(self.str_dir)
        res.append(self.str_name)
        return res

    def print(self):
        print("Настройки работы с файлами (L2):")
        print("\tstr_dir = ", self.str_dir)
        print("\tstr_name = ", self.str_name)

    def save_data(self, list_set, out_data, id_script):
        # сохранить файл
        print("\nСОХРАНЕНИЕ ФАЙЛА")
        # проверка и создание директории файла
        self.check_dir()
        # наименование файла
        self.name_file(list_set, out_data, id_script)
        # сохранение файла
        self.save_file(list_set, out_data)

    def name_file(self, list_set, out_data, id_script):
        # инициализация параметров
        arr_size, alg_crit, ctl_type = list_set[2][1], list_set[3][0], list_set[3][5]
        mean_indpt, mean_inatn = out_data[4][8], out_data[4][9]
        mean_outdpt, mean_outatn = out_data[4][10], out_data[4][11]
        mean_outsnir = out_data[3][5]
        # формируем название
        str_arr = '_N' + str(int(arr_size)) + '_ALG' + str(int(alg_crit)) + '_CTL' + str(int(ctl_type))
        str_prog = '_SCR' + str(int(id_script))
        str_dpt = '_DPT' + str(self.get_round((mean_outdpt - mean_indpt).sum()))
        str_atn = '_ATN' + str(self.get_round((mean_outatn - mean_inatn).sum()))
        str_snir = '_SNIR' + str(self.get_round(mean_outsnir))
        self.str_name = self.str_name + str_arr + str_prog + str_dpt + str_atn + str_snir

    def save_file(self, list_set, out_data):
        # распаковка данных для обучения
        out_env, out_array, out_proc, out_syntnet = out_data[1], out_data[2], out_data[3], out_data[4]
        # сохранение csv
        data_file = pd.DataFrame(columns=['sig_deg', 'sig_amp', 'sig_band', 'int_deg', 'int_amp', 'int_band',
                                          'nois_amp', 'depth', 'atten', 'outsnir', 'vec_sum', 'outweight'])
        # цикл по времени
        for i in range(out_env[0].shape[0]):
            data_file.at[i, 'sig_deg'] = out_env[0][i].tolist()
            data_file.at[i, 'sig_amp'] = out_env[1][i].tolist()
            data_file.at[i, 'sig_band'] = out_env[2][i].tolist()
            data_file.at[i, 'int_deg'] = out_env[3][i].tolist()
            data_file.at[i, 'int_amp'] = out_env[4][i].tolist()
            data_file.at[i, 'int_band'] = out_env[5][i].tolist()
            data_file.at[i, 'nois_amp'] = (np.array([list_set[2][5]])).tolist()
            data_file.at[i, 'depth'] = (out_syntnet[5][i] - out_syntnet[1][i]).tolist()
            data_file.at[i, 'atten'] = (out_syntnet[6][i] - out_syntnet[2][i]).tolist()
            data_file.at[i, 'outsnir'] = out_proc[3][i].tolist()
            data_file.at[i, 'vec_sum'] = out_array[11][0][i].tolist()
            data_file.at[i, 'outweight'] = out_proc[1][i].tolist()
        data_file.to_csv(self.str_dir + '/' + self.str_name + '.csv')
        # результат сохранения
        print("Файл успешно сохранен:\n" + self.str_dir + '/' + self.str_name + ".csv")

    def check_dir(self):
        # проверка и создание директории файла
        if os.path.exists(self.str_dir):
            pass
        else:
            os.mkdir(self.str_dir)

    def get_round(self, num):
        # округление числа до тысячных
        return np.round(num*100)/100
