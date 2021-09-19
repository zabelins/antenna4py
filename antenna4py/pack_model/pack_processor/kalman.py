if __name__ == "__main__":
    print("Вы запустили модуль модели фильтра Калмана (L3)")

class Kalman:
    """Класс моделирования фильтра Калмана"""

    def __init__(self, id):
        self.id = id
        self.kalman_type = []
        self.kalman_coef = []

    def set(self, init):
        self.kalman_type = init[4]
        self.kalman_coef = init[5]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.kalman_type)
        res.append(self.kalman_coef)
        return res

    def print(self):
        print(" --- Параметры модели фильтра Калмана (L3) --- ")
        print("id = ", self.id)
        print("kalman_type = ", self.kalman_type)
        print("coef_kalman = ", self.kalman_coef)

    def print_short(self):
        print(" --- Параметры модели фильтра Калмана (L3) --- ")
        print("kalman = ", self.get())