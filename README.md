# use binder to allow others to interact with notes

# can i import gurobipy into a vm or requirements.txt and upload to github? binder?


**TO-DO**:
  * buscar datos para todos los parametros (con medias y desviaciones estandar) []
  * armar set de datos de 3 tamanos distintos []
  * crear jupyter notebook online []
  *



#research:

**budget**
  * at least a couple different budget situations

**GWh demand for each period**
  * will correlate to budget, basically the lower limit is satisfying all population with cheapest energy, upper limit is doing
  it with highest cost energy


**GWh price in market**
  * 10.21 cents per kWh average, 15.8 cents in Chile
  source: https://bit.ly/3eNkc3O

**pollution for each GWh produced by each energy**

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
  source: https://bit.ly/3eOQdZ4

**GWh limit per unit in each energy**
  * el limite estara dado por los kW de capacidad construidos

**initial investment for each energy**
    ```python
    # costos iniciales por kW
      on_cost_per_source = {
          'solar': [1331, 1313, 1100],
          'wind': [1100, 1500, 1319],
          'hydroelectric': [5316, 1750, 7500, 3500],
          'nuclear': [6041, 6317, 6900, 12000],
          'gas': [950, 713, 1084, 1300],
          'coal': [3000, 6250, 5876, 3676],
          'oil': [1170, 1175, 713], # usamos steam engine como tipo de oil fired power plant
        }
    ```
    source:
    - https://www.irena.org/costs/Power-Generation-Costs/Hydropower
    - https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2019/May/IRENA_Renewable-Power-Generations-Costs-in-2018.pdf
    - https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2020.pdf
    - https://www.eia.gov/outlooks/aeo/assumptions/pdf/table_8.2.pdf
    - https://www.lazard.com/media/451086/lazards-levelized-cost-of-energy-version-130-vf.pdf


**initial  construction pollution**


**price of GW storage**
  ```python
    price_per_kw_storage = [1389, 845, 1383]
  ```
  source:
  - https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capital_cost_AEO2020.pdf
  - https://www.eia.gov/outlooks/aeo/assumptions/pdf/table_8.2.pdf


**loss of energy when storing in batteries**

**pollution for each battery**


**max energy centrals per energy allowed**
