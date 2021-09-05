# модуль динамической модели ААР

import pack_model
from pack_model import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль динамической модели ААР (L1)")
    print("Модуль использует пакет:", pack_model.NAME)

class Model_AAA:
    def __init__(self, id_control, id_view, id_model, mode):
        self.id_control = id_control
        self.id_view = id_view
        self.id_model = id_model
        self.mode = mode
        self.list_settings = pack_model.settings.Model(1)
        self.list_env = pack_model.environment.Env(1)
        self.list_array = pack_model.array.Array(1)
        self.list_proc = pack_model.processor.Processor(1)
        self.list_syntnet = pack_model.synthes_net.Synt_net(1)
        self.list_train = pack_model.train_nn.Train(1)
        self.list_test = pack_model.test.Test(1)
        self.list_file = pack_model.file_io.File_IO(1)
    def set(self, obj_set):
        # инициализация параметров уровня L2
        self.list_settings.set(obj_set.list_setmodel.get())
        self.list_env.set(obj_set.list_parenv.get())
        self.list_array.set(obj_set.list_pararray.get())
        self.list_proc.set(obj_set.list_paradapt.get())
        self.list_syntnet.set(obj_set.list_paradapt.get())
        self.list_train.set(obj_set.list_setnn.get())
        self.list_test.set(obj_set.list_settest.get())
        # инициализация параметров уровня L3
        self.list_env.list_gen.set(obj_set.list_parenv.get())
        self.list_array.list_factor.set(obj_set.list_pararray.get())
        self.list_array.list_element.set(obj_set.list_pararray.get())
        self.list_proc.list_tradalg.set(obj_set.list_paradapt.get())
        self.list_proc.list_neuroalg.set(obj_set.list_paradapt.get())
        self.list_proc.list_kalman.set(obj_set.list_paradapt.get())
    def get(self):
        res = []
        res.append(self.id_control)
        res.append(self.id_view)
        res.append(self.id_model)
        res.append(self.mode)
        return res
    def print(self):
        print(" --- ПАРАМЕТРЫ ДИНАМИЧЕСКОЙ МОДЕЛИ ААР (L1) --- ")
        print("id_control = ", self.id_control)
        print("id_view = ", self.id_view)
        print("id_model = ", self.id_model)
        print("mode = ", self.mode)
        self.list_settings.print_short()
        self.list_env.print_short()
        self.list_array.print_short()
        self.list_proc.print_short()
        self.list_syntnet.print_short()
        self.list_train.print_short()
        self.list_test.print_short()
        self.list_file.print_short()
    def print_short(self):
        print(" --- ПАРАМЕТРЫ ДИНАМИЧЕСКОЙ МОДЕЛИ ААР (L1) --- ")
        print("prog_model = ", self.get())
    def calc_out(self):
        # создание векторов изменения параметров
        self.list_settings.calc_out()
        out_set = self.list_settings.get_out()
        # создание векторов изменения сигналов и помех от времени
        self.list_env.calc_out(out_set)
        out_env = self.list_env.get_out()
        # вычисление сигналов с антенной решётки
        self.list_array.calc_out(out_set, out_env)
        out_array = self.list_array.get_out()
        # вычисление векторов ВК
        self.list_proc.calc_out(out_array)
        self.list_proc.calc_optout(out_array)
        out_weight = self.list_proc.get_out()
        # вычисление ДН и характеристик
        self.list_syntnet.calc_out(out_array, out_weight)
        out_syntnet = self.list_syntnet.get_out()
        # подгонка формата выходного вектора
        len_deg = out_array[0].shape[1]
        out_set[0] = out_set[0].reshape((len_deg, 1))
        #print(out_set[0].shape)
        #print(out_syntnet[0].shape)
        return [out_set[0], out_syntnet[0]]
    def print_out(self):
        # вывод информации о ходе вычислений
        self.list_settings.print_out()
        self.list_env.print_out()
        self.list_array.print_out()
        self.list_proc.print_out()