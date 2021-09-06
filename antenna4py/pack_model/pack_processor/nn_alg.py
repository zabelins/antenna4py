# модуль модели нейросетевого алгоритма

if __name__ == "__main__":
    print("Вы запустили модуль модели НС алгоритма (L3)")

class Neuro_alg:
    """Класс моделирования НС алгоритмов"""

    def __init__(self, id):
        self.id = id
        self.time_calc = []

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.time_calc)
        return res

    def print(self):
        print(" --- Параметры модели НС алгоритма (L3) --- ")
        print("id = ", self.id)
        print("time_calc = ", self.time_calc)

    def print_short(self):
        print(" --- Параметры модели НС алгоритма (L3) --- ")
        print("neuro_alg = ", self.get())