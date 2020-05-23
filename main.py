import numpy as np
import random
from data import Synthesize

Y = 6 # numero de horas de cada periodo
N_PERIODS_YEAR = int((24/Y) * 365) # numero de periodos per year

# conjuntos
sources = ['solar', 'wind', 'hydroelectric', 'nuclear', 'gas', 'coal', 'oil'] # conjunto _i
periods = [i for i in range(1, N_PERIODS_YEAR+1)] # conjunto _t

# parametros constantes
P = 700000000000 # presupuesto en dolares

pi = 40 # cantidad de anos en los que se espera recuperar la inversion inicial

D_t = Synthesize().synthesize_data(N_PERIODS_YEAR) # diccionario tipo {periodo:demanda}

AC = 103240 # costo por bateria en dolares
AQ = 232 # capacidad de almacenamiento en kWh por bateria
AE = 0.87 # eficiencia de energia de las baterias
AZ = 46400 # kgs de CO2 emitidos por bateria producida

S = 0.1 # valor por kWh en el mercado promedio en dolares

# parametro CI_i costo inicial por kW de capacidad en dolares
overnight_cost = {
    'solar': [1331, 1313, 1100],
    'wind': [1100, 1500, 1319],
    'hydroelectric': [5316, 1750, 7500, 3500],
    'nuclear': [6041, 6317, 6900, 12000],
    'gas': [950, 713, 1084],
    'coal': [3000, 6250, 5876, 3676],
    'oil': [1170, 1175, 713],
    }

# modelaremos ocupando la media en casos donde hayan mas de un dato
CI_i = {
    key:np.mean(value) for key, value in  zip(overnight_cost.keys(),
                                              overnight_cost.values())
}

# parametro C_i costo de produccion por kWh en dolares
production_cost = {
    'solar': [0.0017, 0.00136],
    'wind': [0.003, 0.0032],
    'hydroelectric': [0.005],
    'nuclear': [0.0210, 0.0138, 0.016],
    'gas': [0.021],
    'coal': [0.0098, 0.014, 0.0173],
    'oil': [0.054, 0.0701, 0.0563],
}

# al igual que el costo inicial, ocuparemos la media
C_i = {
    key:np.mean(value) for key, value in zip(production_cost.keys(),
                                            production_cost.values())
}

# kg de CO2 emitidos por producir un kWh Z_i
Z_i = {
    'solar': 0.085,
    'wind': 0.026,
    'hydroelectric': 0.026,
    'nuclear': 0.029,
    'gas': 0.499,
    'coal': 0.888,
    'oil': 0.733,
    }

QM_i = {source:150000000 for source in sources}

### Modelamiento ###

from gurobipy import GRB, Model, quicksum

model = Model('Energy production planning')

xi_i = model.addVars(sources, vtype=GRB.INTEGER, name='prod_units')
a = model.addVar(vtype=GRB.INTEGER, name='storage')
x_it = model.addVars(periods, sources, vtype=GRB.CONTINUOUS, name='output')
b_t = model.addVars(periods, vtype=GRB.CONTINUOUS, name='stored')

model.update()


initial_investment = quicksum(xi_i[source] * CI_i[source]
                        for source in sources) + a * AC

# restriccion 1: inversion inicial menor o igual a presupuesto
model.addConstr(initial_investment <= P, name='budget_limit')

# restriccion 2: recuperacion de inversion (el presupuesto dividido en la cantidad de anos nos indica
# cuanto debemos recuperar cada ano)
profit = quicksum(x_it[period, source] * (S - C_i[source])
                     for source in sources for period in periods)

model.addConstr((profit >= (initial_investment/pi)), name='payback')

# restriccion 3: satisfaccion de demanda y flujo
model.addConstrs((b_t[period] == quicksum(x_it[period, source] for source in sources) - D_t[str(period)] +
                                            (b_t[period - 1] * AE)
                                                for idx, period in enumerate(periods) if idx != 0),
                                                                                     name='demand_meet')

# restriccion 4: produccion de energia limitada
model.addConstrs((x_it[period, source] <= xi_i[source] * Y for source in sources
                                                                                for period in periods),
                                                                                 name='energy_limit')
# restriccion 5: construccion de kw de capacidad limitadas
model.addConstrs((xi_i[source] <= QM_i[source] for source in sources), name='prod_limit')

# restriccion 6: cantidad maxima de almacenamiento
model.addConstrs((b_t[period] <= a * AQ for period in periods), name='storage_limit')

# Naturaleza de las variables
# restriccion 7:
model.addConstrs((x_it[period, source] >= 0 for source in sources for period in periods), name='v_nature_7')
# restriccion 8:
model.addConstrs((xi_i[source] >= 0 for source in sources), name='v_nature_8')
# restriccion 9:
model.addConstr(a >= 0, name='v_nature_9')
# restriccion 10 y 11:
model.addConstrs((b_t[period] >= 0 for idx, period in enumerate(periods) if idx != 0), name='v_nature_10')
model.addConstrs((b_t[period] == 0 for idx, period in enumerate(periods) if idx == 0), name='v_nature_11')

obj = quicksum(x_it[period, source] * Z_i[source]\
               for source in sources for period in periods) + a * AZ

model.setObjective(obj, GRB.MINIMIZE)

if __name__ == '__main__':
    model.optimize()
    print('\n---------------------\n')

    with open('gurobi_files/slack.text', 'w') as file:
        for constr in model.getConstrs():
            file.writelines(f"{constr}: {constr.getAttr('slack')}\n")
        file.close()

    model.write('gurobi_files/model.sol')

    with open('gurobi_files/model_sol.txt', 'w') as file:
        for var in model.getVars():
            file.write(f'{var.varName} {var.x}\n')
        file.close()

    if model.status == GRB.INFEASIBLE:
        model.computeIIS()
        model.write('gurobi_files/model.ilp')
