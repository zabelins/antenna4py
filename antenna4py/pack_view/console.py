# модуль вывода текста

if __name__ == "__main__":
    print("Вы запустили модуль вывода текста (L2)")

class Console:
    """Класс вывода текста для пользователя"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Параметры вывода текста (L2) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Параметры вывода текста (L2) --- ")
        print("console = ", self.get())