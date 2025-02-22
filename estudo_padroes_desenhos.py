import pandas as pd
import numpy as np
import random
from collections import Counter

def carregar_arquivo():
    try:
        df = pd.read_csv('jogos.csv')
        return df
    except FileNotFoundError:
        print("Erro: O arquivo 'jogos.csv' não foi encontrado.")
        return None

def criar_matriz_concurso(concurso):
    todos_numeros = set(range(1, 26))
    numeros_sorteados = set(concurso)
    numeros_ausentes = todos_numeros - numeros_sorteados

    matriz = np.array([[f"{i:02}" for i in range(j, j + 5)] for j in range(1, 26, 5)], dtype=object)

    for numero in numeros_sorteados:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = 'XX'

    for numero in numeros_ausentes:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = f"{numero:02}"

    return matriz

def contar_padroes(matrizes, concursos):
    padroes_por_linha = [Counter() for _ in range(5)]
    concursos_padroes = [{} for _ in range(5)]
    for matriz, concurso in zip(matrizes, concursos):
        for i, linha in enumerate(matriz):
            padrao = " ".join(linha)
            padroes_por_linha[i][padrao] += 1
            if padrao not in concursos_padroes[i]:
                concursos_padroes[i][padrao] = [concurso]
            else:
                concursos_padroes[i][padrao].append(concurso)
    return padroes_por_linha, concursos_padroes

def calcular_intervalos(concursos):
    intervalos = []
    for i in range(len(concursos) - 1):
        intervalos.append(abs(concursos[i + 1] - concursos[i]))
    return intervalos

def calcular_estatisticas(intervalos):
    if intervalos:
        minimo = min(intervalos)
        media = np.mean(intervalos)
        maximo = max(intervalos)
    else:
        minimo = media = maximo = 0
    return minimo, media, maximo

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    x1 = 5 * n * n + 4
    x2 = 5 * n * n - 4
    return int(x1**0.5)**2 == x1 or int(x2**0.5)**2 == x2

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

def is_multiple_of_3(n):
    return n % 3 == 0

def is_magico(n):
    return n in {5, 6, 7, 12, 13, 14, 19, 20, 21}

def main():

    moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    miolo = {7, 8, 9, 12, 13, 14, 17, 18, 19}

    # Define the blacklist of patterns
    blacklist = {
        "21 22 23 24 25",
        "16 17 18 19 20",
        "11 12 13 14 15",
        "06 07 08 09 10"
    }

    # Initialize counters for each line
    total_padroes_por_linha = [0] * 5

    df = carregar_arquivo()
    if df is not None:
        try:
            concurso_inicio = int(input("Digite o número do concurso inicial: ").strip())
            concurso_fim = int(input("Digite o número do concurso final: ").strip())
        except ValueError:
            print("Erro: Por favor, digite números inteiros válidos.")
            return

        df = df[(df.iloc[:, 0] >= concurso_inicio) & (df.iloc[:, 0] <= concurso_fim)]

        matrizes = []
        concursos = []
        for index, row in df.iterrows():
            concurso = list(map(int, row.iloc[2:]))
            matriz = criar_matriz_concurso(concurso)
            matrizes.append(matriz)
            concursos.append(row.iloc[0])

        padroes_por_linha, concursos_padroes = contar_padroes(matrizes, concursos)
        for i, padroes in enumerate(padroes_por_linha):
            print(f"Padroes na linha {i + 1}:")
            sorted_padroes = sorted(padroes.items(), key=lambda item: (concurso_fim - concursos_padroes[i][item[0]][0]))
            for padrao, quantidade in sorted_padroes:
                concursos = concursos_padroes[i][padrao]
                intervalos = calcular_intervalos(concursos)
                intervalos_str = " ".join(map(str, intervalos))
                primeiro_encontrado = concurso_fim - concursos[0]
                media_intervalos = np.mean(intervalos) if intervalos else 0
                vezes_str = f"{quantidade:02}"
                print("{:<5} = {:<2} Vezes -> Freq: {:<130} Atraso: {:<5} Média: {:.2f}".format(
                    padrao, vezes_str, intervalos_str, primeiro_encontrado, media_intervalos))
            print('-' * 50)

        # New section: Medias das linhas
        print("\nMedias das linhas:")
        for i in range(5):
            ocorrencias = [f"{padrao}={quantidade}v" for padrao, quantidade in sorted(padroes_por_linha[i].items(), key=lambda item: item[1])]
            print(f"Debug: Ocorrencias for linha {i + 1}: {ocorrencias}")  # Debug print
            minimo = min(padroes_por_linha[i].values()) if padroes_por_linha[i] else 0
            maximo = max(padroes_por_linha[i].values()) if padroes_por_linha[i] else 0
            print(f"linha {i + 1} = Minimo: {minimo} Vezes, Maximo: {maximo} Vezes")

        # New section: Generate 15 cards with specific criteria
        cartoes = []
        historico_jogos = [set(map(int, row.iloc[2:])) for index, row in df.iterrows()][::-1]
        penultimo_concurso = historico_jogos[-1]
        ausentes_penultimo_concurso = set(range(1, 26)) - penultimo_concurso

        for _ in range(15):
            while True:
                total_numeros = 0
                cartao = []
                numeros_escolhidos = set()
                for i in range(5):
                    padroes_validos = []
                    for padrao, quantidade in padroes_por_linha[i].items():
                        if 20 < quantidade < 90:
                            concursos = concursos_padroes[i][padrao]
                            atraso = concurso_fim - concursos[0]
                            if atraso not in range(1, 3) and atraso not in range(30, 40):
                                padroes_validos.append(padrao)
                    if not padroes_validos:
                        break
                    padrao_escolhido = random.choice(padroes_validos)
                    if padrao_escolhido in blacklist:
                        continue
                    for idx, num in enumerate(padrao_escolhido.split()):
                        if num == 'XX':
                            numero = (i * 5) + idx + 1
                            if numero not in numeros_escolhidos:
                                numeros_escolhidos.add(numero)
                                total_numeros += 1
                    cartao.append(padrao_escolhido)

                soma_numeros = sum(numeros_escolhidos)
                primos = sum(1 for num in numeros_escolhidos if is_prime(num))
                fibonacci = sum(1 for num in numeros_escolhidos if is_fibonacci(num))
                magicos = sum(1 for num in numeros_escolhidos if is_magico(num))
                pares = sum(1 for num in numeros_escolhidos if is_even(num))
                impares = sum(1 for num in numeros_escolhidos if is_odd(num))
                multiplos_de_3 = sum(1 for num in numeros_escolhidos if is_multiple_of_3(num))
                repetidos = len(numeros_escolhidos & penultimo_concurso)
                repetidos_ausentes = len(numeros_escolhidos & ausentes_penultimo_concurso)
                if (
                        total_numeros == 15 and
                        10 <= repetidos <= 10 and
                        3 <= repetidos_ausentes <= 5 and
                        170 <= soma_numeros <= 190 and
                        primos in [4, 5] and
                        fibonacci in [2, 3] and
                        multiplos_de_3 in [4, 5] and
                        magicos in [4, 5] and
                        pares >= 9 and
                        len(numeros_escolhidos & miolo) >= 5 and
                        numeros_escolhidos not in historico_jogos
                ):
                    for i, linha in enumerate(cartao):
                        total_padroes_por_linha[i] += 1
                    print(f" ")
                    print(f"Padroes escolhidos: {cartao}")
                    print(f"Repetidos = {repetidos}")
                    print(f"Repetidos do Ausentes = {repetidos_ausentes}")
                    print(f"Soma = {soma_numeros}")
                    print(f"Primos = {primos}")
                    print(f"Fibonacci = {fibonacci}")
                    print(f"Multiplos  = {multiplos_de_3}")
                    print(f"Magicos = {magicos}")
                    print(f"Pares = {pares}, Impares = {impares}")
                    print(f"Miolo = {len(numeros_escolhidos & miolo)}, Moldura = {len(numeros_escolhidos & moldura)}")
                    print(f" ")
                    print(f"---------------------------------------------")
                    break
            cartoes.append(cartao)

        # Print the list of chosen numbers for each card
        print("\nLista dos 15 cartões:")
        for cartao in cartoes:
            numeros = []
            for i, linha in enumerate(cartao):
                for j, num in enumerate(linha.split()):
                    if num == 'XX':
                        numeros.append((i * 5) + j + 1)
            print(", ".join(map(str, sorted(numeros))))

if __name__ == '__main__':
    main()