__author__ = 'edilson'

import numpy as np
from random import randint, uniform


tamanho_populacao = 100
tamanho_codigo = 50
geracoes = 50
i = 0

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

    for i in range(0, tamanho_populacao):
        for j in range(0, tamanho_codigo):
            lista.append(randint(0, 1))
        populacao_criada.append(lista)
        lista = []
    return populacao_criada


def avaliacao_aptidao(vetor_populacao):
    vetor_aptidao = []
    for i in range(0, len(vetor_populacao)):
        aptidao = 0
        x, y = valor_da_variavel(bits_valores(), vetor_populacao[i])
        aptidao = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2))
        vetor_aptidao.append(aptidao)
    return vetor_aptidao


def selecao(populacao_selecao, vetor_aptidao, tamanho_populacao):
    nova_populacao = []
    soma = 0
    var_1 = 0
    acumulador = 0
    for i in range(0, len(vetor_aptidao)):
        soma += vetor_aptidao[i]
    while len(nova_populacao) < tamanho_populacao:
        valor = uniform(0, soma)
        acumulador += vetor_aptidao[var_1]
        var_1 += 1

        if acumulador >= valor:
            nova_populacao.append(populacao_selecao[var_1])
            print(nova_populacao)

    return nova_populacao


def cruzamento(populacao_1, tamanho_populacao):
    contador = 0
    nova_populacao = []
    filho_1 = []
    filho_2 = []

    while contador < tamanho_populacao:
        ponto = randint(1, 49)
        pai_1 = populacao_1[contador]
        pai_2 = populacao_1[contador + 1]
        for i in range(0, ponto):
            filho_1.append(pai_1[i])
            filho_2.append(pai_2[i])
        for i in range(ponto + 1, 50):
            filho_1.append(pai_1[i])
            filho_2.append(pai_2[i])
        populacao_1.append(filho_1)
        populacao_1.append(filho_2)
        filho_1 = []
        filho_2 = []
        contador += 2
    return populacao_1


def mutacao(vetor_populacao):
    taxa_de_mutacao = 10
    for i in range(0, len(vetor_populacao)):
        numero_aleatorio = randint(0, 100)
        if numero_aleatorio < taxa_de_mutacao:
            indice = randint(0, 50)
            vetor = vetor_populacao[i]
            if vetor[indice] == 0:
                vetor[indice] = 1
            else:
                vetor[indice] = 0
            vetor_populacao[i] = vetor
    return vetor_populacao

populacao = criar_populacao(tamanho_populacao, tamanho_codigo)
while i == geracoes:
    populacao = cruzamento(populacao, tamanho_populacao)
    populacao = mutacao(populacao)
    aptidao = avaliacao_aptidao(populacao)
    populacao = selecao(populacao, aptidao, tamanho_populacao)
    i += 1
print(populacao)
