if __name__ == "__main__":
    print("Вы запустили модуль модели НС алгоритма (L3)")

class Neuro_alg:
    """Класс моделирования НС алгоритмов"""

    def __init__(self, id):
        self.id = id
        self.adapt_type = []
        self.alg_crit = []

    def set(self, init):
        self.adapt_type = init[1]
        self.alg_crit = init[2]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.adapt_type)
        res.append(self.alg_crit)
        return res

    def print(self):
        print(" --- Параметры модели НС алгоритма (L3) --- ")
        print("id = ", self.id)
        print("adapt_type = ", self.adapt_type)
        print("alg_crit = ", self.alg_crit)

    def print_short(self):
        print(" --- Параметры модели НС алгоритма (L3) --- ")
        print("neuro_alg = ", self.get())