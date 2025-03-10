import csv
import sys
import logging
import numpy as np
from itertools import combinations
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import asyncio
import random
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
NUMEROS_PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23}
NUMEROS_FIBONACCI = {1, 2, 3, 5, 8, 13, 21}
NUMEROS_MAGICOS = {5, 6, 7, 12, 13, 14, 19, 20, 21}
NUMEROS_MULTIPLOS_3 = {3, 6, 9, 12, 15, 18, 21, 24}

def ler_dados_arquivo(arquivo):
    try:
        with open(arquivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            dados = list(reader)
        logging.info(f"Arquivo '{arquivo}' lido com sucesso.")
        return dados
    except FileNotFoundError:
        logging.critical(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

def obter_intervalo_concursos():
    while True:
        try:
            inicio = int(input("Digite o número do concurso inicial: "))
            fim = int(input("Digite o número do concurso final: "))
            if inicio > fim:
                logging.warning("Erro: O número do concurso inicial deve ser menor ou igual ao número do concurso final.")
            else:
                return inicio, fim
        except ValueError:
            logging.warning("Erro: Por favor, insira um número válido.")

def obter_quantidades():
    while True:
        try:
            qtd_fixos = int(input("Digite a quantidade de números fixos sorteados: "))
            qtd_ausentes = int(input("Digite a quantidade de números ausentes: "))
            if qtd_fixos + qtd_ausentes > 15:
                logging.error("Erro: A soma de números fixos e ausentes não pode exceder 15.")
            else:
                return qtd_fixos, qtd_ausentes
        except ValueError:
            logging.warning("Erro: Por favor, insira um número válido.")

def obter_numeros(tipo, quantidade):
    numeros = []
    for _ in range(quantidade):
        while True:
            try:
                numero = int(input(f"Digite um número {tipo}: "))
                numeros.append(numero)
                break
            except ValueError:
                logging.warning("Erro: Por favor, insira um número válido.")
    return numeros

def obter_miolo_cartao():
    while True:
        try:
            qtd_miolo = int(input("Digite a quantidade de números no miolo do cartão: "))
            return qtd_miolo
        except ValueError:
            logging.warning("Erro: Por favor, insira um número válido.")

def obter_filtros():
    while True:
        try:
            primos_min = int(input("Digite o valor mínimo para a quantidade de números primos: "))
            primos_max = int(input("Digite o valor máximo para a quantidade de números primos: "))
            fibonacci_min = int(input("Digite o valor mínimo para a quantidade de números Fibonacci: "))
            fibonacci_max = int(input("Digite o valor máximo para a quantidade de números Fibonacci: "))
            magicos_min = int(input("Digite o valor mínimo para a quantidade de números mágicos: "))
            magicos_max = int(input("Digite o valor máximo para a quantidade de números mágicos: "))
            multiplos_3_min = int(input("Digite o valor mínimo para a quantidade de números múltiplos de 3: "))
            multiplos_3_max = int(input("Digite o valor máximo para a quantidade de números múltiplos de 3: "))
            return {
                'primos': (primos_min, primos_max),
                'fibonacci': (fibonacci_min, fibonacci_max),
                'magicos': (magicos_min, magicos_max),
                'multiplos_3': (multiplos_3_min, multiplos_3_max)
            }
        except ValueError:
            logging.warning("Erro: Por favor, insira um número válido.")

def aplicar_filtros(numeros, filtros):
    count_primos = len([num for num in numeros if num in NUMEROS_PRIMOS])
    count_fibonacci = len([num for num in numeros if num in NUMEROS_FIBONACCI])
    count_magicos = len([num for num in numeros if num in NUMEROS_MAGICOS])
    count_multiplos_3 = len([num for num in numeros if num in NUMEROS_MULTIPLOS_3])

    if not (filtros['primos'][0] <= count_primos <= filtros['primos'][1] and
            filtros['fibonacci'][0] <= count_fibonacci <= filtros['fibonacci'][1] and
            filtros['magicos'][0] <= count_magicos <= filtros['magicos'][1] and
            filtros['multiplos_3'][0] <= count_multiplos_3 <= filtros['multiplos_3'][1]):
        return False
    return True

def analise_estatistica_frequencia(dados):
    frequencia = {i: 0 for i in range(1, 26)}
    for linha in dados:
        numeros = map(int, linha[2:])
        for numero in numeros:
            frequencia[numero] += 1
    return frequencia

def modelos_regressao(dados):
    X = []
    y = []
    for linha in dados:
        numeros = list(map(int, linha[2:]))
        X.append(numeros)
        y.append(1)  # Placeholder for actual target variable
    model = LinearRegression()
    model.fit(X, y)
    return model

def clustering(dados):
    X = []
    for linha in dados:
        numeros = list(map(int, linha[2:]))
        X.append(numeros)
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(X)
    return kmeans

def simulacoes_monte_carlo(dados):
    # Implementar simulações de Monte Carlo
    pass

def calcular_media_numeros(dados, numeros_especiais):
    medias = []
    for linha in dados:
        numeros = list(map(int, linha[2:]))
        especiais = [num for num in numeros if num in numeros_especiais]
        if especiais:
            medias.append(np.mean(especiais))
    return int(np.mean(medias)) if medias else None

def gerar_numeros(frequencia, modelo_regressao, modelo_clustering, numeros_fixos, numeros_ausentes, qtd_miolo, dados, filtros):
    # Calcular médias para números especiais
    media_primos = calcular_media_numeros(dados, NUMEROS_PRIMOS)
    media_fibonacci = calcular_media_numeros(dados, NUMEROS_FIBONACCI)
    media_magicos = calcular_media_numeros(dados, NUMEROS_MAGICOS)
    media_multiplos_3 = calcular_media_numeros(dados, NUMEROS_MULTIPLOS_3)

    # Usar análise de frequência, modelo de regressão e modelo de clustering para gerar números
    numeros_gerados = set(numeros_fixos)  # Começar com números fixos

    # Lógica de exemplo: Selecionar números com base na frequência
    sorted_freq = sorted(frequencia.items(), key=lambda item: item[1], reverse=True)
    for num, freq in sorted_freq[:10]:  # Selecionar os 10 números mais frequentes
        numeros_gerados.add(num)

    # Remover números ausentes dos números gerados
    numeros_gerados.difference_update(numeros_ausentes)

    # Garantir que a entrada para a previsão tenha o número correto de características
    while len(numeros_gerados) < 15:
        num = random.randint(1, 25)
        if num not in numeros_ausentes:
            numeros_gerados.add(num)

    # Lógica de exemplo: Usar modelo de regressão para prever números
    predicted_numbers = modelo_regressao.predict([list(numeros_gerados)])
    for num in predicted_numbers:
        if num not in numeros_ausentes:
            numeros_gerados.add(int(num))

    # Garantir que o conjunto tenha exatamente 15 elementos
    if len(numeros_gerados) > 15:
        numeros_gerados = set(list(numeros_gerados)[:15])

    # Lógica de exemplo: Usar modelo de clustering para refinar a seleção
    cluster_labels = modelo_clustering.predict([list(numeros_gerados)])
    for label in set(cluster_labels):
        cluster_numbers = [num for num, lbl in zip(numeros_gerados, cluster_labels) if lbl == label]
        for num in cluster_numbers[:5]:
            if num not in numeros_ausentes:
                numeros_gerados.add(num)

    # Garantir que os números gerados incluam exatamente a quantidade especificada para o "miolo do cartão"
    miolo_cartao = {7, 8, 9, 12, 13, 14, 17, 18, 19}
    miolo_selecionado = miolo_cartao.intersection(numeros_gerados)
    while len(miolo_selecionado) < qtd_miolo:
        num = random.choice(list(miolo_cartao - miolo_selecionado))
        if num not in numeros_ausentes:
            numeros_gerados.add(num)
        miolo_selecionado = miolo_cartao.intersection(numeros_gerados)
    if len(miolo_selecionado) > qtd_miolo:
        miolo_selecionado = set(list(miolo_selecionado)[:qtd_miolo])

    # Adicionar médias de números especiais aos números gerados
    if media_primos and media_primos not in numeros_ausentes:
        numeros_gerados.add(media_primos)
    if media_fibonacci and media_fibonacci not in numeros_ausentes:
        numeros_gerados.add(media_fibonacci)
    if media_magicos and media_magicos not in numeros_ausentes:
        numeros_gerados.add(media_magicos)
    if media_multiplos_3 and media_multiplos_3 not in numeros_ausentes:
        numeros_gerados.add(media_multiplos_3)

    # Garantir que o conjunto tenha exatamente 15 elementos
    while len(numeros_gerados) > 15:
        numeros_gerados.pop()

    # Aplicar filtros de ranges de valor
    if not aplicar_filtros(numeros_gerados, filtros):
        return gerar_numeros(frequencia, modelo_regressao, modelo_clustering, numeros_fixos, numeros_ausentes, qtd_miolo, dados, filtros)

    # Adicionar rótulos aos números gerados e contar os números especiais
    labeled_numeros_gerados = []
    count_primos = count_fibonacci = count_magicos = count_multiplos_3 = 0
    for num in numeros_gerados:
        label = str(num)
        if num in NUMEROS_PRIMOS:
            label += 'p'
            count_primos += 1
        if num in NUMEROS_FIBONACCI:
            label += 'f'
            count_fibonacci += 1
        if num in NUMEROS_MAGICOS:
            label += 'm'
            count_magicos += 1
        if num in NUMEROS_MULTIPLOS_3:
            label += 'x'
            count_multiplos_3 += 1
        labeled_numeros_gerados.append(label)

    # Criar outro conjunto de números gerados sem rótulos
    numeros_gerados_sem_labels = [str(num) for num in numeros_gerados]

    # Obter os números rotulados no "miolo do cartão"
    miolo_labeled = [label for label in labeled_numeros_gerados if int(label.split('p')[0].split('f')[0].split('m')[0].split('x')[0]) in miolo_selecionado]

    return ', '.join(labeled_numeros_gerados), ', '.join(numeros_gerados_sem_labels), ', '.join(miolo_labeled), count_primos, count_fibonacci, count_magicos, count_multiplos_3

def apresentar_numeros(numeros_fixos, numeros_ausentes):
    print(f"Números fixos sorteados escolhidos: {numeros_fixos}")
    print(f"Números ausentes escolhidos: {numeros_ausentes}")

async def main():
    try:
        arquivo = 'jogos_copy.csv'
        dados = ler_dados_arquivo(arquivo)
        inicio, fim = obter_intervalo_concursos()
        qtd_fixos, qtd_ausentes = obter_quantidades()
        numeros_fixos = obter_numeros("fixo sorteado", qtd_fixos)
        numeros_ausentes = obter_numeros("ausente", qtd_ausentes)
        apresentar_numeros(numeros_fixos, numeros_ausentes)
        qtd_miolo = obter_miolo_cartao()
        filtros = obter_filtros()

        # Ask how many suggestions to generate
        qtd_sugestoes = int(input("Quantas sugestões de números você gostaria de gerar? "))
        print("\n\n")

        # Filtrar os dados para o intervalo especificado
        dados_intervalo = [linha for linha in dados if inicio <= int(linha[0]) <= fim]

        # Análise estatística de frequência
        frequencia = analise_estatistica_frequencia(dados_intervalo)

        # Modelos de regressão
        modelo_regressao = modelos_regressao(dados_intervalo)

        # Clustering
        modelo_clustering = clustering(dados_intervalo)

        # Simulações de Monte Carlo
        simulacoes_monte_carlo(dados_intervalo)

        # Collect suggestions
        suggestions = []

        # Gerar números com base nos filtros e algoritmos
        for i in range(qtd_sugestoes):
            if i > 0:
                print("\n---\n")
            numeros_gerados_com_labels, numeros_gerados_sem_labels, miolo_labeled, count_primos, count_fibonacci, count_magicos, count_multiplos_3 = gerar_numeros(frequencia, modelo_regressao, modelo_clustering, numeros_fixos, numeros_ausentes, qtd_miolo, dados_intervalo, filtros)
            print(f"Sugestão de números gerados PFMX: {numeros_gerados_com_labels}")
            print(f"Sugestão de números gerados: {numeros_gerados_sem_labels}")
            print(f"Números no miolo PFMX: {miolo_labeled}")
            print(f"Quantidade de primos: {count_primos}")
            print(f"Quantidade de Fibonacci: {count_fibonacci}")
            print(f"Quantidade de mágicos: {count_magicos}")
            print(f"Quantidade de múltiplos de 3: {count_multiplos_3}")
            suggestions.append(numeros_gerados_sem_labels)

        # Print suggestions as lottery tickets
        print("\nCartelas para levar para a loteria:")
        for suggestion in suggestions:
            print(suggestion)

    except ValueError as e:
        logging.exception(f"Erro de valor: {e}")
    except Exception as e:
        logging.exception(f"Erro inesperado: {e}")

if __name__ == '__main__':
    asyncio.run(main())