if __name__ == "__main__":
    print("Вы запустили модуль модели фильтра Калмана (L3)")

class Kalman:
    """Класс моделирования фильтра Калмана"""

    def __init__(self, id):
        self.id = id
        self.id_kalman = []
        self.coef_kalman = []
        self.time_calc = []

    def set(self, init):
        self.id_kalman = init[5]
        self.coef_kalman = init[6]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_kalman)
        res.append(self.coef_kalman)
        res.append(self.time_calc)
        return res

    def print(self):
        print(" --- Параметры модели фильтра Калмана (L3) --- ")
        print("id = ", self.id)
        print("id_kalman = ", self.id_kalman)
        print("coef_kalman = ", self.coef_kalman)
        print("time_calc = ", self.time_calc)

    def print_short(self):
        print(" --- Параметры модели фильтра Калмана (L3) --- ")
        print("kalman = ", self.get())