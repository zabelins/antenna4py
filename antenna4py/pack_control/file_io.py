if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_IO:
    """Класс работы с сохранёнными файлами"""

    def __init__(self, id):
        self.id = id
        self.dir = 'C:/crazy'

    def get(self):
        res = []
        res.append(self.dir)
        return res

    def print(self):
        print("Настройки работы с файлами (L2):")
        print("\tdir = ", self.dir)
