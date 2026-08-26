# Análisis de Riesgo Laboral y Gestión Preventiva

## 1. Descripción del proyecto

Este proyecto corresponde al **Lab Aplicado Data Analytics #2: Risk Management & OSH Analytics**, cuyo objetivo es analizar información de trabajadores, empresas e incidentes laborales para identificar patrones de riesgo y convertirlos en recomendaciones preventivas.

El análisis se desarrolló utilizando la metodología **CRISP-DM**, con un enfoque iterativo. La información inicial permitió responder las preguntas principales del negocio y, posteriormente, los resultados obtenidos llevaron a generar nuevas segmentaciones y validaciones para profundizar el análisis.

## 2. Problema de negocio

Un conglomerado de **150 empresas** presenta preocupación por los accidentes laborales y su impacto humano y productivo. La necesidad de negocio no consiste únicamente en conocer cuántos accidentes ocurrieron, sino en identificar **dónde y bajo qué condiciones se concentra el riesgo**, con el fin de orientar acciones preventivas.

Las preguntas principales fueron:

- ¿Influye la jornada laboral en la ocurrencia de incidentes?
- ¿La capacitación está asociada con una menor tasa de incidentes?
- ¿Las empresas con sistema de gestión presentan menores tasas de incidentes?
- ¿Qué otros patrones aparecen al combinar variables como sector, jornada, capacitación y antigüedad?
- ¿Cómo convertir los hallazgos en una regla preventiva accionable?

## 3. Datos utilizados

Se trabajó con tres fuentes principales:

- **trabajadores.csv:** información del perfil de los trabajadores, incluyendo cargo, jornada, capacitación y antigüedad.
- **empresas.csv:** información de las empresas, sector económico y sistema de gestión.
- **accidentes.csv:** registros históricos de incidentes laborales asociados mediante `id_trabajador`.

## 4. Data Understanding

Se cargaron y exploraron las tres fuentes para comprender su estructura y las variables disponibles.

Durante esta etapa se identificaron las variables necesarias para construir el análisis de riesgo y se revisó la distribución de los datos.

La población final contiene:

- **3.000 trabajadores**
- **150 empresas**
- **1.067 trabajadores con incidente**
- **1.933 trabajadores sin incidente**
- **35,57 % de tasa global de incidentes**

## 5. Data Preparation — Triple Join

La información fue consolidada mediante un **Triple Join**:

1. Se relacionaron trabajadores con empresas mediante la empresa correspondiente.
2. Se incorporaron los registros de accidentes mediante `id_trabajador`.
3. Se utilizó un **Left Join** para conservar también a los trabajadores que no registraron accidentes.
4. Se creó la variable binaria `incidente`:
   - `1`: existe un accidente registrado.
   - `0`: no existe un accidente registrado.

### Validaciones

El proceso fue validado para comprobar que:

- Los **3.000 trabajadores originales** permanecieran en la tabla final.
- Los **3.000 trabajadores** fueran únicos después de la integración.
- No se perdieran trabajadores durante la unión con empresas.
- Cada trabajador con accidente tuviera su correspondiente registro.
- La variable `incidente` quedara correctamente distribuida entre casos con y sin incidente.

## 6. Primera iteración: análisis descriptivo

La primera iteración permitió obtener una visión general del comportamiento de los incidentes mediante tasas porcentuales.

Se analizaron principalmente:

- Jornada laboral.
- Capacitación.
- Sector económico.
- Sistema de gestión.

Esta etapa permitió detectar patrones iniciales y formular nuevas preguntas para profundizar el análisis.

## 7. Segunda iteración: segmentación y matrices de riesgo

A partir de los primeros resultados se realizaron análisis adicionales combinando variables.

### Sector × Jornada

Se construyeron mapas de calor y gráficos segmentados para localizar los sectores donde la jornada nocturna concentra mayores tasas de incidentes.

Los resultados destacados fueron:

- Jornada nocturna: **44,96 %**
- Jornada diurna: **32,26 %**
- Jornada mixta: **34,49 %**
- Minería + jornada nocturna: **65,63 %**
- Construcción + jornada nocturna: **58,09 %**

Esto permitió pasar de una conclusión general sobre la jornada a una identificación de segmentos específicos de mayor exposición.

### Sector × Capacitación

Se analizaron las tasas de incidentes combinando sector económico y condición de capacitación para determinar si el comportamiento observado globalmente se mantenía dentro de los sectores de mayor riesgo.

### Sector × Sistema de Gestión

Se comparó la tasa de incidentes entre empresas con y sin sistema de gestión dentro de los sectores con mayores tasas.

## 8. Capacitación

La comparación global mostró:

- **No capacitados:** 31,03 %
- **Capacitados:** 41,67 %

La condición de estar capacitado no presentó una menor tasa descriptiva de incidentes en los datos analizados.

Este resultado **no permite concluir que la capacitación aumente el riesgo ni que sea ineficaz**, porque la variable disponible solamente identifica si el trabajador fue capacitado. No contiene información suficiente sobre contenido, calidad, frecuencia u oportunidad de la capacitación.

Por esta razón, la recomendación es complementar este indicador con variables que permitan evaluar la efectividad real de las actividades de capacitación.

## 9. Sistema de gestión

La comparación global mostró:

- **Con sistema de gestión:** 31,10 %
- **Sin sistema de gestión:** 57,62 %
- **Diferencia:** 26,52 puntos porcentuales

Las empresas con sistema de gestión presentan una menor tasa de incidentes en los datos analizados. La segmentación por sector permitió profundizar este patrón dentro de los sectores de mayor exposición.

El resultado debe interpretarse como una **asociación descriptiva**, no como una demostración de causalidad.

## 10. Antigüedad y otros hallazgos adicionales

También se exploró la relación entre la antigüedad de los trabajadores y la ocurrencia de incidentes, utilizando rangos de permanencia:

- 0–2 años
- 3–5 años
- 6–10 años
- Más de 10 años

Este análisis permitió incorporar una característica individual del trabajador dentro de la evaluación del riesgo.

En conjunto, los análisis adicionales mostraron que el riesgo cambia al combinar variables y considerar el contexto. Las segmentaciones por sector y jornada localizaron concentraciones de mayor riesgo, mientras que los cruces con capacitación, sistema de gestión y antigüedad permitieron profundizar la interpretación.

## 11. Tercera iteración: validación

Antes de formular las conclusiones finales se realizaron comprobaciones adicionales sobre:

- Cantidad de trabajadores.
- Unicidad de trabajadores.
- Cantidad de incidentes.
- Distribución de la variable `incidente`.
- Relación trabajador–empresa.
- Valores faltantes.
- Categorías de las principales variables.
- Tamaño de las poblaciones detrás de cada porcentaje.

Esta etapa fue importante porque permitió evaluar no solamente las tasas, sino también la cantidad de observaciones que respaldaba cada comparación.

## 12. Principales conclusiones de negocio

### 1. Focalizar la prevención

La jornada nocturna concentra la mayor tasa de incidentes y el riesgo se intensifica en sectores como minería y construcción. Estos segmentos deben recibir prioridad en las acciones preventivas.

### 2. Replantear la evaluación de la capacitación

La condición de estar capacitado no muestra una reducción descriptiva de los incidentes. Se recomienda evaluar la capacitación considerando contenido, frecuencia, oportunidad y exposición al riesgo.

### 3. Fortalecer la gestión preventiva

Las empresas con sistema de gestión presentan una tasa de incidentes considerablemente menor que aquellas sin sistema. La implementación y seguimiento de sistemas de gestión representa una oportunidad prioritaria de prevención.

## 13. Insight accionable para un ERP

Se propone que el sistema utilice los patrones identificados para **priorizar automáticamente la prevención**.

Los trabajadores pertenecientes a **minería o construcción que desarrollen actividades durante la jornada nocturna** deberían generar una alerta preventiva para revisar sus condiciones de trabajo.

Cuando la empresa **no cuente con un sistema de gestión**, la alerta debería recibir una prioridad mayor.

La alerta puede orientar el siguiente flujo:

**Identificar → Alertar → Inspeccionar → Intervenir → Hacer seguimiento**

El objetivo es utilizar la evidencia disponible para anticipar dónde se requiere mayor atención preventiva, en lugar de actuar únicamente después de que ocurra un accidente.

## 14. Consideraciones metodológicas

El análisis es principalmente **descriptivo**. Las tasas y diferencias encontradas muestran asociaciones en los datos disponibles, pero no permiten establecer relaciones causales.

En particular, el resultado de capacitación debe interpretarse con cautela porque la variable disponible no describe la calidad ni las características de la capacitación.

Del mismo modo, la menor tasa observada en empresas con sistema de gestión no demuestra por sí sola que el sistema sea la causa de la reducción de incidentes.

## 15. Resultado final

El proyecto permitió pasar de tres fuentes de datos dispersas a una tabla consolidada de riesgo, identificar patrones generales, profundizar los hallazgos mediante iteraciones y convertir la evidencia en recomendaciones de negocio.

La lógica final del proyecto puede resumirse como:

**Datos → Integración → Exploración → Iteración → Evidencia → Decisión → Prevención**

---

### Archivos de referencia

- `trabajadores.csv`
- `empresas.csv`
- `accidentes.csv`
- `lab_Sem4_DA_20262.ipynb - Colab`
- `Lab aplicado Data Analytics #2`

### Autoría

Proyecto académico de **Data Analytics — Risk Management & OSH Analytics**, desarrollado bajo el marco metodológico CRISP-DM.
