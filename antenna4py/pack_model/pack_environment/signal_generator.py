# модуль генератора сигналов

if __name__ == "__main__":
    print("Вы запустили модуль генератора сигналов (L3)")

class Generator:
    def __init__(self, id):
        self.id = id
    def set(self, init):
        pass
    def get(self):
        res = []
        res.append(self.id)
        return res
    def print(self):
        print(" --- Параметры генератора сигналов (L3) --- ")
        print("id = ", self.id)
    def print_short(self):
        print(" --- Параметры генератора сигналов (L3) --- ")
        print("signal_generator = ", self.get())

