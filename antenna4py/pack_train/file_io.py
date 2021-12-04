import pack_calc.calc_list as cl
import numpy as np
import os

if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_IO:
    """Класс работы с сохранёнными файлами"""

    def __init__(self, id):
        self.id = id
        # параметры работы с файлами
        self.dir_data = []
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

    def save_file(self, vec_data):
        # сохранить файл
        print("\nСОХРАНЕНИЕ ФАЙЛА")
        # распаковка исходных данных
        out_array2nd, out_proc2nd, out_model = vec_data[0], vec_data[1], vec_data[2]
        # проверка и создание директории файла
        self.check_dir()
        # создание и сохранение файла
        name_file = self.get_namefile(out_model)
        # сохранение файла
        buf_report = self.save_data(name_file, out_array2nd, out_proc2nd)
        # результат сохранения
        print(buf_report)

    def load_files(self):
        # проверка списка доступных файлов
        if os.path.exists(self.dir_data + '/'):
            file_list = os.listdir(self.dir_data + '/')
        else:
            print("Файлы с обучающими выборками не найдены")
            return []
        # вывод числа доступных файлов
        len_files = len(file_list)
        print("Найдено файлов с обучающими выборками:", len_files)
        # запуск цикла по файлам
        for i in range(len_files):
            # прочитать файл
            var_file = np.load(self.dir_data + '/' + file_list[i])
            # загрузка данных
            var_data = self.read_data(var_file)
            # заполнение векторов
            self.vec_sig.append(var_data[0])
            self.vec_int.append(var_data[1])
            self.vec_nois.append(var_data[2])
            self.matrix_sig.append(var_data[3])
            self.matrix_int.append(var_data[4])
            self.matrix_nois.append(var_data[5])
            self.vec_inweight.append(var_data[6])
            self.vec_outweight.append(var_data[7])
        # возврат данных
        return [self.vec_sig, self.vec_int, self.vec_nois, self.matrix_sig,
                self.matrix_int, self.matrix_nois, self.vec_inweight, self.vec_outweight]

    def get_namefile(self, out_model):
        # получить название файла
        array_N, alg_type, control_type, id_script = out_model[0], out_model[1], out_model[2], out_model[3]
        mean_depth, mean_atten, mean_snir = out_model[4], out_model[5], out_model[6]
        # формируем название
        name_file = self.name_file + '_N' + str(int(array_N))
        name_file = name_file + '_A' + str(int(alg_type))
        name_file = name_file + '_C' + str(int(control_type))
        name_file = name_file + '_SCR' + str(int(id_script))
        name_file = name_file + '_DPT' + str(self.get_round(mean_depth))
        name_file = name_file + '_ATT' + str(self.get_round(mean_atten))
        name_file = name_file + '_SNIR' + str(self.get_round(mean_snir))
        return self.dir_data + '/' + name_file

    def save_data(self, name_file, out_array2nd, out_proc2nd):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = out_array2nd[0], out_array2nd[1], out_array2nd[2]
        matrix_sig, matrix_int, matrix_nois = out_array2nd[3], out_array2nd[4], out_array2nd[5]
        vec_inweight, vec_outweight = out_proc2nd[0], out_proc2nd[1]
        # проверка типа на ndarray
        res = self.check_type(vec_sig, vec_int, vec_nois, matrix_sig,
                              matrix_int, matrix_nois, vec_inweight, vec_outweight)
        if (res != True):
            return "Ошибка проверки типа данных"
        # сохранение
        np.savez(name_file, vec_sig=vec_sig, vec_int=vec_int, vec_nois=vec_nois,
                 matrix_sig=matrix_sig, matrix_int=matrix_int, matrix_nois=matrix_nois,
                 vec_inweight=vec_inweight, vec_outweight=vec_outweight)
        return "Файл успешно сохранён:\n" + name_file + ".npz"

    def read_data(self, var_file):
        # распаковка исходных данных
        vec_sig, vec_int, vec_nois = var_file['vec_sig'], var_file['vec_int'], var_file['vec_nois']
        matrix_sig, matrix_int, matrix_nois = var_file['matrix_sig'], var_file['matrix_int'], var_file['matrix_nois']
        vec_inweight, vec_outweight = var_file['vec_inweight'], var_file['vec_outweight']
        # проверка типа на ndarray
        res = self.check_type(vec_sig, vec_int, vec_nois, matrix_sig,
                              matrix_int, matrix_nois, vec_inweight, vec_outweight)
        if (res != True):
            print("Ошибка проверки типа данных")
            return
        # возврат данных
        return [vec_sig, vec_int, vec_nois, matrix_sig, matrix_int, matrix_nois, vec_inweight, vec_outweight]

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
