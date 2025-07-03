from flask import Flask, render_template, request, jsonify
import sys
import os
import json

# Permite importar desde la carpeta ml/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ml')))
from preprocess import preprocesar_texto, cargar_vectorizador, vectorizar_texto
from predict import cargar_modelo, predecir

app = Flask(__name__)

# Rutas relativas desde flask-template/
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')
SVM_MODEL_PATH = os.path.join(MODELS_DIR, 'svm_model.pkl')
NB_MODEL_PATH = os.path.join(MODELS_DIR, 'nb_model.pkl')

# Cargar modelos al iniciar la app
vectorizer = cargar_vectorizador(VECTORIZER_PATH)
svm_modelo = cargar_modelo(SVM_MODEL_PATH)
nb_modelo = cargar_modelo(NB_MODEL_PATH)

@app.route("/")
def home():
    """Sirve la página principal con el nuevo diseño"""
    return render_template("home.html")

@app.route("/about")
def about():
    """Ruta para compatibilidad, redirige a la página principal"""
    return render_template("about.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint para predicción - Compatible con el nuevo frontend
    Devuelve JSON para ser consumido por JavaScript
    """
    try:
        # Obtener datos del formulario
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        model_choice = request.form.get("model", "svm")
        
        # Validar entrada
        if not title or not description:
            return jsonify({
                "success": False,
                "error": "Título y descripción son requeridos"
            }), 400
        
        # Combinar título y descripción
        texto = f"{title}. {description}"
        
        # Preprocesar y vectorizar
        texto_proc = preprocesar_texto(texto)
        vector = vectorizar_texto(vectorizer, texto_proc)
        
        # Realizar predicciones según el modelo seleccionado
        resultados = []
        prediccion_final = None
        confianza_final = 0.0
        
        if model_choice == "svm" or model_choice == "both":
            pred_svm = predecir(svm_modelo, vector)
            etiqueta_svm = "Verdadera" if pred_svm == 1 else "Falsa"
            
            # Intentar obtener probabilidades si están disponibles
            try:
                if hasattr(svm_modelo, "predict_proba"):
                    prob_svm = svm_modelo.predict_proba(vector)[0]
                    confianza_svm = max(prob_svm) * 100
                else:
                    # Si no tiene predict_proba, usar decision_function para SVM
                    decision = svm_modelo.decision_function(vector)[0]
                    # Convertir decision_function a pseudo-probabilidad
                    confianza_svm = min(95, max(55, abs(decision) * 20 + 60))
                
                resultados.append({
                    "modelo": "SVM",
                    "prediccion": etiqueta_svm,
                    "confianza": round(confianza_svm, 1),
                    "es_verdadera": pred_svm == 1
                })
                
                if prediccion_final is None:
                    prediccion_final = pred_svm
                    confianza_final = confianza_svm
                    
            except Exception as e:
                # Fallback sin probabilidades
                resultados.append({
                    "modelo": "SVM",
                    "prediccion": etiqueta_svm,
                    "confianza": 75.0,  # Valor por defecto
                    "es_verdadera": pred_svm == 1
                })
                if prediccion_final is None:
                    prediccion_final = pred_svm
                    confianza_final = 75.0
        
        if model_choice == "nb" or model_choice == "both":
            pred_nb = predecir(nb_modelo, vector)
            etiqueta_nb = "Verdadera" if pred_nb == 1 else "Falsa"
            
            # Naive Bayes generalmente tiene predict_proba
            try:
                if hasattr(nb_modelo, "predict_proba"):
                    prob_nb = nb_modelo.predict_proba(vector)[0]
                    confianza_nb = max(prob_nb) * 100
                else:
                    confianza_nb = 75.0  # Valor por defecto
                
                resultados.append({
                    "modelo": "Naive Bayes",
                    "prediccion": etiqueta_nb,
                    "confianza": round(confianza_nb, 1),
                    "es_verdadera": pred_nb == 1
                })
                
                # Si es el único modelo o tiene mayor confianza, usar como final
                if prediccion_final is None or confianza_nb > confianza_final:
                    prediccion_final = pred_nb
                    confianza_final = confianza_nb
                    
            except Exception as e:
                resultados.append({
                    "modelo": "Naive Bayes",
                    "prediccion": etiqueta_nb,
                    "confianza": 75.0,
                    "es_verdadera": pred_nb == 1
                })
                if prediccion_final is None:
                    prediccion_final = pred_nb
                    confianza_final = 75.0
        
        # Preparar respuesta
        if model_choice == "both" and len(resultados) == 2:
            # Consenso entre modelos
            consenso = all(r["es_verdadera"] for r in resultados)
            if consenso or not any(r["es_verdadera"] for r in resultados):
                # Ambos coinciden
                confianza_final = sum(r["confianza"] for r in resultados) / len(resultados)
            else:
                # Discrepancia - reducir confianza
                confianza_final = max(r["confianza"] for r in resultados) * 0.7
        
        return jsonify({
            "success": True,
            "prediccion_final": "Verdadera" if prediccion_final == 1 else "Falsa",
            "es_verdadera": prediccion_final == 1,
            "confianza": round(confianza_final, 1),
            "modelo_usado": model_choice,
            "resultados_detalle": resultados,
            "texto_analizado": f"{title[:50]}..." if len(title) > 50 else title
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error interno del servidor: {str(e)}"
        }), 500

@app.route("/api/health")
def health_check():
    """Endpoint para verificar que la API está funcionando"""
    return jsonify({
        "status": "OK",
        "message": "FactCheck AI API está funcionando correctamente",
        "models_loaded": {
            "svm": svm_modelo is not None,
            "naive_bayes": nb_modelo is not None,
            "vectorizer": vectorizer is not None
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)