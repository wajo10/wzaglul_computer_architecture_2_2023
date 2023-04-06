import random
import math

def hypergeometric_distribution(M: int, n: int, N: int, k: int):
    """
    Muestreo aleatorio sin reemplazo de una distribución hipergeométrica
    :param M: número de elementos de interés en la población
    :param n:el tamaño de la muestra
    :param N: el tamaño de la población
    :param k: el número de elementos de interés en la muestra
    :return: Muestra de tamaño k de la distribución hipergeométrica
    """
    samples = []
    for i in range(k):
        sample = 0
        for j in range(n):
            if random.random() < float(M) / N:
                sample += 1
                M -= 1
            if N > 1:
                N -= 1
        samples.append(sample)
        M += sample
        N += n - sample
    return samples

def poisson(lmbda):
    """
    :param lmbda: parámetro de la distribución de Poisson
    :return: Número aleatorio de una distribución de Poisson
    """
    L = math.exp(-lmbda)
    k = 0
    p = 1
    while p > L:
        k = k + 1
        u = random.uniform(0, 1)
        p = p * u
    return k - 1

def create_hex_data():
    """
    :return: Dirección de memoria en formato hexadecimal
    """
    list = hypergeometric_distribution(10, 1, 20, 16)
    binary_string = ''.join(map(str, list))
    return hex(int(binary_string, 2))

class Logs(object):
    def __init__(self):
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)

    def print_logs(self):
        for log in self.logs:
            print(log)

    def pop_log(self):
        if len(self.logs) > 0:
            return self.logs.pop(0)
        else:
            return False
