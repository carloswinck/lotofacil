import csv
from itertools import combinations
from collections import Counter

# Definir os números da moldura e do miolo
moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
miolo = {7, 8, 9, 12, 13, 14, 17, 18, 19}

# Inicializar contadores
total_moldura = 0
total_miolo = 0
num_jogos = 0

# Lê os dados do arquivo CSV
with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    data = [row[2:] for row in reader]

# Converte os dados para inteiros
data = [[int(num) for num in row] for row in data]

# Conta todas as combinações de 7 números
comb_counter = Counter()
for row in data:
    comb_counter.update(combinations(row, 7))

# Encontra a combinação mais comum
most_common_comb = comb_counter.most_common(1)

print(f'A combinação que mais aparece é: {most_common_comb[0][0]}')
print(f'Essa combinação aparece {most_common_comb[0][1]} vezes')


# Função para verificar se um número é primo
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# Função para verificar se um número é de Fibonacci
def is_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or n == 0


# Função para verificar se um número é múltiplo de 3
def is_multiple_of_3(n):
    return n % 3 == 0

with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        numeros = set(map(int, row[2:]))
        total_moldura += len(numeros & moldura)
        total_miolo += len(numeros & miolo)
        num_jogos += 1

    # Calcular as médias
    if num_jogos != 0:
        media_moldura = total_moldura / num_jogos
    else:
        media_moldura = 0  # or handle the case as needed
    if num_jogos != 0:
        media_miolo = total_miolo / num_jogos
    else:
        media_miolo = 0  # or handle the case as needed

    print(f'Média de números na moldura: {media_moldura:.2f}')
    print(f'Média de números no miolo: {media_miolo:.2f}')