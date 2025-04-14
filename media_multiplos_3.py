import csv

# Função para verificar se um número é múltiplo de 3
def eh_multiplo_de_3(n):
    return n % 3 == 0

# Ler o arquivo csv
with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    linhas = list(reader)

# Contar a quantidade de múltiplos de 3 por concurso
total_multiplos_de_3 = 0
total_concursos = len(linhas)

for linha in linhas:
    numeros = list(map(int, linha[2:]))
    multiplos_de_3 = [num for num in numeros if eh_multiplo_de_3(num)]
    total_multiplos_de_3 += len(multiplos_de_3)

# Calcular a média de múltiplos de 3 por concurso
media_multiplos_de_3 = total_multiplos_de_3 / total_concursos

print(f'A média de múltiplos de 3 por concurso é: {media_multiplos_de_3:.2f}')