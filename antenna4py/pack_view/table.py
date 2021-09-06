# модуль вывода таблицы

if __name__ == "__main__":
    print("Вы запустили модуль вывода таблицы (L2)")

class Table:
    """Класс вывода таблиц для пользователя"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Параметры вывода таблицы (L2) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Параметры вывода таблицы (L2) --- ")
        print("table = ", self.get())