import numpy as np

def ones_modul(a, b):
    # функция поэлементного умножения элементов списка на векторы
    # a - направляющий вектор, b - скользящий вектор
    c = np.zeros(shape=[len(a), len(b)])
    buf = np.zeros(shape=[len(b)])
    for i in range(len(a)):
        for j in range(len(b)):
            buf[j] = a[i] * b[j]
        c[i] = buf
        buf = np.zeros(shape=[len(b)])
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
