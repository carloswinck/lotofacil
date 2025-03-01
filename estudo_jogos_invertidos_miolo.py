import csv
from collections import Counter
from itertools import combinations
from collections import defaultdict
import sys

def ler_dados_arquivo(arquivo):
    with open(arquivo, mode='r', newline='', encoding='utf-8') as file:
        return list(csv.reader(file))

def calcular_diferencas(sequencias):
    diferencas = defaultdict(list)
    for num, concursos in sequencias.items():
        if len(concursos) > 1:
            seq = []
            for i in range(1, len(concursos)):
                diff = concursos[i-1] - concursos[i]
                seq.append(f"{concursos[i-1]} - {concursos[i]} (Qtd {diff})")
            diferencas[num] = seq
    return diferencas

# Função para gerar o relatório de sequências
def gerar_relatorio_sequencias(dados, miolo_numeros):
    sequencias = defaultdict(list)  # Dicionário para armazenar as sequências
    ultima_ocorrencia = {num: -1 for num in miolo_numeros}  # Última ocorrência de cada número
    contagem_sequencias = {num: 0 for num in miolo_numeros}  # Contagem de sequências para cada número
    maior_sequencia = {num: (0, 0, 0) for num in miolo_numeros}  # (tamanho, inicio, fim)

    # Itera sobre cada linha dos dados
    for linha in dados:
        concurso = int(linha[0])  # Número do concurso
        numeros_jogo = set(map(int, linha[2:]))  # Números sorteados no concurso
        for num in miolo_numeros:
            if num in numeros_jogo:
                # Se o número está no jogo atual, verifica se continua a sequência ou inicia uma nova
                if ultima_ocorrencia[num] == -1 or ultima_ocorrencia[num] == concurso + 1:
                    contagem_sequencias[num] += 1  # Continua a sequência
                else:
                    # Adiciona a sequência atual à lista de sequências
                    sequencias[num].append((ultima_ocorrencia[num], contagem_sequencias[num]))
                    # Atualiza a maior sequência se necessário
                    if contagem_sequencias[num] > maior_sequencia[num][0]:
                        maior_sequencia[num] = (contagem_sequencias[num], ultima_ocorrencia[num] - contagem_sequencias[num] + 1, ultima_ocorrencia[num])
                    contagem_sequencias[num] = 1  # Inicia uma nova sequência
                ultima_ocorrencia[num] = concurso  # Atualiza a última ocorrência
            else:
                # Se o número não está no jogo atual, finaliza a sequência atual
                if contagem_sequencias[num] > 0:
                    sequencias[num].append((ultima_ocorrencia[num], contagem_sequencias[num]))
                    # Atualiza a maior sequência se necessário
                    if contagem_sequencias[num] > maior_sequencia[num][0]:
                        maior_sequencia[num] = (contagem_sequencias[num], ultima_ocorrencia[num] - contagem_sequencias[num] + 1, ultima_ocorrencia[num])
                    contagem_sequencias[num] = 0  # Reseta a contagem de sequência

    # Adiciona as sequências restantes
    for num in miolo_numeros:
        if contagem_sequencias[num] > 0:
            sequencias[num].append((ultima_ocorrencia[num], contagem_sequencias[num]))
            # Atualiza a maior sequência se necessário
            if contagem_sequencias[num] > maior_sequencia[num][0]:
                maior_sequencia[num] = (contagem_sequencias[num], ultima_ocorrencia[num] - contagem_sequencias[num] + 1, ultima_ocorrencia[num])

    return sequencias, maior_sequencia

def main():
    arquivo = 'jogos_invertidos.csv'
    dados = ler_dados_arquivo(arquivo)
    miolo_numeros = {7, 8, 9, 12, 13, 14, 17, 18, 19}
    jogos = []
    contador_numeros = Counter()

    # Define sets for prime, Fibonacci, and multiples of 3
    primos = {7, 13, 17, 19}
    fibonacci = {8, 13}
    multiplos_3 = {9, 12, 18}

    # Counters for averages
    total_primos = total_fibonacci = total_multiplos_3 = 0

    for linha in dados:
        numeros_jogo = set(map(int, linha[2:]))
        jogo = numeros_jogo & miolo_numeros
        if len(jogo) > 1:
            jogos.append((linha[0], sorted(jogo)))
            contador_numeros.update(jogo)
            total_primos += len(jogo & primos)
            total_fibonacci += len(jogo & fibonacci)
            total_multiplos_3 += len(jogo & multiplos_3)

    combinacoes = [tuple(sorted(jogo[1])) for jogo in jogos]
    contador = Counter(combinacoes)
    combinacoes_ordenadas = contador.most_common()

    print("\nCombinações mais frequentes:")
    for combinacao, frequencia in combinacoes_ordenadas:
        concursos = [jogo[0] for jogo in jogos if tuple(sorted(jogo[1])) == combinacao]
        print(f"Combinação: {combinacao}, Frequência: {frequencia}, Concursos: {', '.join(concursos)}")

    combinacoes_ordenadas = sorted(contador.items(), key=lambda x: (-len(x[0]), x[0]))

    print("\nCombinações ordenadas por quantidade de números:")
    for combinacao, frequencia in combinacoes_ordenadas:
        if frequencia > 1:
            print(f"Combinação: {combinacao}, Frequência: {frequencia}")

    print("\nQuantidade de cada número do miolo:")
    for numero, quantidade in contador_numeros.most_common():
        print(f"Número: {numero:02}, Quantidade: {quantidade}")

    padroes = Counter()
    for linha in dados:
        numeros_jogo = set(map(int, linha[2:]))
        jogo = numeros_jogo & miolo_numeros
        card = [f"{num:02}" if num in jogo else "XX" for num in [7, 8, 9, 12, 13, 14, 17, 18, 19]]
        linhas = [" ".join(card[i:i+3]) for i in range(0, 9, 3)]
        for comb in combinations(enumerate(linhas, 1), 2):
            (idx1, linha1), (idx2, linha2) = comb
            padroes[((linha1, idx1), (linha2, idx2))] += 1

    print("\nPadrões que se repetem mais de 5 vezes:")
    for padrao, frequencia in sorted(padroes.items(), key=lambda x: x[1], reverse=True):
        if frequencia > 5:
            (linha1, idx1), (linha2, idx2) = padrao
            print(f"Frequência: {frequencia}\n{linha1} - Linha {idx1}\n{linha2} - Linha {idx2}")

    # Calculate and print averages per game
    total_jogos = len(jogos)
    media_primos = total_primos / total_jogos
    media_fibonacci = total_fibonacci / total_jogos
    media_multiplos_3 = total_multiplos_3 / total_jogos

    print(f"\nMédias dos jogos:")
    print(f"Média de primos por jogo: {media_primos:.2f}")
    print(f"Média de Fibonacci por jogo: {media_fibonacci:.2f}")
    print(f"Média de múltiplos de 3 por jogo: {media_multiplos_3:.2f}")

    # Calculate and print most frequent combinations of primes, Fibonacci, and multiples of 3
    combinacoes_primos = Counter()
    combinacoes_fibonacci = Counter()
    combinacoes_multiplos_3 = Counter()

    for jogo in jogos:
        numeros_jogo = set(jogo[1])
        combinacoes_primos[tuple(sorted(numeros_jogo & primos))] += 1
        combinacoes_fibonacci[tuple(sorted(numeros_jogo & fibonacci))] += 1
        combinacoes_multiplos_3[tuple(sorted(numeros_jogo & multiplos_3))] += 1

    print("\nCombinações de primos mais frequentes:")
    for combinacao, frequencia in combinacoes_primos.most_common():
        concursos = [jogo[0] for jogo in jogos if tuple(sorted(set(jogo[1]) & primos)) == combinacao]
        print(f"Combinação: {combinacao}, Frequência: {frequencia}, Concursos: {', '.join(concursos)}")

    print("\nCombinações de Fibonacci mais frequentes:")
    for combinacao, frequencia in combinacoes_fibonacci.most_common():
        concursos = [jogo[0] for jogo in jogos if tuple(sorted(set(jogo[1]) & fibonacci)) == combinacao]
        print(f"Combinação: {combinacao}, Frequência: {frequencia}, Concursos: {', '.join(concursos)}")

    print("\nCombinações de múltiplos de 3 mais frequentes:")
    for combinacao, frequencia in combinacoes_multiplos_3.most_common():
        concursos = [jogo[0] for jogo in jogos if tuple(sorted(set(jogo[1]) & multiplos_3)) == combinacao]
        print(f"Combinação: {combinacao}, Frequência: {frequencia}, Concursos: {', '.join(concursos)}")

    # Calculate and print most frequent combinations of primes, Fibonacci, and multiples of 3 together
    combinacoes_todos = Counter()

    for jogo in jogos:
        numeros_jogo = set(jogo[1])
        combinacao = tuple(sorted(numeros_jogo & (primos | fibonacci | multiplos_3)))
        combinacoes_todos[combinacao] += 1

    print("\nCombinações de primos, Fibonacci e múltiplos de 3 mais frequentes:")
    for combinacao, frequencia in combinacoes_todos.most_common():
        concursos = [jogo[0] for jogo in jogos if tuple(sorted(set(jogo[1]) & (primos | fibonacci | multiplos_3))) == combinacao]
        print(f"Combinação: {combinacao}, Frequência: {frequencia}, Concursos: {', '.join(concursos)}")

    # Calculate and print the number of repeated numbers between consecutive games
    repeticoes = Counter()
    for i in range(len(jogos) - 1):
        jogo_atual = set(jogos[i][1])
        proximo_jogo = set(jogos[i + 1][1])
        repetidos = len(jogo_atual & proximo_jogo)
        repeticoes[repetidos] += 1

    print("\nRepetições de números entre jogos consecutivos:")
    for repetidos, frequencia in repeticoes.most_common():
        print(f"Repetiu {repetidos} números = {frequencia} vezes")

    # Calculate and print the number of times a certain number of numbers from a set of 9 appeared
    numeros_nove = {7, 8, 9, 12, 13, 14, 17, 18, 19}
    repeticoes_nove = Counter()
    for jogo in jogos:
        numeros_jogo = set(jogo[1])
        repetidos = len(numeros_jogo & numeros_nove)
        repeticoes_nove[repetidos] += 1

    print("\nQuantidade de números do conjunto de 9 que apareceram:")
    for repetidos, frequencia in repeticoes_nove.most_common():
        print(f"{repetidos} números dos 9 apareceram = {frequencia} vezes")

    # Calculate most frequent combinations of primes, Fibonacci, and multiples of 3 together
    combinacoes_todos = Counter()
    for jogo in jogos:
        numeros_jogo = set(jogo[1])
        combinacao = tuple(sorted(numeros_jogo & (primos | fibonacci | multiplos_3)))
        combinacoes_todos[combinacao] += 1

    # Calculate the number of times a certain number of numbers from a set of 9 appeared
    numeros_nove = {7, 8, 9, 12, 13, 14, 17, 18, 19}
    repeticoes_nove = Counter()
    for jogo in jogos:
        numeros_jogo = set(jogo[1])
        repetidos = len(numeros_jogo & numeros_nove)
        repeticoes_nove[repetidos] += 1

    contagem_repeticoes = {num: 0 for num in miolo_numeros}
    repeticoes = {num: 0 for num in miolo_numeros}
    numeros_zerados = []

    # Get the latest contest numbers
    numeros_ultimo_jogo = set(map(int, dados[0][2:]))

    # Treat absent numbers in the latest contest as 0
    for num in miolo_numeros:
        if num not in numeros_ultimo_jogo:
            contagem_repeticoes[num] = 0

    numeros_jogo_anterior = numeros_ultimo_jogo

    for linha in dados:
        numeros_jogo_atual = set(map(int, linha[2:]))
        for num in miolo_numeros:
            if num in numeros_jogo_atual and num not in numeros_zerados:
                if num in numeros_ultimo_jogo and num in numeros_ultimo_jogo & numeros_jogo_anterior:
                    repeticoes[num] += 1
                else:
                    if num not in numeros_zerados:
                        numeros_zerados.append(num)
                        if len(numeros_zerados) == 9:
                            break

        numeros_jogo_anterior = numeros_jogo_atual

    # Update the count for numbers that are still being repeated
    for num in miolo_numeros:
        if repeticoes[num] > 0:
            contagem_repeticoes[num] = repeticoes[num]

    print("\nNúmeros do centro que estão se repetindo desde a última vez que não apareceram:")
    for num in sorted(miolo_numeros):
        print(f"Número: {num:02}, Quantidade: {contagem_repeticoes[num]}")

    sequencias, maior_sequencia = gerar_relatorio_sequencias(dados, miolo_numeros)

    print("\nMaior Sequência de Cada Número:")
    for num in sorted(miolo_numeros):
        tamanho, inicio, fim = maior_sequencia[num]
        print(f"Número: {num:02}, Maior Sequência: {tamanho}, Intervalo: {inicio} - {fim}")

    # Imprime o relatório de sequências seguidas
    print("\nRelatório de Sequências Seguidas:")
    for num in sorted(miolo_numeros):
        sequencia_str = f"Número: {num:02}"
        ultima_ocorrencia = None
        inicio_sequencia = None
        tamanho_sequencia = 0
        for linha in dados:
            concurso = int(linha[0])
            numeros_jogo = set(map(int, linha[2:]))
            if num in numeros_jogo:
                if ultima_ocorrencia is None or ultima_ocorrencia == concurso + 1:
                    # Continua a sequência
                    if inicio_sequencia is None:
                        inicio_sequencia = concurso
                    tamanho_sequencia += 1
                else:
                    # Quebra a sequência e inicia uma nova
                    sequencia_str += f", {inicio_sequencia}[{tamanho_sequencia}]"
                    inicio_sequencia = concurso
                    tamanho_sequencia = 1
                ultima_ocorrencia = concurso
            else:
                if ultima_ocorrencia is not None:
                    # Quebra a sequência
                    sequencia_str += f", {inicio_sequencia}[{tamanho_sequencia}]"
                    ultima_ocorrencia = None
                    inicio_sequencia = None
                    tamanho_sequencia = 0
        if ultima_ocorrencia is not None:
            # Adiciona a última sequência
            sequencia_str += f", {inicio_sequencia}[{tamanho_sequencia}]"
        print(sequencia_str)

if __name__ == '__main__':
    # Redireciona a saída padrão para um arquivo
    sys.stdout = open('output.txt', 'w', encoding='utf-8')
    main()
    # Restaura a saída padrão
    sys.stdout.close()
    sys.stdout = sys.__stdout__