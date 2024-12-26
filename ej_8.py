from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# Datos del problema
prioridad = [6, 1, 3, 2, 5]  # p[i]: prioridad de cada especialidad
pacientes = [40, 20, 18, 10, 24]  # d[i]: pacientes en lista de espera
capacidad = [
    [4, 8, 2, 7],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
    [5, 1, 7, 9],
    [6, 6, 8, 3],
    [4, 3, 9, 10],
    [5, 2, 8, 8]
]
recursos_por_paciente = [7, 1, 4, 5, 7]  # r[i]: recursos necesarios por paciente de especialidad i
recursos_disponibles = [9, 19, 34, 15]  # R[j]: recursos disponibles en cada semana

num_especialidades = len(prioridad)
num_semanas = len(recursos_disponibles)

# Crear el problema de optimización
problema = LpProblem("Planificacion_Hospitalaria", LpMinimize)

# Variables de decisión
x = [[LpVariable(f"x_{i+1}_{j+1}", lowBound=0, cat="Integer") for j in range(num_semanas)]
     for i in range(num_especialidades)]

# Función objetivo: Minimizar los pacientes no atendidos ponderados por prioridad
problema += lpSum(prioridad[i] * (pacientes[i] - lpSum(x[i][j] for j in range(num_semanas)))
                  for i in range(num_especialidades))

# Restricciones:
# 1. No atender más pacientes de los que están en lista de espera
for i in range(num_especialidades):
    problema += lpSum(x[i][j] for j in range(num_semanas)) <= pacientes[i]

# 2. No exceder la capacidad semanal por especialidad
for i in range(num_especialidades):
    for j in range(num_semanas):
        problema += x[i][j] <= capacidad[i][j]

# 3. Los recursos utilizados no deben superar los disponibles semanalmente
for j in range(num_semanas):
    problema += lpSum(recursos_por_paciente[i] * x[i][j] for i in range(num_especialidades)) <= recursos_disponibles[j]

# Resolver el problema
problema.solve()

# Mostrar los resultados
print("Estado de la solución:", problema.status)
for i in range(num_especialidades):
    for j in range(num_semanas):
        print(f"x_{i+1}_{j+1} (pacientes atendidos por especialidad {i+1} en semana {j+1}): {x[i][j].varValue}")

# Mostrar valor de la función objetivo
print("Valor de la función objetivo:", problema.objective.value())
