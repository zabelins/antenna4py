if __name__ == "__main__":
    print("Вы запустили модуль тестирования ПО (L2)")

class Test:
    """Класс тестирования программы"""

    def __init__(self):
        self.test_type = []

    def set(self, init):
        self.test_type = init[0]

    def get(self):
        res = []
        res.append(self.test_type)
        return res

    def print(self):
        print("Настройки тестирования ПО (L2):")
        print("\ttest_type = ", self.test_type)