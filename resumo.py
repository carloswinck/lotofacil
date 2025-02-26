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
def calcular_resumo(ultimo_concurso, numeros_escolhidos, penultimo_concurso, antepenultimo_concurso):
    numeros_ausentes = sorted([num for num in range(1, 26) if num not in ultimo_concurso])
    ausentes = ' '.join(map(rotular_numero, numeros_ausentes))
    sorteados = ' '.join(map(rotular_numero, ultimo_concurso))
    acertei = ' '.join(map(rotular_numero, [num for num in numeros_escolhidos if num in ultimo_concurso]))
    repetidos = ' '.join(map(rotular_numero, [num for num in ultimo_concurso if num in penultimo_concurso]))
    rept_dos_repetidos = ' '.join(map(rotular_numero, [num for num in penultimo_concurso if num in antepenultimo_concurso]))
    ausentes_penultimo = sorted([num for num in range(1, 26) if num not in penultimo_concurso])
    rept_dos_ausentes = ' '.join(map(rotular_numero, [num for num in numeros_ausentes if num in ausentes_penultimo]))
    acertei_list = acertei.split()

    def marcar_acertos(section):
        return ' '.join([num + '***' if num in acertei_list else num for num in section.split()])

    sorteados = marcar_acertos(sorteados)
    repetidos = marcar_acertos(repetidos)
    rept_dos_repetidos = marcar_acertos(rept_dos_repetidos)
    ausentes = marcar_acertos(ausentes)
    rept_dos_ausentes = marcar_acertos(rept_dos_ausentes)
    primos = marcar_acertos(' '.join([num for num in acertei_list if 'p' in num]))
    fibonacci = marcar_acertos(' '.join([num for num in acertei_list if 'f' in num]))
    magicos = marcar_acertos(' '.join([num for num in acertei_list if 'm' in num]))
    multiplos_de_3 = marcar_acertos(' '.join([num for num in acertei_list if 'x' in num]))
    miolo = ' '.join([num for num in sorteados.split() if int(num[:2]) in {7, 8, 9, 12, 13, 14, 17, 18, 19}])
    moldura = ' '.join([num for num in sorteados.split() if int(num[:2]) in {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}])

    primos_miolo = ' '.join([num for num in miolo.split() if 'p' in num])
    fibonacci_miolo = ' '.join([num for num in miolo.split() if 'f' in num])
    magicos_miolo = ' '.join([num for num in miolo.split() if 'm' in num])
    multiplos_de_3_miolo = ' '.join([num for num in miolo.split() if 'x' in num])

    primos_ausentes = ' '.join([num for num in ausentes.split() if 'p' in num])
    fibonacci_ausentes = ' '.join([num for num in ausentes.split() if 'f' in num])
    magicos_ausentes = ' '.join([num for num in ausentes.split() if 'm' in num])
    multiplos_de_3_ausentes = ' '.join([num for num in ausentes.split() if 'x' in num])
    miolo_ausentes = ' '.join([num for num in ausentes.split() if int(num[:2]) in {7, 8, 9, 12, 13, 14, 17, 18, 19}])
    moldura_ausentes = ' '.join([num for num in ausentes.split() if int(num[:2]) in {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}])

    primos_miolo_ausentes = ' '.join([num for num in miolo_ausentes.split() if 'p' in num])
    fibonacci_miolo_ausentes = ' '.join([num for num in miolo_ausentes.split() if 'f' in num])
    magicos_miolo_ausentes = ' '.join([num for num in miolo_ausentes.split() if 'm' in num])
    multiplos_de_3_miolo_ausentes = ' '.join([num for num in miolo_ausentes.split() if 'x' in num])

    soma = sum(ultimo_concurso)
    par_impar = f"{sum(eh_par(num) for num in ultimo_concurso)}/{sum(eh_impar(num) for num in ultimo_concurso)}"
    qtd_miolo = len(miolo.split())
    qtd_moldura = len(moldura.split())
    qtd_primos = sum(eh_primo(num) for num in ultimo_concurso)
    qtd_fibonacci = sum(eh_fibonacci(num) for num in ultimo_concurso)
    qtd_magicos = sum(eh_magico(num) for num in ultimo_concurso)
    qtd_multiplos_de_3 = sum(eh_multiplo_de_3(num) for num in ultimo_concurso)

    return {
        'Soma': soma,
        'Par/Impar': par_impar,
        'Sorteados': sorteados,
        'Acertei': acertei,
        'Repetidos': repetidos,
        'Rept. dos Repetidos': rept_dos_repetidos,
        'Ausentes': ausentes,
        'Rept. dos Ausentes': rept_dos_ausentes,
        'Primos': primos,
        'Fibonacci': fibonacci,
        'Mágicos': magicos,
        'Múltiplo de 3': multiplos_de_3,
        'Miolo': miolo,
        'Moldura': moldura,
        'Miolo dos ausentes': miolo_ausentes,
        'Moldura dos ausentes': moldura_ausentes,
        'Qtd. Primos no miolo': len(primos_miolo.split()),
        'Qtd. Fibonacci no miolo': len(fibonacci_miolo.split()),
        'Qtd. Mágicos no miolo': len(magicos_miolo.split()),
        'Qtd. Múltiplo de 3 no miolo': len(multiplos_de_3_miolo.split()),
        'Qtd. Acertos': len(acertei_list),
        'Qtd. Repetidos': len(repetidos.split()),
        'Qtd. Primos': qtd_primos,
        'Qtd. Fibonacci': qtd_fibonacci,
        'Qtd. Mágicos': qtd_magicos,
        'Qtd. Múltiplo de 3': qtd_multiplos_de_3,
        'Qtd. Miolo': qtd_miolo,
        'Qtd. Moldura': qtd_moldura,
        'Qtd. Primos nos ausentes': len(primos_ausentes.split()),
        'Qtd. Fibonacci nos ausentes': len(fibonacci_ausentes.split()),
        'Qtd. Mágicos nos ausentes': len(magicos_ausentes.split()),
        'Qtd. Múltiplo de 3 nos ausentes': len(multiplos_de_3_ausentes.split()),
        'Qtd. de ausentes no Miolo': len(miolo_ausentes.split()),
        'Qtd. de ausentes na Moldura': len(moldura_ausentes.split()),
        'Qtd. Primos no miolo dos ausentes': len(primos_miolo_ausentes.split()),
        'Qtd. Fibonacci no miolo dos ausentes': len(fibonacci_miolo_ausentes.split()),
        'Qtd. Mágicos no miolo dos ausentes': len(magicos_miolo_ausentes.split()),
        'Qtd. Múltiplo de 3 no miolo dos ausentes': len(multiplos_de_3_miolo_ausentes.split())
    }

# Função principal
def main():
    file_path = 'jogos_copy.csv'
    linhas = ler_csv(file_path)

    # Ordenar os concursos pelo número do concurso em ordem decrescente
    linhas.sort(key=lambda x: int(x[0]), reverse=True)

    try:
        # Perguntar ao usuário o intervalo de concursos que ele quer analisar
        concurso_inicio = input("Digite o número do concurso inicial: ").strip()
        concurso_fim = input("Digite o número do concurso final: ").strip()
        if not concurso_inicio.isdigit() or not concurso_fim.isdigit():
            print("Erro: Os números dos concursos devem ser inteiros.")
            return

        concurso_inicio = int(concurso_inicio)
        concurso_fim = int(concurso_fim)

        # Encontrar os índices dos concursos especificados
        index_inicio = next((i for i, linha in enumerate(linhas) if int(linha[0]) == concurso_inicio), None)
        index_fim = next((i for i, linha in enumerate(linhas) if int(linha[0]) == concurso_fim), None)
        if index_inicio is None or index_fim is None:
            print("Erro: Concurso não encontrado.")
            return

        # Determinar a ordem do intervalo
        if index_inicio > index_fim:
            indices = range(index_inicio, index_fim - 1, -1)
        else:
            indices = range(index_inicio, index_fim + 1)

        for i in indices:
            # Obter os concursos especificados
            ultimo_concurso = list(map(int, linhas[i][2:]))
            penultimo_concurso = list(map(int, linhas[i + 1][2:])) if i + 1 < len(linhas) else []
            x_antepenultimo_concurso = list(map(int, linhas[i + 2][2:])) if i + 2 < len(linhas) else []
            antepenultimo_concurso = [num for num in x_antepenultimo_concurso if num in ultimo_concurso]

            numero_concurso = linhas[i][0]
            data_concurso = linhas[i][1]

            # Perguntar ao usuário se ele quer passar os números sorteados ou os números ausentes
            escolha = input("Você quer passar os números sorteados (1) ou os números ausentes (2)? ").strip()
            if not escolha:
                escolha = '1'
            if escolha not in ['1', '2']:
                print("Erro: Escolha inválida. Digite '1' para sorteados ou '2' para ausentes.")
                continue

            if escolha == '1':
                numeros_escolhidos = input("Quais números você escolheu? (separados por espaço): ").strip()
                if not numeros_escolhidos:
                    numeros_escolhidos = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15"
                try:
                    numeros_escolhidos = list(map(int, numeros_escolhidos.split()))
                except ValueError:
                    print("Erro: Todos os números devem ser inteiros.")
                    continue

                numeros_ausentes = None

            elif escolha == '2':
                numeros_ausentes = input("Quais números serão ausentes? (separados por espaço): ").strip()
                if not numeros_ausentes:
                    print("Erro: Você deve digitar os números ausentes.")
                    continue

                try:
                    numeros_ausentes = list(map(int, numeros_ausentes.split()))
                except ValueError:
                    print("Erro: Todos os números devem ser inteiros.")
                    continue

                if len(numeros_ausentes) != 10:
                    print("Erro: Você deve digitar exatamente 10 números ausentes.")
                    continue

                numeros_escolhidos = [num for num in range(1, 26) if num not in numeros_ausentes]

            # Calcular o resumo do último concurso
            resumo = calcular_resumo(ultimo_concurso, numeros_escolhidos, penultimo_concurso, antepenultimo_concurso)

            # Gerar o relatório de resumo
            print(f"\nRESUMO DO CONCURSO {numero_concurso} DA DATA {data_concurso}:\n")
            print(f"Escolhidos:".ljust(40) + ' '.join(map(str, numeros_escolhidos)))
            print("---")
            print(f"Soma:".ljust(40) + str(resumo['Soma']))
            print(f"Par/Impar:".ljust(40) + resumo['Par/Impar'])
            print("---")
            print(f"Sorteados:".ljust(40) + resumo['Sorteados'])
            print(f"Acertei:".ljust(40) + resumo['Acertei'])
            print("---")
            print(f"Repetidos:".ljust(40) + resumo['Repetidos'])
            print(f"Rept. dos Repetidos:".ljust(40) + resumo['Rept. dos Repetidos'])
            print("---")
            print(f"Primos:".ljust(40) + str(resumo['Qtd. Primos']))
            print(f"Fibonacci:".ljust(40) + str(resumo['Qtd. Fibonacci']))
            print(f"Mágicos:".ljust(40) + str(resumo['Qtd. Mágicos']))
            print(f"Múltiplo de 3:".ljust(40) + str(resumo['Qtd. Múltiplo de 3']))
            print("---")
            print(f"Miolo:".ljust(40) + f"{resumo['Miolo']}")
            print(f"Moldura:".ljust(40) + f"{resumo['Moldura']}")
            print("---")
            print(f"Primos no miolo:".ljust(40) + str(resumo['Qtd. Primos no miolo']))
            print(f"Fibonacci no miolo:".ljust(40) + str(resumo['Qtd. Fibonacci no miolo']))
            print(f"Mágicos no miolo:".ljust(40) + str(resumo['Qtd. Mágicos no miolo']))
            print(f"Múltiplo de 3 no miolo:".ljust(40) + str(resumo['Qtd. Múltiplo de 3 no miolo']))
            print("---")
            print(f"Qtd. Acertos:".ljust(40) + str(resumo['Qtd. Acertos']))
            print(f"Qtd. Repetidos:".ljust(40) + str(resumo['Qtd. Repetidos']))
            print(f"Qtd. Primos:".ljust(40) + str(resumo['Qtd. Primos']))
            print(f"Qtd. Fibonacci:".ljust(40) + str(resumo['Qtd. Fibonacci']))
            print(f"Qtd. Mágicos:".ljust(40) + str(resumo['Qtd. Mágicos']))
            print(f"Qtd. Múltiplo de 3:".ljust(40) + str(resumo['Qtd. Múltiplo de 3']))
            print(f"Qtd. Miolo:".ljust(40) + str(resumo['Qtd. Miolo']))
            print(f"Qtd. Moldura:".ljust(40) + str(resumo['Qtd. Moldura']))
            print("---")
            print(f"Ausentes:".ljust(40) + resumo['Ausentes'])
            print(f"Rept. dos Ausentes:".ljust(40) + resumo['Rept. dos Ausentes'])
            print("---")
            print(f"Miolo dos ausentes:".ljust(40) + f"{resumo['Miolo dos ausentes']}")
            print(f"Moldura dos ausentes:".ljust(40) + f"{resumo['Moldura dos ausentes']}")
            print("---")
            print(f"Qtd. Primos nos ausentes:".ljust(40) + str(resumo['Qtd. Primos nos ausentes']))
            print(f"Qtd. Fibonacci nos ausentes:".ljust(40) + str(resumo['Qtd. Fibonacci nos ausentes']))
            print(f"Qtd. Mágicos nos ausentes:".ljust(40) + str(resumo['Qtd. Mágicos nos ausentes']))
            print(f"Qtd. Múltiplo de 3 nos ausentes:".ljust(40) + str(resumo['Qtd. Múltiplo de 3 nos ausentes']))
            print(f"Qtd. de ausentes no Miolo:".ljust(40) + str(resumo['Qtd. de ausentes no Miolo']))
            print(f"Qtd. de ausentes na Moldura:".ljust(40) + str(resumo['Qtd. de ausentes na Moldura']))
            print("---")
            print(f"Qtd. Primos no miolo dos ausentes:".ljust(40) + str(resumo['Qtd. Primos no miolo dos ausentes']))
            print(f"Qtd. Fibonacci no miolo dos ausentes:".ljust(40) + str(resumo['Qtd. Fibonacci no miolo dos ausentes']))
            print(f"Qtd. Mágicos no miolo dos ausentes:".ljust(40) + str(resumo['Qtd. Mágicos no miolo dos ausentes']))
            print(f"Qtd. Múltiplo de 3 no miolo dos ausentes:".ljust(40) + str(resumo['Qtd. Múltiplo de 3 no miolo dos ausentes']))

            # Adicionar uma linha dupla antes do próximo concurso
            print("\n" + "-"*50 + "\n")
    except KeyboardInterrupt:
        print("\nSaindo da aplicação.")

if __name__ == '__main__':
    main()