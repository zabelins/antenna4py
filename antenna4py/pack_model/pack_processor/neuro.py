if __name__ == "__main__":
    print("Вы запустили модуль модели НС алгоритма (L3)")

class Neuro_alg:
    """Класс моделирования НС алгоритмов"""

    def __init__(self, id):
        self.id = id
        # номер критерия адаптации
        self.alg_crit = []
        # тип управления
        self.control_type = []

    def set(self, init):
        self.alg_crit = init[1]
        self.control_type = init[5]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.alg_crit)
        res.append(self.control_type)
        return res

    def print(self):
        print(" --- Параметры модели НС алгоритма (L3) --- ")
        print("id = ", self.id)
        print("alg_crit = ", self.alg_crit)
        print("control_type = ", self.control_type)

    def print_short(self):
        print(" --- Параметры модели НС алгоритма (L3) --- ")
        print("neuro_alg = ", self.get())