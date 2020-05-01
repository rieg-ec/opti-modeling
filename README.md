

### TO-DO
- [x] buscar datos para todos los parametros
- [ ] hacer que la demanda sea distinta para cada periodo dentro de un dia y para cada mes de un ano
- [ ] el limite de produccion para algunas fuentes debe ser dependiente de la hora del dia y mes del ano
- [ ] buscar demandas y presupuestos proporcionales
- [ ] restriccion de satisfaccion de demanda
- [ ] revisar conversion de unidades
- [ ] corregir funcion objetivo en latex
- [ ] recuperacion de inversion en x anos &rightarrow; definir x

### TO-DO modelo:
1. ahora la contaminacion se mide solamente con contaminacion x kWh producido
2. la capacidad o limite por energia es simplemente los kW de capacidad construidos multiplicado por las horas de un periodo &rightarrow; limite en kWh para cada periodo

quedarian en total 13 parametros

### Datos recolectados:
1. [x] tipos de energia (i)
2. [x] periodos de tiempo (t)
3. [ ] presupuesto (P) &rightarrow; depende de la demanda que ocupemos, la idea es probar con distintos presupuestos
4. [x] valor GWh (S)
5. [x] costo por unidad construida (CI_i) &rightarrow; costo por kW de capacidad
6. [x] costo produccion GWh (C_i)

8. [x] contaminacion por GWh producido &rightarrow; contempla todas las fases de la produccion
9. [x] capacidad por unidad construida (K_i) &rightarrow; capacidad en kW/GW construidos
*importante: la capacidad esta en kW, para la restriccion de capacidad se debe multiplicar la capacidad por la cantidad de horas del periodo para obtener la capacidad de la planta en kWh para ese periodo*
10. [ ] demanda por periodo (D_t) &rightarrow; la idea tambien es probar con distintas demandas simulando ciudades pequenas con bajo presupuesto o ciudades mas ricas

11. [x] costo por unidad de almacenamiento (A)
12. [x] capacidad maxima de kWh por unidad de almacenamiento
13. [x] eficiencia de las unidades de almacenamiento (constante)
14. [x] Contaminacin por unidad de almacenamiento de energia (AZ)
15. [ ] Cantidad maxima disponible para instalaciones por energıa (QM_i)



# research:

- [ ] **presupuesto**


---

- [ ] **Demanda por periodo**


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
production_cost = {
    'solar': [0.17, 0.136],
    'wind': [0.3, 0.32],
    'hydroelectric': 0.5,
    'nuclear': [2.10, 1.38, 1.6],
    'gas': [2.1],
    'coal': [0.98, 1.4, 1.73],
    'oil': [5.4, 7.01, 5.63],
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
