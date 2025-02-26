import csv
from itertools import combinations
from collections import Counter

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


# Listas de números primos, de Fibonacci e múltiplos de 3
primes = [n for n in range(1, 26) if is_prime(n)]
fibonacci = [n for n in range(1, 26) if is_fibonacci(n)]
multiples_of_3 = [n for n in range(1, 26) if is_multiple_of_3(n)]

# Contadores para as combinações
prime_counter = Counter()
fibonacci_counter = Counter()
multiple_of_3_counter = Counter()

# Iterar sobre todas as combinações de 7 números em cada jogo
for row in data:
    for comb in combinations(row, 10):
        prime_count = sum(1 for num in comb if num in primes)
        fibonacci_count = sum(1 for num in comb if num in fibonacci)
        multiple_of_3_count = sum(1 for num in comb if num in multiples_of_3)

        prime_counter[comb] = prime_count
        fibonacci_counter[comb] = fibonacci_count
        multiple_of_3_counter[comb] = multiple_of_3_count

# Encontrar a maior combinação para cada critério
max_prime_comb = max(prime_counter, key=prime_counter.get)
max_fibonacci_comb = max(fibonacci_counter, key=fibonacci_counter.get)
max_multiple_of_3_comb = max(multiple_of_3_counter, key=multiple_of_3_counter.get)

print(f"Maior combinação de primos: {max_prime_comb} com {prime_counter[max_prime_comb]} primos")
print(
    f"Maior combinação de Fibonacci: {max_fibonacci_comb} com {fibonacci_counter[max_fibonacci_comb]} números de Fibonacci")
print(
    f"Maior combinação de múltiplos de 3: {max_multiple_of_3_comb} com {multiple_of_3_counter[max_multiple_of_3_comb]} múltiplos de 3")