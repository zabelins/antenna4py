if __name__ == "__main__":
    print("Вы запустили модуль модели фильтра Калмана (L3)")

class Kalman:
    """Класс моделирования фильтра Калмана"""

    def __init__(self, id):
        self.id = id
        # параметры фильтра Калмана
        self.kalman_type = []
        self.kalman_coef = []

    def set(self, init):
        self.kalman_type = init[2]
        self.kalman_coef = init[3]

    def get(self):
        res = []
        res.append(self.kalman_type)
        res.append(self.kalman_coef)
        return res

    def print(self):
        print("Параметры модели фильтра Калмана (L3):")
        print("\tkalman_type = ", self.kalman_type)
        print("\tcoef_kalman = ", self.kalman_coef)