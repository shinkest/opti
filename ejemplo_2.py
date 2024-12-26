import random
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD

# Generar 10 ejemplos distintos
def generar_ejemplos():
    ejemplos = []
    for _ in range(10):
        n = random.randint(3, 5)  # Número de especialidades (entre 3 y 5)
        semanas = 4

        p = [random.randint(1, 10) for _ in range(n)]  # Prioridades
        d = [random.randint(20, 50) for _ in range(n)]  # Pacientes en espera
        c = [[random.randint(5, 15) for _ in range(semanas)] for _ in range(n)]  # Capacidad semanal
        r = [random.randint(1, 3) for _ in range(n)]  # Recursos por paciente
        R = [random.randint(50, 100) for _ in range(semanas)]  # Recursos disponibles por semana

        ejemplos.append({"n": n, "p": p, "d": d, "c": c, "r": r, "R": R})

    return ejemplos

ejemplos = generar_ejemplos()

# Resolver un ejemplo con PuLP
def resolver_ejemplo(ejemplo):
    n = ejemplo["n"]
    p = ejemplo["p"]
    d = ejemplo["d"]
    c = ejemplo["c"]
    r = ejemplo["r"]
    R = ejemplo["R"]
    semanas = len(R)

    # Crear el modelo
    problema = LpProblem("Minimizacion_Pacientes_No_Atendidos", LpMinimize)

    # Variables de decisión
    x = [[LpVariable(f"x_{i}_{j}", lowBound=0, cat="Integer") for j in range(semanas)] for i in range(n)]

    # Función objetivo
    problema += lpSum(p[i] * (d[i] - lpSum(x[i][j] for j in range(semanas))) for i in range(n)), "Funcion_Objetivo"

    # Restricciones
    for i in range(n):
        # Restricción 1: No atender más pacientes de los que hay en lista de espera
        problema += lpSum(x[i][j] for j in range(semanas)) <= d[i], f"Pacientes_Especialidad_{i}"

        for j in range(semanas):
            # Restricción 2: Capacidad máxima semanal por especialidad
            problema += x[i][j] <= c[i][j], f"Capacidad_{i}_{j}"

    for j in range(semanas):
        # Restricción 3: Recursos disponibles por semana
        problema += lpSum(r[i] * x[i][j] for i in range(n)) <= R[j], f"Recursos_Semana_{j}"

    # Resolver el problema
    problema.solve(PULP_CBC_CMD(msg=0))

    # Extraer resultados
    resultado = {
        "estado": problema.status,
        "objetivo": problema.objective.value(),
        "x": [[x[i][j].value() for j in range(semanas)] for i in range(n)]
    }
    return resultado

# Resolver los 10 ejemplos
def resolver_todos_los_ejemplos(ejemplos):
    resultados = []
    for idx, ejemplo in enumerate(ejemplos):
        print(f"Resolviendo ejemplo {idx + 1}...")
        resultado = resolver_ejemplo(ejemplo)
        resultados.append(resultado)
        print(f"Estado: {resultado['estado']}, Objetivo: {resultado['objetivo']}")
        print("x:", resultado["x"])
    return resultados

resultados = resolver_todos_los_ejemplos(ejemplos)
