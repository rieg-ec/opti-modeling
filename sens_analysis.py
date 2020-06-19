import re
from collections import defaultdict
from data import Synthesize
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from gurobipy import GRB
from main import Model
from analysis import plot_results
from os import path, makedirs

model = Model('Sensibility analysis of original model')
# model.AE = 0.95
# model.AZ *= 0.5
# model.AC *= 0.8
# model.AQ *= 2
# model.P *= 1.5
#
# for period in model.D_t:
#     model.D_t[period] *= 1.2
# for source in model.sources:
#     if source in ['coal', 'oil', 'gas']:
#         model.QM_i[source] *= 0.7

if __name__ == '__main__':
    model.optimize()
    folder = 'storage_improves'
    dirname = path.join('sens_analysis_results', folder)
    if not path.exists(dirname):
        plot_dir = path.join(dirname, 'plots')
        gurobi_files_dir = path.join(dirname, 'gurobi_files')
        makedirs(plot_dir)
        makedirs(gurobi_files_dir)
    model.save_results(where=dirname)
    plot_results(where=dirname)
