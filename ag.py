__author__ = 'edilson'

import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
import csv

tamanho_populacao = 50
tamanho_codigo = 50
geracoes = 5000
melhor_individuo = 0
melhor_individuo_cromossomo = []
geracao_atual = 0
taxa_cruzamento = 75
taxa_mutacao = 1
eixo = np.linspace(0, 4999, 5000)


def criar_populacao():
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
        x, y = valor_da_variavel(bits_valores(), vetor_populacao[i])
        aptd = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2))
        vetor_aptidao.append(aptd)
    return vetor_aptidao


def selecao(populacao_selecao, vetor_aptidao):
    soma, acumulador, ind = 0, vetor_aptidao[0], 0
    selecionado = []
    soma = sum(vetor_aptidao)
    num_aleatorio = uniform(0, soma)
    while len(selecionado) != 50:
        acumulador += vetor_aptidao[ind]
        if acumulador >= num_aleatorio:
            selecionado = populacao_selecao[ind]
            break
        ind += 1
    # print(selecionado)
    return selecionado


def cruzamento(populacao_1):
    contador = 0
    filho_1 = []
    filho_2 = []
    populacao_2 = []
    aptidao_cruzamento = avaliacao_aptidao(populacao_1)

    while contador < tamanho_populacao:
        ponto = randint(1, 49)
        vetor = selecao(populacao_1, aptidao_cruzamento)
        pai_1 = vetor
        vetor = selecao(populacao_1, aptidao_cruzamento)
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
            indice_vetor = randint(0, 49)
            vetor = vetor_populacao[i]
            if vetor[indice_vetor] == 0:
                vetor[indice_vetor] = 1
            else:
                vetor[indice_vetor] = 0
            vetor_populacao[i] = vetor
    return vetor_populacao


def mais_apto(aptidao_apto, populacao_apto):
    apto = aptidao_apto[0]
    menos_apto = aptidao_apto[0]
    cromossomo = []
    for i in range(1, len(aptidao_apto)):
        if apto < aptidao_apto[i]:
            apto = aptidao_apto[i]
            cromossomo = populacao_apto[i]
        if menos_apto > aptidao_apto[i]:
            menos_apto = aptidao_apto[i]
    return apto, cromossomo, menos_apto


def media(arquivo):
    vetor_media = []
    for p in range(0, geracoes):
        vetor_media.append(0)
    with open(arquivo, 'r') as arq:
        reader = csv.reader(arq, delimiter=',')

        for linha in reader:
            var_indice = 0
            for valor in linha:
                vetor_media[var_indice] += float(valor)
                var_indice += 1
    for indice in range(0, len(media_apt)):
        vetor_media[indice] /= 30
    return vetor_media

# Execução do Algoritmo Genético
c = csv.writer(open('aptos.csv', 'w'))
d = csv.writer(open('media.csv', 'w'))
r = csv.writer(open('piores_individuos.csv', 'w'))
for var1 in range(0, 10):
    populacao_nova = criar_populacao()
    var = 0
    while var < 3:
        print(var)
        aptos = []
        media_apt = []
        pior_individuo = []
        populacao = populacao_nova
        while geracao_atual < geracoes:
            print(geracao_atual)
            populacao = cruzamento(populacao)
            populacao = mutacao(populacao, taxa_mutacao)
            aptidao = avaliacao_aptidao(populacao)
            individuo_apto, cromossomo_apto, menor_fitness = mais_apto(aptidao, populacao)
            aptos.append(individuo_apto)
            pior_individuo.append(menor_fitness)
            if individuo_apto > melhor_individuo:
                melhor_individuo = individuo_apto
                melhor_individuo_cromossomo = cromossomo_apto
            media_apt.append(sum(aptidao)/len(aptidao))
            geracao_atual += 1
        if len(aptos) and len(media_apt) == geracoes:
            c.writerow(aptos)
            d.writerow(media_apt)
            r.writerow(pior_individuo)
            var += 1
        geracao_atual = 0

media_apt = media('media.csv')
aptos = media('aptos.csv')
pior_individuo = media('piores_individuos.csv')

melhor_individuo_x, melhor_individuo_y = valor_da_variavel(bits_valores(), melhor_individuo_cromossomo)

print("Melhor indivíduo:")
print(melhor_individuo)
print("Cromossomo")
print(melhor_individuo_cromossomo)
print("Posição")
print(melhor_individuo_x, melhor_individuo_y)

plt.subplot(3, 1, 1)
plt.plot(eixo, aptos)
plt.ylabel('Melhor indivíduo')

plt.subplot(3, 1, 2)
plt.plot(eixo, pior_individuo)
plt.ylabel('Pior Individuo')

plt.subplot(3, 1, 3)
plt.plot(eixo, media_apt)
plt.xlabel('Gerações')
plt.ylabel('Média de todos os indivíduos')

plt.show()
