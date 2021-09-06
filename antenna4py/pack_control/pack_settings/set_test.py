# модуль настроек теста ПО

if __name__ == "__main__":
    print("Вы запустили модуль теста ПО (L3)")

class Set_test:
    """Класс настроек тестирования программы"""

    def __init__(self, id):
        self.id = id
        self.id_test = 1

    def set(self, init):
        self.id_test = init[0]

    def get(self):
        res = []
        res.append(self.id)
        res.append(self.id_test)
        return res

    def print(self):
        print(" --- Значения настроек тестирования ПО (L3) --- ")
        print("id = ", self.id)
        print("id_test = ", self.id_test)

    def print_short(self):
        print(" --- Значения настроек тестирования ПО (L3) --- ")
        print("settings_test = ", self.get())