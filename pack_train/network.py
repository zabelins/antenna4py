import os
import numpy as np
import matplotlib.pylab as plt
from keras.models import Sequential, load_model
from keras.layers import Layer, Dense, Conv2D, Flatten, AveragePooling1D, Dropout, SimpleRNN, Input, LSTM
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras import backend as K

if __name__ == "__main__":
    print("Вы запустили модуль обучения НС (L2)")

class Network:
    """Класс модуль обучения НС"""

    def __init__(self):
        # параметры нейронной сети
        self.net_type = []
        self.net_nodes = []
        # параметры выборки
        self.learn_size = 0
        # параметры обучения
        self.learn_batch = []
        self.learn_epoch = []
        # имя сохранения НС
        self.dir_net = ''
        self.name_net = 'NN'
        self.name_file = ''
        # вектора обучающей выборки
        self.x_train = []
        self.y_train = []
        # вектора тестовой выборки
        self.x_test = []
        self.y_test = []

    def set(self, init0, init1, init2):
        self.learn_size = np.array(init0[16])
        self.net_type = init1[0]
        self.net_nodes = init1[1]
        self.learn_batch = init1[2]
        self.learn_epoch = init1[3]
        self.dir_net = init2[23]

    def get(self):
        res = []
        res.append(self.net_type)
        res.append(self.net_nodes)
        res.append(self.learn_batch)
        res.append(self.learn_epoch)
        res.append(self.dir_net)
        return res

    def print(self):
        print("Параметры обучения НС (L3):")
        print("\tnet_type = ", self.net_type)
        print("\tnet_nodes = ", self.net_nodes)
        print("\tlearn_batch = ", self.learn_batch)
        print("\tlearn_epoch = ", self.learn_epoch)
        print("\tdir_net = ", self.dir_net)

    def calc_out(self, out_sampling, id_train):
        # распаковка исходных данных
        self.x_train, self.y_train = out_sampling[0], out_sampling[1]
        self.x_test, self.y_test = out_sampling[2], out_sampling[3]
        # приветствие
        print("\nИНИЦИАЛИЗАЦИЯ НС...")
        print("\tАлгоритм обучения ", id_train)
        # обучение НС
        self.start_train()

    def print_out(self):
        pass

    def start_train(self):
        # эксперименты с НС
        print("Тестовое обучение НС")
        # отключение предупреждений
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        # создаём модель НС
        net_model = Sequential()
        # определяем тип архитектуры НС
        if self.net_type == 0:
            net_model = self.create_mlp(net_model)
        elif self.net_type == 1:
            net_model = self.create_rbf(net_model)
        elif self.net_type == 2:
            net_model = self.create_cnn(net_model)
        elif self.net_type == 3:
            net_model = self.create_rnn(net_model)
        # вывод информации о сети
        print(net_model.summary())
        # возможные значения гиперпараметров
        activation = ['softmax', 'relu', 'tanh', 'sigmoid', 'linear']
        neurons = [5, 10, 15, 25, 35, 50]
        param_grid = dict(activation=activation, neurons=neurons)
        # ранняя остановка обучения
        es = EarlyStopping(monitor='val_loss', mode='min', patience=5)
        # запуск тренировки сети
        fit_results = net_model.fit(x=self.x_train, y=self.y_train,
                                    validation_data=(self.x_test, self.y_test),
                                    batch_size=self.learn_batch,
                                    epochs=self.learn_epoch,
                                    callbacks=[es])
        # сохранение сети
        self.save_net(net_model)
        # графики обучения
        self.show_graph(fit_results)
        # оценка точности сохранённой сети на тестовых данных
        print("Оценка точности сохранённой НС на тестовых данных")
        net_loaded = load_model(self.dir_net + '/' + self.name_file)
        score = net_loaded.evaluate(self.x_test, self.y_test, batch_size=1)
        print('test loss, test acc:', score)
        # прогноз 1 значения (проверка НС)
        #print("Прогноз значения")
        #x = np.expand_dims(self.x_test[0], axis=0)  # формируем вектор
        #predicted = net_loaded.predict(x)
        #print("predicted = ", predicted)

    def create_mlp(self, net_model):
        # создаём многослойный персептрон (MLP)
        # добавляем линейный стек слоёв
        net_model.add(Dense(units=self.net_nodes[1],            # выходная размерность
                            input_shape=(self.net_nodes[0],),   # входная размерность
                            activation='sigmoid'))              # активация (sigmoid, tanh)
        #net_model.add(Dense(units=self.net_nodes[1],
        #                    activation='sigmoid'))
        net_model.add(Dense(units=self.net_nodes[2],
                            activation='linear'))
        # компилятор НС
        net_model.compile(optimizer='adam', loss='mse', metrics=['mse', 'mae', 'mape'])
        return net_model

    def create_rbf(self, net_model):
        # создаём радиально-базисную сеть (RBF)
        net_model.add(Dense(units=self.net_nodes[0],
                            input_shape=(self.net_nodes[0],),
                            activation='linear'))
        net_model.add(RBFLayer(self.net_nodes[1], 0.5))
        net_model.add(Dense(self.net_nodes[2],
                            activation='linear'))
        # компиляция НС с оптимизацией Adam
        net_model.compile(optimizer='adam', loss='mse', metrics=['mse', 'mae', 'mape'])
        return net_model

    def create_cnn(self, net_model):
        # создаём свёрточную НС (CNN)
        # преобразуем входные данные
        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0], 3, 10, 1))
        self.x_test = np.reshape(self.x_test, (self.x_test.shape[0], 3, 10, 1))
        print("x_train.shape = ", self.x_train.shape)
        # создаём слои CNN, padding='same' (с нулями), padding='valid' (без нулей)
        net_model.add(Conv2D(filters=6, kernel_size=(1, 3), input_shape=(3, 10, 1), padding='same', activation='sigmoid'))
        # net_model.add(AveragePooling2D(pool_size=(1, 2), padding='valid', data_format=None))
        net_model.add(Flatten(data_format=None))
        net_model.add(Dense(20, activation='sigmoid'))
        net_model.add(Dense(30, activation='linear'))
        # компиляция НС с оптимизацией Adam
        net_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return net_model

    def create_rnn(self, net_model):
        # создаём рекуррентную нейронную сеть (RNN)
        net_model.add(LSTM(units=80, input_shape=(self.learn_size-1, 20)))    # return_sequences=True
        net_model.add(Dense(units=20, activation='sigmoid'))
        # компиляция НС с оптимизацией Adam
        net_model.compile(optimizer='adam', loss='mse', metrics=['mae']) # 'mse', 'mae', 'mape'
        return net_model

    def save_net(self, net_model):
        # сохранение НС
        print("Сохранение НС")
        self.check_dir(self.dir_net)
        self.get_namefile()
        net_model.save(self.dir_net + '/' + self.name_file)

    def get_namefile(self):
        # получить название файла
        name_file = self.name_net + '_TYP' + str(int(self.net_type))
        #name_file = name_file + '_LAY' + str(int(self.net_layers))
        #name_file = name_file + '_NOD' + str(self.net_nodes)
        self.name_file = name_file

    def check_dir(self, dir_net):
        # проверка и создание директории файла
        if os.path.exists(dir_net):
            pass
        else:
            os.mkdir(dir_net)

    def show_graph(self, fit_results):
        # отрисовка графиков обучения
        fig = plt.figure(figsize=(12, 5))
        ax_1 = fig.add_subplot(1, 2, 1)
        ax_2 = fig.add_subplot(1, 2, 2)
        ax_1.set(title='Ошибка обучения', xlabel='epoch', ylabel='loss')
        ax_2.set(title='Метрика обучения', xlabel='epoch', ylabel='mae')
        ax_1.plot(fit_results.history['loss'])
        ax_1.plot(fit_results.history['val_loss'])
        ax_1.legend(['training set', 'test set'], loc='best')
        ax_2.plot(fit_results.history['mae'])
        ax_2.plot(fit_results.history['val_mae'])
        ax_2.legend(['training set', 'test set'], loc='best')
        ax_1.grid()
        ax_2.grid()
        plt.show()

class RBFLayer(Layer):

    def __init__(self, units, gamma, **kwargs):
        super(RBFLayer, self).__init__(**kwargs)
        self.units = units
        self.gamma = K.cast_to_floatx(gamma)

    def build(self, input_shape):
        self.mu = self.add_weight(name='mu',
                                  shape=(int(input_shape[1]), self.units),
                                  initializer='uniform',
                                  trainable=True)
        super(RBFLayer, self).build(input_shape)

    def call(self, inputs):
        diff = K.expand_dims(inputs) - self.mu
        l2 = K.sum(K.pow(diff,2), axis=1)
        res = K.exp(-1 * self.gamma * l2)
        return res

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.units)





