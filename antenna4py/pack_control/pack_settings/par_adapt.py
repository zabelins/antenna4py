if __name__ == "__main__":
    print("Вы запустили модуль параметров адаптации (L3)")

class Par_adapt:
    """Класс исходных параметров адаптивного алгоритма"""

    def __init__(self, id):
        self.id = id
        # номера критерия адаптации (ограничения есть или нет)
        # номера алгоритма (прямое обращение матрицы, нейросеть)
        # задержка на такт вычсления
        self.alg_crit = 1
        self.alg_type = 1
        self.alg_delay = 1
        # параметры фильтра Калмана
        self.kalman_type = 0
        self.kalman_coef = 1
        # тип управления (amp+phi, phi)
        self.control_type = 1
        # дискретность управления
        self.control_stepphi = 0
        self.control_stepamp = 1

    def set(self, init):
        self.alg_crit = init[0]
        self.alg_type = init[1]
        self.alg_delay = init[2]
        self.kalman_type = init[3]
        self.kalman_coef = init[4]
        self.control_type = init[5]
        self.control_stepphi = init[6]
        self.control_stepamp = init[7]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.alg_type)
        res.append(self.alg_delay)
        res.append(self.kalman_type)
        res.append(self.kalman_coef)
        res.append(self.control_type)
        res.append(self.control_stepphi)
        res.append(self.control_stepamp)
        return res

    def print(self):
        print("Параметры адаптации (L3):")
        print("\talg_crit = ", self.alg_crit)
        print("\talg_type = ", self.alg_type)
        print("\talg_delay = ", self.alg_delay)
        print("\tkalman_type = ", self.kalman_type)
        print("\tkalman_coef = ", self.kalman_coef)
        print("\tcontrol_type = ", self.control_type)
        print("\tcontrol_stepphi = ", self.control_stepphi)
        print("\tcontrol_stepamp = ", self.control_stepamp)
