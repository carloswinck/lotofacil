import re

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a + b
    return b == n or n == 0

def is_multiple_of_3(n):
    return n % 3 == 0

def is_magic_number(n):
    return n in {5, 6, 7, 12, 13, 14, 19, 20, 21}

def analyze_numbers(numbers):
    prime_count = 0
    fibonacci_count = 0
    multiple_of_3_count = 0
    magic_number_count = 0
    even_count = 0
    odd_count = 0
    total_sum = 0

    for number in numbers:
        if is_prime(number):
            prime_count += 1
        if is_fibonacci(number):
            fibonacci_count += 1
        if is_multiple_of_3(number):
            multiple_of_3_count += 1
        if is_magic_number(number):
            magic_number_count += 1
        if number % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
        total_sum += number

    return {
        "Quantidade Primos": prime_count,
        "Quantidade Fibonacci": fibonacci_count,
        "quantidade Multiplos de 3": multiple_of_3_count,
        "quantidade Numeros Magicos": magic_number_count,
        "Quantidade Pares": even_count,
        "Quantidade Impares": odd_count,
        "Soma": total_sum
    }

# Solicitar entrada do usuário
user_input = input("Digite uma sequência de números separados por espaço: ")
sanitized_input = re.sub(r'[^0-9\s]', '', user_input)
numbers = list(map(int, sanitized_input.split()))
result = analyze_numbers(numbers)
print(result)