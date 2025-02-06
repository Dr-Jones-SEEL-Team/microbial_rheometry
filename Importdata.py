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
    ## Class to store the data from the files.
    ## The class has the following attributes: biological species and substrate, time of the experiment, temperature, shear strain, storage modulus, loss modulus, tan delta, and an additional attribute for replicates, means and standard error.

    def __init__(self):
        self.species = ""
        self.substrate = ""
        self.time = ""
        self.temperature = []
        self.shearstrain = []
        self.storagemodulus = []
        self.lossmodulus = []
        self.tan_delta = [] 
        self.attribute = ""
    # def __getattribute__(self, name):
    #     pass

def get_from_filename(filename, key):
    """Extracts values from filename including bacteria species, substrate, time."""
    mappings = {
        "species": {
            "Sepi": "S. epidermidis",
            "Saureu" or "Saureus": "S. aureus",
            "control" or "Control": "Control"
        },
        "substrate": {
            "TSA": "TSA",
            "Epi" or "Epi200": "Epiderm"
        },
        "time": {
            "24h": 24,
            "48h": 48,
            "72h": 72
        }
    }

    if key in mappings:
        mapping = mappings[key]
        for key_part, value in mapping.items():
            if key_part in filename:
                return value

    # Return None if the key is not found
    return None

def read_files_in_folder(folder_path):
    """Reads all files in the specified folder."""
    ## The function reads all files in the specified folder and stores the data in a list of Sweep objects.
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
                    Experiment[i].species = get_from_filename(filename, "species")
                    if Experiment[i].species == None:
                        Experiment[i].species = "Control"
                    Experiment[i].substrate = get_from_filename(filename, "substrate")
                    Experiment[i].time = get_from_filename(filename, "time")
                    content = pd.read_csv(file_path, delimiter='\t', header=[4], encoding=filetype)
                    content = content.drop([0, 1])
                    L = len(content["Loss Modulus"])
                    Experiment[i].storagemodulus[0:L] = content['Storage Modulus'].astype(float)
                    Experiment[i].lossmodulus[0:L] = content['Loss Modulus'].astype(float)
                    Experiment[i].shearstrain[0:L] = content['Shear Strain'].astype(float) 
                    Experiment[i].tan_delta[0:L] = np.divide(Experiment[i].lossmodulus, Experiment[i].storagemodulus)
        i = i+1
        count = count + 1
    Experiment=Experiment[:count]   
    return Experiment

def matches_criteria(Exper,substrate,species,time):
    """Checks if the experiment matches the specified criteria."""
    return Exper.species == species and Exper.substrate == substrate and Exper.time == time

# Compute means, standard deviations, and standard errors
def analyze_data(Exper,substrate,species,time):
    """Confirms number of replcates for each time, substrate, speices and computes means, standard deviations, and standard errors."""
    temp = [exper for exper in Exper if matches_criteria(exper, substrate, species, time)]
    L = len(temp)
    analysis = {}
    mean = np.mean([temp.storagemodulus for temp in temp],axis=0)
    std = np.std([temp.storagemodulus for temp in temp],axis=0)
    sem = stats.sem([temp.storagemodulus for temp in temp],axis=0)
    analysis["StorageModulus"] = {"mean": mean, "std": std, "sem": sem} 
    mean = np.mean([temp.lossmodulus for temp in temp],axis=0)
    std = np.std([temp.lossmodulus for temp in temp],axis=0)
    sem = stats.sem([temp.lossmodulus for temp in temp],axis=0)
    analysis["LossModulus"] = {"mean": mean, "std": std, "sem": sem}
    mean = np.mean([temp.tan_delta for temp in temp],axis=0)
    std = np.std([temp.tan_delta for temp in temp],axis=0)
    sem = stats.sem([temp.tan_delta for temp in temp],axis=0)
    analysis["TanDelta"] = {"mean": mean, "std": std, "sem": sem}
    mean = np.mean([temp.shearstrain for temp in temp],axis=0)
    std = np.std([temp.shearstrain for temp in temp],axis=0)
    sem = stats.sem([temp.shearstrain for temp in temp],axis=0)
    analysis["ShearStrain"] = {"mean": mean, "std": std, "sem": sem}
    return analysis

def plot_data(Exper,time):
    """Plots the data for the specified criteria."""
    # # Calculate confidence intervals
    ci = stats.t.interval(0.95, len(Exper["ShearStrain"]["mean"]) - 1, loc=Exper["StorageModulus"]["mean"], scale=Exper["StorageModulus"]["sem"])  
    ci_s = stats.t.interval(0.95, len(Exper["ShearStrain"]["mean"]) - 1, loc=Exper["LossModulus"]["mean"], scale=Exper["LossModulus"]["sem"])  
    # Plot data and confidence intervals
    plt.plot(Exper["ShearStrain"]["mean"], Exper["StorageModulus"]["mean"], 'o',label='Storage Modulus '+str(time)+'h')
    plt.plot(Exper["ShearStrain"]["mean"], Exper["LossModulus"]["mean"], '+',label='Loss Modulus '+str(time)+'h')    

    plt.fill_between(Exper["ShearStrain"]["mean"], ((Exper["StorageModulus"]["mean"]) - ci[1]), ((Exper["StorageModulus"]["mean"]) + ci[1]), alpha=0.3)
    plt.fill_between(Exper["ShearStrain"]["mean"], ((Exper["LossModulus"]["mean"]) - ci_s[1]), ((Exper["LossModulus"]["mean"]) + ci_s[1]), alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.legend(loc='upper right',bbox_to_anchor=(1, 1),fontsize='small')
    # plt.tight_layout()
    plt.xlabel('Log Shear Strain')
    plt.ylabel('Shear Modulus [Pa]')
    return plt
    
def linearviscoelasticity(Exper):
    """Calculates the linear viscoelasticity of the data."""
    ##Uses a running average of tan\delta to determine the linear viscoelastic region of the data.
    tand = Exper["TanDelta"]["mean"]   
    tandbar = tand[0]+tand[1]+tand[2]+tand[3]+tand[4]+tand[5]
    for i in range(5,len(tand)-1):
        if np.abs(tand[i+1]*(i+1) - tandbar)/tandbar<0.03:
            break
        else:
            tandbar = tandbar + tand[i+1]
            continue

    return i    

if __name__ == "__main__":
    folder_path = r"/Users/aj343/Downloads/Biofilm_Rheometry"
    Experiment = read_files_in_folder(folder_path)
    # temp = [Experiment for Experiment in Experiment if matches_criteria(Experiment, "Epiderm", "Control", 24)]
    # print([temp.storagemodulus for temp in temp])
    # # for i in range(len(Experiment)):
    # #     print(Experiment[i].species)
    # #     print(Experiment[i].substrate)
    plotalldata = [0,0,0,0]
    for i in range (1,2,1):
            Exp_analyzed = analyze_data(Experiment,"Epiderm","Control",24*i)
            plotalldata[i] = plot_data(Exp_analyzed,24*i)
            lver_index = (linearviscoelasticity(Exp_analyzed))
            # plt.loglog(Exp_analyzed["ShearStrain"]["mean"][lver_index], Exp_analyzed["StorageModulus"]["mean"][lver_index], 'X')
    
    # plt.title('Shear Modulus of '+'S. epidermidis'+' on '+'Epiderm')
    plt.title('Shear Modulus of '+'Epiderm'+' Control')
    # plt.show()
    plotalldata[1].show()
    # plotalldata[2].show()
    # plotalldata[3].show()
    
    




