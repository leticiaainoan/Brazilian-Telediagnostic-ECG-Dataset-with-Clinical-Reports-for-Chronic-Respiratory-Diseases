import json
import matplotlib.pyplot as plt
import numpy as np

# 1. Path to your JSON file (Example with UUID in the filename)
arquivo_json = "ecg-00cb0d50-8837-11ec-a9fe-bf4589f8c682.json"

# 2. Load and extract data from JSON
with open(arquivo_json, 'r', encoding='utf-8') as f:
    dados_completos = json.load(f)

# Extracting the list of leads (adjusted to your JSON structure)
# Your JSON has a list 'conteudosExame', we take the first item [0]
exame = dados_completos["conteudosExame"][0]
derivacoes_lista = exame["derivacoes"]

print(f"Exam loaded. Total number of leads: {len(derivacoes_lista)}")


#  PLOT OF ALL LEADS


n_cols = 3  
n_rows = int(np.ceil(len(derivacoes_lista) / n_cols))

plt.figure(figsize=(15, 10))

for i, deriv in enumerate(derivacoes_lista):
    nome_deriv = deriv["descricao"]
    sinal = deriv["amostra"] # In the JSON, 'amostra' is already a list of numbers

    ax = plt.subplot(n_rows, n_cols, i + 1)
    # Plot the first 2000 samples
    ax.plot(sinal[:2000], linewidth=1, color='#d62728') # ECG-style red

    ax.set_title(f"{nome_deriv}", fontsize=10, fontweight='bold')

    # Graph paper-style aesthetics
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("#fffafa")
    ax.grid(True, which='major', color='#ffcccc', linewidth=0.5)
    ax.minorticks_on()
    ax.grid(True, which='minor', color='#ffeeee', linewidth=0.2)

plt.suptitle(f"ECG Signals - File: {arquivo_json}", fontsize=16)
plt.tight_layout()
plt.show()


# HIGHLIGHT OF LEAD DII


# Specifically search for DII within the list
dados_dii = next((d["amostra"] for d in derivacoes_lista if d["descricao"] == "DII"), None)

if dados_dii:
    plt.figure(figsize=(15, 4))
    plt.plot(dados_dii[:2000], linewidth=1.2, color='black')

    plt.title("Highlight: Lead DII", fontsize=14)
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")

    plt.grid(True, color='#e0e0e0')
    plt.minorticks_on()
    plt.show()
else:
    print("Warning: Lead DII not found in this file.")
