import csv
import sys
import logging
import traceback
from collections import Counter, defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}

def ler_dados_arquivo(arquivo):
    try:
        with open(arquivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            dados = [row for row in reader if row[0].isdigit()]
        logging.info(f"Arquivo '{arquivo}' lido com sucesso.")
        return dados
    except FileNotFoundError:
        logging.critical(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

def calcular_primos(numeros):
    return len({2, 3, 5, 7, 11, 13, 17, 19, 23} & numeros)

def calcular_fibonacci(numeros):
    return len({1, 2, 3, 5, 8, 13, 21} & numeros)

def calcular_magicos(numeros):
    return len({5, 6, 7, 12, 13, 14, 19, 20, 21} & numeros)

def calcular_multiplos_de_3(numeros):
    return len({3, 6, 9, 12, 15, 18, 21, 24} & numeros)

def calcular_pfmx(numeros):
    return len({1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24} & numeros)

def rotular_ausentes(ausentes):
    labels = []
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    fibonacci = {1, 2, 3, 5, 8, 13, 21}
    magicos = {5, 6, 7, 12, 13, 14, 19, 20, 21}
    multiplos_de_3 = {3, 6, 9, 12, 15, 18, 21, 24}

    for num in ausentes:
        label = f"{num}"
        if num in primos:
            label += "p"
        if num in fibonacci:
            label += "f"
        if num in magicos:
            label += "m"
        if num in multiplos_de_3:
            label += "x"
        labels.append(label)

    return ', '.join(labels)

def calcular_medias(dados):
    total_primos = total_fibonacci = total_magicos = total_multiplos_de_3 = total_pfmx = 0

    for linha in dados:
        numeros = set(map(int, linha[2:])) & moldura
        ausentes = moldura - numeros
        total_primos += calcular_primos(ausentes)
        total_fibonacci += calcular_fibonacci(ausentes)
        total_magicos += calcular_magicos(ausentes)
        total_multiplos_de_3 += calcular_multiplos_de_3(ausentes)
        total_pfmx += calcular_pfmx(ausentes)

    n = len(dados)
    return {
        'primos': total_primos / n,
        'fibonacci': total_fibonacci / n,
        'magicos': total_magicos / n,
        'multiplos_de_3': total_multiplos_de_3 / n,
        'pfmx': total_pfmx / n
    }

def identificar_numeros_quentes_frios(dados):
    frequencia = Counter()

    for linha in dados:
        numeros = set(map(int, linha[2:])) & moldura
        ausentes = moldura - numeros
        frequencia.update(ausentes)

    quentes = [num for num, freq in frequencia.items() if freq > len(dados) / 2]
    frios = [num for num, freq in frequencia.items() if freq <= len(dados) / 2]
    return quentes, frios

def calcular_padroes_sequencia(dados):
    padroes = {num: 0 for num in moldura}
    ultimo_concurso = {num: None for num in moldura}

    for linha in reversed(dados):
        concurso = int(linha[0])
        numeros = set(map(int, linha[2:])) & moldura
        ausentes = moldura - numeros

        for num in moldura:
            if num in ausentes:
                if ultimo_concurso[num] is None:
                    ultimo_concurso[num] = concurso
                padroes[num] += 1
            else:
                if ultimo_concurso[num] is not None:
                    break

    return padroes

def calcular_atraso_por_coluna(dados):
    atraso = {num: 0 for num in moldura}
    ultimo_concurso = {num: None for num in moldura}

    for linha in dados:
        concurso = int(linha[0])
        numeros = set(map(int, linha[2:])) & moldura
        ausentes = moldura - numeros

        for num in moldura:
            if num in ausentes:
                if ultimo_concurso[num] is not None:
                    atraso[num] = max(atraso[num], concurso - ultimo_concurso[num])
                ultimo_concurso[num] = concurso

    return atraso

def exibir_tabela(dados):
    print(f"{'Concurso':<10}\t{'Primos':<10}\t{'Fibonacci':<10}\t{'Mágicos':<10}\t{'Múltiplos de 3':<15}\t{'PFMX':<10}\t{'Números Ausentes':<20}")
    print("-" * 125)
    total_primos = total_fibonacci = total_magicos = total_multiplos_de_3 = total_pfmx = 0
    combinacoes = []
    combinacao_ocorrencias = defaultdict(list)

    for linha in dados:
        concurso = int(linha[0])
        numeros = set(map(int, linha[2:])) & moldura
        ausentes = moldura - numeros
        primos = calcular_primos(ausentes)
        fibonacci = calcular_fibonacci(ausentes)
        magicos = calcular_magicos(ausentes)
        multiplos_de_3 = calcular_multiplos_de_3(ausentes)
        pfmx = calcular_pfmx(ausentes)
        total_primos += primos
        total_fibonacci += fibonacci
        total_magicos += magicos
        total_multiplos_de_3 += multiplos_de_3
        total_pfmx += pfmx
        ausentes_str = rotular_ausentes(sorted(ausentes))
        combinacao = tuple(sorted(ausentes))
        combinacoes.append(combinacao)
        combinacao_ocorrencias[combinacao].append(concurso)
        print(f"{concurso:<10}\t{primos:<10}\t{fibonacci:<10}\t{magicos:<10}\t{multiplos_de_3:<15}\t{pfmx:<10}\t\t\t{ausentes_str:<20}")

    n = len(dados)
    print("-" * 125)
    print(f"{'Médias':<10}\t{total_primos/n:<10.2f}\t{total_fibonacci/n:<10.2f}\t{total_magicos/n:<10.2f}\t{total_multiplos_de_3/n:<15.2f}\t{total_pfmx/n:<10.2f}")

    combinacao_freq = Counter(combinacoes)
    sorted_combinacoes = combinacao_freq.most_common()

    print("\nCombinações mais frequentes (mais de 2 vezes):")
    for combinacao, freq in sorted_combinacoes:
        if freq > 2 and len(combinacao) > 2:
            combinacao_str = ', '.join(map(str, combinacao))
            print(f"{combinacao_str:<40} - {freq} vezes")

def calcular_frequencia(dados):
    numeros = [int(num) for linha in dados for num in linha[2:]]
    return Counter(numeros)

def regressao_logistica(dados):
    X, y = [], []
    for linha in dados:
        numeros = list(map(int, linha[2:]))
        for num in range(1, 26):
            X.append([num])
            y.append(1 if num in numeros else 0)
    model = LogisticRegression()
    model.fit(X, y)
    return model

def clustering(dados):
    numeros = [int(num) for linha in dados for num in linha[2:]]
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(np.array(numeros).reshape(-1, 1))
    return kmeans

def analise_series_temporais(dados):
    numeros = [int(num) for linha in dados for num in linha[2:]]
    model = ARIMA(numeros, order=(5, 1, 0))
    return model.fit()

def simulacao_monte_carlo(dados, n_simulacoes=1000):
    numeros = [int(num) for linha in dados for num in linha[2:]]
    return [np.random.choice(numeros, size=15, replace=True) for _ in range(n_simulacoes)]

def main():
    try:
        arquivo = 'jogos_copy.csv'
        dados = ler_dados_arquivo(arquivo)

        while True:
            try:
                inicio = int(input("Digite o número do concurso inicial: "))
                break
            except ValueError:
                print("Erro: Por favor, digite um número inteiro válido para o concurso inicial.")

        while True:
            try:
                fim = int(input("Digite o número do concurso final: "))
                break
            except ValueError:
                print("Erro: Por favor, digite um número inteiro válido para o concurso final.")

        if inicio > fim:
            logging.warning("Erro: O número do concurso inicial deve ser menor ou igual ao número do concurso final.")
            sys.exit(1)

        dados_intervalo = [linha for linha in dados if inicio <= int(linha[0]) <= fim]

        print("\nTABELA PFMX DOS AUSENTES")
        exibir_tabela(dados_intervalo)

    except Exception as e:
        logging.critical(f"Erro inesperado: {e}")
        logging.critical("Stack trace: %s", traceback.format_exc())

if __name__ == '__main__':
    main()