import csv
from itertools import combinations
import time
import sys
import asyncio
import logging
import threading
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.error(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

@lru_cache(maxsize=None)
def calcular_acertos(numeros_sorteados, numeros_escolhidos):
    return len(numeros_sorteados & numeros_escolhidos)

def analisar_combinacao(linha, acertos_desejados, combinacoes_ausentes):
    try:
        resultados = []
        # Validate and convert the values to integers
        try:
            numeros_sorteados = set(map(int, linha[2:]))
            numero_concurso = int(linha[0])
        except ValueError as e:
            logging.error(f"Erro de valor ao converter linha: {linha} - {e}")
            return []

        for qtd_ausentes in combinacoes_ausentes:
            for combinacao in combinations(range(1, 26), qtd_ausentes):
                numeros_escolhidos = set(range(1, 26)) - set(combinacao)
                acertos = calcular_acertos(frozenset(numeros_sorteados), frozenset(numeros_escolhidos))
                if acertos in acertos_desejados:
                    resultados.append((qtd_ausentes, combinacao, acertos, numero_concurso))
        return resultados
    except Exception as e:
        logging.error(f"Erro ao analisar a combinação: {e}")
        return []

def spinner():
    while True:
        for cursor in '|/-\\':
            yield cursor

async def main():
    try:
        arquivo = 'jogos.csv'
        dados = ler_dados_arquivo(arquivo)
        acertos_desejados = {11, 12, 13, 14, 15}
        combinacoes_ausentes = [5, 6, 7, 8, 9]

        # Definir o intervalo de concursos para análise
        inicio = int(input("Digite o número do concurso inicial: "))
        fim = int(input("Digite o número do concurso final: "))

        if inicio > fim:
            logging.warning("Erro: O número do concurso inicial deve ser menor ou igual ao número do concurso final.")
            sys.exit(1)

        # Perguntar quantos melhores resultados o usuário deseja ver
        top_n = int(input("Quantos melhores resultados você gostaria de ver? "))

        # Filtrar os dados para o intervalo especificado
        dados_intervalo = [linha for linha in dados if inicio <= int(linha[0]) <= fim]
        args = [(linha, acertos_desejados, combinacoes_ausentes) for linha in dados_intervalo]

        start_time = time.time()  # Iniciar a contagem do tempo

        # Iniciar o spinner em uma thread separada
        spin = spinner()
        stop_spinner = False

        def spin_indicator():
            while not stop_spinner:
                sys.stdout.write(next(spin))
                sys.stdout.flush()
                time.sleep(0.1)
                sys.stdout.write('\b')

        spinner_thread = threading.Thread(target=spin_indicator)
        spinner_thread.start()

        # Executar as análises de forma assíncrona usando ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            resultados = await asyncio.gather(*(loop.run_in_executor(executor, analisar_combinacao, *arg) for arg in args))

        # Parar o spinner
        stop_spinner = True
        spinner_thread.join()

        end_time = time.time()  # Finalizar a contagem do tempo
        elapsed_time = end_time - start_time
        logging.info(f"Tempo de execução: {elapsed_time:.2f} segundos")

        # Contar a frequência de cada combinação
        combinacao_freq = {}
        for resultado in resultados:
            for res in resultado:
                qtd_ausentes, combinacao, acertos, numero_concurso = res
                key = (qtd_ausentes, combinacao, acertos)
                if key not in combinacao_freq:
                    combinacao_freq[key] = []
                combinacao_freq[key].append(numero_concurso)

        # Ordenar os resultados pela frequência e exibir os top_n resultados
        sorted_combinacoes = sorted(combinacao_freq.items(), key=lambda x: len(x[1]), reverse=True)
        top_resultados = sorted_combinacoes[:top_n]

        for (qtd_ausentes, combinacao, acertos), concursos in top_resultados:
            numeros = ', '.join(map(str, combinacao))
            concursos_str = ', '.join(map(str, concursos))
            logging.info(f"Qtd de ausentes: {qtd_ausentes}, Números ausentes: {numeros}, Acertos: {acertos}, Concursos: {concursos_str}")

    except ValueError as e:
        logging.error(f"Erro de valor: {e}")
    except Exception as e:
        logging.critical(f"Erro inesperado: {e}")

if __name__ == '__main__':
    asyncio.run(main())