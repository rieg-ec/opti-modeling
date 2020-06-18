import re
from collections import defaultdict
from data import Synthesize
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from gurobipy import GRB
from main import Model
from analysis import results_plot

model = Model('Sensibility analysis of original model')
model.Z_i['wind'] = 2

if __name__ == '__main__':
    model.optimize()
    model.save_results(path='sens_analysis_results/gurobi_files')
    plot_results(path='sens_analysis_results/plots')
