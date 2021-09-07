if __name__ == "__main__":
    print("Вы запустили модуль параметров адаптации (L3)")

class Par_adapt:
    """Класс исходных параметров адаптивного алгоритма"""

    def __init__(self, id):
        self.id = id
        self.id_type = 1
        self.id_crit = 1
        self.id_alg = 1
        self.id_kalman = 1
        self.coef_kalman = 1
        self.control_phistep = 0
        self.control_ampstep = 1

    def set(self, init):
        self.id_type = init[0]
        self.id_crit = init[1]
        self.id_alg = init[2]
        self.id_kalman = init[3]
        self.coef_kalman = init[4]
        self.control_phistep = init[5]
        self.control_ampstep = init[6]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_type)
        res.append(self.id_crit)
        res.append(self.id_alg)
        res.append(self.id_kalman)
        res.append(self.coef_kalman)
        res.append(self.control_phistep)
        res.append(self.control_ampstep)
        return res

    def print(self):
        print(" --- Значения параметров адаптации (L3) --- ")
        print("id = ", self.id)
        print("id_type = ", self.id_type)
        print("id_crit = ", self.id_crit)
        print("id_alg = ", self.id_alg)
        print("id_kalman = ", self.id_kalman)
        print("coef_kalman = ", self.coef_kalman)
        print("control_phistep = ", self.control_phistep)
        print("control_ampstep = ", self.control_ampstep)

    def print_short(self):
        print(" --- Значения параметров адаптации (L3) --- ")
        print("parameters_adapt = ", self.get())