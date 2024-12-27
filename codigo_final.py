from pulp import LpProblem, LpMinimize, LpVariable, lpSum

def planificar_hospital(prioridad, pacientes, capacidad, recursos_por_paciente, recursos_disponibles):
    """
    Resuelve el problema de planificación hospitalaria basado en los parámetros dados.

    Parámetros:
        - prioridad (list): Lista con la prioridad de cada especialidad.
        - pacientes (list): Lista con el número de pacientes en lista de espera por especialidad.
        - capacidad (list of lists): Matriz de capacidad semanal por especialidad y semana.
        - recursos_por_paciente (list): Lista de recursos necesarios por paciente por especialidad.
        - recursos_disponibles (list): Lista de recursos disponibles por semana.

    Retorna:
        - dict: Diccionario con los valores de las variables de decisión y el valor de la función objetivo.
    """
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

    # Recopilar resultados
    resultados = {
        "estado": problema.status,
        "variables": {},
        "funcion_objetivo": problema.objective.value()
    }

    for i in range(num_especialidades):
        for j in range(num_semanas):
            resultados["variables"][f"x_{i+1}_{j+1}"] = x[i][j].varValue

    return resultados

# Ejemplos de uso
def main():
    #Ejemplo 1:
    prioridad_ej_1 = [5, 3, 4]  # p[i]: prioridad de cada especialidad
    pacientes_ej_1 = [20, 15, 25]  # d[i]: pacientes en lista de espera
    capacidad_ej_1 = [
        [5, 6, 4, 5],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [4, 3, 5, 2],
        [6, 5, 7, 6]
    ]
    recursos_por_paciente_ej_1 = [2, 3, 1]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_1 = [30, 25, 35, 40]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 2:
    prioridad_ej_2 = [5, 3, 4, 1]  # p[i]: prioridad de cada especialidad
    pacientes_ej_2 = [20, 15, 25, 18]  # d[i]: pacientes en lista de espera
    capacidad_ej_2 = [
        [5, 6, 4, 5],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [4, 3, 5, 2],
        [6, 5, 7, 6],
        [3, 7, 8, 4]
    ]
    recursos_por_paciente_ej_2 = [2, 3, 1, 4]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_2 = [30, 25, 35, 40]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 3:
    prioridad_ej_3 = [4, 2, 3, 5, 1]  # p[i]: prioridad de cada especialidad
    pacientes_ej_3 = [15, 17, 30, 23, 27]  # d[i]: pacientes en lista de espera
    capacidad_ej_3 = [
        [5, 6, 4, 5, 7],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [4, 3, 5, 2, 6],
        [6, 5, 7, 6, 4],
        [3, 7, 8, 4, 5],
        [2, 4, 7, 5, 6]
    ]
    recursos_por_paciente_ej_3 = [7, 4, 3, 5, 2]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_3 = [25, 24, 35, 40, 23]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 4:
    prioridad_ej_4 = [5, 2, 3]  # p[i]: prioridad de cada especialidad
    pacientes_ej_4 = [10, 19, 13]  # d[i]: pacientes en lista de espera
    capacidad_ej_4 = [
        [6, 5, 7, 6, 4],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [3, 7, 8, 4, 5],
        [2, 4, 7, 5, 6]
    ]
    recursos_por_paciente_ej_4 = [4, 2, 6]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_4 = [10, 7, 20, 20, 8]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 5:
    prioridad_ej_5 = [6, 2, 3, 1, 4]  # p[i]: prioridad de cada especialidad
    pacientes_ej_5 = [33, 19, 13, 15, 26]  # d[i]: pacientes en lista de espera
    capacidad_ej_5 = [
        [6, 5, 7],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [3, 7, 8],
        [2, 4, 7],
        [5, 7, 9],
        [9, 3, 7]
    ]
    recursos_por_paciente_ej_5 = [5, 2, 4, 2, 1]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_5 = [9, 12, 7]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 6:
    prioridad_ej_6 = [5, 3, 4, 2]  # p[i]: prioridad de cada especialidad
    pacientes_ej_6 = [29, 15, 20, 11]  # d[i]: pacientes en lista de espera
    capacidad_ej_6 = [
        [6, 7, 8, 9],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [4, 5, 6, 7],
        [7, 8, 9, 10],
        [5, 6, 7, 8]
    ]
    recursos_por_paciente_ej_6 = [6, 3, 2, 4]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_6 = [27, 25, 31, 42]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 7:
    prioridad_ej_7 = [4, 5, 3]  # p[i]: prioridad de cada especialidad
    pacientes_ej_7 = [22, 18, 20]  # d[i]: pacientes en lista de espera
    capacidad_ej_7 = [
        [6, 9, 9],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [14, 5, 3],
        [7, 2, 5]
    ]
    recursos_por_paciente_ej_7 = [4, 4, 2]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_7 = [11, 30, 21]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 8:
    prioridad_ej_8 = [6, 1, 3, 2, 5]  # p[i]: prioridad de cada especialidad
    pacientes_ej_8 = [40, 20, 18, 10, 24]  # d[i]: pacientes en lista de espera
    capacidad_ej_8 = [
        [4, 8, 2, 7],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [5, 1, 7, 9],
        [6, 6, 8, 3],
        [4, 3, 9, 10],
        [5, 2, 8, 8]
    ]
    recursos_por_paciente_ej_8 = [7, 1, 4, 5, 7]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_8 = [9, 19, 34, 15]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 9:
    prioridad_ej_9 = [2, 5, 3, 1]  # p[i]: prioridad de cada especialidad
    pacientes_ej_9 = [34, 29, 10, 40]  # d[i]: pacientes en lista de espera
    capacidad_ej_9 = [
        [4, 8, 2, 7],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [7, 2, 6, 9],
        [9, 6, 8, 5],
        [4, 3, 9, 12]
    ]
    recursos_por_paciente_ej_9 = [1, 2, 1, 3]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_9 = [27, 29, 30, 35]  # R[j]: recursos disponibles en cada semana

    #Ejemplo 10:
    prioridad_ej_10 = [2, 4, 3]  # p[i]: prioridad de cada especialidad
    pacientes_ej_10 = [13, 24, 21]  # d[i]: pacientes en lista de espera
    capacidad_ej_10 = [
        [4, 6, 9],  # c[i][j]: capacidad semanal para cada especialidad i, semana j
        [7, 5, 4],
        [9, 6, 8]
    ]
    recursos_por_paciente_ej_10 = [2, 4, 2]  # r[i]: recursos necesarios por paciente de especialidad i
    recursos_disponibles_ej_10 = [18, 18, 19]  # R[j]: recursos disponibles en cada semana
    #FIN DE EJEMPLOS

    #Se resuelva ejemplos cambiando solamente numero de ejemplo dentro de parametros
    resultados = planificar_hospital(prioridad_ej_10, pacientes_ej_10, capacidad_ej_10, recursos_por_paciente_ej_10, recursos_disponibles_ej_10)

    # Mostrar los resultados
    print("Estado de la solución:", resultados["estado"])
    for variable, valor in resultados["variables"].items():
        print(f"{variable}: {valor}")
    print("Valor de la función objetivo:", resultados["funcion_objetivo"])

if __name__ == "__main__":
    main()
