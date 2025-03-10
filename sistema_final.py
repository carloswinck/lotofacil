import pandas as pd
import numpy as np
from collections import Counter
import random

primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
fibonacci = {1, 2, 3, 5, 8, 13, 21}
multiplos_de_3 = {3, 6, 9, 12, 15, 18, 21, 24}
magicos = {5, 6, 7, 12, 13, 14, 19, 20, 21}
centro = {7, 8, 9, 12, 13, 14, 17, 18, 19}
moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}

def carregar_arquivo():
    try:
        df = pd.read_csv('jogos.csv')
        df_sorted = df.sort_values(by='jogo')
        return df_sorted
    except FileNotFoundError:
        print("Erro: O arquivo 'jogos.csv' não foi encontrado.")
        return None

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


def gerar_cartao(ultimo_concurso, primos_range, fibonacci_range, multiplos_de_3_range, magicos_range, centro_range,
                 qtd_ultimo_concurso_range):
    todos_numeros = set(range(1, 26))
    qtd_centro = random.randint(centro_range[0], centro_range[1])
    numeros_centro = set(random.sample(list(centro), qtd_centro))
    ultimo_concurso_set = set(ultimo_concurso)

    while True:
        numeros_selecionados = set(random.sample(list(moldura), 15 - len(numeros_centro)))
        numeros_selecionados = numeros_selecionados | numeros_centro
        qtd_ultimo_concurso = len(numeros_selecionados & ultimo_concurso_set)

        if qtd_ultimo_concurso_range[0] <= qtd_ultimo_concurso <= qtd_ultimo_concurso_range[1]:
            qtd_primos = len(numeros_selecionados & primos)
            qtd_fibonacci = len(numeros_selecionados & fibonacci)
            qtd_multiplos_de_3 = len(numeros_selecionados & multiplos_de_3)
            qtd_magicos = len(numeros_selecionados & magicos)

            if (primos_range[0] <= qtd_primos <= primos_range[1] and
                    fibonacci_range[0] <= qtd_fibonacci <= fibonacci_range[1] and
                    multiplos_de_3_range[0] <= qtd_multiplos_de_3 <= multiplos_de_3_range[1] and
                    magicos_range[0] <= qtd_magicos <= magicos_range[1] and
                    centro_range[0] <= qtd_centro <= centro_range[1]):
                break

    numeros_sorteados = numeros_selecionados
    numeros_ausentes = todos_numeros - numeros_sorteados

    if not (170 <= sum(numeros_sorteados) <= 220):
        return gerar_cartao(ultimo_concurso, primos_range, fibonacci_range, multiplos_de_3_range, magicos_range,
                            centro_range, qtd_ultimo_concurso_range)

    matriz = np.array([[f"{i:02}" for i in range(j, j + 5)] for j in range(1, 26, 5)], dtype=object)

    for numero in numeros_sorteados:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = 'XX'

    for numero in numeros_ausentes:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = f"{numero:02}"

    return matriz, sorted(numeros_sorteados)

def gerar_cartoes(n=20, ultimo_concurso=[], primos_range=(1, 6), fibonacci_range=(1, 6), multiplos_de_3_range=(1, 6), magicos_range=(1, 6), centro_range=(3, 6), qtd_ultimo_concurso_range=(8, 12)):
    return [gerar_cartao(ultimo_concurso, primos_range, fibonacci_range, multiplos_de_3_range, magicos_range, centro_range, qtd_ultimo_concurso_range) for _ in range(n)]

def exibir_cartoes(cartoes, ultimo_concurso, concursos):
    for i, (cartao, numeros) in enumerate(cartoes, 1):
        print(f"Cartão {i}:")
        for linha in cartao:
            print(" ".join(linha))
        print("Números:", end=" ")
        qtd_primos = qtd_fibonacci = qtd_multiplos_de_3 = qtd_magicos = qtd_repetidos = 0
        for numero in numeros:
            tags = ""
            if numero in primos:
                tags += "p"
                qtd_primos += 1
            if numero in fibonacci:
                tags += "f"
                qtd_fibonacci += 1
            if numero in multiplos_de_3:
                tags += "x"
                qtd_multiplos_de_3 += 1
            if numero in magicos:
                tags += "m"
                qtd_magicos += 1
            if numero in ultimo_concurso:
                qtd_repetidos += 1
            print(f"{numero:02}{tags}", end=" ")
        print(f"\nRelatório: {qtd_primos} primos, {qtd_fibonacci} fibonacci, {qtd_multiplos_de_3} múltiplos de 3, {qtd_magicos} mágicos, {qtd_repetidos} repetidos\n")

def main():
    df = carregar_arquivo()

    if df is not None:
        try:
            concurso_inicio = int(input("Digite o número do concurso inicial: ").strip())
            concurso_fim = int(input("Digite o número do concurso final: ").strip())
        except ValueError:
            print("Erro: Por favor, digite números inteiros válidos.")
            return

        primos_range = tuple(map(int, input("Digite o intervalo para primos (ex: 1 6): ").strip().split()))
        fibonacci_range = tuple(map(int, input("Digite o intervalo para fibonacci (ex: 1 6): ").strip().split()))
        multiplos_de_3_range = tuple(map(int, input("Digite o intervalo para múltiplos de 3 (ex: 1 6): ").strip().split()))
        magicos_range = tuple(map(int, input("Digite o intervalo para mágicos (ex: 1 6): ").strip().split()))
        centro_range = tuple(map(int, input("Digite o intervalo para centro (ex: 1 6): ").strip().split()))
        qtd_ultimo_concurso_range = tuple(
            map(int, input("Digite o intervalo para qtd_ultimo_concurso (ex: 8 12): ").strip().split()))

        df = df[(df.iloc[:, 0] >= concurso_inicio) & (df.iloc[:, 0] <= concurso_fim)]

        matrizes = []
        concursos = []
        for index, row in df.iterrows():
            concurso = list(map(int, row.iloc[2:]))
            matriz = criar_matriz_concurso(concurso)
            matrizes.append(matriz)
            concursos.append(row.iloc[0])

        padroes_por_linha, concursos_padroes_linha = contar_padroes(matrizes, concursos)
        padroes_por_coluna, concursos_padroes_coluna = contar_padroes([matriz.T for matriz in matrizes], concursos)

        for i, padroes in enumerate(padroes_por_linha):
            print(f"Padroes na linha {i + 1}:")
            sorted_padroes = sorted(padroes.items(), key=lambda item: (concurso_fim - concursos_padroes_linha[i][item[0]][-1]))
            for padrao, quantidade in sorted_padroes:
                concursos = concursos_padroes_linha[i][padrao]
                intervalos = calcular_intervalos(concursos)
                intervalos_str = " ".join(map(str, intervalos))
                primeiro_encontrado = concurso_fim - concursos[-1]
                media_intervalos = np.mean(intervalos) if intervalos else 0
                vezes_str = f"{quantidade:02}"
                print("{:<5} = {:<2} Vezes -> Freq: {:<200} Atraso: {:<5} Média: {:.2f}".format(
                    padrao, vezes_str, intervalos_str, primeiro_encontrado, media_intervalos))
            print('-' * 50)

        for j, padroes in enumerate(padroes_por_coluna):
            print(f"Padroes na coluna {j + 1}:")
            sorted_padroes = sorted(padroes.items(), key=lambda item: (concurso_fim - concursos_padroes_coluna[j][item[0]][-1]))
            for padrao, quantidade in sorted_padroes:
                concursos = concursos_padroes_coluna[j][padrao]
                intervalos = calcular_intervalos(concursos)
                intervalos_str = " ".join(map(str, intervalos))
                primeiro_encontrado = concurso_fim - concursos[-1]
                media_intervalos = np.mean(intervalos) if intervalos else 0
                vezes_str = f"{quantidade:02}"
                print("{:<5} = {:<2} Vezes -> Freq: {:<200} Atraso: {:<5} Média: {:.2f}".format(
                    padrao, vezes_str, intervalos_str, primeiro_encontrado, media_intervalos))
            print('-' * 50)

    if df is not None:
        ultimo_concurso = list(map(int, df.iloc[-1, 2:]))
        cartoes = gerar_cartoes(20, ultimo_concurso, primos_range, fibonacci_range, multiplos_de_3_range, magicos_range, centro_range, qtd_ultimo_concurso_range)

        # Print the selected numbers for the lottery
        for _, numeros in cartoes:
            print(", ".join(map(str, numeros)))

if __name__ == '__main__':
    main()