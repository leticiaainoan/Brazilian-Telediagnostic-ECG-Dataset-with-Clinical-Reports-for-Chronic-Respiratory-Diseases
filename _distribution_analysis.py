import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown

# --- Initial Settings ---
# Make sure the filename below is exactly the one you uploaded to Colab
FILE_PATH = "/content/Base de dados - PNTD - DPOC  - Estruturado(in) (1).csv"
SEPARATOR = ';'
ENCODING = 'latin-1'

# --- 1. Data Loading ---
try:
    df = pd.read_csv(FILE_PATH, sep=SEPARATOR, encoding=ENCODING)
    print(f"Data loaded successfully! Total of {len(df)} records.")
except FileNotFoundError:
    print(f"ERROR: The file '{FILE_PATH}' was not found in the Colab environment.")
    exit()

# --- 2. Generate Distribution Table by State and Gender ---
# Rename columns to facilitate manipulation
df = df.rename(columns={'estabelecimento_municipio_uf_descricao': 'State', 'paciente_sexo': 'Gender'})

# Group by State and Gender and count occurrences
tabela_estado_sexo = df.groupby(['State', 'Gender']).size().unstack(fill_value=0)

# Add total column per row and sort
tabela_estado_sexo['Total'] = tabela_estado_sexo.sum(axis=1)
tabela_estado_sexo = tabela_estado_sexo.sort_values(by='Total', ascending=False)

# Format table for display
tabela_final = tabela_estado_sexo.reset_index()
tabela_final.columns.name = None

# --- NEW: Calculate overall total for each column ---
# Sum numeric columns (F, M, and Total)
total_geral = tabela_final[['F', 'M', 'Total']].sum()
total_geral['State'] = '**GRAND TOTAL**'

# Append total row to the DataFrame
tabela_final = pd.concat([tabela_final, pd.DataFrame([total_geral])], ignore_index=True)

print("\n" + "="*50)
print("Distribution Table of Exams by State and Gender")
print("="*50)
display(Markdown(tabela_final.to_markdown(index=False)))

# --- 3. Generate Distribution Plot by State ---
contagem_estados = df["State"].value_counts().reset_index()
contagem_estados.columns = ["State", "Frequency"]
contagem_estados = contagem_estados.sort_values(by="Frequency", ascending=False)

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 8))

grafico = sns.barplot(
    x="Frequency",
    y="State",
    data=contagem_estados,
    palette="viridis",
    hue="State",
    legend=False
)

for container in grafico.containers:
    grafico.bar_label(container, padding=5, fontsize=10, fontweight="bold")

plt.title("Distribution of ECG Exams by State", fontsize=16, pad=20, fontweight="bold")
plt.xlabel("Number of Exams", fontsize=12)
plt.ylabel("State", fontsize=12)
plt.tight_layout()
plt.show()
