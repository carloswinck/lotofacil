import csv

# Função para encontrar números ausentes em uma lista
def encontrar_ausentes(numeros, total=25):
    return [str(i) for i in range(1, total + 1) if i not in numeros]

# Ler o arquivo csv
with open('jogos.csv', 'r') as file:
    reader = csv.reader(file)
    linhas = list(reader)

# Processar cada linha para encontrar números ausentes
resultados = []
for linha in linhas:
    jogo = linha[0]
    data = linha[1]
    numeros = list(map(int, linha[2:]))
    ausentes = encontrar_ausentes(numeros)
    resultados.append([jogo, data] + ausentes)

# Escrever o resultado no novo arquivo
with open('jogos_invertidos.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for resultado in resultados:
        writer.writerow(resultado)