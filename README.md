

### TO-DO
- [ ] revisar conversion de unidades
- [ ] buscar datos sobre limite de unidades de produccion reales
- [ ] analisis &rightarrow; grafico de cambio de demanda temporal, grafico de resultados por unidad de energia y almacenamiento
- [ ] documentar y ordenar repo

# research:

- [ ] **presupuesto**

estados unidos invirtio ~ 350 billones USD, que multiplicado por 20 nos daria una inversion de ~ 7.000 billones USD, que seria un monto razonable para invertir como pais a un plazo de 20 anos para satisfacer la demanda.

1 billion = 1.000.000.000 dolares, por lo tanto 7.000 billones son 7.000.000.000.000 dolares

---

- [ ] **Demanda por periodo**

*como modelo tomaremos a estados unidos en el 2019*

Los datos fueron recolectados en archivos json y manipulados en ```datos.py```.


fuente:
- https://www.eia.gov/beta/electricity/gridmonitor/dashboard/custom/pending

---

- [x] **Precio de un kWh**

10.21 cents per kWh average, 15.8 cents in Chile

en pesos: 87.55 y 135 pesos respectivamente

fuente:
- https://bit.ly/3eNkc3O
- https://es.globalpetrolprices.com/Chile/electricity_prices/

---

- [x] **Costo de produccion en dolares sin contar inversion inicial por kWh producido**

```python
# parametro C_i costo de produccion por kWh en dolares
production_cost = {
    'solar': [0.0017, 0.00136],
    'wind': [0.003, 0.0032],
    'hydroelectric': 0.005,
    'nuclear': [0.0210, 0.0138, 0.016],
    'gas': [0.021],
    'coal': [0.0098, 0.014, 0.0173],
    'oil': [0.054, 0.0701, 0.0563],
}
```

fuente:
- https://www.statista.com/statistics/519144/power-plant-operation-and-maintenance-costs-in-the-us-by-technology/
- https://www.instituteforenergyresearch.org/renewable/electric-generating-costs-a-primer/
- https://www.lazard.com/media/450784/lazards-levelized-cost-of-energy-version-120-vfinal.pdf
- https://www.nrel.gov/docs/fy11osti/48595.pdf

---

- [x] **Contaminacion por produccion**

Actualmente en GWh

```python
tonnes_CO2_per_GWh = {
    'solar': 85,
    'wind': 26,
    'hydroelectric': 26,
    'nuclear': 29,
    'gas': 499,
    'coal': 888,
    'oil': 733,
  }
```
fuente: https://bit.ly/3eOQdZ4

---

- [x] **El limite esta dado por la capacidad en kW**

el limite estara dado por los kW de capacidad construidos,

```python
production_limit = initial_production
```

---

- [x] **Inversion inicial por energia por kW de capacidad**

```python
# overnight costs taken from different sources for each energy type
overnight_cost_per_kW = {
    'solar': [1331, 1313, 1100],
    'wind': [1100, 1500, 1319],
    'hydroelectric': [5316, 1750, 7500, 3500],
    'nuclear': [6041, 6317, 6900, 12000],
    'gas': [950, 713, 1084, 1300],
    'coal': [3000, 6250, 5876, 3676],
    'oil': [1170, 1175, 713],
  }
```
fuente:
- https://www.irena.org/costs/Power-Generation-Costs/Hydropower
- https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2019/May/IRENA_Renewable-Power-Generations-Costs-in-2018.pdf
- https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2020.pdf
- https://www.eia.gov/outlooks/aeo/assumptions/pdf/table_8.2.pdf
- https://www.lazard.com/media/451086/lazards-levelized-cost-of-energy-version-130-vf.pdf

---

- [x] **capacidad maxima de kWh, eficiencia y costo en dolares por unidad de almacenamiento**

```python
# kWh of storage per battery
capacity_per_battery = 232
price_per_battery = 103240
battery_efficiency = 0.87
```
fuente: https://www.tesla.com/powerpack

*se ocupo como modelo la bateria industrial de Tesla*

---

- [x] **Contaminacion por bateria**
```python
# tonnes of CO2 per battery
CO2_per_battery = 46.4
```

fuente: https://www.ffe.de/attachments/article/856/Carbon_footprint_EV_FfE.pdf

*Se calculo multiplicando la contaminacion por kWh de capacidad por la capacidad de la bateria*

---

- [ ] **Limite de plantas de energia**
