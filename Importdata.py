import random
import numpy as np
import math
import matplotlib.pyplot as plt
import copy
import scipy.stats as stats
import os
import pathlib
from numpy import random, sqrt, log, sin, cos, pi
from pylab import show,subplot,figure

print(os.getcwd())
print(pathlib.Path().absolute())

def read_files_in_folder(folder_path):
    """Reads all files in the specified folder."""

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                print(f"File: {filename}\nContent:\n{content}\n")

if __name__ == "__main__":
    folder_path = "../Users/aj343/OneDrive\ -\ Duke\ University/Biofilm_Rheometry/"
      # Replace with your folder path
    read_files_in_folder(folder_path)

# # Plot data with confidence Intervals
# # Confirm number of replcates for each time, substrate, speices
# # Compute means and standard deviations

# Temperature
# ShearStrain = 
# StorageModulus.mean = np.mean(StorageModulus)
# StorageModulus.std = np.std(StorageModulus)
# LossModulus.mean = np.mean(LossModulus)
# LossModulus.std = np.std(LossModulus)

# class StorageModulus:
#     x = []
#     mean = 0
#     sem = 0

# # Generate sample data
# ShearStrain = np.linspace(0, 10, 100)
# StorageModulus.x = 2 * ShearStrain + np.random.normal(0, 1, 100)
# StorageModulus.mean = np.mean(StorageModulus.x)
# StorageModulus.sem = stats.sem(StorageModulus.x)
# # Calculate confidence intervals
# ci = stats.t.interval(0.95, len(ShearStrain) - 1, loc=StorageModulus.mean, scale=stats.sem(StorageModulus.x))

# # Plot data and confidence intervals
# plt.plot(ShearStrain, StorageModulus.x, 'o')
# plt.plot(ShearStrain, 2 * ShearStrain, '-')
# plt.fill_between(ShearStrain, (2 * ShearStrain) - ci[1], (2 * ShearStrain) + ci[1], alpha=0.3)
# plt.show()