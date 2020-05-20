import numpy as np
import random
from data import Synthesize

PERIOD_LENGTH = 6 # numero de horas de cada periodo
N_PERIODS_YEAR = int((24/PERIOD_LENGTH) * 365) # numero de periodos per year

# conjuntos
sources = ['solar', 'wind', 'hydroelectric', 'nuclear', 'gas', 'coal', 'oil'] # conjunto _i
periods = [i for i in range(1, N_PERIODS_YEAR+1)] # conjunto _t

# parametros constantes
budget = 700000000000 # presupuesto en dolares # 7000000000000

years_return = 40 # cantidad de anos en los que se espera recuperar la inversion inicial

demand = Synthesize().synthesize_data(N_PERIODS_YEAR) # diccionario tipo {periodo:demanda}

battery_cost = 103240 # costo por bateria en dolares AC
battery_capacity = 232 # capacidad de almacenamiento en kWh por bateria AQ
battery_efficiency = 0.87 # eficiencia de energia de las baterias AE
pollution_per_battery = 46400 # kgs de CO2 emitidos por bateria producida AZ

kwh_price_mean = 0.1 # valor por kWh en el mercado promedio en dolares
kwh_price_chile = 0.16 # valor por kWh en chile en dolares

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
overnight_cost_mean = {
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
production_cost_mean = {
    key:np.mean(value) for key, value in zip(production_cost.keys(),
                                            production_cost.values())
}

# kg de CO2 emitidos por producir un kWh Z_i
kg_CO2_per_kwh = {
    'solar': 0.085,
    'wind': 0.026,
    'hydroelectric': 0.026,
    'nuclear': 0.029,
    'gas': 0.499,
    'coal': 0.888,
    'oil': 0.733,
    }

# to-do: cantidad maxima disponible para instalaciones QM_i
# prod_units_limit = {source:limit for source,
#                     limit in zip(sources, np.array([random.randint(9448046//6, 267628704//6) for _ in
#                                                                                 range(len(sources))]))}

prod_units_limit = {source:120000000 for source in sources}

from gurobipy import GRB, Model, quicksum

model = Model('Energy production planning')

prod_units = model.addVars(sources, vtype=GRB.INTEGER, name='prod_units')
storage = model.addVar(vtype=GRB.INTEGER, name='storage')
output = model.addVars(periods, sources, vtype=GRB.CONTINUOUS, name='output')
stored = model.addVars(periods, vtype=GRB.CONTINUOUS, name='stored')

model.update()


initial_investment = quicksum(prod_units[source] * overnight_cost_mean[source]
                        for source in sources) + storage * battery_cost

# restriccion 1: inversion inicial menor o igual a presupuesto
model.addConstr(initial_investment <= budget, name='budget_limit')

# restriccion 2: recuperacion de inversion (el presupuesto dividido en la cantidad de anos nos indica
# cuanto debemos recuperar cada ano)
profit = quicksum(output[period, source] * (kwh_price_mean - production_cost_mean[source])
                     for source in sources for period in periods)

model.addConstr((profit >= (initial_investment/years_return)), name='payback')

# restriccion 3: satisfaccion de demanda y flujo
model.addConstrs((stored[period] == quicksum(output[period, source] for source in sources) - demand[str(period)] +
                                            (stored[period - 1] * battery_efficiency)
                                                for idx, period in enumerate(periods) if idx != 0),
                                                                                     name='demand_meet')

# restriccion 4: produccion de energia limitada
model.addConstrs((output[period, source] <= prod_units[source] * PERIOD_LENGTH for source in sources
                                                                                for period in periods),
                                                                                 name='energy_limit')
# restriccion 5: construccion de kw de capacidad limitadas
model.addConstrs((prod_units[source] <= prod_units_limit[source] for source in sources), name='prod_limit')

# restriccion 6: cantidad maxima de almacenamiento
model.addConstrs((stored[period] <= storage * battery_capacity for period in periods), name='storage_limit')

# Naturaleza de las variables
# restriccion 7:
model.addConstrs((output[period, source] >= 0 for source in sources for period in periods), name='v_nature_7')
# restriccion 8:
model.addConstrs((prod_units[source] >= 0 for source in sources), name='v_nature_8')
# restriccion 9:
model.addConstr(storage >= 0, name='v_nature_9')
# restriccion 10 y 11:
model.addConstrs((stored[period] >= 0 for idx, period in enumerate(periods) if idx != 0), name='v_nature_10')
model.addConstrs((stored[period] == 0 for idx, period in enumerate(periods) if idx == 0), name='v_nature_11')

obj = quicksum(output[period, source] * kg_CO2_per_kwh[source]\
               for source in sources for period in periods) + storage * pollution_per_battery

model.setObjective(obj, GRB.MINIMIZE)

if __name__ == '__main__':
    model.optimize()
    print('\n---------------------\n')

    with open('slack.text', 'w') as file:
        for constr in model.getConstrs():
            file.writelines(f"{constr}: {constr.getAttr('slack')}\n")
        file.close()

    model.write('model.sol')

    with open('model_sol.txt', 'w') as file:
        for var in model.getVars():
            file.write(f'{var.varName} {var.x}\n')
        file.close()

    if model.status == GRB.INFEASIBLE:
        model.computeIIS()
        model.write('model.ilp')
