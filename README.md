

### TO-DO
- [ ] buscar datos para todos los parametros (con medias y desviaciones estandar)
- [ ] armar set de datos de 3 tamanos distintos
- [ ] crear jupyter notebook online
- [ ] hacer analisis de los datos recolectados
- [ ] armar modelo y resolver
- [ ] analizar resultados

### Datos recolectados:
1. [x] tipos de energia (i)
2. [x] periodos de tiempo (t)
3. [ ] presupuesto (P) &rightarrow; depende de la demanda que ocupemos, la idea es probar con distintos presupuestos
4. [x] valor GWh (S)
5. [x] costo por unidad construida (CI_i) &rightarrow; costo por kW de capacidad
6. [x] costo produccion GWh (C_i)
7. [x] contaminacion por unidad construida (ZI_i) &rightarrow; tenemos contaminacion por unidad producida que contempla contaminacion inicial
8. [x] contaminacion por GWh producido
9. [x] capacidad por unidad construida (K_i) &rightarrow; capacidad en kW/GW construidos
10. [ ] demanda por periodo (D_t) &rightarrow; la idea tambien es probar con distintas demandas simulandon ciudades pequenas con bajo presupuesto o ciudades mas ricas
11. [x] costo por almacenamiento (A) &rightarrow; costo por capacidad en kW, la inversion es inicial
12. [ ] perdida de energia por almacenamiento (constante)
13. [ ] contaminacion de almacenamiento de unidad energ. (Alpha_i)
14. [ ] cantidad maxima de instalaciones por energia (QM_i)



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

- [x] **Costo de produccion sin contar inversion inicial por kWh producido**

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

el limite estara dado por los kW de capacidad construidos

---

- [x] **Inversion inicial por energia por kW de capacidad**

```python
# overnight costs taken from different fuentes for each enrgy type
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

- [ ] **Contaminacion por construccion inicial**

El parametro contaminacion por produccion incluye este tipo de contaminacion

---

- [x] **Precio por capacidad de almacenamiento**

```python
# price for storing a kWh from different fuentes
price_per_kw_storage = [1389, 845, 1383]
```
fuente:
- https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2020.pdf
- https://www.eia.gov/outlooks/aeo/assumptions/pdf/table_8.2.pdf

---

- [ ] **Perdida de energia por almacenamiento**

---

- [ ] **Contaminacion por bateria**

---

- [ ] **Limite de plantas de energia**
