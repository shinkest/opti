# Importar PuLP para programación lineal
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

# Definir los datos del problema
dias = range(1, 6)  # Planificación para 5 días
pacientes = range(1, 101)  # 100 pacientes en espera
urgentes = set(range(1, 16))  # 15 pacientes prioritarios
capacidad_diaria = 30  # 3 médicos * 10 pacientes por día

# Crear el modelo de optimización
model = LpProblem("Gestion_Lista_Espera", LpMinimize)

# Variables de decisión: si el paciente i es atendido el día j
x = LpVariable.dicts("x", [(i, j) for i in pacientes for j in dias], cat="Binary")

# Función objetivo: minimizar el tiempo total en lista de espera
model += lpSum(j * x[i, j] for i in pacientes for j in dias), "Minimizar_Tiempo_Espera"

# Restricción 1: Cada paciente debe ser atendido exactamente un día
for i in pacientes:
    model += lpSum(x[i, j] for j in dias) == 1, f"Paciente_{i}_Atendido_Una_Vez"

# Restricción 2: No superar la capacidad diaria
for j in dias:
    model += lpSum(x[i, j] for i in pacientes) <= capacidad_diaria, f"Capacidad_Diaria_{j}"

# Restricción 3: Los pacientes urgentes deben ser atendidos en los primeros 3 días
for i in urgentes:
    model += lpSum(x[i, j] for j in range(1, 4)) == 1, f"Urgente_{i}_En_3_Dias"

# Resolver el modelo utilizando CPLEX
solver = "CPLEX_CMD"
try:
    model.solve()
except Exception as e:
    print("Error al resolver el modelo:", e)
    exit()

# Mostrar los resultados
print(f"Estado del modelo: {LpStatus[model.status]}")
print("Resultados:")
for i in pacientes:
    for j in dias:
        if x[i, j].value() == 1:
            print(f"Paciente {i} atendido el día {j}")