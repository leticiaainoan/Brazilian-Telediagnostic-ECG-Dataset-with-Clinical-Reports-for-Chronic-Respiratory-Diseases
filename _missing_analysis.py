import pandas as pd
import io

try:
    df = pd.read_csv('/content/Base de dados - PNTD - DPOC  - processo de estruturação(in) (3).csv', encoding='latin-1', sep=';')
    print("File loaded successfully!")
except FileNotFoundError:
    print("ERROR: File not found. Please make sure the filename is correct and that it has been uploaded to the Colab environment.")
    exit()
except UnicodeDecodeError as e:
    print(f"Decoding ERROR: Unable to read the file with the specified encoding. Try another encoding. Details: {e}")
    exit()
except pd.errors.ParserError as e:
    print(f"Parser ERROR: There was a problem reading the CSV file. This may indicate an incorrect delimiter or malformed lines. Details: {e}")
    print("Try checking the file manually or experimenting with other delimiters such as tab ('\\t').")
    exit()

num_colunas = df.shape[1]
print(f"\n--- 1. Total Number of Columns ---")
print(f"The dataset contains {num_colunas} columns.")


nomes_colunas = df.columns.tolist()
print(f"\n--- 2. Column Names ---")
print(nomes_colunas)

print(f"\n--- 3. and 4. Missing Values Analysis ---")
total_linhas = len(df)
analise_colunas = []

for col in df.columns:
    preenchidos = df[col].count()
    ausentes = df[col].isnull().sum()
    percentual_ausente = (ausentes / total_linhas) * 100
    incompleta = ausentes > 0

    analise_colunas.append({
        'Column': col,
        'Filled': preenchidos,
        'Missing': ausentes,
        '% Missing': f"{percentual_ausente:.2f}%",
        'Incomplete': 'Yes' if incompleta else 'No'
    })

df_analise = pd.DataFrame(analise_colunas)
df_analise_ordenada = df_analise.sort_values(by=['Incomplete', 'Missing'], ascending=[False, False])

print("\nDetailed Column Completeness Table:")
print(df_analise_ordenada.to_markdown(index=False))

colunas_incompletas = df_analise_ordenada[df_analise_ordenada['Incomplete'] == 'Yes']['Column'].tolist()

print(f"\nIncomplete Columns (with Missing Values):")
if colunas_incompletas:
    print(colunas_incompletas)
else:
    print("No columns contain missing values. The dataset is complete.")
