import csv
from collections import Counter

# Funções para verificar propriedades dos números
def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def eh_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or n == 0

def eh_par(n):
    return n % 2 == 0

def eh_impar(n):
    return n % 2 != 0

def eh_multiplo_de_3(n):
    return n % 3 == 0

# Função para ler o arquivo CSV
def ler_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

# Função para processar os dados e calcular as métricas
def processar_dados(linhas, num_concursos):
    pares_contador = Counter()
    impares_contador = Counter()
    soma_contador = Counter()
    dezenas_linha_contador = Counter()
    dezenas_coluna_contador = Counter()
    repetidas_contador = Counter()
    sequencia_numeros_contador = Counter()
    sequencia_saltos_contador = Counter()
    fibonacci_contador = Counter()
    primos_contador = Counter()
    multiplos_de_3_contador = Counter()
    total_repetidos = 0

    for idx in range(len(linhas) - num_concursos, len(linhas)):
        numeros = list(map(int, linhas[idx][2:]))
        soma = sum(numeros)
        dezenas_linha = [num // 10 for num in numeros]
        dezenas_coluna = [num % 10 for num in numeros]

        for num in numeros:
            if eh_par(num):
                pares_contador[num] += 1
            if eh_impar(num):
                impares_contador[num] += 1
            if eh_fibonacci(num):
                fibonacci_contador[num] += 1
            if eh_primo(num):
                primos_contador[num] += 1
            if eh_multiplo_de_3(num):
                multiplos_de_3_contador[num] += 1

        soma_contador[soma] += 1
        dezenas_linha_contador.update(dezenas_linha)
        dezenas_coluna_contador.update(dezenas_coluna)

        if idx > 0:
            numeros_anteriores = set(map(int, linhas[idx - 1][2:]))
            repetidas = set(numeros).intersection(numeros_anteriores)
            repetidas_contador.update(repetidas)
            total_repetidos += len(repetidas)

        sequencia_numeros = sorted(numeros)
        for i in range(len(sequencia_numeros) - 1):
            salto = sequencia_numeros[i + 1] - sequencia_numeros[i]
            sequencia_saltos_contador[salto] += 1

    media_repetidos = total_repetidos / (num_concursos - 1)
    return {
        'pares_contador': pares_contador,
        'impares_contador': impares_contador,
        'soma_contador': soma_contador,
        'dezenas_linha_contador': dezenas_linha_contador,
        'dezenas_coluna_contador': dezenas_coluna_contador,
        'repetidas_contador': repetidas_contador,
        'sequencia_numeros_contador': sequencia_numeros_contador,
        'sequencia_saltos_contador': sequencia_saltos_contador,
        'fibonacci_contador': fibonacci_contador,
        'primos_contador': primos_contador,
        'multiplos_de_3_contador': multiplos_de_3_contador,
        'media_repetidos': media_repetidos
    }

# Função para predizer os resultados
def predizer_resultados(metrica, ranges, numeros_anteriores):
    predicted_numbers = set()

    for key, value in ranges.items():
        if key == 'pares':
            predicted_numbers.update([num for num, _ in metrica['pares_contador'].most_common(value)])
        elif key == 'impares':
            predicted_numbers.update([num for num, _ in metrica['impares_contador'].most_common(value)])
        elif key == 'fibonacci':
            predicted_numbers.update([num for num, _ in metrica['fibonacci_contador'].most_common(value)])
        elif key == 'primos':
            predicted_numbers.update([num for num, _ in metrica['primos_contador'].most_common(value)])
        elif key == 'multiplos_de_3':
            predicted_numbers.update([num for num, _ in metrica['multiplos_de_3_contador'].most_common(value)])
        elif key == 'repetidas':
            repetidas = [num for num, _ in metrica['repetidas_contador'].most_common(value)]
            predicted_numbers.update(repetidas[:value])

    # Garantir que pelo menos um número do concurso anterior esteja presente
    if not predicted_numbers.intersection(numeros_anteriores):
        predicted_numbers.add(next(iter(numeros_anteriores)))

    # Ajustar para garantir que a soma esteja dentro do intervalo especificado
    predicted_numbers = list(predicted_numbers)
    while sum(predicted_numbers) < ranges['soma_min'] or sum(predicted_numbers) > ranges['soma_max']:
        predicted_numbers.pop()
        if not predicted_numbers:
            break

    # Garantir que sempre haja 10 números
    while len(predicted_numbers) < 10:
        predicted_numbers.append(next(iter(numeros_anteriores)))

    return predicted_numbers[:10]

# Função para rotular os números previstos
def rotular_numeros(numeros):
    rotulados = []
    for num in numeros:
        label = str(num)
        if eh_primo(num):
            label += 'p'
        if eh_fibonacci(num):
            label += 'f'
        if eh_multiplo_de_3(num):
            label += 'x'
        rotulados.append(label)
    return rotulados

# Função principal
def main():
    file_path = 'jogos_invertidos.csv'
    linhas = ler_csv(file_path)

    # Obter os números do primeiro concurso (último sorteado)
    numeros_primeiro_concurso = set(map(int, linhas[0][2:]))

    # Perguntar ao usuário os ranges para cada filtro e a quantidade de concursos a serem testados
    num_concursos = int(input("Quantos concursos deseja testar? "))
    repetidas = int(input("Quantos números repetidos do concurso anterior? "))
    pares = int(input("Quantos números pares? "))
    impares = int(input("Quantos números ímpares? "))
    primos = int(input("Quantos números primos? "))
    fibonacci = int(input("Quantos números de Fibonacci? "))
    multiplos_de_3 = int(input("Quantos números múltiplos de 3? "))
    miolo = int(input("Quantos números no miolo? "))
    moldura = int(input("Quantos números na moldura? "))
    soma_min = int(input("Qual o valor mínimo da soma dos números? "))
    soma_max = int(input("Qual o valor máximo da soma dos números? "))

    if repetidas > len(numeros_primeiro_concurso):
        print("A quantidade de números repetidos não pode exceder a quantidade de números do primeiro concurso. Tente novamente.")
        return

    if pares + impares > 10 or moldura + miolo > 10:
        print("A soma de números pares e ímpares ou moldura e miolo não pode exceder 10. Tente novamente.")
        return

    ranges = {
        'pares': pares,
        'impares': impares,
        'fibonacci': fibonacci,
        'primos': primos,
        'multiplos_de_3': multiplos_de_3,
        'repetidas': repetidas,
        'soma_min': soma_min,
        'soma_max': soma_max,
        'moldura': moldura,
        'miolo': miolo
    }

    # Espaço em branco
    print()

    metrica = processar_dados(linhas, num_concursos)
    predicted_numbers = predizer_resultados(metrica, ranges, numeros_primeiro_concurso)

    if not predicted_numbers:
        print("Erro: Não foi possível prever os números. Tente novamente.")
        return

    predicted_numbers_rotulados = rotular_numeros(predicted_numbers)

    repetidas_no_concurso_anterior = [num for num in predicted_numbers if num in numeros_primeiro_concurso]

    def extrair_numero(label):
        return int(''.join(filter(str.isdigit, label)))

    moldura_numeros = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    miolo_numeros = {7, 8, 9, 12, 13, 14, 17, 18, 19}

    moldura_previstos = [num for num in predicted_numbers if num in moldura_numeros]
    miolo_previstos = [num for num in predicted_numbers if num in miolo_numeros]

    report = {
        'Números Previstos': ' '.join(predicted_numbers_rotulados),
        'Concursos Testados': f"{len(linhas) - num_concursos + 1} até {len(linhas)}",
        'Números do Concurso Anterior': ' '.join(map(str, numeros_primeiro_concurso)),
        'Repetidas no Concurso Anterior': ' '.join(map(str, repetidas_no_concurso_anterior[:ranges['repetidas']])),
        'Números Primos': ' '.join([num for num in predicted_numbers_rotulados if 'p' in num]),
        'Números de Fibonacci': ' '.join([num for num in predicted_numbers_rotulados if 'f' in num]),
        'Números Múltiplos de 3': ' '.join([num for num in predicted_numbers_rotulados if 'x' in num][:ranges['multiplos_de_3']]),
        'Números Pares': ' '.join([num for num in predicted_numbers_rotulados if eh_par(extrair_numero(num))]),
        'Números Ímpares': ' '.join([num for num in predicted_numbers_rotulados if eh_impar(extrair_numero(num))]),
        'Números no Miolo': ' '.join(map(str, miolo_previstos)),
        'Números na Moldura': ' '.join(map(str, moldura_previstos)),
        'Soma dos Números': str(sum(extrair_numero(num) for num in predicted_numbers_rotulados)),
        'Dezenas por Linha': ' '.join(map(str, [extrair_numero(num) // 10 for num in predicted_numbers_rotulados])),
        'Dezenas por Coluna': ' '.join(map(str, [extrair_numero(num) % 10 for num in predicted_numbers_rotulados])),
        'Sequência Grande de Números': ' '.join(sorted(predicted_numbers_rotulados, key=extrair_numero)),
        'Sequência Grande de Saltos': ' '.join(map(str, metrica['sequencia_saltos_contador']))
    }

    print('Relatório:')
    for key, value in report.items():
        print(f'{key}: {value}')

if __name__ == '__main__':
    main()