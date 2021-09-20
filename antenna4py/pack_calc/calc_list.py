import numpy as np

def ones_modul(a, b):
    # функция поэлементного умножения элементов списка на векторы
    # a - временной вектор, b - вектор статичных параметров
    len_time, len_param = a.shape[1], b.shape[0]
    c = np.zeros(shape=[len_time, len_param])
    buf = np.zeros(shape=[len_param])
    # цикл по времени
    for i in range(len_time):
        # цикл по параметрам
        for j in range(len_param):
            buf[j] = a[j][i] * b[j]
        c[i] = buf
        buf = np.zeros(shape=[len_param])
    return c

def approx(M, x_graph, x_n, y_n, lamda=0):
    # x_n, y_n - аппроксимируемые данные
    # x_graph - массив оси x со всеми значениями
    # M - порядок полинома
    order = np.arange(M+1)
    order = order[:, np.newaxis]
    e = np.tile(order, [1, len(x_n)])
    XT = np.power(x_n, e)
    X = np.transpose(XT)
    a = np.matmul(XT, X) + lamda * np.identity(M+1)
    b = np.matmul(XT, y_n)
    w = np.linalg.solve(a, b)
    e2 = np.tile(order, [1, x_graph.shape[0]])
    XT2 = np.power(x_graph, e2)
    y_graph = np.matmul(w, XT2)
    return y_graph

def is_ndarray(vec):
    bool_res = True
    for i in range(len(vec)):
        bool_buf = isinstance(vec[i], np.ndarray)
        bool_res = (bool_res == True) and (bool_buf == True)
    return bool_res

def is_list(vec):
    bool_res = True
    for i in range(len(vec)):
        bool_buf = isinstance(vec[i], list)
        bool_res = (bool_res == True) and (bool_buf == True)
    return bool_res