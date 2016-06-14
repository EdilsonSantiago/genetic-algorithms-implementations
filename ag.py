__author__ = 'edilson'

import numpy as np
from random import randint


def bits_valores():
    precisao_bits = [200 / ((2 ** 25) - 1)]
    for k in range(1, 25):
        precisao_bits.append(precisao_bits[k - 1] * 2)
    return precisao_bits


def valor_da_variavel(vetor_precisao, cromossomo):
    eixo_x = 0
    eixo_y = 0
    for i in range(0, 25):
        if cromossomo[i]:
            eixo_x += vetor_precisao[i]
    for i in range(26, 50):
        if cromossomo[i]:
            eixo_y += vetor_precisao[i - 26]
    return eixo_x, eixo_y


def criar_populacao(tamanho_populacao, tamanho_codigo):
    populacao_criada = []
    lista = []

    for i in range(tamanho_populacao):
        for j in range(0, tamanho_codigo):
            lista.append(randint(0, 1))
        populacao_criada.append(lista)
        lista = []
    return populacao_criada


def avaliacao_aptidao(x, y):
    aptidao = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2))
    return aptidao


def selecao():
    pass


def cruzamento(populacao_1):
    contador = 0
    nova_populacao = []
    filho_1 = []
    filho_2 = []
    while contador < len(populacao_1):
        pai_1 = populacao_1[contador]
        pai_2 = populacao_1[contador + 1]
        for i in range(0, 25):
            filho_1.append(pai_1[i])
            filho_2.append(pai_2[i])
        for i in range(26, 50):
            filho_1.append(pai_1[i])
            filho_2.append(pai_2[i])
        nova_populacao.append(filho_1)
        nova_populacao.append(filho_2)
        filho_1 = []
        filho_2 = []
        contador += 2
    return nova_populacao


def mutacao():
    pass


populacao = criar_populacao(10, 50)
individuos = cruzamento(populacao)
variavel_x, variavel_y = valor_da_variavel(bits_valores(), populacao[1])
print(populacao[1])
print(bits_valores())
print(variavel_x)
print(avaliacao_aptidao(variavel_x, variavel_y))
print(individuos)
