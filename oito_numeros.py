import csv
from itertools import combinations
from collections import Counter

# Ler o arquivo csv
with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    linhas = list(reader)

# Contar a frequência das combinações de 8 números
combinacoes_contador = Counter()

for linha in linhas:
    numeros = list(map(int, linha[2:]))
    combinacoes = combinations(numeros, 2)
    combinacoes_contador.update(combinacoes)

# Encontrar a combinação mais frequente
combinacao_mais_frequente = combinacoes_contador.most_common(1)[0]

print(f'A combinação de 2 números que mais aparece é: {combinacao_mais_frequente[0]} com {combinacao_mais_frequente[1]} ocorrências')