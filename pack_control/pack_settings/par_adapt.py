if __name__ == "__main__":
    print("Вы запустили модуль параметров адаптации (L3)")

class Par_adapt:
    """Класс исходных параметров адаптивного алгоритма"""

    def __init__(self):
        # АЛГОРИТМ АДАПТАЦИИ
        # критерий (0=максОСШП, 1=минШУМ), алгоритм (0=обрат_матрица, 1=нейросеть)
        # задержка на такт вычсления (0=выкл, 1=вкл)
        self.alg_crit = 0
        self.alg_type = 0
        self.alg_delay = 0
        # ФИЛЬТР КАЛМАНА
        # вкл. (0=нет, 1=да), коэф. (flt)
        self.klm_type = 0
        self.klm_sigma = 1
        # СХЕМА УПРАВЛЕНИЯ
        # тип (0=amp+phi, 1=phi), шаг дискретизации (flt)
        self.ctl_type = 0
        self.ctl_stepphi = 0
        self.ctl_stepamp = 1

    def set(self, init):
        self.alg_crit = init[0]
        self.alg_type = init[1]
        self.alg_delay = init[2]
        self.klm_type = init[3]
        self.klm_sigma = init[4]
        self.ctl_type = init[5]
        self.ctl_stepphi = init[6]
        self.ctl_stepamp = init[7]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.alg_type)
        res.append(self.alg_delay)
        res.append(self.klm_type)
        res.append(self.klm_sigma)
        res.append(self.ctl_type)
        res.append(self.ctl_stepphi)
        res.append(self.ctl_stepamp)
        return res

    def print(self):
        print("Параметры адаптации (L3):")
        print("\talg_crit = ", self.alg_crit)
        print("\talg_type = ", self.alg_type)
        print("\talg_delay = ", self.alg_delay)
        print("\tklm_type = ", self.klm_type)
        print("\tklm_sigma = ", self.klm_sigma)
        print("\tctl_type = ", self.ctl_type)
        print("\tctl_stepphi = ", self.ctl_stepphi)
        print("\tctl_stepamp = ", self.ctl_stepamp)
