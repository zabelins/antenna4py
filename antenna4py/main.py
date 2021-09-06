# главный скрипт запуска программы моделирования ААР

import prog_control
import prog_model
import prog_view
import numpy as np

if __name__ == "__main__":
    print("Добро пожаловать в программу моделирования ААР!")

# индексные переменные
id_control, id_view, id_model, mode = [1, 1, 1, 1]

# создаём контроллер-вид-модель
control1 = prog_control.Control(id_control, id_view, id_model, mode)
view1 = prog_view.View(id_control, id_view, id_model, mode)
model1 = prog_model.Model_AAA(id_control, id_view, id_model, mode)

# инициализируем числовую модель
view1.set(control1.list_set)
model1.set(control1.list_set)

# вывод служебной информации
#control1.print()
#view1.print()
#model1.print()

# вывод служебной информации для графика
out_model = model1.calc_out()
model1.print_out()

# вывод графика ДН
x = np.array([out_model[0], out_model[0]])
y = np.array([out_model[1], out_model[2]])
deg = out_model[3]
view1.list_graph.draw_pattern(x, y, deg)

# вывод графика характеристик
#x = np.array([[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]])
#y = np.array([[1, 2, 2, 2, 3], [2, 1, 0, 1, 0], [3, 4, 2, 1, 1]])
#view1.list_graph.draw_charact(x, y, ['s1','s2'])


#model1.list_proc.get_out(10)