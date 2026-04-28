import pandas as pd

def analyze_detailed_duplicates(file_path):
    try:
        # Load CSV file
        # Fixed: Removed duplicated single quotes and added encoding and separator
        df = pd.read_csv(file_path, encoding='latin-1', sep=';')

        # Check if required columns exist
        if 'id' not in df.columns or 'paciente_id' not in df.columns:
            print("Error: Make sure the file contains the columns 'id' and 'paciente_id'.")
            return

        # Identify which paciente_id values appear more than once
        contagem = df['paciente_id'].value_counts()
        pacientes_repetidos = contagem[contagem > 1].index.tolist()

        if not pacientes_repetidos:
            print("No duplicate paciente_id values were found.")
            return

        print(f"{len(pacientes_repetidos)} patients with multiple records were found.\n")
        print("-" * 65)

        for p_id in pacientes_repetidos:
            # Filter all rows for this specific patient
            # df.index + 2 accounts for the header and pandas index starting at 0 (to match Excel)
            ocorrencias = df[df['paciente_id'] == p_id].copy()

            print(f"Patient ID: {p_id}")
            for idx, row in ocorrencias.iterrows():
                linha_excel = idx + 2  # +1 for index 0 and +1 for CSV header
                print(f"  -> Row {linha_excel} in file | Record ID: {row['id']}")
            print("-" * 65)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Fixed: Updated filename to full path
    nome_arquivo = '//content/Base de dados - PNTD - DPOC  - Estruturado(in).csv'
    analyze_detailed_duplicates(nome_arquivo)
