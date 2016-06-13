__author__ = 'edilson'

import numpy as np
from random import randint

# z = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2


def criar_populacao(tamanho_populacao, tamanho_codigo):
    populacao_criada = []
    lista = []

    for i in range(tamanho_populacao):
        for j in range(0, tamanho_codigo):
            lista.append(randint(0, 1))
        populacao_criada.append(lista)
        lista = []
    return populacao_criada


def avaliacao_aptidao(populacao):
    pass


def selecao():
    pass


def cruzamento():
    pass


def mutacao():
    pass


populacao = criar_populacao(10, 50)
print(populacao)
