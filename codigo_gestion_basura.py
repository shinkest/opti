from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Conjuntos de municipalidades y actividades
municipalidades = ['M1', 'M2', 'M3']
actividades = ['Educacion_Ambiental', 'Fomento_Reciclaje', 'Economia_Circular']

# Parámetros
R = {'M1': 330900, 'M2': 258300, 'M3': 202600}  # Residuos anuales generados (en toneladas)
F = {'M1': 1000000, 'M2': 800000, 'M3': 600000}  # Fondos disponibles (en pesos chilenos)
I = {'Educacion_Ambiental': 5000, 'Fomento_Reciclaje': 10000, 'Economia_Circular': 15000}  # Impacto (toneladas evitadas por peso invertido)
C = {'Educacion_Ambiental': 100000, 'Fomento_Reciclaje': 200000, 'Economia_Circular': 300000}  # Costo mínimo de cada actividad (en pesos chilenos)

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

# Resultados
print("Estado del problema:", model.status)
for m in municipalidades:
    print(f"Reducción de residuos en {m}: {y[m].varValue:.2f} toneladas")
    for a in actividades:
        print(f"  Fondos asignados a {a} en {m}: ${x[a, m].varValue:.2f}")
print("\nObjetivo (residuos totales minimizados):", model.objective.value())
