__author__ = 'edilson'

import numpy as np
from random import randint, uniform
import matplotlib.pyplot as plt
import csv

tamanho_populacao = 50
tamanho_codigo = 50
geracoes = 1000
melhor_individuo = 0
melhor_individuo_cromossomo = []
geracao_atual = 0
taxa_cruzamento = 75
taxa_mutacao = 1
eixo = np.linspace(0, 4999, 5000)

media_apt = []
aptos = []
soma_desvio = []
for p in range(0, geracoes):
    media_apt.append(0)
    aptos.append(0)
    soma_desvio.append(0)

with open('media.csv', 'r') as media:
    reader = csv.reader(media, delimiter=',')

    for linha in reader:
        var = 0
        for valor in linha:
            media_apt[var] += float(valor)
            var += 1

with open('aptos.csv', 'r') as ap:
    reader = csv.reader(ap, delimiter=',')

    for linha in reader:
        var = 0
        for valor in linha:
            aptos[var] += float(valor)
            var += 1

for indice in range(0, len(media_apt)):
    media_apt[indice] /= 30
    aptos[indice] /= 30

# Média desvio padrão
with open('media.csv', 'r') as media:
    reader = csv.reader(media, delimiter=',')
    for linha in reader:
        var = 0
        for valor in linha:
            soma_desvio[var] += ((float(valor) - media_apt[var]) ** 2)
            var += 1
for indice in range(0, len(soma_desvio)):
    soma_desvio[indice] /= 30
desvio_padrao = np.sqrt(soma_desvio)
print(desvio_padrao)

# plt.plot(eixo, desvio_padrao)
plt.errorbar(eixo, media_apt, yerr=desvio_padrao, errorevery = 10)
plt.show()