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
        self.alg_crit = init[0]
        self.control_type = init[5]

    def get(self):
        res = []
        res.append(self.alg_crit)
        res.append(self.control_type)
        return res

    def print(self):
        print("Параметры модели НС алгоритма (L3):")
        print("\talg_crit = ", self.alg_crit)
        print("\tcontrol_type = ", self.control_type)
