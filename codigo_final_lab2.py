from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

def optimizar_gestion_residuos(municipalidades, actividades, R, F, I, C):
    """
    Función para optimizar la gestión de residuos minimizando los residuos finales.
    
    Parámetros:
    - municipalidades: Lista de municipalidades.
    - actividades: Lista de actividades disponibles.
    - R: Diccionario con residuos anuales generados (toneladas) por municipalidad.
    - F: Diccionario con fondos disponibles (pesos chilenos) por municipalidad.
    - I: Diccionario con impacto (toneladas evitadas por peso invertido) por actividad.
    - C: Diccionario con costo mínimo de cada actividad (pesos chilenos).
    
    Retorno:
    - results: Diccionario con los fondos asignados y residuos reducidos por municipalidad.
    - objetivo: Valor de la función objetivo (residuos totales minimizados).
    """
    # Variables de decisión
    x = {(a, m): LpVariable(f"x_{a}_{m}", lowBound=0, cat='Continuous') for a in actividades for m in municipalidades}
    y = {m: LpVariable(f"y_{m}", lowBound=0, cat='Continuous') for m in municipalidades}

    # Problema de optimización
    model = LpProblem("Gestion_de_Residuos", LpMinimize)

    # Función objetivo: Minimizar residuos finales
    model += lpSum(R[m] - y[m] for m in municipalidades), "Minimizar_Residuos_Finales"

    # Restricciones
    for m in municipalidades:
        # Cálculo de reducción de residuos
        model += y[m] == lpSum((I[a] * x[a, m]) / C[a] for a in actividades), f"Calculo_Reduccion_Residuos_{m}"
        # Restricción de presupuesto
        model += lpSum(x[a, m] for a in actividades) <= F[m], f"Presupuesto_{m}"
        # Límite de residuos reducidos
        model += y[m] <= R[m], f"Limite_Residuos_Reducidos_{m}"

    for a in actividades:
        for m in municipalidades:
            # Asignación mínima por actividad
            model += x[a, m] >= C[a], f"Asignacion_Minima_{a}_{m}"

    # Resolver el modelo
    model.solve()

    # Preparar resultados
    results = {}
    for m in municipalidades:
        results[m] = {
            "reduccion_residuos": y[m].varValue,
            "fondos_asignados": {a: x[a, m].varValue for a in actividades}
        }
    objetivo = model.objective.value()

    return results, objetivo

# 10 Ejemplos
municipalidades = ['M1', 'M2', 'M3']
actividades = ['Educacion_Ambiental', 'Fomento_Reciclaje', 'Economia_Circular']

# Ejemplo 1
R1 = {'M1': 330900, 'M2': 258300, 'M3': 202600}
F1 = {'M1': 1000000, 'M2': 800000, 'M3': 600000}
I1 = {'Educacion_Ambiental': 5000, 'Fomento_Reciclaje': 10000, 'Economia_Circular': 15000}
C1 = {'Educacion_Ambiental': 100000, 'Fomento_Reciclaje': 200000, 'Economia_Circular': 300000}

# Ejemplo 2
R2 = {'M1': 350000, 'M2': 270000, 'M3': 190000}
F2 = {'M1': 1200000, 'M2': 750000, 'M3': 500000}
I2 = {'Educacion_Ambiental': 6000, 'Fomento_Reciclaje': 12000, 'Economia_Circular': 18000}
C2 = {'Educacion_Ambiental': 110000, 'Fomento_Reciclaje': 220000, 'Economia_Circular': 330000}

# Ejemplo 3
R3 = {'M1': 400000, 'M2': 250000, 'M3': 220000}
F3 = {'M1': 1000000, 'M2': 800000, 'M3': 700000}
I3 = {'Educacion_Ambiental': 7000, 'Fomento_Reciclaje': 15000, 'Economia_Circular': 20000}
C3 = {'Educacion_Ambiental': 120000, 'Fomento_Reciclaje': 240000, 'Economia_Circular': 360000}

# Ejemplo 4
R4 = {'M1': 370000, 'M2': 290000, 'M3': 390000}
F4 = {'M1': 1300000, 'M2': 850000, 'M3': 690000}
I4 = {'Educacion_Ambiental': 9000, 'Fomento_Reciclaje': 13000, 'Economia_Circular': 16000}
C4 = {'Educacion_Ambiental': 100000, 'Fomento_Reciclaje': 250000, 'Economia_Circular': 350000}

# Ejemplo 5
R5 = {'M1': 310000, 'M2': 260000, 'M3': 210000}
F5 = {'M1': 900000, 'M2': 700000, 'M3': 600000}
I5 = {'Educacion_Ambiental': 8000, 'Fomento_Reciclaje': 14000, 'Economia_Circular': 17000}
C5 = {'Educacion_Ambiental': 90000, 'Fomento_Reciclaje': 230000, 'Economia_Circular': 320000}

# Ejemplo 6
R6 = {'M1': 300000, 'M2': 240000, 'M3': 200000}
F6 = {'M1': 800000, 'M2': 600000, 'M3': 500000}
I6 = {'Educacion_Ambiental': 4000, 'Fomento_Reciclaje': 11000, 'Economia_Circular': 15000}
C6 = {'Educacion_Ambiental': 100000, 'Fomento_Reciclaje': 200000, 'Economia_Circular': 300000}

# Ejemplo 7
R7 = {'M1': 290000, 'M2': 250000, 'M3': 220000}
F7 = {'M1': 1100000, 'M2': 700000, 'M3': 400000}
I7 = {'Educacion_Ambiental': 5500, 'Fomento_Reciclaje': 12500, 'Economia_Circular': 16000}
C7 = {'Educacion_Ambiental': 120000, 'Fomento_Reciclaje': 240000, 'Economia_Circular': 340000}

# Ejemplo 8
R8 = {'M1': 350000, 'M2': 270000, 'M3': 200000}
F8 = {'M1': 950000, 'M2': 650000, 'M3': 550000}
I8 = {'Educacion_Ambiental': 7000, 'Fomento_Reciclaje': 13000, 'Economia_Circular': 17000}
C8 = {'Educacion_Ambiental': 110000, 'Fomento_Reciclaje': 220000, 'Economia_Circular': 320000}

# Ejemplo 9
R9 = {'M1': 280000, 'M2': 260000, 'M3': 230000}
F9 = {'M1': 870000, 'M2': 720000, 'M3': 670000}
I9 = {'Educacion_Ambiental': 4500, 'Fomento_Reciclaje': 12500, 'Economia_Circular': 15500}
C9 = {'Educacion_Ambiental': 95000, 'Fomento_Reciclaje': 210000, 'Economia_Circular': 310000}

# Ejemplo 10
R10 = {'M1': 320000, 'M2': 250000, 'M3': 190000}
F10 = {'M1': 920000, 'M2': 670000, 'M3': 460000}
I10 = {'Educacion_Ambiental': 6000, 'Fomento_Reciclaje': 14000, 'Economia_Circular': 19000}
C10 = {'Educacion_Ambiental': 105000, 'Fomento_Reciclaje': 230000, 'Economia_Circular': 330000}

# Llamar la función
resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R1, F1, I1, C1)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R2, F2, I2, C2)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R3, F3, I3, C3)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R4, F4, I4, C4)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R5, F5, I5, C5)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R6, F6, I6, C6)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R7, F7, I7, C7)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R8, F8, I8, C8)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R9, F9, I9, C9)
#resultados, objetivo = optimizar_gestion_residuos(municipalidades, actividades, R10, F10, I10, C10)


# Imprimir resultados
print("Resultados:")
for m, data in resultados.items():
    print(f"Municipalidad: {m}")
    print(f"  Reducción de residuos: {data['reduccion_residuos']:.2f} toneladas")
    for a, fondos in data['fondos_asignados'].items():
        print(f"  Fondos asignados a {a}: ${fondos:.2f}")
print(f"\nObjetivo (residuos totales minimizados): {objetivo:.2f}")
