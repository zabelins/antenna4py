if __name__ == "__main__":
    print("Вы запустили модуль тестирования ПО (L2)")

class Test:
    """Класс тестирования программы"""

    def __init__(self, id):
        self.id = id
        self.id_test = 1

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id_test)
        return res

    def print(self):
        print("Настройки тестирования ПО (L2):")
        print("\tid_test = ", self.id_test)