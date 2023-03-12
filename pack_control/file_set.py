if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_set:
    """Класс работы с сохранёнными файлами"""

    def __init__(self):
        self.dir_set = []

    def set(self, init):
        self.dir_set = init[19]

    def get(self):
        res = []
        res.append(self.dir_set)
        return res

    def print(self):
        print("Настройки работы с файлами (L2):")
        print("\tdir_set = ", self.dir_set)
