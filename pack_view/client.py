DESCRIPTION_MENU_MAIN = """Действия: 
\t1: статичная ДН ААР [static: t=const, par=const]
\t2: временные хар-ки [time: t=var, par=const]
\t3: усреднённые хар-ки [par: t=var, par=var]
\t4: дополнительно
\t0: выход"""
DESCRIPTION_MENU_ADD = """Дополнительные действия: 
\t1: сравнение алгоритмов
\t2: обучение нейросети 
\t3: параметры программы
\t4: параметры моделей (проверка)
\t5: параметры графиков (проверка)
\t0: выход"""
DESCRIPTION_MENU_TIME = """Помеховая обстановка:
\t1: тест - модуляция [mod=var]
\t2: тест - углы одной помехи [deg=var]
\t3: обучение - одиночная помеха [amp,deg,band=rand]
\t4: обучение - мерцающая помеха [amp,deg,band=rand]
\t5: обучение с накоплением - шумовая помеха [amp,deg,band=rand]
\t6: обучение с накоплением - импульсная помеха [amp,deg,band=rand]
\t7: обучение с накоплением - мерцающая помеха [amp,deg,band=rand]
\t0: выход"""
DESCRIPTION_MENU_PAR = """Зависимости:
\t1: тест - полоса помехи [band=var]
\t2: тест - мощность сигнала [amp=var]
\t0: выход"""
DESCRIPTION_TRAIN = """\nСценарии обучения:
\t1: запустить обучение
\t0: выход"""
NAME_MODE1 = "\nРАСЧЁТ ДИАГРАММЫ НАПРАВЛЕННОСТИ"
NAME_MODE2 = "\nРАСЧЁТ ВРЕМЕННЫХ ХАРАКТИРИСТИК"
NAME_MODE3 = "\nРАСЧЁТ УСРЕДНЁННЫХ ХАРАКТЕРИСТИК"
NAME_MODE4 = "\nСРАВНЕНИЕ АЛГОРИТМОВ"
NAME_MODE5 = "\nОБУЧЕНИЕ НЕЙРОСЕТИ"
NAME_MODE6 = "\nПРОСМОТР НАСТРОЕК ПРОГРАММЫ"
NAME_MODE7 = "\nПРОСМОТР ПАРАМЕТРОВ МОДЕЛИ (ПРОВЕРКА)"
NAME_MODE8 = "\nПРОСМОТР ПАРАМЕТРОВ ГРАФИКОВ (ПРОВЕРКА)"
MSG_INPUT = "Введите номер: "
MSG_ERRNUM = "\tнеобходимо ввести число"
MSG_ERRACT = "\tтакого номера нет"

if __name__ == "__main__":
    print("Вы запустили модуль интерфейса клиента (L2)")

class Client:
    """Класс интерфейса клиента"""

    def __init__(self):
        pass

    def set(self, init):
        pass

    def get(self):
        res = []
        return res

    def print(self):
        print("Параметры интерфейса пользователя (L2):")
        print("\t-")

    def menu_main(self):
        # главное меню действий
        print(DESCRIPTION_MENU_MAIN)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input(MSG_INPUT))
                # проверка наличия действия
                if input_buf < 0 or input_buf > 4:
                    print(MSG_ERRACT)
                else:
                    res = 1
                    # выход из программы
                    if input_buf == 0:
                        exit()
                    # дополнительные действия
                    if input_buf == 4:
                        input_buf = self.menu_add()
                self.print_mode(input_buf)
            except ValueError:
                print(MSG_ERRNUM)
        return input_buf

    def menu_add(self):
        # меню дополнительных действий
        print(DESCRIPTION_MENU_ADD)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input(MSG_INPUT))
                # проверка наличия действия
                if input_buf < 0 or input_buf > 5:
                    print(MSG_ERRACT)
                else:
                    res = 1
                    # выход из программы
                    if input_buf == 0:
                        exit()
                    # коррекция номера
                    input_buf = input_buf + 3
            except ValueError:
                print(MSG_ERRNUM)
        return input_buf

    def menu_time(self):
        # меню сценариев временных характеристик
        print(DESCRIPTION_MENU_TIME)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input(MSG_INPUT))
                # проверка наличия действия
                if (input_buf < 0) or (input_buf > 7):
                    print(MSG_ERRACT)
                else:
                    res = 1
                    # обработка выхода из программы
                    if input_buf == 0:
                        exit()
            except ValueError:
                print(MSG_ERRNUM)
        return input_buf

    def menu_par(self):
        # меню сценариев усреднённых характеристик
        print(DESCRIPTION_MENU_PAR)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input(MSG_INPUT))
                # проверка наличия действия
                if (input_buf < 0) or (input_buf > 2):
                    print(MSG_ERRACT)
                else:
                    res = 1
                    # обработка выхода из программы
                    if input_buf == 0:
                        exit()
                    # коррекция номера
                    input_buf = input_buf + 7
            except ValueError:
                print(MSG_ERRNUM)
        return input_buf

    def input_train(self):
        # меню выбора сценария для динамического режима
        print(DESCRIPTION_TRAIN)
        res, input_buf = 0, []
        while res == 0:
            try:
                # ввод номера действия
                input_buf = int(input(MSG_INPUT))
                # проверка наличия действия
                if (input_buf < 0) or (input_buf > 1):
                    print(MSG_ERRACT)
                else:
                    res = 1
                    # обработка выхода из программы
                    if input_buf == 0:
                        exit()
            except ValueError:
                print(MSG_ERRNUM)
        return input_buf

    def print_mode(self, id_mode):
        # вывод названия режима
        if id_mode == 1:
            print(NAME_MODE1)
        elif id_mode == 2:
            print(NAME_MODE2)
        elif id_mode == 3:
            print(NAME_MODE3)
        elif id_mode == 4:
            print(NAME_MODE4)
        elif id_mode == 5:
            print(NAME_MODE5)
        elif id_mode == 6:
            print(NAME_MODE6)
        elif id_mode == 7:
            print(NAME_MODE7)
        elif id_mode == 8:
            print(NAME_MODE8)