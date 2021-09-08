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
#model1.print_out()

# распаковка данных
out_syntnet = out_model[0]
vec_pattern, vec_time = out_model[1], out_model[2]
vec_degsig, vec_degint = out_model[3], out_model[4]
vec_eqdegsig, vec_eqdegint = out_model[5], out_model[6]

# вывод графика ДН
time = 1
x = np.array([vec_pattern, vec_pattern])
y = np.array([out_syntnet[0][time], out_syntnet[1][time]])
view1.list_graph.draw_pattern(x, y, vec_degint[time])

# вывод графика характеристик
depth = out_syntnet[2].T
atten = out_syntnet[3].T
x = np.array([vec_time, vec_time, vec_time])
y = np.array([atten[0], depth[0], depth[1]])
view1.list_graph.draw_charact(x, y, ['dp','time'])


#model1.list_proc.get_out(10)