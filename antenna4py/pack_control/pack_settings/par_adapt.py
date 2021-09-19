if __name__ == "__main__":
    print("Вы запустили модуль параметров адаптации (L3)")

class Par_adapt:
    """Класс исходных параметров адаптивного алгоритма"""

    def __init__(self, id):
        self.id = id
        # номер типа адаптации (amp, phase, amp+phase)
        self.adapt_type = 1
        # номера критерия адаптации (ограничения есть или нет)
        # номера алгоритма (прямое обращение матрицы, нейросеть)
        self.alg_crit = 1
        self.alg_type = 1
        # параметры фильтра Калмана
        self.kalman_type = 1
        self.kalman_coef = 1
        # дискретность управления
        self.control_stepphi = 0
        self.control_stepamp = 1

    def set(self, init):
        self.adapt_type = init[0]
        self.alg_crit = init[1]
        self.alg_type = init[2]
        self.kalman_type = init[3]
        self.kalman_coef = init[4]
        self.control_stepphi = init[5]
        self.control_stepamp = init[6]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.adapt_type)
        res.append(self.alg_crit)
        res.append(self.alg_type)
        res.append(self.kalman_type)
        res.append(self.kalman_coef)
        res.append(self.control_stepphi)
        res.append(self.control_stepamp)
        return res

    def print(self):
        print(" --- Значения параметров адаптации (L3) --- ")
        print("id = ", self.id)
        print("adapt_type = ", self.adapt_type)
        print("alg_crit = ", self.alg_crit)
        print("alg_type = ", self.alg_type)
        print("kalman_type = ", self.kalman_type)
        print("kalman_coef = ", self.kalman_coef)
        print("control_stepphi = ", self.control_stepphi)
        print("control_stepamp = ", self.control_stepamp)

    def print_short(self):
        print(" --- Значения параметров адаптации (L3) --- ")
        print("par_adapt = ", self.get())