import prog_control
import prog_model
import prog_train
import prog_view
import numpy as np

if __name__ == "__main__":
    print("Добро пожаловать в antenna4py!")

# создаём вид-модель-контроллер
model_antenna = prog_model.Model_antenna()
model_train = prog_train.Model_train()
controller = prog_control.Control(model_antenna, model_train)
view = prog_view.View(model_antenna, model_train, controller)

# запускаем вывод всей доступной информации
view.start_prog()
