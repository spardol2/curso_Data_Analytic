# Análisis de ventas de restaurante

## Objetivo

El objetivo de este proyecto es analizar las ventas de un restaurante durante dos semanas para identificar el comportamiento de los ingresos, la frecuencia de compra de los productos, la recurrencia de los clientes y los grupos de ocupación que concentran mayores ingresos.

El análisis se realizó utilizando Python, Pandas, SQL y visualizaciones para comparar los resultados y obtener conclusiones que puedan apoyar la toma de decisiones del negocio.

## Archivos utilizados

Para realizar el análisis se utilizaron los siguientes archivos:

- `Restaurant-Foods.csv`: contiene la información de los productos y sus precios.
- `Restaurant-Week1-Sales.csv`: contiene los registros de ventas de la semana 1.
- `Restaurant-Week2-Sales.csv`: contiene los registros de ventas de la semana 2.
- `Restaurant-Customers.csv`: contiene la información de los clientes utilizada para relacionar las ventas con sus datos.

> Nota: el archivo `Restaurant-Customers.csv` no debe publicarse en un repositorio público debido a que contiene información de clientes.

## Instrucciones para ejecutar

1. Abrir el notebook de análisis en Google Colab o en un entorno compatible con Python.
2. Cargar los archivos CSV necesarios.
3. Ejecutar las celdas del notebook en orden.
4. Verificar que las validaciones de los datos se ejecuten correctamente.
5. Revisar las tablas, resultados y visualizaciones generadas.
6. Para ejecutar el análisis se requieren las librerías:
   - Pandas
   - Matplotlib
   - SQLite3

## Principales hallazgos

- Se analizaron **500 registros de venta**, correspondientes a 250 registros de la semana 1 y 250 de la semana 2.
- Los ingresos totales observados fueron de **3886.56**.
- La semana 1 registró ingresos de **1962.68**, mientras que la semana 2 registró **1923.88**.
- El número de registros de venta se mantuvo igual en ambas semanas, con **250 registros** por semana.
- El **Burrito** presentó la mayor frecuencia de compra, con **57 registros**.
- El **Steak** presentó los mayores ingresos, con **1249.50**.
- La tasa de recurrencia de clientes fue de **20.8 %**.
- Las ocupaciones que concentraron mayores ingresos fueron Compensation Analyst, Sales Representative, Marketing Manager, Cost Accountant y Assistant Media Planner.
- Los resultados permiten identificar diferencias y asociaciones en las ventas, pero no permiten demostrar causalidad ni determinar rentabilidad, utilidad o margen debido a las limitaciones de los datos.