__author__ = 'edilson'

# import numpy as np
from random import randint

# z = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2


def bits_valores():
    precisao_bits = [200 / ((2 ** 25) - 1)]
    for k in range(1, 25):
        precisao_bits.append(precisao_bits[k - 1] * 2)
    return precisao_bits


def valor_da_variavel(vetor_precisao, genoma):
    x = 0
    y = 0
    for i in range(0, 25):
        if genoma[i]:
            x += vetor_precisao[i]
    for i in range(26, 50):
        if genoma[i]:
            y += vetor_precisao[i - 26]
    return x, y


def criar_populacao(tamanho_populacao, tamanho_codigo):
    populacao_criada = []
    lista = []

    for i in range(tamanho_populacao):
        for j in range(0, tamanho_codigo):
            lista.append(randint(0, 1))
        populacao_criada.append(lista)
        lista = []
    return populacao_criada


def avaliacao_aptidao():
    pass


def selecao():
    pass


def cruzamento():
    pass


def mutacao():
    pass


populacao = criar_populacao(10, 50)
x, y = valor_da_variavel(bits_valores(), populacao[1])
print(populacao[1])
print(bits_valores())
print(x)
