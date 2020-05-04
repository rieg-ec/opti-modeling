'''
En este archivo recopilo los datos que descargue de
https://www.eia.gov/beta/electricity/gridmonitor/dashboard/electric_overview/US48/US48
con los cambios en la demanda en estados unidos por hora durante un mes desde el dia 4 de abril 2020 al
3 de mayo 2020, y los cambios diarios de energia durante un ano.
'''

import pandas as pd
from datetime import datetime
from collections import defaultdict
import numpy as np

class Synthesize:
    def __init__(self):
        self.hourly = 'data/hourly.json'
        self.daily = 'data/daily.json'

    def read_data(self, datafile):
        df = pd.read_json(datafile)
        # lo que nos interesa es la fila 'US48 demand'
        # es la primera fila en la columna 'series', la cual es un dict que contiene los datos
        # bajo la llave 'data', esto retorna una lista donde cada elemento es un diccionario con dos elementos,
        # la fecha/hora y la demanda

        demand = df.series.values[0]['data']

        demand_per_period = defaultdict(list)

        for dicc in demand:
            # por alguna razon el archivo .json de los datos anuales venia con cada dia repetido una vez,
            # y el dia repetido tenia valor nulo
            if dicc['value'] is not None:
                demand = dicc['value'] * 1000 # los valores estan en MWh, por lo tanto los pasamos a kWh

                if datafile == 'data/hourly.json':
                    # en este archivo queremos saber los cambios hora a hora de la demanda
                    timestamp = dicc['Timestamp (Hour Ending)'].replace(' EDT', '').replace('a.m.', 'AM').replace('p.m.', 'PM')
                    timestamp = datetime.strptime(timestamp, '%m/%d/%Y %I %p') # convertir timestamp a un objeto datetime
                    demand_per_period[timestamp.hour].append(demand)
                elif datafile == 'data/daily.json':
                    # en este archivo queremos saber los cambios mes a mes en la demanda
                    timestamp = datetime.strptime(dicc['Timestamp (Hour Ending)'].replace(', Eastern Time', ''), '%m/%d/%Y')
                    demand_per_period[timestamp.month].append(demand)

        if datafile == 'data/daily.json':
            # ordenar por mes
            keys = sorted(demand_per_period, key=lambda x: int(x))
            demand_per_period = {key:demand_per_period[key] for key in keys}
        return demand_per_period

    def synthesize_data(self, periods):
        n_periods_day = int(periods/365) # numero de periodos por dia
        daily = self.read_data(self.daily)
        hourly = self.read_data(self.hourly)
        for hour in hourly.keys():
            hourly[hour] = np.mean(hourly[hour]) # solo nos interesa el promedio
        # ahora cambiamos el formato de hourly, en vez de ser 24 horas, agrupamos la demanda en periodos
        # de a 6 horas:
        periods_day = defaultdict(int) # periodos en un solo dia
        for i in range(1, n_periods_day+1):
            demand = 0
            for j in range((i-1)*int(1+24/n_periods_day), i*int(24/n_periods_day)):
                demand += hourly[j]
            periods_day[i] = demand

        # calculamos el promedio de demanda diario para usar como referencia en la variacion porcentual
        mean_demand_daily = sum([sum(i) for i in daily.values()]) / sum([len(i) for i in daily.values()])
        periods_year = defaultdict(int)
        period_count = 1
        for month in daily:
            for day in daily[month]:
                pv = day / mean_demand_daily # diferencia porcentual respecto al promedio
                for c in range(1, n_periods_day+1):
                    periods_year[str(period_count)] = periods_day[c] * pv
                    period_count += 1

        return periods_year

print(Synthesize().synthesize_data(1460))
