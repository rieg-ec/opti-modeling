from data import Synthesize

demand = Synthesize().synthesize_data(1460)

print(max(demand.values()), min(demand.values()))
