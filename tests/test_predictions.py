# Test para verificar predicciones del modelo

import joblib
import os

# Noticia de prueba
noticia = ("la tierra es esferica")

# Cargar vectorizador
vectorizer = joblib.load(os.path.join("../models", "vectorizer.pkl"))

# Preprocesar y vectorizar la noticia
# Si tienes una función de preprocesamiento, úsala aquí. Si no, solo vectoriza.
X = vectorizer.transform([noticia])

# Lista de modelos a probar
modelos = [
    "svm.pkl",
    "naive_bayes.pkl",
    "logistic_regression.pkl",
    "decision_tree.pkl",
    "random_forest.pkl",
    "mlp.pkl"
]

nombres = [
    "SVM",
    "Naive Bayes",
    "Regresión Logística",
    "Árbol de Decisión",
    "Random Forest",
    "MLP"
]

for nombre_archivo, nombre_modelo in zip(modelos, nombres):
    modelo_path = os.path.join("../models", nombre_archivo)
    if os.path.exists(modelo_path):
        modelo = joblib.load(modelo_path)
        pred = modelo.predict(X)[0]
        etiqueta = "Real" if pred == 1 else "Fake"
        # Si el modelo soporta predict_proba, muestra la probabilidad
        if hasattr(modelo, "predict_proba"):
            proba = modelo.predict_proba(X)[0][pred]
            print(f"{nombre_modelo}: {etiqueta} (confianza: {proba:.2%})")
        else:
            print(f"{nombre_modelo}: {etiqueta} (probabilidad no disponible)")
    else:
        print(f"{nombre_modelo}: Modelo no encontrado ({modelo_path})")
