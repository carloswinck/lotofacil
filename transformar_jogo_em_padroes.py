import numpy as np

def transformar_numeros_em_padroes(numeros_escolhidos):
    todos_numeros = set(range(1, 26))
    numeros_sorteados = set(numeros_escolhidos)
    numeros_ausentes = todos_numeros - numeros_sorteados

    matriz = np.array([[f"{i:02}" for i in range(j, j + 5)] for j in range(1, 26, 5)], dtype=object)

    for numero in numeros_sorteados:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = 'XX'

    for numero in numeros_ausentes:
        linha = (numero - 1) // 5
        coluna = (numero - 1) % 5
        matriz[linha][coluna] = f"{numero:02}"

    formatted_string = "\n".join([" ".join(row) for row in matriz])
    return formatted_string

# Solicitar os 15 números ao usuário
numeros_escolhidos = []
print("Digite 15 números entre 1 e 25:")
while len(numeros_escolhidos) < 15:
    try:
        numero = int(input(f"Número {len(numeros_escolhidos) + 1}: ").strip())
        if 1 <= numero <= 25 and numero not in numeros_escolhidos:
            numeros_escolhidos.append(numero)
        else:
            print("Número inválido ou já escolhido. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")

# Imprimir a matriz formatada
matriz_tabulada = transformar_numeros_em_padroes(numeros_escolhidos)
print(matriz_tabulada)