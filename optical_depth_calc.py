import os
import numpy as np
import pandas as pd
import scipy.signal
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import AOM_calibration 


# Fitting function for Beer-Lambert's Law
def BL1(x,b,a):
    return np.exp(-(b/(1+4*(x-a)**2)))

def BL2(x,b,a,c):
    return (1-c)*np.exp(-(b/(1+4*(x-a)**2)))+c


# Load Ramp from oscilloscope data
pd_file_number = 11

dir_path = 'data'

ramp_path = os.path.join(dir_path, f"C2_RL_{pd_file_number:05d}.txt")


## Reading Ramp data
Ramp = np.loadtxt(ramp_path, skiprows=5)[:, 1]
Ramp_smooth = scipy.signal.savgol_filter(Ramp, 20, 1)
Derivative_Ramp = np.gradient(Ramp_smooth)
Derivative_Ramp = Derivative_Ramp / max(Derivative_Ramp)
Derivative_Peaks = scipy.signal.find_peaks(Derivative_Ramp, height=0.7, distance=2000)[0]

## Identiyfing the key points in the experiment.
##      1. When pulse start: Ramp starts for absorption data
##      2. When pulse ends: Ramp ends for absorption data
##      3. When pulse start: Ramp starts for without absorption data
##      4. When pulse ends: Ramp ends for without absorption data

if len(Derivative_Peaks) == 4:
    start_pulseWA = np.argmin(abs(Derivative_Ramp[Derivative_Peaks[0]:Derivative_Peaks[0]+(Derivative_Peaks[1]-Derivative_Peaks[0])//2]-0.5))+Derivative_Peaks[0]
    end_pulseWA = np.argmin(abs(Derivative_Ramp[Derivative_Peaks[0]+(Derivative_Peaks[1]-Derivative_Peaks[0])//2:Derivative_Peaks[1]]-0.5))+Derivative_Peaks[0]+(Derivative_Peaks[1]-Derivative_Peaks[0])//2
    start_pulseWoA = np.argmin(abs(Derivative_Ramp[Derivative_Peaks[2]:Derivative_Peaks[2]+(Derivative_Peaks[3]-Derivative_Peaks[2])//2]-0.5))+Derivative_Peaks[2]
    end_pulseWoA = np.argmin(abs(Derivative_Ramp[Derivative_Peaks[2]+(Derivative_Peaks[3]-Derivative_Peaks[2])//2:Derivative_Peaks[3]]-0.5))+Derivative_Peaks[2]+(Derivative_Peaks[3]-Derivative_Peaks[2])//2
else:
    print("Check Ramp")

print("Start pulse with atoms      :", start_pulseWA)
print("Start pulse without atoms   :", start_pulseWoA)
print("End pulse with atoms        :", end_pulseWA)
print("End pulse without atoms     :", end_pulseWoA)

## Now Loading data, that carries data of absorption from the cloud using point markers extracted earlier.
photodiode_path = os.path.join(dir_path, f"F1_RL_{pd_file_number:05d}.txt")

With_atoms = np.loadtxt(photodiode_path, skiprows=5)[:,1][start_pulseWA:end_pulseWA]
Without_atoms = np.loadtxt(photodiode_path, skiprows=5)[:,1][start_pulseWoA:end_pulseWoA]


### To make length of the arrays equal
size = min([len(With_atoms),len(Without_atoms)])
With_atoms = With_atoms[:size]
Without_atoms = Without_atoms[:size]

## Fetching photodiode background (Approximately in the middle of the cycle) 
background = np.mean(With_atoms[size//2-20:size//2+20])

## Making an x-axis using the calibration data
delta_min = ((11.32*min(Ramp) + 131.79) + AOM_calibration.LockingFrequencyProbe + AOM_calibration.SPassProbe)/6.06
delta_max = ((11.32*max(Ramp) + 131.79) + AOM_calibration.LockingFrequencyProbe + AOM_calibration.SPassProbe)/6.06
Delta_list_PD = np.linspace(delta_min, delta_max, size)  # x-axis for PD

## Calculation of the photodiode Transmission.
t_pd = (With_atoms-background)/(Without_atoms-background)

# Adding Offset in the data for more clean data
Points_to_remove_from_everyone = 300

if Points_to_remove_from_everyone != 0:
    Delta_list_PD = Delta_list_PD[Points_to_remove_from_everyone:-Points_to_remove_from_everyone]
    t_pd = t_pd[Points_to_remove_from_everyone:-Points_to_remove_from_everyone]
    With_atoms = With_atoms[Points_to_remove_from_everyone:-Points_to_remove_from_everyone]
    Without_atoms = Without_atoms[Points_to_remove_from_everyone:-Points_to_remove_from_everyone]

# Fitting function
param_pd, param_cov = curve_fit(BL2, Delta_list_PD, t_pd, p0=[10,0.1,0], maxfev = int(1e6))

print('Estimated OD of cloud is = {:.2f}'.format(param_pd[0]))

fig, ax = plt.subplots()
ax.plot(Delta_list_PD, t_pd, '.', alpha=0.3, label='Photodiode')
ax.plot(Delta_list_PD, BL2(Delta_list_PD, param_pd[0], param_pd[1], param_pd[2]), '-', c='b', label='Photodiode fit - OD = {:.2f}'.format(param_pd[0]))
ax.set_xlabel('Detuning (Gamma)')
ax.set_ylabel('Transmission')
ax.legend()
ax.grid()
plt.show(block=False)

PlotWAandWoA = True
if PlotWAandWoA == True:
    fig, ax1 = plt.subplots()
    ax1.plot(Delta_list_PD,(With_atoms-min(With_atoms))/max(With_atoms-min(With_atoms)))
    ax1.plot(Delta_list_PD,(Without_atoms-min(Without_atoms))/max(Without_atoms-min(Without_atoms)))
    plt.show()
