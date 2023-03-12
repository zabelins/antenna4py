if __name__ == "__main__":
    print("Вы запустили модуль теста ПО (L3)")

class Set_test:
    """Класс настроек тестирования программы"""

    def __init__(self):
        self.test_type = 0

    def set(self, init):
        self.test_type = init[0]

    def get(self):
        res = []
        res.append(self.test_type)
        return res

    def print(self):
        print("Значения настроек тестирования ПО (L3):")
        print("\ttest_type = ", self.test_type)
