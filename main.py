import numpy as np
import random
from data import Synthesize
from gurobipy import GRB, quicksum
from gurobipy import Model as GurobiModel
from os import path

class Model(GurobiModel):
    Y = 6 # numero de horas de cada periodo
    N_PERIODS_YEAR = int((24/Y) * 365) # numero de periodos per year
    D_t = Synthesize().synthesize_data(N_PERIODS_YEAR) # diccionario tipo
                                                        # {periodo:demanda}
    sources = ['solar', 'wind', 'hydroelectric', 'nuclear', 'gas', 'coal', 'oil'] # conjunto _i
    periods = [i for i in range(1, N_PERIODS_YEAR+1)] # conjunto _t

    P = 700000000000 # presupuesto en dolares
    pi = 40 # cantidad de anos en los que se espera recuperar la inversion inicial
    AC = 103240 # costo por bateria en dolares
    AQ = 232 # capacidad de almacenamiento en kWh por bateria por periodo
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
    # buying limit of capacity per source
    QM_i = {source:150000000 for source in sources}

    def __init__(self, name):
        super().__init__(name)

    def __setattr__(self, attr, value):
        super().__dict__[attr] = value

    def optimize(self):
        a = self.addVar(vtype=GRB.INTEGER, name='storage', lb=0)
        xi_i = self.addVars(self.sources, vtype=GRB.INTEGER,
                            name='prod_units', lb=0)
        x_it = self.addVars(self.periods, self.sources,
                            vtype=GRB.CONTINUOUS, name='output', lb=0)
        b_t = self.addVars(self.periods, vtype=GRB.CONTINUOUS,
                        name='stored', lb=0)

        self.update()

        initial_investment = quicksum(xi_i[source] * self.CI_i[source]
                                for source in self.sources) + a * self.AC

        # restriccion 1: inversion inicial menor o igual a presupuesto
        self.addConstr(initial_investment <= self.P, name='budget_limit')

        # restriccion 2: recuperacion de inversion (el presupuesto dividido en la cantidad de anos nos indica
        # cuanto debemos recuperar cada ano)
        profit = quicksum(x_it[period, source] * (self.S - self.C_i[source])
                             for source in self.sources for period in self.periods)

        self.addConstr((profit >= (initial_investment/self.pi)), name='payback')

        # restriccion 3: satisfaccion de demanda y flujo
        self.addConstrs((b_t[period] == quicksum(x_it[period, source] for source in self.sources) - self.D_t[str(period)] +
                                                    (b_t[period - 1] * self.AE)
                                                        for idx, period in enumerate(self.periods) if idx != 0),
                                                                                             name='demand_meet')

        # restriccion 4: produccion de energia limitada
        self.addConstrs((x_it[period, source] <= xi_i[source] * self.Y for source in self.sources for period in self.periods), name='energy_limit')
        # restriccion 5: construccion de kw de capacidad limitadas
        self.addConstrs((xi_i[source] <= self.QM_i[source] for source in self.sources), name='prod_limit')

        # restriccion 6: cantidad maxima de almacenamiento
        self.addConstrs((b_t[period] <= a * self.AQ for period in self.periods), name='storage_limit')

        # restriccion 7: comenzamos sin baterias
        self.addConstrs((b_t[period] == 0 for idx, period in enumerate(self.periods) if idx == 0))

        obj = quicksum(x_it[period, source] * self.Z_i[source]\
                       for source in self.sources for period in self.periods) + a * self.AZ

        self.setObjective(obj, GRB.MINIMIZE)
        super().optimize()

    def save_results(self, where=''):
        with open(path.join(where, 'gurobi_files', 'slack.txt'), 'w') as file:
            for constr in self.getConstrs():
                file.writelines(f"{constr}: {constr.getAttr('slack')}\n")
            file.close()

        self.write(path.join(where, 'gurobi_files', 'model.sol'))

        if self.status == GRB.INFEASIBLE:
            self.computeIIS()
            self.write(path.join(where, 'gurobi_files', 'model.ilp'))

if __name__ == '__main__':
    from analysis import plot_demand, plot_results # avoids circular imports

    model = Model('Energy production planning')
    model.optimize()
    model.save_results()
    plot_demand()
    plot_results()
