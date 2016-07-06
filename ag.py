__author__ = 'edilson'

import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
import csv

tamanho_populacao = 50
tamanho_codigo = 50
geracoes = 1000
geracao_atual = 0
taxa_cruzamento = 75
taxa_mutacao = 1
eixo = np.linspace(0, 999, 1000)


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
    soma = sum(vetor_aptidao)
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


c = csv.writer(open("aptos.csv", "w"))
d = csv.writer(open("media.csv", "w"))
for var1 in range(0, 10):
    populacao = criar_populacao(tamanho_populacao, tamanho_codigo)
    for var in range(0, 3):
        print(var)
        apto = []
        media_apt = []
        while geracao_atual < geracoes:
            print(geracao_atual)
            populacao = cruzamento(populacao, tamanho_populacao, taxa_cruzamento)
            populacao = mutacao(populacao, taxa_mutacao)
            aptidao = avaliacao_aptidao(populacao)
            apto.append(mais_apto(aptidao))
            media_apt.append(sum(aptidao)/len(aptidao))
            geracao_atual += 1

        c.writerow(apto)
        d.writerow(media_apt)
        geracao_atual = 0


media_apt = []
apto = []
for i in range(0, geracoes):
    media_apt.append(0)
    apto.append(0)
with open('media.csv', 'r') as media:
    reader = csv.reader(media, delimiter=',')

    for linha in reader:
        var = 0
        for valor in linha:
            media_apt[var] += float(valor)
            var += 1

with open('aptos.csv', 'r') as aptos:
    reader = csv.reader(aptos, delimiter=',')

    for linha in reader:
        var = 0
        for valor in linha:
            apto[var] += float(valor)
            var += 1

    for indice in range(0, len(media_apt)):
        media_apt[indice] /= 30
        apto[indice] /= 30


f, vetor = plt.subplots(2)
vetor[0].plot(eixo, apto)
vetor[1].plot(eixo, media_apt)

plt.show()
