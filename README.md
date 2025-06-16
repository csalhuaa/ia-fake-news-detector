# Fake News Detector

Este proyecto desarrolla un sistema para detectar noticias falsas en español, combinando procesamiento de lenguaje natural (NLP) y algoritmos de aprendizaje automático (ML). El flujo de trabajo abarca desde la exploración de datos hasta la evaluación de modelos, con posibilidad de extenderse a una aplicación web.

## Objetivo

Clasificar noticias políticas en español como verdaderas o falsas mediante técnicas de NLP y clasificadores supervisados. El proyecto está organizado en etapas modulares documentadas en cuadernos Jupyter, lo que permite su análisis y reproducción.

## Conjunto de Datos

Se emplea el dataset [Spanish Political Fake News](https://www.kaggle.com/datasets/javieroterovizoso/spanish-political-fake-news?select=D57000_complete.csv). Este archivo debe colocarse en la ruta `data/raw/D57000_complete.csv` para su correcta lectura y procesamiento.

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
   ```

4. Iniciar Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

## Flujo de Trabajo (Cuadernos Jupyter)

1. **01\_exploracion.ipynb**: Exploración inicial y visualización del dataset.
2. **03\_preprocesamiento.ipynb**: Limpieza de texto, normalización y vectorización con TF-IDF.
3. **04\_modelos.ipynb**: Entrenamiento de clasificadores Naive Bayes y SVM.
4. **05\_evaluacion.ipynb**: Evaluación de los modelos mediante métricas y visualizaciones.

> Nota: El archivo `02_traduccion.ipynb` está presente por compatibilidad, pero no es necesario ya que el dataset está originalmente en español.

## Prueba Manual

Puedes realizar pruebas ingresando noticias manualmente con el script:

```bash
python test_manual.py
```

Este script carga el modelo entrenado y permite clasificar textos ingresados por el usuario.

## Futuras Extensiones

* Implementación de una aplicación web con Flask para exponer el modelo.
* Incorporación de técnicas avanzadas de NLP como lematización o embeddings.
* Experimentación con modelos adicionales como Random Forest, XGBoost o transformers.

## Estructura del Proyecto

```
.
├── data/            # Datos crudos, procesados y divididos
├── notebooks/       # Cuadernos por etapa del flujo
├── models/          # Modelos y objetos serializados
├── app/             # Código de la futura aplicación web
├── tests/           # Scripts de prueba
├── requirements.txt # Lista de dependencias
└── README.md        # Documentación principal
```

## Licencia

Este proyecto es de uso académico y experimental. No se recomienda su uso directo en entornos productivos sin revisiones adicionales.
