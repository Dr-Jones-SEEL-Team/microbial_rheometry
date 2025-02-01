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
                    Experiment[i].storagemodulus[0:30] = content['Storage Modulus']
                    Experiment[i].lossmodulus[0:30] = content['Loss Modulus'].astype(float)
                    Experiment[i].shearstrain = content['Shear Strain'] 
        i = i+1
        count = count + 1
    Experiment=Experiment[:count]   
    return Experiment


if __name__ == "__main__":
    folder_path = r"/Users/aj343/Downloads/Biofilm_Rheometry"
      # Replace with your folder path
Experiment = read_files_in_folder(r"/Users/aj343/Downloads/Biofilm_Rheometry")  


# L = len(Experiment)
# print(L)
# for i in range(L):
    # L = Experiment[i].lossmodulus
    # S = Experiment[i].storagemodulus
    # print(L)
    # print(S)
    # print(i)
    # Experiment[i].tan_delta = np.divide(L, S)
    # print(Experiment[i].tan_delta)
Experiment.tan_delta = np.divide(Experiment.lossmodulus, Experiment.storagemodulus)
# print(Experiment[1].lossmodulus)

# for i in range(100):
#     Experiment[i].tan_delta = np.divide(Experiment[i].lossmodulus, Experiment[i].storagemodulus)    
#     print(i)
#     print(Experiment[i].tan_delta)

# Plot data with confidence Intervals
# Confirm number of replcates for each time, substrate, speices
# Compute means, standard deviations, and standard errors

# StorageModulus.mean = np.mean(StorageModulus)
# StorageModulus.std = np.std(StorageModulus)
# LossModulus.mean = np.mean(LossModulus)
# LossModulus.std = np.std(LossModulus)
# TanDelta.mean = np.mean(TanDelta)
# TanDelta.std = np.std(TanDelta)
# StorageModulus.sem = stats.sem(StorageModulus)
# LossModulus.sem = stats.sem(LossModulus)
# TanDelta.sem = stats.sem(TanDelta)

# # Generate sample data
# ShearStrain = np.linspace(0, 10, 100)
# StorageModulus.x = 2 * ShearStrain + np.random.normal(0, 1, 100)
# StorageModulus.mean = np.mean(StorageModulus.x)
# StorageModulus.sem = stats.sem(StorageModulus.x)
# # Calculate confidence intervals
# ci = stats.t.interval(0.95, len(ShearStrain) - 1, loc=StorageModulus.mean, scale=stats.sem(StorageModulus.x))

# Plot data and confidence intervals
# plt.plot(Experiment[1].shearstrain, Experiment[1].tan_delta, 'o')
# print(Experiment[1].shearstrain)
# print(Experiment[1].tan_delta)

# plt.plot(ShearStrain, 2 * ShearStrain, '-')
# plt.fill_between(ShearStrain, (2 * ShearStrain) - ci[1], (2 * ShearStrain) + ci[1], alpha=0.3)
# plt.show()