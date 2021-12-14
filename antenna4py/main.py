import prog_model
import prog_train
import prog_control
import prog_view

if __name__ == "__main__":
    print("Добро пожаловать в antenna4py!")

# создаём вид-модель-контроллер
model = prog_model.Model_antenna()
train = prog_train.Model_train()
controller = prog_control.Control(model, train)
view = prog_view.View(controller, model, train)

# запускаем вывод всей доступной информации
view.start_prog()
