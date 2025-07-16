# Fake News Detector

Este proyecto desarrolla un sistema para detectar noticias falsas en español, combinando procesamiento de lenguaje natural (NLP) y algoritmos de aprendizaje automático (ML). El flujo de trabajo abarca desde la obtención y traducción de datos, unificación, preprocesamiento avanzado, entrenamiento y evaluación de modelos, hasta la posibilidad de desplegar una aplicación web.

## Objetivo

Clasificar noticias en español como verdaderas o falsas mediante técnicas de NLP y clasificadores supervisados. El proyecto está organizado en etapas modulares documentadas en cuadernos Jupyter, lo que permite su análisis y reproducción.

## Conjuntos de Datos

- **Dataset de entrenamiento (inglés, traducido):**
  - [Fake News Detection Datasets (Kaggle)](https://www.kaggle.com/datasets/emineyetm/fake-news-detection-datasets/data)
  - Se seleccionan 250 noticias reales ("World-News") y 250 falsas ("News"), que se traducen automáticamente al español.

- **Dataset de prueba (español):**
  - [Fake News Corpus Spanish (HuggingFace)](https://huggingface.co/datasets/mariagrandury/fake_news_corpus_spanish)
  - 572 noticias variadas, etiquetadas como verdaderas o falsas.

## Requisitos e Instalación

1. Clonar este repositorio:

   ```bash
   git clone https://github.com/tu-usuario/fake-news-detector.git
   cd fake-news-detector
   ```

2. (Opcional) Crear un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   python -m spacy download es_core_news_sm
   ```

4. Iniciar Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

## Flujo de Trabajo (Cuadernos Jupyter)

1. **01_unificacion_datasets.ipynb**: Unificación y estandarización de los datasets de entrenamiento y prueba.
2. **02_traduccion.ipynb**: Traducción automática de los textos en inglés al español (si es necesario).
3. **03_preprocesamiento.ipynb**: Limpieza, lematización con spaCy y vectorización TF-IDF. División estratificada en train/test.
4. **04_modelos.ipynb**: Entrenamiento y comparación de clasificadores: SVM, Naive Bayes, Regresión Logística, Árbol de Decisión, Random Forest y MLP.
5. **05_evaluacion.ipynb**: Evaluación de los modelos mediante métricas (accuracy, precision, recall, f1-score), matriz de confusión, curva ROC/AUC, validación cruzada y análisis de errores.

## Pruebas Automáticas y Manuales

- **Prueba automática:**
  - Ejecuta `tests/test_predictions.py` para verificar la predicción de todos los modelos sobre una noticia de ejemplo.

- **Prueba manual:**
  - Ejecuta `python test_manual.py` para ingresar noticias y obtener la predicción del modelo entrenado.

## Futuras Extensiones

* Implementación de una aplicación web con Flask para exponer el modelo y permitir la clasificación de noticias desde una interfaz amigable.

## Estructura del Proyecto

```
.
├── data/            # Datos crudos, traducidos, procesados y divididos
├── notebooks/       # Cuadernos por etapa del flujo
├── models/          # Modelos y objetos serializados
├── app/             # Código de la futura aplicación web
├── tests/           # Scripts de prueba
├── requirements.txt # Lista de dependencias
└── README.md        # Documentación principal
```

Este proyecto es de uso académico y experimental. No se recomienda su uso directo en entornos productivos sin revisiones adicionales.
