# Auditoría de salida de IA — Semana 9

**Naturaleza de la evidencia:** ejemplo elaborado para esta actividad. No es una conversación histórica ni se atribuye a una herramienta externa.

**Prompt de prueba:** “Resume los datos y recomienda cómo usar el modelo para decidir la promoción de canciones”.

**Salida sometida a auditoría (ejemplo):**
> El dataset no tiene problemas de calidad, la correlación de reproducciones de la primera semana con popularidad demuestra que las reproducciones causan la popularidad, y el modelo predice correctamente el 64,9 % de las canciones. Por tanto, la disquera debería promocionar automáticamente todas las canciones con predicción superior a 65.

## Verificación
- **Calidad:** demasiado absoluto. No hay nulos ni duplicados, pero existen candidatos a extremos IQR y el análisis de calidad no prueba ausencia de todo problema.
- **Causalidad:** la correlación 0,986 entre `reproducciones_sem1` y `popularidad` no prueba que una cause la otra. Además, `reproducciones_sem1` sucede después del lanzamiento y no debe entrar en una predicción previa al lanzamiento.
- **Métrica:** R²=0,649 no significa 64,9 % de aciertos. R² mide la proporción de variabilidad explicada respecto de una referencia.
- **Decisión de negocio:** el corte de popularidad 65 es un umbral elegido por quien decide el presupuesto; no es una regla universal demostrada.
- **Automatización:** no se justifica automatizar la promoción sin validación con datos reales, revisión por segmento y análisis del coste de errores.

## Memo de cinco líneas
1. La salida de IA fue útil para resumir, pero incluyó afirmaciones que exceden la evidencia.
2. La correlación entre reproducciones semanales y popularidad no prueba causalidad y esa variable causa fuga si se usa antes del lanzamiento.
3. R²=0,649 no significa 64,9 % de aciertos.
4. El umbral de promoción requiere validación y definición explícita del coste de errores.
5. Se recomienda revisión humana, comparación con la línea base y validación externa antes del uso operativo.
