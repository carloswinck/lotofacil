import csv
from collections import Counter

# Funções para verificar propriedades dos números
def eh_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def eh_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or n == 0

def eh_par(n):
    return n % 2 == 0

def eh_impar(n):
    return n % 2 != 0

def eh_multiplo_de_3(n):
    return n % 3 == 0

def eh_magico(n):
    return n in {5, 6, 7, 12, 13, 14, 19, 20, 21}

# Função para rotular números
def rotular_numero(num):
    label = f'{num:02}'
    if eh_primo(num):
        label += 'p'
    if eh_fibonacci(num):
        label += 'f'
    if eh_magico(num):
        label += 'm'
    if eh_multiplo_de_3(num):
        label += 'x'
    return label

# Função para ler o arquivo CSV
def ler_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return list(reader)

# Função para calcular o resumo do último concurso
def calcular_resumo(ultimo_concurso, numeros_escolhidos, penultimo_concurso):
    ausentes = ' '.join(map(rotular_numero, [num for num in range(1, 26) if num not in ultimo_concurso]))
    sorteados = ' '.join(map(rotular_numero, ultimo_concurso))
    acertei = ' '.join(map(rotular_numero, [num for num in numeros_escolhidos if num in ultimo_concurso]))
    repetidos = ' '.join(map(rotular_numero, [num for num in penultimo_concurso if num in ultimo_concurso]))
    acertei_list = acertei.split()
    primos = ' '.join([num for num in acertei_list if 'p' in num])
    fibonacci = ' '.join([num for num in acertei_list if 'f' in num])
    magicos = ' '.join([num for num in acertei_list if 'm' in num])
    multiplos_de_3 = ' '.join([num for num in acertei_list if 'x' in num])
    miolo = ' '.join([num for num in acertei_list if int(num[:2]) in {7, 8, 9, 12, 13, 14, 17, 18, 19}])
    moldura = ' '.join([num for num in acertei_list if int(num[:2]) in {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}])

    primos_miolo = ' '.join([num for num in miolo.split() if 'p' in num])
    fibonacci_miolo = ' '.join([num for num in miolo.split() if 'f' in num])
    magicos_miolo = ' '.join([num for num in miolo.split() if 'm' in num])
    multiplos_de_3_miolo = ' '.join([num for num in miolo.split() if 'x' in num])

    return {
        'Sorteados': sorteados,
        'Acertei': acertei,
        'Repetidos': repetidos,
        'Ausentes': ausentes,
        'Primos': primos,
        'Fibonacci': fibonacci,
        'Mágicos': magicos,
        'Múltiplo de 3': multiplos_de_3,
        'Miolo': miolo,
        'Moldura': moldura,
        'Primos no miolo': primos_miolo,
        'Fibonacci no miolo': fibonacci_miolo,
        'Mágicos no miolo': magicos_miolo,
        'Múltiplo de 3 no miolo': multiplos_de_3_miolo,
        'Qtd. Acertos': len(acertei_list),
        'Qtd. Repetidos': len(repetidos.split()),
        'Qtd. Primos': len(primos.split()),
        'Qtd. Fibonacci': len(fibonacci.split()),
        'Qtd. Mágicos': len(magicos.split()),
        'Qtd. Múltiplo de 3': len(multiplos_de_3.split()),
        'Qtd. Miolo': len(miolo.split()),
        'Qtd. Moldura': len(moldura.split()),
        'Qtd. Primos no miolo': len(primos_miolo.split()),
        'Qtd. Fibonacci no miolo': len(fibonacci_miolo.split()),
        'Qtd. Mágicos no miolo': len(magicos_miolo.split()),
        'Qtd. Múltiplo de 3 no miolo': len(multiplos_de_3_miolo.split())
    }

# Função principal
def main():
    file_path = 'jogos.csv'
    linhas = ler_csv(file_path)

    # Ordenar os concursos pelo número do concurso e obter o último e penúltimo
    linhas.sort(key=lambda x: int(x[0]))
    ultimo_concurso = list(map(int, linhas[-1][2:]))
    penultimo_concurso = list(map(int, linhas[-2][2:]))
    numero_concurso = linhas[-1][0]
    data_concurso = linhas[-1][1]

    # Perguntar ao usuário quais números ele escolheu
    numeros_escolhidos = list(map(int, input("Quais números você escolheu? (separados por espaço): ").split()))

    # Calcular o resumo do último concurso
    resumo = calcular_resumo(ultimo_concurso, numeros_escolhidos, penultimo_concurso)

    # Gerar o relatório de resumo
    print(f"\nRESUMO DO CONCURSO {numero_concurso} DA DATA {data_concurso}:\n")
    print(f"Sorteados:".ljust(20) + resumo['Sorteados'])
    print(f"Acertei:".ljust(20) + resumo['Acertei'])
    print("---")
    print(f"Repetidos:".ljust(20) + resumo['Repetidos'])
    print(f"Ausentes:".ljust(20) + resumo['Ausentes'])
    print("---")
    print(f"Primos:".ljust(20) + resumo['Primos'])
    print(f"Fibonacci:".ljust(20) + resumo['Fibonacci'])
    print(f"Mágicos:".ljust(20) + resumo['Mágicos'])
    print(f"Múltiplo de 3:".ljust(20) + resumo['Múltiplo de 3'])
    print("---")
    print(f"Miolo:".ljust(20) + resumo['Miolo'])
    print(f"Moldura:".ljust(20) + resumo['Moldura'])
    print("---")
    print(f"Primos no miolo:".ljust(20) + resumo['Primos no miolo'])
    print(f"Fibonacci no miolo:".ljust(20) + resumo['Fibonacci no miolo'])
    print(f"Mágicos no miolo:".ljust(20) + resumo['Mágicos no miolo'])
    print(f"Múltiplo de 3 no miolo:".ljust(20) + resumo['Múltiplo de 3 no miolo'])
    print("---")
    print(f"Qtd. Acertos:".ljust(20) + str(resumo['Qtd. Acertos']))
    print(f"Qtd. Repetidos:".ljust(20) + str(resumo['Qtd. Repetidos']))
    print(f"Qtd. Primos:".ljust(20) + str(resumo['Qtd. Primos']))
    print(f"Qtd. Fibonacci:".ljust(20) + str(resumo['Qtd. Fibonacci']))
    print(f"Qtd. Mágicos:".ljust(20) + str(resumo['Qtd. Mágicos']))
    print(f"Qtd. Múltiplo de 3:".ljust(20) + str(resumo['Qtd. Múltiplo de 3']))
    print(f"Qtd. Miolo:".ljust(20) + str(resumo['Qtd. Miolo']))
    print(f"Qtd. Moldura:".ljust(20) + str(resumo['Qtd. Moldura']))
    print("---")
    print(f"Qtd. Primos no miolo:".ljust(20) + str(resumo['Qtd. Primos no miolo']))
    print(f"Qtd. Fibonacci no miolo:".ljust(20) + str(resumo['Qtd. Fibonacci no miolo']))
    print(f"Qtd. Mágicos no miolo:".ljust(20) + str(resumo['Qtd. Mágicos no miolo']))
    print(f"Qtd. Múltiplo de 3 no miolo:".ljust(20) + str(resumo['Qtd. Múltiplo de 3 no miolo']))

if __name__ == '__main__':
    main()