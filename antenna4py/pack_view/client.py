DESCRIPTION_MODE1 = """Возможные действия: 
\t1: расчёт диаграммы направленности ААР (t = const, par = const)
\t2: расчёт временных характеристик ААР для одного параметра (t = var, par = const)
\t3: расчёт временных характеристик ААР для различных параметров (t = var, par = var)
\t4: дополнительные действия
\t0: выход из программы"""
DESCRIPTION_MODE2 = """Возможные дополнительные действия: 
\t1: обучение нейронной сети 
\t2: настройки и параметры программы
\t0: выход из программы"""
DESCRIPTION_SCRIPT = """Возможные сценарии моделирования:
\t1: амплитуды - симуляция синусоидальных помех
\t2: амплитуды - симуляция меандровых помех
\t3: амплитуды - симуляция импульсных помех
\t4: углы - линейное изменение углов для одной помехи
\t5: рандом - генерирование случайных амплитуд, углов и частотных полос
\t0: выход из программы"""
NAME_MODE1 = "РЕЖИМ РАСЧЁТА ДИАГРАММЫ НАПРАВЛЕННОСТИ"
NAME_MODE2 = "РЕЖИМ РАСЧЁТА ВРЕМЕННЫХ ХАРАКТЕРИСТИК ААР (1 ПАРАМЕТР)"
NAME_MODE3 = "РЕЖИМ РАСЧЁТА ВРЕМЕННЫХ ХАРАКТЕРИСТИК ААР (N ПАРАМЕТРОВ)"
NAME_MODE4 = "РЕЖИМ ОБУЧЕНИЯ НЕЙРОННОЙ СЕТИ"
NAME_MODE5 = "РЕЖИМ ПРОСМОТРА НАСТРОЕК И ПАРАМЕТРОВ ПРОГРАММЫ"

if __name__ == "__main__":
    print("Вы запустили модуль интерфейса клиента (L2)")

class Client:
    """Класс интерфейса клиента"""

    def __init__(self, id):
        self.id = id

    def set(self, init):
        pass

    def get(self):
        res = []
        res.append(self.id)
        return res

    def print(self):
        print(" --- Параметры интерфейса пользователя (L2) --- ")
        print("id = ", self.id)

    def print_short(self):
        print(" --- Параметры интерфейса пользователя (L2) --- ")
        print("client = ", self.get())

    def input_mode(self):
        # главное меню действий
        print(DESCRIPTION_MODE1)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input("Введите номер действия: "))
                # проверка наличия действия
                if (input_buf < 0) or (input_buf > 4):
                    print("\tтакого действия нет")
                else:
                    # обработка выхода из программы
                    if input_buf == 0:
                        exit()
                    # обработка дополнительных действий
                    if input_buf == 4:
                        input_buf = self.input_modeadd()
                    # обработка выхода из цикла
                    res = 1
                    print("")
            except ValueError:
                print("\tнеобходимо ввести число")
        return input_buf

    def input_modeadd(self):
        # меню дополнительных действий
        print(DESCRIPTION_MODE2)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input("Введите номер действия: "))
                # проверка наличия действия
                if (input_buf < 0) or (input_buf > 2):
                    print("\tтакого действия нет")
                else:
                    res = 1
                    # обработка выхода из программы
                    if input_buf == 0:
                        exit()
                    # обработка действий
                    input_buf = input_buf + 3
            except ValueError:
                print("\tнеобходимо ввести число")
        return input_buf

    def print_namemode(self, id_mode):
        # вывод в консоль названия действия
        if (id_mode == 1):
            print(NAME_MODE1)
        if (id_mode == 2):
            print(NAME_MODE2)
        if (id_mode == 3):
            print(NAME_MODE3)
        if (id_mode == 4):
            print(NAME_MODE4)
        if (id_mode == 5):
            print(NAME_MODE5)

    def input_script(self):
        # меню выбора сценария для динамического режима
        print(DESCRIPTION_SCRIPT)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input("Введите номер сценария: "))
                # проверка наличия действия
                if (input_buf < 0) or (input_buf > 5):
                    print("\tтакого сценария нет")
                else:
                    res = 1
                    # обработка выхода из программы
                    if input_buf == 0:
                        exit()
            except ValueError:
                print("\tнеобходимо ввести число")
        return input_buf
