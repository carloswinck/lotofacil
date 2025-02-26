import pandas as pd
import numpy as np
from collections import Counter
from collections import defaultdict

def carregar_arquivo():
    try:
        df = pd.read_csv('jogos.csv')
        df_sorted = df.sort_values(by='jogo')
        return df_sorted
    except FileNotFoundError:
        print("Erro: O arquivo 'jogos.csv' não foi encontrado.")
        return None

def criar_matriz_concurso(concurso):
    todos_numeros = set(range(1, 26))
    numeros_sorteados = set(concurso)
    numeros_ausentes = todos_numeros - numeros_sorteados

    matriz = np.array([[f"{i:02}" for i in range(j, j + 5)] for j in range(1, 26, 5)], dtype=object)
    numeros_ocultos = []

    for numero in numeros_sorteados:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = 'XX'
        numeros_ocultos.append(numero)

    for numero in numeros_ausentes:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = f"{numero:02}"

    return matriz, numeros_ocultos


def contar_padroes(matrizes, concursos):
    padroes_por_linha = [Counter() for _ in range(5)]
    padroes_por_coluna = [Counter() for _ in range(5)]
    concursos_padroes_linha = [{} for _ in range(5)]
    concursos_padroes_coluna = [{} for _ in range(5)]

    for matriz, concurso in zip(matrizes, concursos):
        for i, linha in enumerate(matriz):
            padrao_linha = " ".join(linha)
            padroes_por_linha[i][padrao_linha] += 1
            if padrao_linha not in concursos_padroes_linha[i]:
                concursos_padroes_linha[i][padrao_linha] = [concurso]
            else:
                concursos_padroes_linha[i][padrao_linha].append(concurso)

        for j in range(5):
            padrao_coluna = " ".join(matriz[:, j])
            padroes_por_coluna[j][padrao_coluna] += 1
            if padrao_coluna not in concursos_padroes_coluna[j]:
                concursos_padroes_coluna[j][padrao_coluna] = [concurso]
            else:
                concursos_padroes_coluna[j][padrao_coluna].append(concurso)

    return padroes_por_linha, concursos_padroes_linha, padroes_por_coluna, concursos_padroes_coluna

def calcular_intervalos(concursos):
    intervalos = []
    for i in range(len(concursos) - 1):
        intervalos.append(abs(concursos[i + 1] - concursos[i]))
    return intervalos

def imprimir_ultimo_jogo():
    df = carregar_arquivo()
    if df is not None:
        df_sorted = df.sort_values(by='jogo', ascending=False)
        ultimo_jogo = df_sorted.iloc[0, 2:]
        print("Ultimo jogo:", " ".join(map(str, ultimo_jogo)))

def main():
    df = carregar_arquivo()
    if df is not None:
        try:
            concurso_inicio = input("Digite o número do concurso inicial [1]: ").strip()
            concurso_inicio = int(concurso_inicio) if concurso_inicio else 1
            concurso_fim_default = df['jogo'].max()
            concurso_fim = input(f"Digite o número do concurso final [{concurso_fim_default}]: ").strip()
            concurso_fim = int(concurso_fim) if concurso_fim else concurso_fim_default
        except ValueError:
            print("Erro: Por favor, digite números inteiros válidos.")
            return

        df = df[(df.iloc[:, 0] >= concurso_inicio) & (df.iloc[:, 0] <= concurso_fim)]

        matrizes = []
        concursos = []
        numeros_ocultos_list = []
        for index, row in df.iterrows():
            concurso = list(map(int, row.iloc[2:]))
            matriz, numeros_ocultos = criar_matriz_concurso(concurso)
            matrizes.append(matriz)
            concursos.append(row.iloc[0])
            numeros_ocultos_list.append(numeros_ocultos)

        padroes_por_linha, concursos_padroes_linha, padroes_por_coluna, concursos_padroes_coluna = contar_padroes(matrizes, concursos)

        # Printing patterns by row
        for i, padroes in enumerate(padroes_por_linha):
            print(f"Padroes na linha {i + 1}:")
            sorted_padroes = sorted(padroes.items(),key=lambda item: (concursos[-1] - concursos_padroes_linha[i][item[0]][-1]))
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

        # Printing patterns by column
        for j, padroes in enumerate(padroes_por_coluna):
            print(f"Padroes na coluna {j + 1}:")
            sorted_padroes = sorted(padroes.items(),key=lambda item: (concursos[-1] - concursos_padroes_coluna[j][item[0]][-1]))
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

        # Nova seção: Estudo das combinações de padrões por linha que mais fizeram 13 pontos
        print("\nEstudo das combinações de padrões fizeram 13 pontos:")
        combinacoes_XX_pontos = Counter()
        relatorio = []

        for i in range(len(matrizes)):
            combinacao = tuple(tuple(matrizes[i][k]) for k in range(5))
            numeros_ocultos = set()
            for linha in combinacao:
                for j, num in enumerate(linha):
                    if num == 'XX':
                        original_num = (combinacao.index(linha) * 5) + j + 1
                        numeros_ocultos.add(original_num)
            for i, concurso in enumerate(numeros_ocultos_list):
                if len(numeros_ocultos.intersection(concurso)) == 13:
                    combinacoes_XX_pontos[combinacao] += 1
                    relatorio.append((sorted(numeros_ocultos), df.iloc[i]['jogo']))

    # Collecting the data
    numeros_jogos = defaultdict(list)
    for numeros_ocultos, jogo in relatorio:
        numeros_jogos[tuple(numeros_ocultos)].append(jogo)

    # Printing the data sorted by the number of occurrences in descending order
    for numeros_ocultos, jogos in sorted(numeros_jogos.items(), key=lambda item: len(item[1]), reverse=True):
        numeros_ocultos_str = ", ".join(map(str, sorted(set(numeros_ocultos))))
        quantidade = len(jogos)
        jogos_unicos = sorted(set(jogos), reverse=True)
        jogos_str = ", ".join(map(str, jogos_unicos))
        print(f"Números: {numeros_ocultos_str}, Vezes: {quantidade}, Jogos: {jogos_str}")

    print("\n")

    # Nova seção: Estudo das combinações de padrões por linha que mais fizeram 12 pontos
    print("\nEstudo das combinações de padrões fizeram 12 pontos:")
    combinacoes_XX_pontos = Counter()
    relatorio = []

    for i in range(len(matrizes)):
        combinacao = tuple(tuple(matrizes[i][k]) for k in range(5))
        numeros_ocultos = set()
        for linha in combinacao:
            for j, num in enumerate(linha):
                if num == 'XX':
                    original_num = (combinacao.index(linha) * 5) + j + 1
                    numeros_ocultos.add(original_num)
        for i, concurso in enumerate(numeros_ocultos_list):
            if len(numeros_ocultos.intersection(concurso)) == 12:
                combinacoes_XX_pontos[combinacao] += 1
                relatorio.append((sorted(numeros_ocultos), df.iloc[i]['jogo']))

    # Collecting the data
    numeros_jogos = defaultdict(list)
    for numeros_ocultos, jogo in relatorio:
        numeros_jogos[tuple(numeros_ocultos)].append(jogo)

    # Printing the data sorted by the number of occurrences in descending order
    for numeros_ocultos, jogos in sorted(numeros_jogos.items(), key=lambda item: len(item[1]), reverse=True):
        numeros_ocultos_str = ", ".join(map(str, sorted(set(numeros_ocultos))))
        quantidade = len(jogos)
        jogos_unicos = sorted(set(jogos), reverse=True)
        jogos_str = ", ".join(map(str, jogos_unicos))
        print(f"Números: {numeros_ocultos_str}, Vezes: {quantidade}, Jogos: {jogos_str}")





if __name__ == '__main__':
    imprimir_ultimo_jogo()
    main()