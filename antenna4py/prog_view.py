# модуль вывода информации

import pack_view
from pack_view import *
import numpy as np

if __name__ == "__main__":
    print("Вы запустили модуль вывода информации (L1)")
    print("Модуль использует пакет:", pack_view.NAME)

class View:
    """Класс вывода информации для пользователя"""

    def __init__(self, id_control, id_view, id_model, mode):
        self.id_control = id_control
        self.id_view = id_view
        self.id_model = id_model
        self.mode = mode
        self.list_graph = pack_view.graph.Graph(1)
        self.list_console = pack_view.console.Console(1)
        self.list_table = pack_view.table.Table(1)

    def set(self, obj_set):
        # инициализация параметров уровня L2
        self.list_graph.set(obj_set.list_setview.get())
        self.list_console.set(obj_set.list_setview.get())
        self.list_table.set(obj_set.list_setview.get())
        # инициализация параметров уровня L3
        self.list_graph.list_pattern.set(obj_set.list_setview.get())
        self.list_graph.list_charact.set(obj_set.list_setview.get())

    def get(self):
        res = []
        res.append(self.id_control)
        res.append(self.id_view)
        res.append(self.id_model)
        res.append(self.mode)
        return res

    def print(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ ВЫВОДА ИНФОРМАЦИИ (L1) --- ")
        print("id_control = ", self.id_control)
        print("id_view = ", self.id_view)
        print("id_model = ", self.id_model)
        print("mode = ", self.mode)
        self.list_graph.print_short()
        self.list_console.print_short()
        self.list_table.print_short()

    def print_short(self):
        print(" --- ПАРАМЕТРЫ МОДУЛЯ ВЫВОДА ИНФОРМАЦИИ (L1) --- ")
        print("prog_view = ", self.get())



