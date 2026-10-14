
"""
Sprint 2: clasificación binaria de canciones.

Objetivo:
Predecir si una canción será un hit antes de su lanzamiento.

Definición:
- es_hit = 1 si popularidad >= 70.
- es_hit = 0 si popularidad < 70.

Variables excluidas:
- popularidad: es el origen del objetivo.
- reproducciones_sem1: ocurre después del lanzamiento.

Evaluación temporal:
- Entrenamiento: 1995-2019.
- Prueba: 2020-2025.

Costo de decisión:
- Falso positivo: 1 unidad.
- Falso negativo: 3 unidades.
- Umbral de decisión: 0.27.

Para ejecutar:
    python -m src.entrenar_clasificacion

IMPORTANTE:
Este script sobrescribe models/modelo.pkl.
Guarda una copia del modelo anterior antes de ejecutarlo.
"""

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from src.artefacto import guardar
from src.variables import (
    COLUMNAS_ENTRADA,
    cargar_canciones,
    derivadas,
    particion_temporal,
    preprocesamiento,
    resumen_periodo,
)


NOMBRE = "Regresion Logistica - Modelo Propio"

UMBRAL = 0.27

# Costos de negocio de los errores de clasificación.
COSTO_FALSO_POSITIVO = 1
COSTO_FALSO_NEGATIVO = 3

VARIABLES_EXCLUIDAS = {
    "reproducciones_sem1": (
        "ocurre después del lanzamiento y no existe "
        "en el momento de decidir la promoción"
    ),
    "popularidad": (
        "es el origen del objetivo es_hit; incluirla "
        "provocaría fuga de información"
    ),
}


def construir_pipeline():
    """
    Construye el pipeline de regresión logística.

    Recibe las columnas originales, aplica las variables
    derivadas y el preprocesamiento dentro del pipeline.
    """
    return make_pipeline(
        FunctionTransformer(derivadas),
        preprocesamiento(),
        LogisticRegression(
            max_iter=2000,
            random_state=42,
        ),
    )


def calcular_costo(y_real, y_pred):
    """
    Calcula el costo total de las decisiones.

    Falso positivo:
    se promociona una canción que no es hit.

    Falso negativo:
    no se promociona una canción que sí es hit.
    """
    tn, fp, fn, tp = confusion_matrix(
        y_real,
        y_pred,
        labels=[0, 1],
    ).ravel()

    costo = (
        COSTO_FALSO_POSITIVO * fp
        + COSTO_FALSO_NEGATIVO * fn
    )

    return int(costo), int(tn), int(fp), int(fn), int(tp)


def entrenar() -> dict:
    """Entrena, evalúa y guarda el modelo de clasificación."""

    # 1. Cargar los datos.
    datos = cargar_canciones()

    # 2. Crear la partición temporal.
    entrenamiento, prueba = particion_temporal(datos)

    # 3. Seleccionar las variables de entrada.
    X = datos[COLUMNAS_ENTRADA]

    # 4. Definir el objetivo binario.
    # Se usa la columna es_hit ya existente en el dataset.
    y = datos["es_hit"].astype(int)

    # 5. Entrenar solo con las canciones del periodo 1995-2019.
    pipeline = construir_pipeline()
    pipeline.fit(
        X.loc[entrenamiento],
        y.loc[entrenamiento],
    )

    # 6. Obtener probabilidades de hit para el periodo de prueba.
    probabilidades = pipeline.predict_proba(
        X.loc[prueba]
    )[:, 1]

    # 7. Aplicar el umbral de decisión.
    pred = (probabilidades >= UMBRAL).astype(int)

    y_prueba = y.loc[prueba]

    # 8. Calcular el costo del modelo.
    (
        costo_modelo,
        tn,
        fp,
        fn,
        tp,
    ) = calcular_costo(y_prueba, pred)

    # 9. Línea base: nunca promocionar ninguna canción.
    base = pd.Series(
        0,
        index=y_prueba.index,
        dtype=int,
    )

    costo_base, _, _, _, _ = calcular_costo(
        y_prueba,
        base,
    )

    # 10. Métricas generales.
    metricas = {
        "costo": costo_modelo,
        "accuracy": round(
            float(accuracy_score(y_prueba, pred)),
            3,
        ),
        "precision": round(
            float(
                precision_score(
                    y_prueba,
                    pred,
                    zero_division=0,
                )
            ),
            3,
        ),
        "recall": round(
            float(
                recall_score(
                    y_prueba,
                    pred,
                    zero_division=0,
                )
            ),
            3,
        ),
        "f1": round(
            float(
                f1_score(
                    y_prueba,
                    pred,
                    zero_division=0,
                )
            ),
            3,
        ),
    }

    # 11. Métricas por género.
    resultados_genero = {}

    generos_prueba = datos.loc[prueba, "genero"]

    for genero in sorted(generos_prueba.unique()):
        mascara = generos_prueba == genero

        y_genero = y_prueba.loc[mascara]
        pred_genero = pd.Series(
            pred,
            index=y_prueba.index,
        ).loc[mascara]

        (
            costo_genero,
            tn_genero,
            fp_genero,
            fn_genero,
            tp_genero,
        ) = calcular_costo(
            y_genero,
            pred_genero,
        )

        resultados_genero[str(genero)] = {
            "n": int(len(y_genero)),
            "costo": costo_genero,
            "precision": round(
                float(
                    precision_score(
                        y_genero,
                        pred_genero,
                        zero_division=0,
                    )
                ),
                3,
            ),
            "recall": round(
                float(
                    recall_score(
                        y_genero,
                        pred_genero,
                        zero_division=0,
                    )
                ),
                3,
            ),
            "f1": round(
                float(
                    f1_score(
                        y_genero,
                        pred_genero,
                        zero_division=0,
                    )
                ),
                3,
            ),
            "tn": tn_genero,
            "fp": fp_genero,
            "fn": fn_genero,
            "tp": tp_genero,
        }

    # 12. Construir la ficha del modelo.
    ficha = {
        "nombre": NOMBRE,
        "tarea": "clasificacion",
        "objetivo": (
            "predecir si una canción será hit "
            "(es_hit = 1 si popularidad >= 70)"
        ),
        "momento_prediccion": (
            "antes del lanzamiento: la disquera decide "
            "si invertir en promoción"
        ),
        "variables_entrada": list(COLUMNAS_ENTRADA),
        "variables_excluidas": VARIABLES_EXCLUIDAS,

        "entrenamiento": resumen_periodo(
            datos,
            entrenamiento,
        ),

        "prueba": {
            **resumen_periodo(datos, prueba),
            "tipo": "temporal",
        },

        "linea_base": {
            "descripcion": (
                "no promocionar ninguna canción; "
                "predecir siempre es_hit = 0"
            ),
            "costo": costo_base,
        },

        "desempeno": {
            **metricas,
            "matriz_confusion": {
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
            },
        },

        "por_genero": resultados_genero,

        "decision": {
            "umbral": UMBRAL,
            "regla": (
                "promocionar si la probabilidad estimada "
                "de hit es igual o superior al umbral"
            ),
            "costo_falso_positivo": COSTO_FALSO_POSITIVO,
            "costo_falso_negativo": COSTO_FALSO_NEGATIVO,
            "nota": (
                "el umbral depende de los costos de negocio; "
                "debe validarse antes de usarlo en producción"
            ),
        },

        "limites": (
            "describe asociaciones en datos sintéticos; "
            "no es evidencia causal"
        ),
    }

    # 13. Guardar el pipeline y su ficha.
    resultado = guardar(pipeline, ficha)

    # 14. Mostrar resultados en CMD.
    print("\nENTRENAMIENTO FINALIZADO")
    print("=" * 55)
    print(f"Modelo: {NOMBRE}")
    print(f"Umbral de clasificación: {UMBRAL}")
    print(
        "Costos: falso positivo = "
        f"{COSTO_FALSO_POSITIVO}, falso negativo = "
        f"{COSTO_FALSO_NEGATIVO}"
    )

    print(
        f"Entrenamiento: {ficha['entrenamiento']}"
    )
    print(
        f"Prueba temporal: {ficha['prueba']}"
    )

    print("\nMÉTRICAS DEL MODELO")
    print(f"Costo:     {metricas['costo']}")
    print(f"Accuracy:  {metricas['accuracy']}")
    print(f"Precision: {metricas['precision']}")
    print(f"Recall:    {metricas['recall']}")
    print(f"F1:        {metricas['f1']}")

    print("\nMATRIZ DE CONFUSIÓN")
    print(f"Verdaderos negativos (TN): {tn}")
    print(f"Falsos positivos (FP):     {fp}")
    print(f"Falsos negativos (FN):     {fn}")
    print(f"Verdaderos positivos (TP): {tp}")

    print("\nLÍNEA BASE")
    print(f"Costo de la línea base: {costo_base}")

    print("\nCOSTO Y MÉTRICAS POR GÉNERO")
    for genero, datos_genero in resultados_genero.items():
        print(
            f"{genero}: costo={datos_genero['costo']}, "
            f"precision={datos_genero['precision']}, "
            f"recall={datos_genero['recall']}, "
            f"F1={datos_genero['f1']}"
        )

    print("\nEl pipeline y la ficha se han guardado.")
    print("Consulta GET /modelo para ver la ficha completa.")

    return resultado


if __name__ == "__main__":
    entrenar()
