__author__ = 'edilson'

import numpy as np
# from random import randint, uniform
# import matplotlib.pyplot as plt
import csv

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
    pass


def normalizacao_linear():
    pass


def avaliacao_aptidao():
    pass


def selecao():
    pass


def elitismo():
    pass


def cruzamento():
    pass


def mutacao():
    pass


def mais_apto():
    pass


def menos_apto():
    pass


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
    soma_desvio = np.zeros(geracoes - 1)
    print(soma_desvio)
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
