import pandas as pd
import numpy as np
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

def main():
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
            # Removed print statements for contests
            # print(f"Concurso {row.iloc[0]}:")
            # for linha in matriz:
            #     print(" ".join(linha))
            # print('-' * 50)

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
                print("{:<5} = {:<2} Vezes -> Freq: {:<100} Atraso: {:<5} Média: {:.2f}".format(
                    padrao, vezes_str, intervalos_str, primeiro_encontrado, media_intervalos))
            print('-' * 50)

if __name__ == '__main__':
    main()