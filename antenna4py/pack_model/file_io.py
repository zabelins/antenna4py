# модуль работы с файлами

if __name__ == "__main__":
    print("Вы запустили модуль работы с файлами (L2)")

class File_IO:
    def __init__(self, id):
        self.id = id
        self.dir = 'C:/crazy'
    def set(self, init):
        pass
    def get(self):
        res = []
        res.append(self.id)
        res.append(self.dir)
        return res
    def print(self):
        print(" --- Настройки работы с файлами (L2) --- ")
        print("id = ", self.id)
        print("dir = ", self.dir)
    def print_short(self):
        print(" --- Настройки работы с файлами (L2) --- ")
        print("file_io = ", self.get())