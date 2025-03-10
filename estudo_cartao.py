import numpy as np
import pandas as pd
from collections import Counter

def criar_cartao_com_numeros(numeros_escolhidos):
    if len(numeros_escolhidos) != 15:
        raise ValueError("Você deve fornecer exatamente 15 números.")
    matriz = np.array([[f"{i:02}" for i in range(j, j + 5)] for j in range(1, 26, 5)], dtype=object)
    for numero in numeros_escolhidos:
        linha, coluna = divmod(numero - 1, 5)
        matriz[linha][coluna] = 'XX'
    return matriz

def criar_matriz_concurso(concurso):
    matriz = np.array([[f"{i:02}" for i in range(j, j + 5)] for j in range(1, 26, 5)], dtype=object)
    for numero in concurso:
        linha, coluna = divmod(numero - 1, 5)
        matriz[linha][coluna] = 'XX'
    return matriz

def contar_padroes(matriz):
    padroes_por_linha = Counter(" ".join(linha) for linha in matriz)
    padroes_por_coluna = Counter(" ".join(coluna) for coluna in matriz.T)
    return padroes_por_linha, padroes_por_coluna

def calcular_intervalos(concursos):
    return [abs(concursos[i + 1] - concursos[i]) for i in range(len(concursos) - 1)]

def gerar_relatorio(cartao, concursos, concurso_fim):
    padroes_por_linha, padroes_por_coluna = contar_padroes(cartao)
    concursos_padroes_linha = {padrao: [] for padrao in padroes_por_linha}
    concursos_padroes_coluna = {padrao: [] for padrao in padroes_por_coluna}

    for idx, concurso in enumerate(concursos):
        matriz = criar_matriz_concurso(concurso)
        for i, linha in enumerate(matriz):
            padrao_linha = " ".join(linha)
            if padrao_linha in concursos_padroes_linha:
                concursos_padroes_linha[padrao_linha].append(idx + 1)
        for j, coluna in enumerate(matriz.T):
            padrao_coluna = " ".join(coluna)
            if padrao_coluna in concursos_padroes_coluna:
                concursos_padroes_coluna[padrao_coluna].append(idx + 1)

    print("\n\nRelatório para o cartão fornecido:\n\nLinhas")
    for padrao, quantidade in padroes_por_linha.items():
        if quantidade == 1:
            concursos = concursos_padroes_linha[padrao]
            intervalos = calcular_intervalos(concursos)
            atraso = concursos[0]
            media_intervalos = np.mean(intervalos) if intervalos else 0
            print(f"{padrao:<5} = {len(concursos):02} Vezes -> Freq: {' '.join(map(str, intervalos)):<200} Atraso: {atraso:<5} Média: {media_intervalos:.2f}")
    print('-' * 50 + "\n\nColunas")
    for padrao, quantidade in padroes_por_coluna.items():
        if quantidade == 1:
            concursos = concursos_padroes_coluna[padrao]
            intervalos = calcular_intervalos(concursos)
            atraso = concursos[0]
            media_intervalos = np.mean(intervalos) if intervalos else 0
            print(f"{padrao:<5} = {len(concursos):02} Vezes -> Freq: {' '.join(map(str, intervalos)):<200} Atraso: {atraso:<5} Média: {media_intervalos:.2f}")
    print('-' * 50)


def main():
    df = pd.read_csv('jogos.csv')

    try:
        concurso_inicio = int(input("Digite o número do concurso inicial (2000): ").strip() or 2000)
    except ValueError:
        concurso_inicio = 2000

    try:
        concurso_fim = int(
            input("Digite o número do concurso final (último concurso): ").strip() or df['jogo'].max())
    except ValueError:
        concurso_fim = df['jogo'].max()

    df = df[(df['jogo'] >= concurso_inicio) & (df['jogo'] <= concurso_fim)]
    concursos = df.iloc[:, 2:].values.tolist()
    numeros_escolhidos = list(map(int, input("Digite 15 números separados por vírgula: ").strip().split(',')))

    if len(numeros_escolhidos) != 15:
        print("Erro: Você deve fornecer exatamente 15 números.")
        return

    print("")
    cartao = criar_cartao_com_numeros(numeros_escolhidos)
    for linha in cartao:
        print(" ".join(linha))

    gerar_relatorio(cartao, concursos, concurso_fim)


if __name__ == '__main__':
    main()