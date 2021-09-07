if __name__ == "__main__":
    print("Вы запустили модуль тестирования ПО (L2)")

class Test:
    """Класс тестирования программы"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Настройки тестирования ПО (L2) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Настройки тестирования ПО (L2) --- ")
        print("test = ", self.get())