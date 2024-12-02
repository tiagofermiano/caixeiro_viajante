import numpy as np
import random

# Matriz de distâncias da instância fornecida
distancias = np.array([
    [0, 19, 17, 34, 7, 20, 10, 17, 28, 15, 23, 29, 23, 29, 21, 20, 9, 16, 21, 13, 12],
    [19, 0, 10, 41, 26, 3, 27, 25, 15, 17, 17, 14, 18, 48, 17, 6, 21, 14, 17, 13, 31],
    [17, 10, 0, 47, 23, 13, 26, 15, 25, 22, 26, 24, 27, 44, 7, 5, 23, 21, 25, 18, 29],
    [34, 41, 47, 0, 36, 39, 25, 51, 36, 24, 27, 38, 25, 44, 54, 45, 25, 28, 26, 28, 27],
    [7, 26, 23, 36, 0, 27, 11, 17, 35, 22, 30, 36, 30, 22, 25, 26, 14, 23, 28, 20, 10],
    [20, 3, 13, 39, 27, 0, 26, 27, 12, 15, 14, 11, 15, 49, 20, 9, 20, 11, 14, 17, 21],
    [10, 27, 26, 25, 11, 26, 0, 26, 31, 14, 23, 32, 22, 25, 31, 28, 6, 17, 21, 19, 25],
    [17, 25, 15, 51, 17, 27, 26, 0, 39, 31, 38, 38, 38, 34, 13, 20, 26, 18, 22, 12, 23],
    [28, 15, 25, 36, 35, 12, 31, 39, 0, 17, 9, 2, 11, 56, 32, 21, 24, 26, 14, 8, 31],
    [15, 17, 22, 24, 22, 15, 14, 31, 17, 0, 9, 18, 8, 39, 29, 21, 11, 9, 7, 6, 27],
    [23, 17, 26, 27, 30, 14, 23, 38, 9, 9, 0, 11, 2, 48, 33, 23, 31, 21, 10, 12, 23],
    [29, 14, 24, 38, 36, 11, 32, 38, 2, 18, 11, 0, 13, 57, 31, 20, 27, 28, 16, 12, 24],
    [23, 18, 27, 25, 30, 15, 22, 38, 11, 8, 2, 13, 0, 47, 34, 25, 28, 15, 17, 14, 30],
    [29, 48, 44, 44, 22, 15, 25, 34, 56, 39, 48, 57, 47, 0, 46, 48, 31, 42, 46, 40, 21],
    [21, 17, 7, 54, 25, 20, 31, 13, 32, 29, 33, 31, 34, 46, 0, 11, 29, 28, 32, 25, 33],
    [20, 6, 5, 45, 26, 9, 28, 20, 21, 23, 28, 21, 25, 48, 11, 0, 10, 19, 23, 18, 16],
    [9, 21, 23, 25, 14, 20, 6, 26, 24, 8, 31, 26, 28, 31, 29, 10, 0, 11, 24, 19, 23],
    [16, 14, 21, 28, 23, 11, 17, 18, 26, 9, 21, 28, 15, 42, 28, 19, 11, 0, 20, 14, 22],
    [21, 17, 25, 26, 28, 14, 31, 22, 14, 7, 10, 16, 17, 46, 32, 23, 24, 20, 0, 21, 12],
    [13, 13, 18, 28, 20, 14, 13, 12, 8, 6, 12, 12, 14, 40, 25, 18, 19, 14, 21, 0, 8],
    [12, 31, 29, 27, 10, 21, 25, 23, 31, 27, 23, 24, 30, 21, 33, 16, 23, 22, 12, 8, 0]
])

# Função para calcular o comprimento do percurso
def calcular_comprimento(percurso):
    distancia_total = 0
    for i in range(len(percurso) - 1):
        distancia_total += distancias[percurso[i]][percurso[i + 1]]
    distancia_total += distancias[percurso[-1]][percurso[0]]  # Voltar à cidade inicial
    return distancia_total

# Função de inicialização da população
def inicializar_populacao(tamanho_populacao, num_cidades):
    return [list(np.random.permutation(num_cidades)) for _ in range(tamanho_populacao)]

# Função de seleção por torneio
def torneio_selecao(populacao, tamanho_torneio):
    selecao = random.sample(populacao, tamanho_torneio)
    selecao.sort(key=lambda x: calcular_comprimento(x))
    return selecao[0]

# Função de cruzamento (crossover) com o método de ordem superior (OX)
def crossover(pai1, pai2):
    tamanho = len(pai1)
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [-1] * tamanho
    filho[inicio:fim] = pai1[inicio:fim]
    idx = fim
    for gene in pai2:
        if gene not in filho:
            if idx == tamanho:
                idx = 0
            filho[idx] = gene
            idx += 1
    return filho

# Função de mutação
def mutacao(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# Algoritmo Genético
def algoritmo_genetico(num_cidades, tamanho_populacao=100, num_geracoes=500, taxa_mutacao=0.01, tamanho_torneio=5):
    populacao = inicializar_populacao(tamanho_populacao, num_cidades)
    for _ in range(num_geracoes):
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai1 = torneio_selecao(populacao, tamanho_torneio)
            pai2 = torneio_selecao(populacao, tamanho_torneio)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)
        populacao = nova_populacao
    melhor_individuo = min(populacao, key=lambda x: calcular_comprimento(x))
    melhor_comprimento = calcular_comprimento(melhor_individuo)
    return melhor_individuo, melhor_comprimento

# Exemplo de execução
melhor_percurso, melhor_distancia = algoritmo_genetico(
    num_cidades=distancias.shape[0],
    tamanho_populacao=100,
    num_geracoes=500,
    taxa_mutacao=0.01,
    tamanho_torneio=5
)

# Exibir o resultado
print("Melhor percurso encontrado:", melhor_percurso)
print("Melhor distância:", melhor_distancia)