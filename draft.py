import numpy as np
import pandas as pd
from collections import Counter
from itertools import combinations

# Helper functions
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def fibonacci_sequence(n):
    fib = [0, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    return set(fib)

def contar_combinacoes_ausentes(concursos):
    todos_numeros = set(range(1, 26))
    contador_combinacoes = {n: Counter() for n in range(3, 9)}
    for concurso in concursos:
        numeros_concurso = set(concurso)
        ausentes = todos_numeros - numeros_concurso
        for n in range(3, 9):
            for combinacao in combinations(ausentes, n):
                contador_combinacoes[n][combinacao] += 1
    return contador_combinacoes

def main():
    df = pd.read_csv('jogos.csv')
    concurso_inicio = int(input("Digite o número do concurso inicial: ").strip())
    concurso_fim = int(input("Digite o número do concurso final: ").strip())
    df = df[(df['jogo'] >= concurso_inicio) & (df['jogo'] <= concurso_fim)]
    concursos = df.iloc[:, 2:].values.tolist()

    # Prime numbers and Fibonacci numbers
    primes = [i for i in range(1, 26) if is_prime(i)]
    fibonacci = fibonacci_sequence(25)

    # Count occurrences
    contador_ausentes = contar_combinacoes_ausentes(concursos)

    # Generate report
    print("Relatório de Análise de Jogos:")
    print("\nNúmeros Primos:", primes)
    print("\nSequência de Fibonacci até 25:", sorted(fibonacci))

    for n in range(3, 9):
        combinacao_mais_ausente = contador_ausentes[n].most_common(1)
        print(f"\nA combinação de {n} números mais ausente em todos os concursos é:")
        for combinacao, contagem in combinacao_mais_ausente:
            print(f"Combinação {combinacao} ausente {contagem} vezes")

if __name__ == '__main__':
    main()