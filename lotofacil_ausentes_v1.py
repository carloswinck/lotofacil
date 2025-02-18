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
    nao_pfmx_contador = Counter()
    total_repetidos = 0

    for idx in range(len(linhas) - num_concursos, len(linhas)):
        numeros = list(map(int, linhas[idx][2:]))
        todos_numeros = set(range(1, 26))
        ausentes = todos_numeros - set(numeros)
        soma = sum(ausentes)
        dezenas_linha = [num // 10 for num in ausentes]
        dezenas_coluna = [num % 10 for num in ausentes]

        for num in ausentes:
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
            if not (eh_primo(num) or eh_fibonacci(num) or eh_multiplo_de_3(num) or num in {5, 6, 7, 12, 13, 14, 19, 20, 21}):
                nao_pfmx_contador[num] += 1

        soma_contador[soma] += 1
        dezenas_linha_contador.update(dezenas_linha)
        dezenas_coluna_contador.update(dezenas_coluna)

        if idx > 0:
            numeros_anteriores = set(map(int, linhas[idx - 1][2:]))
            ausentes_anteriores = todos_numeros - numeros_anteriores
            repetidas = set(ausentes).intersection(ausentes_anteriores)
            repetidas_contador.update(repetidas)
            total_repetidos += len(repetidas)

        sequencia_numeros = sorted(ausentes)
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
        'nao_pfmx_contador': nao_pfmx_contador,
        'media_repetidos': media_repetidos
    }

# Função para predizer os resultados
def predizer_resultados(metrica, ranges, numeros_anteriores):
    predicted_numbers = set()
    magic_numbers = {5, 6, 7, 12, 13, 14, 19, 20, 21}

    for key, (min_val, max_val) in ranges.items():
        if key == 'repetidas':
            repetidas = [num for num, _ in metrica['repetidas_contador'].most_common(max_val)]
            predicted_numbers.update(repetidas[:max_val])
        elif key == 'primos':
            predicted_numbers.update([num for num, _ in metrica['primos_contador'].most_common(max_val)])
        elif key == 'fibonacci':
            predicted_numbers.update([num for num, _ in metrica['fibonacci_contador'].most_common(max_val)])
        elif key == 'magicos':
            predicted_numbers.update([num for num in magic_numbers if num in numeros_anteriores][:max_val])
        elif key == 'multiplos_de_3':
            predicted_numbers.update([num for num, _ in metrica['multiplos_de_3_contador'].most_common(max_val)])
        elif key == 'pares':
            predicted_numbers.update([num for num, _ in metrica['pares_contador'].most_common(max_val)])
        elif key == 'impares':
            predicted_numbers.update([num for num, _ in metrica['impares_contador'].most_common(max_val)])
        elif key == 'miolo':
            miolo_numeros = {7, 8, 9, 12, 13, 14, 17, 18, 19}
            predicted_numbers.update([num for num in miolo_numeros if num in numeros_anteriores][:max_val])
        elif key == 'moldura':
            moldura_numeros = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
            predicted_numbers.update([num for num in moldura_numeros if num in numeros_anteriores][:max_val])
        elif key == 'nao_pfmx':
            nao_pfmx = [num for num, _ in metrica['nao_pfmx_contador'].most_common(max_val)]
            predicted_numbers.update(nao_pfmx[:max_val])

    # Garantir que pelo menos um número do concurso anterior esteja presente
    if not predicted_numbers.intersection(numeros_anteriores):
        predicted_numbers.add(next(iter(numeros_anteriores)))

    # Ajustar para garantir que a soma esteja dentro do intervalo especificado
    predicted_numbers = list(predicted_numbers)
    while sum(predicted_numbers) < ranges['soma'][0] or sum(predicted_numbers) > ranges['soma'][1]:
        predicted_numbers.pop()
        if not predicted_numbers:
            break

    # Garantir que sempre haja 10 números
    while len(predicted_numbers) < 10:
        predicted_numbers.append(next(iter(numeros_anteriores)))

    # Garantir que o número de "números não são PFMX" esteja dentro do intervalo especificado
    nao_pfmx_count = sum(1 for num in predicted_numbers if not (eh_primo(num) or eh_fibonacci(num) or eh_multiplo_de_3(num) or num in magic_numbers))
    while nao_pfmx_count < ranges['nao_pfmx'][0]:
        for num in numeros_anteriores:
            if not (eh_primo(num) or eh_fibonacci(num) or eh_multiplo_de_3(num) or num in magic_numbers) and num not in predicted_numbers:
                predicted_numbers.append(num)
                nao_pfmx_count += 1
                if nao_pfmx_count >= ranges['nao_pfmx'][0]:
                    break

    return sorted(list(predicted_numbers)[:10])

# Função para rotular os números
def rotular_numeros(numeros):
    rotulados = []
    for num in numeros:
        label = f"{num:02d}"
        if eh_primo(num):
            label += 'p'
        if eh_fibonacci(num):
            label += 'f'
        if eh_multiplo_de_3(num):
            label += 'x'
        if num in {5, 6, 7, 12, 13, 14, 19, 20, 21}:
            label += 'm'
        rotulados.append(label)
    return list(set(rotulados))

# Função principal
def main():
    file_path = 'jogos_invertidos.csv'
    linhas = ler_csv(file_path)

    # Obter os números do primeiro concurso (último sorteado)
    numeros_primeiro_concurso = set(map(int, linhas[0][2:]))
    todos_numeros = set(range(1, 26))
    ausentes_primeiro_concurso = todos_numeros - numeros_primeiro_concurso

    # Apresentar a mensagem antes das perguntas
    print("ANÁLISE DOS NÚMEROS AUSENTES (TODAS AS PERGUNTAS SÃO SOBRE NÚMEROS AUSENTES):")
    print("---")

    # Perguntar ao usuário os ranges para cada filtro e a quantidade de concursos a serem testados
    while True:
        try:
            num_concursos = int(input(f"Quantos concursos deseja analisar? (1-{len(linhas)}) "))
            if 1 <= num_concursos <= len(linhas):
                break
            else:
                print(f"Por favor, insira um número entre 1 e {len(linhas)}.")
        except ValueError:
            print("Por favor, insira um número válido.")

    def obter_range(prompt):
        while True:
            try:
                min_val = int(input(f"{prompt} (mínimo): "))
                max_val = int(input(f"{prompt} (máximo): "))
                if min_val <= max_val:
                    return (min_val, max_val)
                else:
                    print("O valor mínimo deve ser menor ou igual ao valor máximo.")
            except ValueError:
                print("Por favor, insira números válidos.")

    def obter_valor(prompt):
        while True:
            try:
                val = int(input(f"{prompt}: "))
                return val
            except ValueError:
                print("Por favor, insira um número válido.")

    repetidas = obter_range("Quantos números repetidos do concurso anterior?")
    nao_pfmx = obter_range("Quantos números não são PFMX?")
    primos = obter_range("Quantos números primos?")
    fibonacci = obter_range("Quantos números de Fibonacci?")
    magicos = obter_range("Quantos números mágicos?")
    multiplos_de_3 = obter_range("Quantos números múltiplos de 3?")
    pares = obter_valor("Quantos números pares")
    impares = obter_valor("Quantos números ímpares")
    miolo = obter_valor("Quantos números no miolo")
    moldura = obter_valor("Quantos números na moldura")
    soma = obter_range("Qual o valor da soma dos números")

    if repetidas[1] > len(ausentes_primeiro_concurso):
        print("A quantidade de números repetidos não pode exceder a quantidade de números ausentes do primeiro concurso. Tente novamente.")
        return

    if pares + impares > 10:
        print("A soma de números pares e ímpares não pode exceder 10. Tente novamente.")
        return

    ranges = {
        'repetidas': repetidas,
        'nao_pfmx': nao_pfmx,
        'primos': primos,
        'fibonacci': fibonacci,
        'magicos': magicos,
        'multiplos_de_3': multiplos_de_3,
        'pares': (pares, pares),
        'impares': (impares, impares),
        'miolo': (miolo, miolo),
        'moldura': (moldura, moldura),
        'soma': soma
    }

    # Espaço em branco
    print()

    metrica = processar_dados(linhas, num_concursos)
    predicted_numbers = predizer_resultados(metrica, ranges, ausentes_primeiro_concurso)

    if not predicted_numbers:
        print("Erro: Não foi possível prever os números. Tente novamente.")
        return

    predicted_numbers_rotulados = rotular_numeros(predicted_numbers)

    repetidas_no_concurso_anterior = [num for num in predicted_numbers if num in ausentes_primeiro_concurso]

    def extrair_numero(label):
        return int(''.join(filter(str.isdigit, label)))

    moldura_numeros = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    miolo_numeros = {7, 8, 9, 12, 13, 14, 17, 18, 19}

    moldura_previstos = [num for num in predicted_numbers if num in moldura_numeros]
    miolo_previstos = [num for num in predicted_numbers if num in miolo_numeros]

    def rotular_com_pfmx(numeros):
        return ' '.join(sorted(rotular_numeros(numeros)))

    report = {
        'Concursos Analisados': f"{len(linhas) - num_concursos + 1} até {len(linhas)}",
        'Previsão dos Números': ' '.join(sorted(predicted_numbers_rotulados)),
        'Números do Concurso Anterior': rotular_com_pfmx(ausentes_primeiro_concurso),
        'Repetidas no Concurso Anterior': rotular_com_pfmx(repetidas_no_concurso_anterior[:ranges['repetidas'][1]]),
        'Números Primos': ' '.join(sorted([num for num in predicted_numbers_rotulados if 'p' in num])),
        'Números de Fibonacci': ' '.join(sorted([num for num in predicted_numbers_rotulados if 'f' in num])),
        'Números Mágicos': ' '.join(sorted([num for num in predicted_numbers_rotulados if 'm' in num][:ranges['magicos'][1]])),
        'Números Múltiplos de 3': ' '.join(sorted([num for num in predicted_numbers_rotulados if 'x' in num][:ranges['multiplos_de_3'][1]])),
        'Números Pares': ' '.join(sorted([num for num in predicted_numbers_rotulados if eh_par(extrair_numero(num))])),
        'Números Ímpares': ' '.join(sorted([num for num in predicted_numbers_rotulados if eh_impar(extrair_numero(num))])),
        'Números no Miolo': rotular_com_pfmx(miolo_previstos),
        'Números na Moldura': rotular_com_pfmx(moldura_previstos),
        'Soma dos Números': str(sum(extrair_numero(num) for num in predicted_numbers_rotulados)),
        'Números não são PFMX': ' '.join(sorted([num for num in predicted_numbers_rotulados if 'p' not in num and 'f' not in num and 'm' not in num and 'x' not in num]))
    }

    print(f"RESULTADOS: (Concursos Analisados: {report['Concursos Analisados']})")
    print(f"Previsão dos Números:\t{report['Previsão dos Números']}".expandtabs(40))
    print("---")
    print(f"Números do Concurso Anterior:\t{report['Números do Concurso Anterior']}".expandtabs(40))
    print(f"Repetidas no Concurso Anterior:\t{report['Repetidas no Concurso Anterior']}".expandtabs(40))
    print("---")
    print(f"Números não são PFMX:\t{report['Números não são PFMX']}".expandtabs(40))
    print("---")
    print(f"Números Primos:\t{report['Números Primos']}".expandtabs(40))
    print(f"Números de Fibonacci:\t{report['Números de Fibonacci']}".expandtabs(40))
    print(f"Números Mágicos:\t{report['Números Mágicos']}".expandtabs(40))
    print(f"Números Múltiplos de 3:\t{report['Números Múltiplos de 3']}".expandtabs(40))
    print("---")
    print(f"Números Pares:\t{report['Números Pares']}".expandtabs(40))
    print(f"Números Ímpares:\t{report['Números Ímpares']}".expandtabs(40))
    print("---")
    print(f"Números no Miolo:\t{report['Números no Miolo']}".expandtabs(40))
    print(f"Números na Moldura:\t{report['Números na Moldura']}".expandtabs(40))
    print("---")
    print(f"Soma dos Números:\t{report['Soma dos Números']}".expandtabs(40))

if __name__ == '__main__':
    main()