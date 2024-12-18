from docplex.mp.model import Model # type: ignore

# Crear modelo de optimización
mdl = Model(name="Lista_de_espera")

# Parámetros del problema
pacientes = ["P1", "P2", "P3", "P4", "P5"]  # Ejemplo: 5 pacientes
horas_disponibles = 40  # Total de horas médicas disponibles en un mes
tiempo_por_paciente = {"P1": 5, "P2": 8, "P3": 6, "P4": 4, "P5": 7}  # Tiempo requerido por paciente
prioridad = {"P1": 3, "P2": 5, "P3": 2, "P4": 4, "P5": 1}  # Prioridad de atención (mayor es más prioritario)

# Variables de decisión
# x[i] = 1 si el paciente i es atendido, 0 en caso contrario
x = mdl.binary_var_dict(pacientes, name="x")

# Función objetivo: maximizar la prioridad total de los pacientes atendidos
mdl.maximize(mdl.sum(prioridad[i] * x[i] for i in pacientes))

# Restricción: El tiempo total de atención no puede superar las horas disponibles
mdl.add_constraint(mdl.sum(tiempo_por_paciente[i] * x[i] for i in pacientes) <= horas_disponibles, 
                   "Horas_disponibles")

# Resolver el modelo
solution = mdl.solve()

# Mostrar resultados
if solution:
    print("Solución encontrada:")
    for i in pacientes:
        print(f"Paciente {i}: {'Atendido' if x[i].solution_value == 1 else 'No atendido'}")
    print(f"Prioridad total maximizada: {solution.objective_value}")
else:
    print("No se encontró solución factible.")
