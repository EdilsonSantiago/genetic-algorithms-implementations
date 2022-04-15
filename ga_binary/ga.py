__author__ = 'edilson'

import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
import csv
import pathlib

script_path = pathlib.Path(__file__).parent.resolve()

tamanho_populacao = 50
tamanho_populacao_cruzamento = tamanho_populacao
tamanho_codigo = 50
geracoes = 200
melhor_individuo = 0
melhor_individuo_cromossomo = []
geracao_atual = 0
taxa_cruzamento = 75
taxa_mutacao = 1
eixo = np.linspace(0, 199, 200)


def criar_populacao():
    populacao_criada = []
    for i in range(0, tamanho_populacao):
        lista = vetor_aleatorio(tamanho_codigo)
        populacao_criada.append(lista)
    return populacao_criada


def vetor_aleatorio(tamanho):
    lista = []
    for i in range(0, tamanho):
        lista.append(randint(0, 1))
    return lista


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


def elitismo(populacao_apto, aptidao_apto, populacao_2):
    global tamanho_populacao_cruzamento
    maior_apitdao, melhor_cromossomo = mais_apto(aptidao_apto, populacao_apto)
    if tamanho_populacao == tamanho_populacao_cruzamento:
        populacao_2.append(melhor_cromossomo)
        tamanho_populacao_cruzamento += 1
    else:
        populacao_2.append(melhor_cromossomo)
    return populacao_2


def um_ponto(pai_1, pai_2, popula):
    # Cruzamento com um ponto de corte aleatório
    filho_1 = []
    filho_2 = []
    ponto = randint(1, tamanho_codigo)
    for i in range(0, ponto):
        filho_1.append(pai_1[i])
        filho_2.append(pai_2[i])
    for i in range(ponto, tamanho_codigo):
        filho_1.append(pai_1[i])
        filho_2.append(pai_2[i])
    popula.append(filho_1)
    popula.append(filho_2)
    return popula


def dois_pontos(pai_1, pai_2, popula):
    # Cruzamento com dois pontos de corte aleatórios
    filho1 = []
    filho2 = []
    num1 = randint(0, 50)
    num2 = randint(0, 50)
    if num2 < num1:
        num1, num2 = num2, num1
    for i in range(0, num1):
        filho1.append(pai_1[i])
        filho2.append(pai_2[i])
    for i in range(num1, num2):
        filho1.append(pai_2[i])
        filho2.append(pai_1[i])
    for i in range(num2, 50):
        filho1.append(pai_1[i])
        filho2.append(pai_2[i])
    popula.append(filho1)
    popula.append(filho2)
    return popula


def uniforme(pai_1, pai_2, popula):
    # Cruzamento máscara binária
    filho1 = []
    filho2 = []
    mascara = vetor_aleatorio(tamanho_codigo)
    for i in range(0, tamanho_codigo):
        if mascara[i]:
            filho1.append(pai_1[i])
            filho2.append(pai_2[i])
        else:
            filho1.append(pai_2[i])
            filho2.append(pai_1[i])
    popula.append(filho1)
    popula.append(filho2)
    return popula


def cruzamento(populacao_1, populacao_2, aptidao_cruzamento):
    contador = 0
    while contador < tamanho_populacao:
        vetor = selecao(populacao_1, aptidao_cruzamento)
        pai_1 = vetor
        vetor = selecao(populacao_1, aptidao_cruzamento)
        pai_2 = vetor
        aleatorio = randint(0, 100)
        if aleatorio < taxa_cruzamento:
            # populacao_2 = um_ponto(pai_1, pai_2, populacao_2)
            # populacao_2 = dois_pontos(pai_1, pai_2, populacao_2)
            populacao_2 = uniforme(pai_1, pai_2, populacao_2)
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


def mutacao_n(vetor_populacao, taxa_de_mutacao):
    for i in range(0, len(vetor_populacao) - 1):
        for j in range(0, tamanho_codigo):
            numero_aleatorio = uniform(0, 100)
            if numero_aleatorio < taxa_de_mutacao:
                if vetor_populacao[i][j] == 0:
                    vetor_populacao[i][j] = 1
                else:
                    vetor_populacao[i][j] = 0
    return vetor_populacao


def mais_apto(aptidao_apto, populacao_apto):
    # Esta função retorna a maior aptidão e o cromossomo do indivíduo com a maior aptidão
    apto = aptidao_apto[0]
    cromossomo = populacao_apto[0]
    for i in range(1, len(aptidao_apto)):
        if apto < aptidao_apto[i]:
            apto = aptidao_apto[i]
            cromossomo = populacao_apto[i]

    return apto, cromossomo


def menos_apto(aptidao_apto):
    individuo_menos_apto = aptidao_apto[0]
    # cromossomo = populacao_apto[0]
    for i in range(1, len(aptidao_apto)):
        if individuo_menos_apto > aptidao_apto[i]:
            individuo_menos_apto = aptidao_apto[i]
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
    for indice in range(0, len(media_apt)):
        vetor_media[indice] /= 30
    return vetor_media


def desv_padrao(arq, vetor_padrao):
    soma_desvio = []
    for p in range(0, geracoes):
        soma_desvio.append(0)
    with open(arq, 'r') as ar:
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

# Execução do Algoritmo Genético
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
        populacao = populacao_nova
        while geracao_atual < geracoes:
            aptidao = avaliacao_aptidao(populacao)
            populacao = nova_populacao(populacao, aptidao)
            populacao = mutacao(populacao, taxa_mutacao)
            aptidao = avaliacao_aptidao(populacao)
            individuo_apto, cromossomo_apto = mais_apto(aptidao, populacao)
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
melhor_individuo_x, melhor_individuo_y = valor_da_variavel(bits_valores(), melhor_individuo_cromossomo)

print("Melhor indivíduo:")
print(melhor_individuo)
print("Cromossomo")
print(melhor_individuo_cromossomo)
print("Posição")
print(melhor_individuo_x, melhor_individuo_y)

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
