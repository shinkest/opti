from pulp import LpProblem, LpMaximize, LpVariable, lpSum

# Datos del problema
municipalidades = ["Municipalidad1", "Municipalidad2", "Municipalidad3"]
actividades = ["Educación Ambiental", "Reciclaje", "Economía Circular"]

impacto = {
    "Educación Ambiental": 8,
    "Reciclaje": 15,
    "Economía Circular": 10,
}

fondos_disponibles = {
    "Municipalidad1": 100,
    "Municipalidad2": 120,
    "Municipalidad3": 150,
}

costos_minimos = {
    "Educación Ambiental": 20,
    "Reciclaje": 30,
    "Economía Circular": 25,
}

# Crear el problema de optimización
problema = LpProblem("Optimización_Fondos_Municipales", LpMaximize)

# Variables de decisión
fondos = {
    (a, m): LpVariable(f"fondos_{a}_{m}", lowBound=0)
    for a in actividades for m in municipalidades
}

# Variables auxiliares para diferencias cuadráticas
diferencias = {
    (a, b, m): LpVariable(f"diferencia_{a}_{b}_{m}", lowBound=0)
    for a in actividades for b in actividades for m in municipalidades if a != b
}

# Función objetivo: Maximizar el impacto total ponderado
problema += (
    lpSum(fondos[a, m] * impacto[a] for a in actividades for m in municipalidades)
    - lpSum(diferencias[a, b, m] for a in actividades for b in actividades for m in municipalidades if a != b),
    "Maximizar impacto y balancear fondos"
)

# Restricciones
# 1. Los fondos asignados no deben exceder los disponibles por municipalidad
for m in municipalidades:
    problema += lpSum(fondos[a, m] for a in actividades) <= fondos_disponibles[m], f"Restriccion_fondos_{m}"

# 2. Los fondos asignados deben cumplir los costos mínimos por actividad
for a in actividades:
    for m in municipalidades:
        problema += fondos[a, m] >= costos_minimos[a], f"Restriccion_minima_{a}_{m}"

# 3. Definir las diferencias cuadráticas con variables auxiliares
for m in municipalidades:
    for a in actividades:
        for b in actividades:
            if a != b:
                problema += diferencias[a, b, m] >= fondos[a, m] - fondos[b, m], f"DiferenciaPositiva_{a}_{b}_{m}"
                problema += diferencias[a, b, m] >= fondos[b, m] - fondos[a, m], f"DiferenciaNegativa_{a}_{b}_{m}"

# Resolver el problema
problema.solve()

# Mostrar resultados
print("Estado de la solución:", problema.status)
for a in actividades:
    for m in municipalidades:
        print(f"Fondos asignados a {a} en {m}: {fondos[a, m].varValue}")

print("Valor de la función objetivo:", problema.objective.value())
