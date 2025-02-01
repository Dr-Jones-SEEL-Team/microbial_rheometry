import random
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import scipy.stats as stats
import os
import pathlib
import chardet
import pandas as pd
from pylab import show,subplot,figure

class Sweep:
     def __init__(Sweep):
        Sweep.species = ""
        Sweep.substrate = ""
        Sweep.time = ""
        Sweep.temperature = []
        Sweep.shearstrain = []
        Sweep.storagemodulus = []
        Sweep.lossmodulus = []
        Sweep.tan_delta = [] 
        Sweep.tan_delta = np.divide(Sweep.lossmodulus, Sweep.storagemodulus)

def read_files_in_folder(folder_path):
    """Reads all files in the specified folder."""
    Experiment = [Sweep() for i in range(200)]
    i = 0
    count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                filetype = chardet.detect(file.read())['encoding']
            with open(file_path, 'r', encoding=filetype) as file:
                 lines = file.readlines()
                 if len(lines) > 4:
                    if filename.__contains__("Sepi"):
                        Experiment[i].species = "S. epidemidis"
                    elif filename.__contains__("Saureu") or filename.__contains__("Saureus"):
                        Experiment[i].species = "S. aureus"
                    # elif filename.__contains__("Ecoli")
                        # Experiment[i].species = "Ecoli"
                    # elif filename.__contains__("Strep")
                        # Experiment[i].species = "Strep"
                    # elif filename.__contains__("Bsub")
                        # Experiment[i].species = "Bsub"
                    # elif filename.__contains__("Bcer")
                        # Experiment[i].species = "Bcer"
                    # elif filename.__contains__("Bthe")
                        # Experiment[i].species = "Bthe
                    if filename.__contains__("24h"):
                        Experiment[i].time = 24
                    elif filename.__contains__("48h"):
                        Experiment[i].time = 48
                    elif filename.__contains__("72h"):
                        Experiment[i].time = 72 
                    if filename.__contains__("TSA"):
                        Experiment[i].substrate = "TSA"
                    elif filename.__contains__("Epi"):
                        Experiment[i].substrate = "Epiderm"
                    content = pd.read_csv(file_path, delimiter='\t', header=[4], encoding=filetype)
                    content = content.drop([0, 1])
                    L = len(content["Loss Modulus"])
                    Experiment[i].storagemodulus[0:L] = content['Storage Modulus'].astype(float)
                    Experiment[i].lossmodulus[0:L] = content['Loss Modulus'].astype(float)
                    Experiment[i].shearstrain[0:L] = content['Shear Strain'].astype(float) 
        i = i+1
        count = count + 1
    Experiment=Experiment[:count]   
    return Experiment

if __name__ == "__main__":
    folder_path = r"/Users/aj343/Downloads/Biofilm_Rheometry"
      # Replace with your folder path
Experiment = read_files_in_folder(r"/Users/aj343/Downloads/Biofilm_Rheometry")  

L = len(Experiment)
for i in range(L):
    L = Experiment[i].lossmodulus
    S = Experiment[i].storagemodulus
    Experiment[i].tan_delta = np.divide(L, S)


# Compute means, standard deviations, and standard errors

def analyze_data(Exper,substrate,species,time):
    """Confirms number of replcates for each time, substrate, speices and computes means, standard deviations, and standard errors."""
    Experiment_analyzed = [Sweep() for i in range(L)]
    L = len(Exper)
    temp = [Sweep() for i in range(L)]
    i = 0
    j = 0

    for i in range(L):
        if Exper[i].species == species and Exper[i].substrate == substrate and Exper[i].time == time:
            temp[j] = Exper[i]
            j = j+1
    Experiment_analyzed[0].storagemodulus = np.mean(temp.storagemodulus)
    Experiment_analyzed[0].lossmodulus = np.mean(temp.lossmodulus)
    Experiment_analyzed[0].tan_delta = np.mean(temp.tan_delta)
    Experiment_analyzed[0].storagemodulus_std = np.std(temp.storagemodulus)
    Experiment_analyzed[0].lossmodulus_std = np.std(temp.lossmodulus)
    Experiment_analyzed[0].tan_delta_std = np.std(temp.tan_delta)
    Experiment_analyzed[0].storagemodulus_sem = stats.sem(temp.storagemodulus)
    Experiment_analyzed[0].lossmodulus_sem = stats.sem(temp.lossmodulus)
    Experiment_analyzed[0].tan_delta_sem = stats.sem(temp.tan_delta)
    return Experiment_analyzed

analyze_data(Experiment)

# StorageModulus.mean = np.mean(StorageModulus)
# StorageModulus.std = np.std(StorageModulus)
# LossModulus.mean = np.mean(LossModulus)
# LossModulus.std = np.std(LossModulus)
# TanDelta.mean = np.mean(TanDelta)
# TanDelta.std = np.std(TanDelta)
# StorageModulus.sem = stats.sem(StorageModulus)
# LossModulus.sem = stats.sem(LossModulus)
# TanDelta.sem = stats.sem(TanDelta)

# Plot data with confidence Intervals
# # Generate sample data
# ShearStrain = np.linspace(0, 10, 100)
# StorageModulus.x = 2 * ShearStrain + np.random.normal(0, 1, 100)
# StorageModulus.mean = np.mean(StorageModulus.x)
# StorageModulus.sem = stats.sem(StorageModulus.x)
# # Calculate confidence intervals
# ci = stats.t.interval(0.95, len(ShearStrain) - 1, loc=StorageModulus.mean, scale=stats.sem(StorageModulus.x))

# Plot data and confidence intervals
plt.plot(Experiment[1].shearstrain, Experiment[1].storagemodulus, 'o')
plt.xscale('log')
# print(Experiment[1].shearstrain)
# print(Experiment[1].tan_delta)

# plt.plot(ShearStrain, 2 * ShearStrain, '-')
# plt.fill_between(ShearStrain, (2 * ShearStrain) - ci[1], (2 * ShearStrain) + ci[1], alpha=0.3)
plt.show()