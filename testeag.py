__author__ = 'edilson'

import csv
import matplotlib.pyplot as plt
import numpy as np

eixo = np.linspace(0, 99, 100)
geracoes = 100
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

media_apt = []
with open('media.csv', 'r') as media:
    reader = csv.reader(media, delimiter=',')
    for i in range(0, tamanho_populacao):
        somatorio = 0
        for linha in reader:
            somatorio += float(linha[i])
        media_apt.append(somatorio)

print(media_apt)

"""
f, vetor = plt.subplots(2)
vetor[0].plot(eixo, vetor5)
vetor[1].plot(eixo, vetor4)

plt.show()
"""

"""
for j in range(0, tamanho_populacao):
    x, y = valor_da_variavel(bits_valores(), populacao[j])
    posicao_x.append(x)
    posicao_y.append(y)
"""
"""
matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(posicao_x, posicao_y, 'o')
plot_X = np.linspace(-100, 100, 200)
plot_Y = np.linspace(-100, 100, 200)

plot_x, plot_y = np.meshgrid(plot_X, plot_Y)

z = 0.5 - (((np.sin(np.sqrt(plot_x**2 + plot_y**2)))**2 - 0.5) / (1 + (0.001 * (plot_x**2 + plot_y**2)) ** 2))
cs1 = plt.contourf(plot_x, plot_y, z, 25)
cs2 = plt.contour(plot_x, plot_y, z, cs1.levels)
"""
"""
    media_armazenamento[var] = media_apt
    apto_armazenamento[var] = apto
    geracao_atual = 0

vetor1 = media_armazenamento[0]
vetor2 = media_armazenamento[1]
vetor3 = media_armazenamento[2]
apto1 = apto_armazenamento[0]
apto2 = apto_armazenamento[1]
apto3 = apto_armazenamento[2]

print(vetor1)
for i in range(0, 100):
    vetor4.append((vetor1[i] + vetor2[i] + vetor3[i])/3)
    vetor5.append((apto1[i] + apto2[i] + apto3[i])/3)
"""
"""
    for j in range(0, tamanho_populacao):
        x, y = valor_da_variavel(bits_valores(), populacao[j])
        posicao_x.append(x)
        posicao_y.append(y)
"""