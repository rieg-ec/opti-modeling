### Proyecto para el ramo Optimización - ICS1113
---
# Modelamiento en gurobi

Objetivo del modelo: optimizar la inversión y producción en la industria energética, sujeto a restricciones como presupuesto, demanda y capacidad

---
### RESEARCH:

- [x] **presupuesto**

---

- [x] **Demanda por periodo**

    *como modelo ocupamos a EE.UU en el 2019*

    Los datos fueron recolectados en archivos json y manipulados en ```datos.py```.

    https://www.eia.gov/beta/electricity/gridmonitor/dashboard/custom/pending

---

- [x] **Precio de un kWh**

    10.21 cents per kWh average

    https://bit.ly/3eNkc3O
    https://es.globalpetrolprices.com/Chile/electricity_prices/

---

- [x] **Costo de producción en dolares sin contar inversión inicial por kWh producido**

    https://www.statista.com/statistics/519144/power-plant-operation-and-maintenance-costs-in-the-us-by-technology/
    https://www.instituteforenergyresearch.org/renewable/electric-generating-costs-a-primer/
    https://www.lazard.com/media/450784/lazards-levelized-cost-of-energy-version-120-vfinal.pdf
    https://www.nrel.gov/docs/fy11osti/48595.pdf

---

- [x] **Contaminacion por produccion**

    https://bit.ly/3eOQdZ4


---

- [x] **Inversion inicial por energia por kW de capacidad**

    https://www.irena.org/costs/Power-Generation-Costs/Hydropower
    https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2019/May/IRENA_Renewable-Power-Generations-Costs-in-2018.pdf
    https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2020.pdf
    https://www.eia.gov/outlooks/aeo/assumptions/pdf/table_8.2.pdf
    https://www.lazard.com/media/451086/lazards-levelized-cost-of-energy-version-130-vf.pdf

---

- [x] **capacidad maxima de kWh, eficiencia y costo en dolares por unidad de almacenamiento**

    https://www.tesla.com/powerpack

    *se ocupo como modelo la bateria industrial de Tesla*
---

- [x] **Contaminacion por bateria**

    https://www.ffe.de/attachments/article/856/Carbon_footprint_EV_FfE.pdf

    *Se calculo multiplicando la contaminacion por kWh de capacidad por la capacidad de la bateria*

---

- [ ] **Limite de plantas de energia**
