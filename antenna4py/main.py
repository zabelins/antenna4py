import prog_control
import prog_model
import prog_view
import numpy as np

if __name__ == "__main__":
    print("Добро пожаловать в программу моделирования ААР!")

# создаём вид-модель-контроллер
model = prog_model.Model_AAA()
controller = prog_control.Control(model)
view = prog_view.View(model, controller)

# запускаем вывод всей доступной информации
view.start_prog()
