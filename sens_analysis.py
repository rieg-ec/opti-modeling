import re
from collections import defaultdict
from data import Synthesize
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from gurobipy import GRB
from main import Model

model = Model('Sensibility analysis of original model')
model.Z_i['wind'] = 2

if __name__ == '__main__':
    model.optimize()

    with open('sens_analysis_results/gurobi_files/slack.text', 'w') as file:
        for constr in model.getConstrs():
            file.writelines(f"{constr}: {constr.getAttr('slack')}\n")
        file.close()

    if model.status == GRB.INFEASIBLE:
        model.computeIIS()
        model.write('sens_analysis_results/gurobi_files/model.ilp')

    ## results analysis
    vars = []
    with open('sens_analysis_results/gurobi_files/model.sol', 'r') as file:
        for _ in range(2):
            file.readline() # saltar 2 primeras lineas
        for result in file.readlines():
            varname = result.split(' ')[0]
            value = result.split(' ')[1].replace('\n', '')
            vars.append([varname, value])

    prod_unit bar plot
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
    fig.savefig('sens_analysis_results/plots/prod_units.png')

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
    fig.savefig('sens_analysis_results/plots/output.png')
