import csv
from itertools import combinations
from collections import Counter

# Função para verificar se um número é primo
def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Função para verificar se um número é de Fibonacci
def eh_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or n == 0

# Função para verificar se um número é múltiplo de 3
def eh_multiplo_de_3(n):
    return n % 3 == 0

# Ler o arquivo csv
with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    linhas = list(reader)

# Contar a frequência das combinações de números primos, Fibonacci, múltiplos de 3 e outros
combinacoes_contador = Counter()

for linha in linhas:
    numeros = list(map(int, linha[2:]))
    primos = [num for num in numeros if eh_primo(num)]
    fibonacci = [num for num in numeros if eh_fibonacci(num)]
    multiplos_de_3 = [num for num in numeros if eh_multiplo_de_3(num)]
    outros = [num for num in numeros if not (eh_primo(num) or eh_fibonacci(num) or eh_multiplo_de_3(num))]
    combinacoes = combinations(primos + fibonacci + multiplos_de_3 + outros, 10)
    combinacoes_contador.update(combinacoes)

# Encontrar a combinação mais frequente
combinacao_mais_frequente = combinacoes_contador.most_common(1)[0]

print(f'A combinação de 10 números (primos, Fibonacci, múltiplos de 3 e outros) que mais aparece é: {combinacao_mais_frequente[0]} com {combinacao_mais_frequente[1]} ocorrências')