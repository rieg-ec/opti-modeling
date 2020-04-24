
# numero de horas de cada periodo
PERIOD_LENGTH = 6
N_PERIODS_YEAR = int((24/PERIOD_LENGTH) * 365)

sources = ['solar', 'wind', 'hydroelectric', 'nuclear', 'gas', 'coal', 'oil']

periods = [i for i in range(N_PERIODS_YEAR)]\


overnight_cost_per_source = {
    'solar': [1331, 1313, 1100],
    'wind': [1100, 1500, 1319],
    'hydroelectric': [5316, 1750, 7500, 3500],
    'nuclear': [6041, 6317, 6900, 12000],
    'gas': [950, 713, 1084, 1300],
    'coal': [3000, 6250, 5876, 3676],
    'oil': [1170, 1175, 713],
    }

tonnes_CO2_per_GWh = {
    'solar': 85,
    'wind': 26,
    'hydroelectric': 26,
    'nuclear': 29,
    'gas': 499,
    'coal': 888,
    'oil': 733,
    }

price_per_kw_storage = [1389, 845, 1383]
