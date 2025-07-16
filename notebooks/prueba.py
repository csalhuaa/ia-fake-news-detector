import pandas as pd

# --- 1. Leer el archivo CSV con configuración especial ---
df = pd.read_csv(
    '../data/raw/test.csv',
    quoting=1,               # Manejar campos entre comillas
    quotechar='"',           # Las celdas que usan " para delimitar texto largo
    encoding='utf-8',
    engine='python'          # Soporta mejor saltos de línea en celdas
)

# --- 2. Renombrar columnas para unificar ---
df_test = df.rename(columns={
    'HEADLINE': 'title',
    'TEXT': 'text',
    'CATEGORY': 'label'
})

# --- 3. Convertir etiquetas 'TRUE'/'FALSE' a 'real'/'fake' ---
df_test['label'] = df_test['label'].map({'TRUE': 'real', 'FALSE': 'fake'})

# --- 4. Dejar solo las columnas necesarias ---
df_test = df_test[['title', 'text', 'label']]

# --- 5. Guardar el resultado ---
df_test.to_csv('../data/processed/test_unificado.csv', index=False)

print("✅ ¡Archivo test_unificado.csv guardado correctamente en /data/processed/!")
