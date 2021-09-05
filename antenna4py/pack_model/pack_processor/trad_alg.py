# модуль модели традиционного алгоритма

if __name__ == "__main__":
    print("Вы запустили модуль модели традиционного алгоритма (L3)")

class Trad_alg:
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
        print(" --- Параметры модели традиционного алгоритма (L3) --- ")
        print("id = ", self.id)
        print("time_calc = ", self.time_calc)
    def print_short(self):
        print(" --- Параметры модели традиционного алгоритма (L3) --- ")
        print("trad_alg = ", self.get())
