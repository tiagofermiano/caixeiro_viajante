import numpy as np
import random
class GeneticAlgorithmTSP:
 def __init__(self, num_cities=10, population_size=50, mutation_rate=0.1,
generations=100):
 self.num_cities = num_cities
 self.population_size = population_size if population_size % 2 == 0 else
population_size + 1
 self.mutation_rate = mutation_rate
 self.generations = generations
 self.cost_matrix = self._generate_cost_matrix()
 self.population = self._initialize_population()
 def _generate_cost_matrix(self):
 """Gera uma matriz de custos simétrica entre as cidades."""
 matrix = np.random.randint(10, 100, size=(self.num_cities, self.num_cities))
 np.fill_diagonal(matrix, 0)
 return (matrix + matrix.T) // 2
 def _initialize_population(self):
 """Inicializa a população com permutações aleatórias das cidades."""
 return [np.random.permutation(self.num_cities) for _ in
range(self.population_size)]
 def _fitness(self, path):
 """Calcula o fitness de um caminho baseado na distância total."""
 distance = sum(self.cost_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))
 distance += self.cost_matrix[path[-1], path[0]] # Fechando o ciclo
 return 1 / distance if distance > 0 else float('inf')
 def _select_parents(self):
 """Seleciona dois pais utilizando o método de roleta."""
 fitness_scores = np.array([self._fitness(ind) for ind in self.population])
 probabilities = fitness_scores / fitness_scores.sum()
 return random.choices(self.population, probabilities, k=2)
 def _crossover(self, parent1, parent2):
 """Realiza o crossover utilizando PMX (Partially Mapped Crossover)."""
 size = len(parent1)
 p1, p2 = sorted(random.sample(range(size), 2))
 child = [None] * size
 child[p1:p2] = parent1[p1:p2]
 for i in range(p1, p2):
 if parent2[i] not in child:
 val = parent2[i]
 pos = i
 while child[pos] is not None:
 pos = np.where(parent1 == parent2[pos])[0][0]
 child[pos] = val
 for i in range(size):
 if child[i] is None:
 child[i] = parent2[i]
 return child
 def _mutate(self, individual):
 """Realiza mutação trocando duas cidades aleatoriamente."""
 if random.random() < self.mutation_rate:
 i, j = random.sample(range(self.num_cities), 2)
 individual[i], individual[j] = individual[j], individual[i]
 return individual
 def run(self):
 """Executa o algoritmo genético."""
 best_solution = None
 best_distance = float('inf')
 for generation in range(self.generations):
 # Avaliar fitness e encontrar o melhor da geração atual
 fitness_scores = [self._fitness(ind) for ind in self.population]
 best_index = np.argmax(fitness_scores)
 current_best = self.population[best_index]
 current_distance = 1 / fitness_scores[best_index]
 if current_distance < best_distance:
 best_distance = current_distance
 best_solution = current_best
 # Nova geração
 new_population = []
 for _ in range(self.population_size // 2):
 parent1, parent2 = self._select_parents()
 child1 = self._crossover(parent1, parent2)
 child2 = self._crossover(parent2, parent1)
 new_population.extend([self._mutate(child1), self._mutate(child2)])
 self.population = new_population
 print(f"Geração {generation + 1}: Melhor distância = {best_distance:.2f}")
 print("\nMelhor solução encontrada:")
 print("Caminho:", best_solution)
 print("Distância:", best_distance)
# Parâmetros
num_cities = 10
population_size = 50
mutation_rate = 0.1
generations = 100
# Executar o algoritmo genético
genetic_tsp = GeneticAlgorithmTSP(num_cities, population_size, mutation_rate,
generations)
genetic_tsp.run()