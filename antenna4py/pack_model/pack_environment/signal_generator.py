import pack_calc.calc_list as cl
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль генератора сигналов (L3)")

class Generator:
    """Класс моделирования генератора сигналов"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Параметры генератора сигналов (L3) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Параметры генератора сигналов (L3) --- ")
        print("signal_generator = ", self.get())

    def get_vecdeg(self, len_time, var_deg, id_modulation):
        # вычисление вектора изменения углов
        len_deg = var_deg.shape[0]
        vec_mod = []
        if (id_modulation == 0):
            # углы без изменений
            vec_mod = np.ones(shape=[len_deg, len_time])
        else:
            # линейное изменение углов (!!! добавить !!!)
            vec_mod = np.ones(shape=[len_deg, len_time])
        # вектора после модуляции
        vec_deg = cl.ones_modul(vec_mod, var_deg)
        return vec_deg

    def get_vecamp(self, len_time, var_amp, id_modulation):
        # вычисление вектора изменения амплитуд
        len_amp = var_amp.shape[0]
        vec_mod = []
        if (id_modulation == 0):
            # амплитуды без изменений
            vec_mod = np.ones(shape=[len_amp, len_time])
        if (id_modulation == 1):
            # синусоидальный сигнал (!!! добавить !!!)
            vec_mod = np.ones(shape=[len_amp, len_time])
        if (id_modulation == 2):
            # прямоугольные импульсы (!!! добавить !!!)
            vec_mod = np.ones(shape=[len_amp, len_time])
        vec_amp = cl.ones_modul(vec_mod, var_amp)
        return vec_amp

    def get_vecband(self, len_time, var_band, id_modulation):
        # вычисление вектора изменения частотных полос
        len_band = var_band.shape[0]
        vec_mod = []
        if (id_modulation == 0):
            # частотные полосы без изменений
            vec_mod = np.ones(shape=[len_band, len_time])
        vec_band = cl.ones_modul(vec_mod, var_band)
        return vec_band

