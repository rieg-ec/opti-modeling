price = 6
price_om = 3.45
price_per_btu = price / 1000000

price_per_kwh = price_per_btu / 0.000293071 + (price_om / (365*24))


print(price_per_kwh)
