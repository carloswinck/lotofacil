import csv

# Função para verificar se um número é primo
def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Ler o arquivo csv
with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    linhas = list(reader)

# Contar a quantidade de primos por concurso
total_primos = 0
total_concursos = len(linhas)

for linha in linhas:
    numeros = list(map(int, linha[2:]))
    primos = [num for num in numeros if eh_primo(num)]
    total_primos += len(primos)

# Calcular a média de primos por concurso
media_primos = total_primos / total_concursos

print(f'A média de números primos por concurso é: {media_primos:.2f}')