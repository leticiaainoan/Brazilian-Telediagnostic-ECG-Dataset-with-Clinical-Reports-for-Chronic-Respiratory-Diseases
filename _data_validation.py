import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Settings for scientific publication
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.grid': True,
    'grid.alpha': 0.3
})

# Load dataset
df = pd.read_csv('/content/Database - PNTD - COPD - Structured(in).csv', sep=';')

# --- DATA CLEANING ---
# 1. Filter gender to keep only 'F' and 'M'
df = df[df['patient_gender'].isin(['F', 'M'])]

# 2. Ensure patient_age is numeric
df['patient_age'] = pd.to_numeric(df['patient_age'], errors='coerce')
df = df.dropna(subset=['patient_age'])

# 3. Function to convert values to boolean
def to_bool(val):
    if isinstance(val, str):
        return val.lower() == 'true'
    return bool(val)

# Identify columns
comorbidities_cols = [col for col in df.columns if col.startswith('history_') and col != 'history_no_comorbidities']
medication_cols = [col for col in df.columns if col.startswith('medication_') and col != 'medication_none']
reason_cols = [col for col in df.columns if col.startswith('reason_')]

# Convert to boolean
for col in comorbidities_cols + medication_cols + reason_cols:
    df[col] = df[col].apply(to_bool)

# List of all formatted comorbidities
all_comorbidities = comorbidities_cols


# --- REGENERATE ORIGINAL PLOTS ---

# 1. Overall Distribution
comorbidities_counts = df[all_comorbidities].sum().sort_values(ascending=False)
comorbidities_counts.index = [idx.replace('history_', '').replace('_', ' ').title() for idx in comorbidities_counts.index]
plt.figure(figsize=(12, 8))
sns.barplot(x=comorbidities_counts.values, y=comorbidities_counts.index, hue=comorbidities_counts.index, palette='viridis', legend=False)
plt.title('Distribution of All Comorbidities')
plt.xlabel('Number of Patients')
plt.ylabel('Comorbidity')
plt.tight_layout()
plt.savefig('/content/comorbidities_distribution.png')
plt.show()

# 2. By Gender (All)
df_melted_gender = df.melt(id_vars=['patient_gender'], value_vars=all_comorbidities, var_name='Comorbidity', value_name='Presence')
df_melted_gender = df_melted_gender[df_melted_gender['Presence'] == True]
df_melted_gender['Comorbidity'] = df_melted_gender['Comorbidity'].apply(lambda x: x.replace('history_', '').replace('_', ' ').title())
plt.figure(figsize=(14, 10))
sns.countplot(data=df_melted_gender, y='Comorbidity', hue='patient_gender', palette='Set2')
plt.title('All Comorbidities and Gender Correlation')
plt.xlabel('Number of Patients')
plt.ylabel('Comorbidity')
plt.legend(title='Gender', labels=['Female', 'Male'])
plt.tight_layout()
plt.savefig('/content/comorbidities_by_gender.png')
plt.show()

# 3. By Age (All)
df_melted_age = df.melt(id_vars=['patient_age'], value_vars=all_comorbidities, var_name='Comorbidity', value_name='Presence')
df_melted_age = df_melted_age[df_melted_age['Presence'] == True]
df_melted_age['Comorbidity'] = df_melted_age['Comorbidity'].apply(lambda x: x.replace('history_', '').replace('_', ' ').title())
plt.figure(figsize=(14, 10))
sns.boxplot(data=df_melted_age, x='patient_age', y='Comorbidity', hue='Comorbidity', palette='coolwarm', legend=False)
plt.title('Relationship between All Comorbidities and Age')
plt.xlabel('Age (Years)')
plt.ylabel('Comorbidity')
plt.tight_layout()
plt.savefig('/content/comorbidities_by_age.png')
plt.show()


medication_counts = df[medication_cols].sum().sort_values(ascending=False)
medication_counts.index = [idx.replace('medication_', '').replace('_', ' ').title() for idx in medication_counts.index]
plt.figure(figsize=(12, 7))
sns.barplot(x=medication_counts.values, y=medication_counts.index, hue=medication_counts.index, palette='magma', legend=False)
plt.title('Distribution of Medication Use')
plt.xlabel('Number of Patients')
plt.ylabel('Medication')
plt.tight_layout()
plt.savefig('/content/medication_distribution.png')
plt.show()

reason_counts = df[reason_cols].sum().sort_values(ascending=False)
reason_counts.index = [idx.replace('reason_', '').replace('_', ' ').title() for idx in reason_counts.index]
plt.figure(figsize=(10, 6))
sns.barplot(x=reason_counts.values, y=reason_counts.index, hue=reason_counts.index, palette='rocket', legend=False)
plt.title('Reasons for Performing the ECG Examination')
plt.xlabel('Number of Patients')
plt.ylabel('Reason')
plt.tight_layout()
plt.savefig('/content/exam_reasons.png')
plt.show()

print("All plots with ALL comorbidities have been generated!")
