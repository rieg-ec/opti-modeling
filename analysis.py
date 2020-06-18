import re
import numpy as np
from collections import defaultdict
from data import Synthesize
from main import Model
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from random import randint

def plot_demand(path='plots'):
    hourly = Synthesize().read_data(Synthesize().hourly)
    # usamos un solo dia ocupando los promedios del mes para ver la variacion segun la hora
    hourly = [np.mean(v) for v in hourly.values()]

    daily = Synthesize().read_data(Synthesize().daily)
    daily_y = []
    for month in daily:
        daily_y.extend(daily[month])

    rndm = randint(0, 1460)
    random_days = [i for i in Model.D_t.values()][rndm:rndm+10]

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(40, 30))

    ax1.set_title('Energy Demand per Hour', fontsize=30)
    ax2.set_title('Energy Demand per Month', fontsize=30)
    ax3.set_title('Energy Demand per Period', fontsize=30)
    ax4.set_title('Energy Demand per Period', fontsize=30)

    ax1.set_xlabel('Hour', fontsize=30)
    ax1.set_ylabel('Demand (kWh)', fontsize=30)

    ax2.set_xlabel('Month', fontsize=30)
    ax2.set_ylabel('Demand (kWh)', fontsize=30)

    ax3.set_xlabel('Period', fontsize=30)
    ax3.set_ylabel('Demand (kWh)', fontsize=30)

    ax4.set_xlabel('Period', fontsize=20)
    ax4.set_ylabel('Demand (kWh)', fontsize=20)


    ax1.xaxis.set_major_locator(MultipleLocator(3))
    ax1.tick_params(axis='both', which='major', labelsize='20')

    ax2.xaxis.set_major_locator(MultipleLocator(30))
    ax2.set_xticklabels([i for i in range(-1, 13)]) # por alguna razon si empieza en 0 el range, el grafico parte en 1
    ax2.tick_params(axis='both', which='major', labelsize='20')

    ax3.xaxis.set_major_locator(MultipleLocator(200))
    ax3.tick_params(axis='both', which='major', labelsize='20')

    ax4.xaxis.set_major_locator(MultipleLocator(1))
    ax4.tick_params(axis='both', which='major', labelsize='20')


    plt.subplots_adjust(hspace=0.3)

    ax1.plot(hourly)
    ax2.plot(daily_y)
    ax3.plot([i for i in Model.D_t.values()])
    ax4.plot(random_days)

    fig.savefig(path + '/demand_graphs.png')

def plot_results(path='plots'):
    vars = []
    with open('gurobi_files/model.sol', 'r') as file:
        for _ in range(2):
            file.readline() # saltar 2 primeras lineas
        for result in file.readlines():
            varname = result.split(' ')[0]
            value = result.split(' ')[1].replace('\n', '')
            vars.append([varname, value])

    # prod_unit bar plot
    sources_prod_units = []
    values_prod_units = []
    for var in vars:
        if var[0].startswith('prod_units'):
            source = re.search('\[([^$]*)]', var[0]).group(1)
            sources_prod_units.append(source)
            values_prod_units.append(float(var[1]))
        elif var[0] == 'storage':
            sources_prod_units.append('storage')
            values_prod_units.append(float(var[1]))

    fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    ax.set_title('Purchased kW of capacity per energy source and purchased storage capacity', fontsize=20)

    ax.set_xlabel('Source', fontsize=20)
    ax.set_ylabel('kW of capacity', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize='15')

    ax.bar(sources_prod_units, values_prod_units, color='green')
    fig.savefig(path + '/prod_units.png')

    ## output graph
    output = defaultdict(list)

    for var in vars:
        if var[0].startswith('output'):
            op = re.search('\[([^$]*)]', var[0]).group(1).split(',')
            source = op[1]
            period = op[0]
            energy = float(var[1])
            output[source].append(energy)

    fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    ax.set_title('Purchased kW of capacity per energy source and purchased storage capacity', fontsize=20)

    ax.set_xlabel('Periods', fontsize=20)
    ax.set_ylabel('Energy output', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize='15')
    ax.xaxis.set_major_locator(MultipleLocator(100))

    for source in output:
        ax.plot([i for i in range(len(output[source]))][0::5], output[source][0::5],
                linewidth=3, label=source)

    ax.legend(loc='upper right', fontsize=20)
    ax.set_xlim(xmin=0.0)
    fig.savefig(path + '/output.png')
