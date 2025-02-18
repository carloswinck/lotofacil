import csv

def ler_dados_arquivo(arquivo):
    with open(arquivo, newline='') as csvfile:
        reader = csv.reader(csvfile)
        dados = [row for row in reader]
    return dados

def converter_para_binario(jogos, total_numeros=25):
    binarios = []
    for jogo in jogos:
        binario = ['0'] * total_numeros
        for num in jogo:
            binario[int(num) - 1] = '1'
        binarios.append(binario)
    return binarios

def agrupar_padroes(padrao):
    padrao_formatado = padrao[0]
    for i in range(1, len(padrao)):
        if padrao[i] != padrao[i - 1]:
            padrao_formatado += '.'
        padrao_formatado += padrao[i]
    return padrao_formatado

def contar_padroes(binarios, padroes, quantidade, concursos):
    contagem = []
    for coluna, padrao in enumerate(padroes):
        count = 0
        resultados_encontrados = []
        for linha in range(len(binarios) - quantidade):
            subpadrao = ''.join(['1' if binarios[linha + i][coluna] == '1' else '0' for i in range(quantidade)])
            if subpadrao == padrao:
                count += 1
                resultados_encontrados.append(binarios[linha][coluna])
        contagem.append((coluna + 1, agrupar_padroes(padrao), count, resultados_encontrados))
    return contagem

def imprimir_binarios(binarios, concursos):
    print("\nBinário de todos os concursos no intervalo:")
    for i, concurso in enumerate(concursos):
        binario_str = ''.join(binarios[i])
        print(f"Concurso {concurso}: {binario_str}")

def main():
    arquivo = 'jogos.csv'
    dados = ler_dados_arquivo(arquivo)

    # Ask for the interval of contests to analyze
    inicio = int(input("Digite o concurso inicial: "))
    fim = int(input("Digite o concurso final: "))

    # Ask for the pattern size (number of contests)
    quantidade = int(input("Digite o tamanho do padrão (quantidade de concursos): "))

    # Filter the data for the specified interval
    dados_intervalo = [linha for linha in dados if inicio <= int(linha[0]) <= fim]

    # Extract the contests and games, and convert to binary
    concursos = [str(linha[0]) for linha in dados_intervalo]
    jogos = [linha[2:] for linha in dados_intervalo]
    binarios = converter_para_binario(jogos)

    # Generate the pattern for each column based on the final contest minus the pattern size
    padroes = [''.join(['1' if binarios[-(fim - inicio + 1 - i)][coluna] == '1' else '0' for i in range(quantidade)]) for coluna in range(len(binarios[0]))]

    # Search for the pattern in all columns
    contagem = contar_padroes(binarios, padroes, quantidade, concursos)

    # Print the results for all columns in tabular format
    for coluna, padrao, count, resultados_encontrados in contagem:
        if count > 0:
            resultados_str = ' '.join(map(str, resultados_encontrados))
            coluna_str = f"{coluna:02d}"  # Add leading zero for columns 1 to 9
            count_str = f"{count:02d}"  # Add leading zero for counts 1 to 9
            print(f"Coluna {coluna_str:<10}{padrao:<20}{count_str} vezes     {resultados_str}")

    # Print the entire range in binary format
    imprimir_binarios(binarios, concursos)

if __name__ == '__main__':
    main()