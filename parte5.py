import numpy as np 

import random 

 

# Matriz de distâncias da instância fornecida 

distancias = np.array([
    [int(x) for x in line.split()] 
    for line in """..."""

0 19 17 34 7 20 10 17 28 15 23 29 23 29 21 20 9 16 21 13 12 
19 0 10 41 26 3 27 25 15 17 17 14 18 48 17 6 21 14 17 13 31 
17 10 0 47 23 13 26 15 25 22 26 24 27 44 7 5 23 21 25 18 29 
34 41 47 0 36 39 25 51 36 24 27 38 25 44 54 45 25 28 26 28 27 
7 26 23 36 0 27 11 17 35 22 30 36 30 22 25 26 14 23 28 20 10 
20 3 13 39 27 0 26 27 12 15 14 11 15 49 20 9 20 11 14 11 30 
10 27 26 25 11 26 0 26 31 14 23 32 22 25 31 28 6 17 21 15 4 
17 25 15 51 17 27 26 0 39 31 38 38 38 34 13 20 26 31 36 28 27 
28 15 25 36 35 12 31 39 0 17 9 2 11 56 32 21 24 13 11 15 35 
15 17 22 24 22 15 14 31 17 0 9 18 8 39 29 21 8 4 7 4 18 
23 17 26 27 30 14 23 38 9 9 0 11 2 48 33 23 17 7 2 10 27 
29 14 24 38 36 11 32 38 2 18 11 0 13 57 31 20 25 14 13 17 36 
23 18 27 25 30 15 22 38 11 8 2 13 0 47 34 24 16 7 2 10 26 
29 48 44 44 22 49 25 34 56 39 48 57 47 0 46 48 31 42 46 40 21 
21 17 7 54 25 20 31 13 32 29 33 31 34 46 0 11 29 28 32 25 33 
20 6 5 45 26 9 28 20 21 21 23 20 24 48 11 0 23 19 22 17 32 
9 21 23 25 14 20 6 26 24 8 17 25 16 31 29 23 0 11 15 9 10 
16 14 21 28 23 11 17 31 13 4 7 14 7 42 28 19 11 0 5 3 21 
21 17 25 26 28 14 21 36 11 7 2 13 2 46 32 22 15 5 0 8 25 
13 13 18 28 20 11 15 28 15 4 10 17 10 40 25 17 9 3 8 0 19 
12 31 29 27 10 30 4 27 35 18 27 36 26 21 33 32 10 21 25 19 0 

.strip().split("\n")
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

 

# Configurações para diferentes critérios 

configuracoes = [ 

    {"tamanho_populacao": 100, "num_geracoes": 500, "taxa_mutacao": 0.01},  # Configuração base 

    {"tamanho_populacao": 20, "num_geracoes": 500, "taxa_mutacao": 0.01},   # População reduzida 

    {"tamanho_populacao": 200, "num_geracoes": 500, "taxa_mutacao": 0.01},  # População aumentada 

    {"tamanho_populacao": 100, "num_geracoes": 500, "taxa_mutacao": 0.1},   # Taxa de mutação aumentada 

    {"tamanho_populacao": 100, "num_geracoes": 1000, "taxa_mutacao": 0.01}  # Mais gerações 

] 

 

# Executar o algoritmo para cada configuração e coletar os resultados 

resultados = [] 

for config in configuracoes: 

    percurso, comprimento = algoritmo_genetico( 

        num_cidades=distancias.shape[0], 

        tamanho_populacao=config["tamanho_populacao"], 

        num_geracoes=config["num_geracoes"], 

        taxa_mutacao=config["taxa_mutacao"] 

    ) 

    resultados.append((config, percurso, comprimento)) 

 

resultados 

 

# Exibir os resultados no terminal 

for i, (config, percurso, comprimento) in enumerate(resultados, start=1): 

    print(f"Configuração {i}:") 

    print(f"  Parâmetros: {config}") 

    print(f"  Melhor Comprimento: {comprimento}") 

    print(f"  Melhor Percurso: {percurso}\n") 