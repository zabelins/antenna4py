if __name__ == "__main__":
    print("Вы запустили модуль отчётов о работе программы (L2)")

class Report:
    """Класс отчётов о работе программы"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Параметры отчётов о работе программы (L2) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Параметры отчётов о работе программы (L2) --- ")
        print("report = ", self.get())