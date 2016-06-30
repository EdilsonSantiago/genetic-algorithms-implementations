__author__ = 'edilson'

import numpy as np
from random import randint, uniform
import matplotlib
import matplotlib.pyplot as plt


tamanho_populacao = 50
tamanho_codigo = 50
geracoes = 100
geracao_atual = 0
taxa_cruzamento = 75
taxa_mutacao = 1
media_armazenamento = [[], [], []]
apto_armazenamento = [[], [], []]
vetor4 = []
vetor5 = []
apto = []
media_apt = []
posicao_x = []
posicao_y = []
eixo = np.linspace(0, 99, 100)


def criar_populacao(tamanho_populacao, tamanho_codigo):
    populacao_criada = []
    lista = []

    for i in range(0, tamanho_populacao):
        for j in range(0, tamanho_codigo):
            lista.append(randint(0, 1))
        populacao_criada.append(lista)
        lista = []
    return populacao_criada


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
    for i in range(25, 50):
        if cromossomo[i]:
            eixo_y += vetor_precisao[i - 26]
    return eixo_x - 100, eixo_y - 100


def avaliacao_aptidao(vetor_populacao):
    vetor_aptidao = []
    for i in range(0, len(vetor_populacao)):
        aptidao = 0
        x, y = valor_da_variavel(bits_valores(), vetor_populacao[i])
        aptidao = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2))
        vetor_aptidao.append(aptidao)
    return vetor_aptidao


def selecao(populacao, vetor_aptidao):
    soma, acumulador, ind = 0, vetor_aptidao[0], 0
    selecionado = []
    for i in range(0, len(vetor_aptidao)):
        soma += vetor_aptidao[i]
    num_aleatorio = uniform(0, soma)
    while len(selecionado) != 50:
        acumulador += vetor_aptidao[ind]
        if acumulador >= num_aleatorio:
            selecionado = populacao[ind]
            break
        ind += 1
    #print(selecionado)
    return selecionado


def cruzamento(populacao_1, tamanho_populacao, taxa_cruzamento):
    contador = 0
    filho_1 = []
    filho_2 = []
    populacao_2 = []
    aptidao = avaliacao_aptidao(populacao_1)

    while contador < tamanho_populacao:
        ponto = randint(1, 49)
        vetor = selecao(populacao_1, aptidao)
        pai_1 = vetor
        vetor = selecao(populacao_1, aptidao)
        pai_2 = vetor
        aleatorio = randint(0, 100)
        if aleatorio < taxa_cruzamento:
            for i in range(0, ponto):
                filho_1.append(pai_1[i])
                filho_2.append(pai_2[i])
            for i in range(ponto, 50):
                filho_1.append(pai_1[i])
                filho_2.append(pai_2[i])
            populacao_2.append(filho_1)
            populacao_2.append(filho_2)
            filho_1 = []
            filho_2 = []
            contador += 2

    return populacao_2


def mutacao(vetor_populacao, taxa_de_mutacao):
    for i in range(0, len(vetor_populacao)):
        numero_aleatorio = uniform(0, 100)
        if numero_aleatorio < taxa_de_mutacao:
            indice = randint(0, 49)
            vetor = vetor_populacao[i]
            if vetor[indice] == 0:
                vetor[indice] = 1
            else:
                vetor[indice] = 0
            vetor_populacao[i] = vetor
    return vetor_populacao


def mais_apto(aptidao):
    apto = 0
    for i in range(0, len(aptidao)):
        if apto < aptidao[i]:
            apto = aptidao[i]
    return apto


populacao = criar_populacao(tamanho_populacao, tamanho_codigo)
for j in range(0, tamanho_populacao):
    x, y = valor_da_variavel(bits_valores(), populacao[j])
    posicao_x.append(x)
    posicao_y.append(y)
for var in range(0, 3):
    while geracao_atual < geracoes:
        print(geracao_atual)
        populacao = cruzamento(populacao, tamanho_populacao, taxa_cruzamento)
        populacao = mutacao(populacao, taxa_mutacao)
        aptidao = avaliacao_aptidao(populacao)

        apto.append(mais_apto(aptidao))
        media_apt.append(sum(aptidao)/len(aptidao))
        geracao_atual += 1
    media_armazenamento[var] = media_apt
    apto_armazenamento[var] = apto

vetor1 = media_armazenamento[0]
vetor2 = media_armazenamento[1]
vetor3 = media_armazenamento[2]
apto1 = apto_armazenamento[0]
apto2 = apto_armazenamento[1]
apto3 = apto_armazenamento[2]

print(len(vetor1))
for i in range(0, 100):
    vetor4.append((vetor1[i] + vetor2[i] + vetor3[i])/3)
    vetor5.append((apto1[i] + apto2[i] + apto3[i])/3)


"""
matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(posicao_x, posicao_y, 'o')
"""
f, vetor = plt.subplots(2)
vetor[0].plot(eixo, apto)
vetor[1].plot(eixo, vetor4)

plt.show()
