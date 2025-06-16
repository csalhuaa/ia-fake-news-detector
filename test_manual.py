# test_manual.py

import os
import re
import joblib
import sys
from nltk.corpus import stopwords
import nltk

# Asegúrate de haber descargado las stopwords una vez
# nltk.download('stopwords')

# — Configuración de rutas —
MODEL_DIR      = os.path.join("models")
VECTORIZER_FP  = os.path.join(MODEL_DIR, "vectorizer.pkl")
NB_MODEL_FP    = os.path.join(MODEL_DIR, "nb_model.pkl")
SVM_MODEL_FP   = os.path.join(MODEL_DIR, "svm_model.pkl")

# — Carga de artefactos —
try:
    vectorizer = joblib.load(VECTORIZER_FP)
    nb_model   = joblib.load(NB_MODEL_FP)
    svm_model  = joblib.load(SVM_MODEL_FP)
except FileNotFoundError as e:
    print("Error al cargar los modelos o el vectorizador:", e)
    sys.exit(1)

# — Funciones de preprocesamiento —
def limpiar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"http\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

stopwords_es = set(stopwords.words('spanish'))
def quitar_stopwords(texto: str) -> str:
    return " ".join(w for w in texto.split() if w not in stopwords_es)

def preparar(texto: str) -> str:
    return quitar_stopwords(limpiar_texto(texto))

# — Bucle interactivo —
def main():
    print("=== Prueba Manual de Detector de Noticias Falsas ===")
    print("Modelos disponibles:")
    print("  1) Naive Bayes")
    print("  2) SVM")
    choice = input("Elige modelo (1 o 2): ").strip()
    if choice == "1":
        model = nb_model
        name = "Naive Bayes"
    elif choice == "2":
        model = svm_model
        name = "SVM"
    else:
        print("Opción inválida")
        return

    print(f"\nHas seleccionado: {name}")
    print("Escribe una noticia (vacío para salir):\n")

    while True:
        text_raw = input("> ")
        if not text_raw:
            print("Saliendo…")
            break

        text_proc = preparar(text_raw)
        X_vec = vectorizer.transform([text_proc])
        pred = model.predict(X_vec)[0]
        etiqueta = "Verdadera" if pred == 1 else "Falsa"

        # Si el modelo ofrece predict_proba, muestra confianza
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X_vec)[0]
            confianza = prob[pred]
            print(f"[{name}] → {etiqueta} (confianza: {confianza:.2%})\n")
        else:
            print(f"[{name}] → {etiqueta}\n")

if __name__ == "__main__":
    # Asegurar nltk
    try:
        stopwords_es
    except LookupError:
        nltk.download('stopwords')
    main()
