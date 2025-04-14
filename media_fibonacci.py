import csv

# Função para verificar se um número é de Fibonacci
def eh_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or n == 0

# Ler o arquivo csv
with open('jogos_invertidos.csv', 'r') as file:
    reader = csv.reader(file)
    linhas = list(reader)

# Contar a quantidade de números de Fibonacci por concurso
total_fibonacci = 0
total_concursos = len(linhas)

for linha in linhas:
    numeros = list(map(int, linha[2:]))
    fibonacci = [num for num in numeros if eh_fibonacci(num)]
    total_fibonacci += len(fibonacci)

# Calcular a média de números de Fibonacci por concurso
media_fibonacci = total_fibonacci / total_concursos

print(f'A média de números de Fibonacci por concurso é: {media_fibonacci:.2f}')