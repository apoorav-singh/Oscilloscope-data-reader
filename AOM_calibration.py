import numpy as np
import matplotlib.pyplot as plt

Gamma = 6.066  # Natural linewidth [MHz]

# Frequency offsets and locking values
C_O_34 = 60.35  # MHz
C_O_24 = 60.35 + 63.4 / 2 - 0.43 * Gamma

SPassMOTnew = 100  # MHz
omega_filtre = 253 - 2.5  # MHz
shift_w85_w87 = 1260      # MHz

omega_34_31 = -113.4      # MHz

LockingFrequency = -92 + (0.518 * Gamma)  # MHz

# Single-pass configuration frequencies [MHz]
SPassMOT = 100
SPassPump = 73.69
SPassProbe = -99.62
SPassRepumper = -103.3
SpassMollow = -120

# Locking frequencies for repumper and probe
LockingFrequencyRepumper = -63.401 / 2
LockingFrequencyProbe = -(63.401 + 120.640) / 2



V_data = np.arange(0, 11)
F_data = 2 * np.array([
    68.8, 74.9, 81.1, 86.7, 91.9,
    97.3, 103, 108.8, 114.8, 120.9, 126.8
])  # [MHz]

# Step 1: Fit 5th-degree polynomial
degree = 5
coefficients = np.polyfit(V_data, F_data, degree)

# Step 2: Create polynomial function
frequency_from_voltage = np.poly1d(coefficients)

def callVoltagetoFrequency(Voltage):
    x = frequency_from_voltage(Voltage)
    freq = x - (LockingFrequencyProbe + SPassProbe - 0.34 * Gamma)
    return freq

PlotWanted = False

if PlotWanted == True:
    # Step 3: Optional - plot the fit
    V_fit = np.linspace(0, 10, 200)
    F_fit = frequency_from_voltage(V_fit)
    plt.figure()
    plt.plot(V_data, F_data, 'o', label='Data')
    plt.plot(V_fit, F_fit, '-', label=f'Poly Fit (deg={degree})')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Frequency [MHz]')
    plt.title('Frequency Calibration Curve')
    plt.grid()
    plt.legend()
    plt.show(block=False)
