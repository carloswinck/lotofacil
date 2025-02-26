import pandas as pd

def inverter_jogos_ausentes(input_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file, header=None)

    # Invert the order of the rows
    df_invertido = df.iloc[::-1]

    # Calculate the absent numbers for each game
    all_numbers = set(range(1, 26))
    all_rows = []

    for index, row in df_invertido.iterrows():
        sorted_numbers = set(row[2:])
        absent_numbers = all_numbers - sorted_numbers
        row_data = f"{row[0]},{row[1]},{','.join(map(str, sorted(absent_numbers)))}"
        all_rows.append(row_data)

    # Reverse the order of all rows
    all_rows.reverse()

    # Print all rows in reversed order
    for row in all_rows:
        print(row)

# Specify the input file name
input_file = 'jogos_copy.csv'

# Call the function to invert the games and print the absent numbers
inverter_jogos_ausentes(input_file)