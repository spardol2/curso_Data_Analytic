
"""
Sprint 1, regresión: cuarto experimento con
HistGradientBoostingRegressor.

Objetivo:
Predecir la popularidad de una canción antes de su lanzamiento.

Experimento 4:
- Algoritmo: HistGradientBoostingRegressor.
- Iteraciones máximas: 300.
- Tasa de aprendizaje: 0.03.
- Máximo de hojas por árbol: 10.
- Regularización L2: 2.0.
- Entrenamiento: 1995-2019.
- Prueba temporal: 2020-2025.

Para ejecutar:
    python -m src.entrenar_regresion

IMPORTANTE:
Este script sobrescribe models/modelo.pkl.
Guarda copias de los experimentos anteriores.
"""

import numpy as np
import pandas as pd

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
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


# Identificación del cuarto experimento.
NOMBRE = "HistGradientBoostingRegressor - Experimento 4"

# Umbral de popularidad esperado para recomendar promoción.
CORTE_PROMOCION = 65

# Variables excluidas para evitar fuga de información.
VARIABLES_EXCLUIDAS = {
    "reproducciones_sem1": (
        "ocurre después del lanzamiento: "
        "no existe en el momento de decidir"
    ),
    "es_hit": (
        "se calcula a partir del objetivo "
        "(popularidad >= 70)"
    ),
}


def construir_pipeline():
    """
    Construye el pipeline del cuarto experimento.
    Aplica las variables derivadas y el preprocesamiento
    antes de entrenar el modelo.
    """
    return make_pipeline(
        FunctionTransformer(derivadas),
        preprocesamiento(),
        HistGradientBoostingRegressor(
            max_iter=300,
            learning_rate=0.03,
            max_leaf_nodes=10,
            l2_regularization=2.0,
            random_state=42,
        ),
    )


def entrenar() -> dict:
    """Entrena, evalúa y guarda el cuarto modelo de regresión."""

    # 1. Cargar los datos.
    datos = cargar_canciones()

    # 2. Crear la partición temporal.
    entrenamiento, prueba = particion_temporal(datos)

    # 3. Seleccionar variables de entrada y objetivo.
    X = datos[COLUMNAS_ENTRADA]
    y = datos["popularidad"]

    # 4. Entrenar exclusivamente con el periodo de entrenamiento.
    pipeline = construir_pipeline()
    pipeline.fit(
        X.loc[entrenamiento],
        y.loc[entrenamiento],
    )

    # 5. Predecir sobre el periodo de prueba.
    pred = pipeline.predict(X.loc[prueba])

    # 6. Calcular los residuos.
    # Residuo positivo: el valor real supera la predicción.
    residuo = y.loc[prueba] - pred

    # 7. Línea base: media por género calculada con entrenamiento.
    media_genero = y.loc[entrenamiento].groupby(
        datos.loc[entrenamiento, "genero"]
    ).mean()

    base = datos.loc[prueba, "genero"].map(media_genero)

    # Si aparece un género no observado en entrenamiento,
    # utilizar la media global del objetivo de entrenamiento.
    base = base.fillna(y.loc[entrenamiento].mean())

    # 8. Calcular métricas por género.
    por_genero = (
        pd.DataFrame(
            {
                "genero": datos.loc[prueba, "genero"],
                "abs": residuo.abs(),
                "res": residuo,
            }
        )
        .groupby("genero")
        .agg(
            mae=("abs", "mean"),
            sesgo=("res", "mean"),
        )
        .round(2)
    )

    # 9. Construir la ficha del modelo.
    ficha = {
        "nombre": NOMBRE,
        "tarea": "regresion",
        "objetivo": (
            "popularidad (0-100) que alcanzará la canción"
        ),
        "momento_prediccion": (
            "antes del lanzamiento: la disquera decide "
            "cuánto invertir en promoción"
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
            "descripcion": "media por género (entrenamiento)",
            "mae": round(
                float(
                    mean_absolute_error(
                        y.loc[prueba],
                        base,
                    )
                ),
                2,
            ),
        },

        "desempeno": {
            "mae": round(
                float(
                    mean_absolute_error(
                        y.loc[prueba],
                        pred,
                    )
                ),
                2,
            ),
            "rmse": round(
                float(
                    np.sqrt(
                        mean_squared_error(
                            y.loc[prueba],
                            pred,
                        )
                    )
                ),
                2,
            ),
            "r2": round(
                float(
                    r2_score(
                        y.loc[prueba],
                        pred,
                    )
                ),
                3,
            ),
            "sesgo": round(
                float(residuo.mean()),
                2,
            ),
        },

        "por_genero": por_genero.to_dict(
            orient="index"
        ),

        "decision": {
            "corte_promocion": CORTE_PROMOCION,
            "regla": (
                "promocionar si la popularidad esperada "
                "supera el corte"
            ),
            "nota": (
                "el corte lo fija quien responde por "
                "el presupuesto, no el modelo"
            ),
        },

        "limites": (
            "describe asociaciones en datos sintéticos; "
            "no es evidencia causal"
        ),
    }

    # 10. Guardar el pipeline y la ficha.
    resultado = guardar(pipeline, ficha)

    # 11. Mostrar los resultados en CMD.
    print("\nENTRENAMIENTO FINALIZADO")
    print("=" * 55)
    print(f"Modelo: {NOMBRE}")
    print("Parámetros: 300 iteraciones, learning_rate=0.03")
    print("Máximo de hojas: 10 | Regularización L2: 2.0")

    print(f"Entrenamiento: {ficha['entrenamiento']}")
    print(f"Prueba temporal: {ficha['prueba']}")

    print("\nMÉTRICAS DEL MODELO")
    print(f"MAE:   {ficha['desempeno']['mae']}")
    print(f"RMSE:  {ficha['desempeno']['rmse']}")
    print(f"R²:    {ficha['desempeno']['r2']}")
    print(f"Sesgo: {ficha['desempeno']['sesgo']}")

    print("\nLÍNEA BASE")
    print(
        "MAE de la línea base: "
        f"{ficha['linea_base']['mae']}"
    )

    print("\nMAE Y SESGO POR GÉNERO")
    for genero, metricas in ficha["por_genero"].items():
        print(
            f"{genero}: MAE={metricas['mae']}, "
            f"sesgo={metricas['sesgo']}"
        )

    print("\nEl pipeline y la ficha se han guardado.")
    print("Consulta GET /modelo para ver la ficha completa.")

    return resultado


if __name__ == "__main__":
    entrenar()
