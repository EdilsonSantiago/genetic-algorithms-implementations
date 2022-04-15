__author__ = 'edilson'

import numpy as np
from random import uniform
import matplotlib.pyplot as plt
import csv
import time
import pathlib

script_path = pathlib.Path(__file__).parent.resolve()

tempo_ini = time.time()
tamanho_populacao = 50
tamanho_populacao_cruzamento = tamanho_populacao
geracoes = 200
melhor_individuo = 0
melhor_individuo_cromossomo = []
geracao_atual = 0
taxa_cruzamento = 75
taxa_mutacao = 1
eixo = np.linspace(0, 199, 200)


def criar_populacao():
    populacao = []
    for i in range(0, tamanho_populacao):
        individuo = [0, 0]
        individuo[0] = uniform(-100, 100)  # Valor de x aleatório
        individuo[1] = uniform(-100, 100)  # Valor de y aleatório
        populacao.append(individuo)
    return populacao


def heap_sort(lista, cromossomo):
    indice_final = len(lista) - 1
    metade_lista = int(indice_final / 2)

    for i in range(metade_lista, -1, -1):
        cria_heap(lista, cromossomo, i, indice_final)

    for i in range(indice_final, 0, -1):
        if lista[0] > lista[i]:
            lista[0], lista[i] = lista[i], lista[0]
            cromossomo[0], cromossomo[i] = cromossomo[i], cromossomo[0]
            cria_heap(lista, cromossomo, 0, i - 1)
    return lista, cromossomo


def cria_heap(lista, cromossomo, inicio, fim):
    filho = inicio * 2 + 1
    while filho <= fim:
        if (filho < fim) and (lista[filho] < lista[filho + 1]):
            filho += 1
        if lista[inicio] < lista[filho]:
            lista[inicio], lista[filho] = lista[filho], lista[inicio]
            cromossomo[inicio], cromossomo[filho] = cromossomo[filho], cromossomo[inicio]
            inicio = filho
            filho = 2 * inicio + 1
        else:
            return


def normalizacao_linear(tamanho_popula, minimo=10, maximo=100):
    aptidao_normalizada = []
    for i in range(0, tamanho_popula):
        normalizada = minimo + (((maximo - minimo)/(tamanho_popula - 1)) * i)
        aptidao_normalizada.append(normalizada)
    return aptidao_normalizada


def avaliacao_aptidao(populacao):
    vetor_aptidao = []
    for i in range(0, len(populacao)):
        x, y = populacao[i][0], populacao[i][1]
        aptd = 0.5 - (((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5) / (1 + (0.001 * (x**2 + y**2)) ** 2))
        vetor_aptidao.append(aptd)
    return vetor_aptidao


def selecao(populacao, vetor_aptidao):  # Esta funcao selecionara um individuo utilizando o metodo da roleta
    soma, acumulador, ind = 0, vetor_aptidao[0], 0
    selecionado = []
    soma = sum(vetor_aptidao)
    num_aleatorio = uniform(0, soma)
    while len(selecionado) != 2:
        acumulador += vetor_aptidao[ind]
        if acumulador >= num_aleatorio:
            selecionado = populacao[ind]
            break
        ind += 1
    return selecionado


def elitismo(populacao_apto, aptidoes, populacao):
    global tamanho_populacao_cruzamento
    maior_apitdao, melhor_cromossomo = mais_apto(aptidoes, populacao_apto)
    if tamanho_populacao == tamanho_populacao_cruzamento:
        populacao.append(melhor_cromossomo)
        tamanho_populacao_cruzamento += 1
    else:
        populacao.append(melhor_cromossomo)
    return populacao


def aritmetico(pai_1, pai_2, populacao):
    # Implemntação do cruzamento aritmético
    # a - número aleatório entre 0 e 1
    # F1 = (a * p1) + ((1 - a) * p2) e F2 = (a * p2) + ((1 - a) * p1)
    a = uniform(0, 1)
    filho1 = []
    filho2 = []
    for i in range(0, 2):
        filho1.append((a * pai_1[i]) + ((1 - a) * pai_2[i]))
        filho2.append((a * pai_2[i]) + ((1 - a) * pai_1[i]))
    populacao.append(filho1)
    populacao.append(filho2)
    return populacao


def cruzamento(populacao_1, populacao_2, aptidao_cruzamento):
    contador = 0
    while contador < tamanho_populacao:
        vetor = selecao(populacao_1, aptidao_cruzamento)
        pai_1 = vetor
        vetor = selecao(populacao_1, aptidao_cruzamento)
        pai_2 = vetor
        aleatorio = uniform(0, 100)
        if aleatorio < taxa_cruzamento:
            populacao_2 = aritmetico(pai_1, pai_2, populacao_2)
            contador += 2
    return populacao_2


def nova_populacao(populacao_1, aptidao_apto, elite=False, normalizacao=False):
    if elite and not normalizacao:
        aptidao_cruzamento = avaliacao_aptidao(populacao_1)
        populacao_2 = elitismo(populacao_1, aptidao_apto, [])
        populacao_2 = cruzamento(populacao_1, populacao_2, aptidao_cruzamento)
    elif not elite and normalizacao:
        aptidao_apto, populacao_1 = heap_sort(aptidao_apto, populacao_1)
        aptidao_cruzamento = normalizacao_linear(len(populacao_1))
        populacao_2 = cruzamento(populacao_1, [], aptidao_cruzamento)
    elif elite and normalizacao:
        aptidao_apto, populacao_1 = heap_sort(aptidao_apto, populacao_1)
        populacao_2 = elitismo(populacao_1, aptidao_apto, [])
        aptidao_cruzamento = normalizacao_linear(len(populacao_1))
        populacao_2 = cruzamento(populacao_1, populacao_2, aptidao_cruzamento)
    else:
        aptidao_cruzamento = avaliacao_aptidao(populacao_1)
        populacao_2 = cruzamento(populacao_1, [], aptidao_cruzamento)

    return populacao_2


def mutacao(populacao):
    # Mutação randômica uniforme
    for i in range(0, len(populacao)):
        for j in range(0, 2):
            numero_aleatorio = uniform(0, 100)
            if numero_aleatorio < taxa_mutacao:
                populacao[i][j] = uniform(-100, 100)
    return populacao


def mais_apto(aptidoes, populacao):
    # Esta função retorna a maior aptidão e o cromossomo do indivíduo com a maior aptidão
    apto = aptidoes[0]
    cromossomo = populacao[0]
    for i in range(1, len(aptidoes)):
        if apto < aptidoes[i]:
            apto = aptidoes[i]
            cromossomo = populacao[i]

    return apto, cromossomo


def menos_apto(aptidoes):
    individuo_menos_apto = aptidoes[0]
    # cromossomo = populacao_apto[0]
    for i in range(1, len(aptidoes)):
        if individuo_menos_apto > aptidoes[i]:
            individuo_menos_apto = aptidoes[i]
            # cromossomo = populacao_apto[i]
    return individuo_menos_apto


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
    for indice in range(0, geracoes):
        vetor_media[indice] /= 30
    return vetor_media


def desv_padrao(arquivo, vetor_padrao):
    soma_desvio = []
    for p in range(0, geracoes):
        soma_desvio.append(0)
    with open(arquivo, 'r') as ar:
        reader = csv.reader(ar, delimiter=',')
        for linha in reader:
            va = 0
            for valor in linha:
                soma_desvio[va] += ((float(valor) - vetor_padrao[va]) ** 2)
                va += 1
    for indice in range(0, len(soma_desvio)):
        soma_desvio[indice] /= 30
    desvio_padrao = np.sqrt(soma_desvio)
    return desvio_padrao


# ----------------------------------Execução do AG------------------------------------------------------
c = csv.writer(open(script_path / 'files/fittest.csv', 'w'))
d = csv.writer(open(script_path / 'files/average.csv', 'w'))
r = csv.writer(open(script_path / 'files/worst_individuals.csv', 'w'))
for var1 in range(0, 10):
    populacao_nova = criar_populacao()
    var = 0
    while var < 3:
        aptos = []
        media_apt = []
        pior_individuo = []
        popula = populacao_nova
        while geracao_atual < geracoes:
            aptidao = avaliacao_aptidao(popula)
            popula = nova_populacao(popula, aptidao, normalizacao=True)
            popula = mutacao(popula)
            aptidao = avaliacao_aptidao(popula)
            individuo_apto, cromossomo_apto = mais_apto(aptidao, popula)
            menor_fitness = menos_apto(aptidao)
            aptos.append(individuo_apto)
            pior_individuo.append(menor_fitness)
            if individuo_apto > melhor_individuo and geracao_atual == 49:
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
# Média dos 30 ensaios
media_apt = media(script_path / 'files/average.csv')
aptos = media(script_path / 'files/fittest.csv')
pior_individuo = media(script_path / 'files/worst_individuals.csv')
# Desvio padrão dos 30 ensaios
media_des = desv_padrao(script_path / 'files/average.csv', media_apt)
aptos_des = desv_padrao(script_path / 'files/fittest.csv', aptos)
pior_individuo_des = desv_padrao(script_path / 'files/worst_individuals.csv', pior_individuo)

print("Melhor indivíduo:")
print(melhor_individuo)
print("Cromossomo")
print(melhor_individuo_cromossomo)
print("Tempo")
tempo_fim = time.time()
print(tempo_fim - tempo_ini)

plt.subplot(4, 1, 1)
plt.plot(eixo, aptos, eixo, pior_individuo, eixo, media_apt)
plt.autoscale(axis='y', tight=False)
plt.ylabel('Aptidão')

plt.subplot(4, 1, 2)
plt.errorbar(eixo, aptos, yerr=aptos_des, errorevery=3)
plt.autoscale(axis='y', tight=True)
plt.ylabel('Melhor indivíduo')

plt.subplot(4, 1, 3)
plt.errorbar(eixo, media_apt, color='r', yerr=media_des, errorevery=3, ecolor='r')
plt.autoscale(axis='y', tight=True)
plt.ylabel('Média dos indivíduos')

plt.subplot(4, 1, 4)
plt.errorbar(eixo, pior_individuo, color='g', yerr=pior_individuo_des, errorevery=3, ecolor='g')
plt.autoscale(axis='y', tight=True)
plt.xlabel('Gerações')
plt.ylabel('Pior Individuo')


plt.show()
