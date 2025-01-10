from pulp import LpProblem, LpMinimize, LpVariable, lpSum
import random

def optimizar_gestion_residuos(
    actividades,
    municipalidades,
    residuos_generados,
    costos_actividad,
    impacto_actividad,
    presupuesto_municipal,
    max_fondos_actividad,
    max_reduccion_porcentual
):
    problema = LpProblem("Optimizacion_Gestion_Residuos", LpMinimize)

    fondos = {
        (a, m): LpVariable(f"fondos_{a}_{m}", lowBound=0)
        for a in actividades for m in municipalidades
    }

    problema += lpSum(
        residuos_generados[m] * (1 - lpSum(impacto_actividad[a, m] * fondos[a, m] for a in actividades) / 100)
        for m in municipalidades
    )

    for m in municipalidades:
        problema += lpSum(fondos[a, m] for a in actividades) <= presupuesto_municipal[m]

    for a in actividades:
        for m in municipalidades:
            problema += fondos[a, m] <= max_fondos_actividad[a, m]

    for m in municipalidades:
        problema += lpSum(impacto_actividad[a, m] * fondos[a, m] for a in actividades) <= max_reduccion_porcentual[m]

    problema.solve()

    resultados = {
        (a, m): fondos[a, m].varValue for a in actividades for m in municipalidades
    }
    return resultados, problema.objective.value()

# Generar 10 ejemplos con datos diferentes

def generar_ejemplos():
    ejemplos = []
    actividades = ["Educacion Ambiental", "Reciclaje", "Economia Circular"]
    municipalidades = ["A", "B", "C"]

    for i in range(10):
        residuos_generados = {m: random.randint(100, 500) for m in municipalidades}
        costos_actividad = {
            (a, m): random.randint(5, 20) for a in actividades for m in municipalidades
        }
        impacto_actividad = {
            (a, m): random.uniform(1, 10) for a in actividades for m in municipalidades
        }
        presupuesto_municipal = {m: random.randint(200, 500) for m in municipalidades}
        max_fondos_actividad = {
            (a, m): random.randint(50, 150) for a in actividades for m in municipalidades
        }
        max_reduccion_porcentual = {m: random.randint(20, 50) for m in municipalidades}

        ejemplos.append({
            "residuos_generados": residuos_generados,
            "costos_actividad": costos_actividad,
            "impacto_actividad": impacto_actividad,
            "presupuesto_municipal": presupuesto_municipal,
            "max_fondos_actividad": max_fondos_actividad,
            "max_reduccion_porcentual": max_reduccion_porcentual
        })
    return ejemplos

ejemplos = generar_ejemplos()

# Resolver los ejemplos
def resolver_ejemplos(ejemplos):
    resultados = []
    for idx, ejemplo in enumerate(ejemplos):
        print(f"Ejemplo {idx + 1}:")
        resultado, objetivo = optimizar_gestion_residuos(
            ["Educacion Ambiental", "Reciclaje", "Economia Circular"],
            ["A", "B", "C"],
            ejemplo["residuos_generados"],
            ejemplo["costos_actividad"],
            ejemplo["impacto_actividad"],
            ejemplo["presupuesto_municipal"],
            ejemplo["max_fondos_actividad"],
            ejemplo["max_reduccion_porcentual"]
        )
        resultados.append((resultado, objetivo))
        print("Resultado:", resultado)
        print("Objetivo:", objetivo)
        print("\n")
    return resultados

resultados = resolver_ejemplos(ejemplos)
