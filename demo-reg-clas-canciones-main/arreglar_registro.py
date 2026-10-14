
import csv
from pathlib import Path

ruta = Path("registro_semana9.csv")
respaldo = Path("registro_semana9_antes_reparacion.csv")

# Conservar una copia del archivo actual.
if not respaldo.exists():
    respaldo.write_bytes(ruta.read_bytes())

columnas = [
    "tarea", "experimento", "modelo",
    "periodo_entrenamiento", "periodo_prueba", "objetivo",
    "variables_excluidas", "MAE", "RMSE", "R2",
    "sesgo_media_pred_menos_real", "accuracy", "precision",
    "recall", "F1", "costo", "costo_baseline",
    "TN", "FP", "FN", "TP", "umbral", "costo_FP",
    "costo_FN", "estado_verificacion", "observaciones"
]

filas = [
    {
        "tarea": "regresion",
        "experimento": "Baseline de regresion",
        "modelo": "Baseline del proyecto",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "popularidad",
        "variables_excluidas": "reproducciones_sem1; es_hit",
        "MAE": 10.44,
        "estado_verificacion": "Verificado en ficha HGB4",
        "observaciones": "MAE de la linea base de media por genero"
    },
    {
        "tarea": "regresion",
        "experimento": "RF1",
        "modelo": "RandomForest",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "popularidad",
        "variables_excluidas": "reproducciones_sem1; es_hit",
        "MAE": 6.96,
        "RMSE": 8.69,
        "R2": 0.584,
        "sesgo_media_pred_menos_real": 2.09,
        "estado_verificacion": "Pendiente de verificar",
        "observaciones": "Metricas historicas reportadas; sesgo por confirmar"
    },
    {
        "tarea": "regresion",
        "experimento": "RF2",
        "modelo": "RandomForest",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "popularidad",
        "variables_excluidas": "reproducciones_sem1; es_hit",
        "MAE": 7.10,
        "RMSE": 8.85,
        "R2": 0.568,
        "sesgo_media_pred_menos_real": 2.29,
        "estado_verificacion": "Pendiente de verificar",
        "observaciones": "Metricas historicas reportadas; sesgo por confirmar"
    },
    {
        "tarea": "regresion",
        "experimento": "HGB3",
        "modelo": "HistGradientBoosting",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "popularidad",
        "variables_excluidas": "reproducciones_sem1; es_hit",
        "MAE": 6.36,
        "RMSE": 8.03,
        "R2": 0.645,
        "sesgo_media_pred_menos_real": 1.96,
        "estado_verificacion": "Pendiente de verificar",
        "observaciones": "Metricas historicas reportadas; sesgo por confirmar"
    },
    {
        "tarea": "regresion",
        "experimento": "HGB4",
        "modelo": "HistGradientBoostingRegressor",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "popularidad",
        "variables_excluidas": "reproducciones_sem1; es_hit",
        "MAE": 6.39,
        "RMSE": 7.98,
        "R2": 0.649,
        "sesgo_media_pred_menos_real": -2.06,
        "estado_verificacion": "Verificado",
        "observaciones": "Ejecutado el 2026-10-14; sesgo convertido a prediccion menos real"
    },
    {
        "tarea": "clasificacion",
        "experimento": "Baseline de clasificacion",
        "modelo": "Nunca promocionar",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "es_hit",
        "variables_excluidas": "reproducciones_sem1; popularidad",
        "costo": 318,
        "costo_baseline": 318,
        "TN": 309,
        "FP": 0,
        "FN": 106,
        "TP": 0,
        "costo_FP": 1,
        "costo_FN": 3,
        "estado_verificacion": "Verificado",
        "observaciones": "Costo y total de casos derivados de la ficha del clasificador"
    },
    {
        "tarea": "clasificacion",
        "experimento": "Logistica propia",
        "modelo": "Regresion Logistica",
        "periodo_entrenamiento": "1995-2019",
        "periodo_prueba": "2020-2025",
        "objetivo": "es_hit",
        "variables_excluidas": "reproducciones_sem1; popularidad",
        "accuracy": 0.858,
        "precision": 0.688,
        "recall": 0.811,
        "F1": 0.745,
        "costo": 99,
        "costo_baseline": 318,
        "TN": 270,
        "FP": 39,
        "FN": 20,
        "TP": 86,
        "umbral": 0.27,
        "costo_FP": 1,
        "costo_FN": 3,
        "estado_verificacion": "Verificado",
        "observaciones": "Metricas consultadas en la ficha guardada del clasificador"
    }
]

with ruta.open("w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(filas)

print("Registro reconstruido correctamente.")
print("Filas:", len(filas))
print("Columnas:", len(columnas))
print("Respaldo:", respaldo)
