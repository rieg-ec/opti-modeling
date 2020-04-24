
# numero de horas de cada periodo
PERIOD_LENGTH = 6
N_PERIODS_YEAR = int((24/PERIOD_LENGTH) * 365)

sources = ['solar', 'wind', 'hydroelectric', 'nuclear', 'gas', 'coal', 'oil']

periods = [i for i in range(N_PERIODS_YEAR)]

# constant parameters
