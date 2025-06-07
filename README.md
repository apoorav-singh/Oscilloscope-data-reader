# Oscilloscope-data-reader
This repository is collection python scripts that is used to analyze the data saved from the oscilloscope on the computer. Currently, it is designed to calculate optical depth of the cold atomic cloud using reading data of photodiode. Idea is to expand and to use it as a general data analysis script bundle. 


⸻


# How to Run `optical_depth_calc.py`

This Python script processes oscilloscope data from a cold atom experiment. It identifies timing markers from a ramp signal, extracts photodiode data with and without atoms, and fits the transmission profile using Beer–Lambert's Law.

---

## Folder Structure Assumption

The script expects data to be organized in the following structure:

data/
└── /YEAR
└── /MONTH
└── /DAY
├── F1_RL_00011.txt     ← Photodiode data
└── C2_RL_00011.txt     ← Ramp signal

Each dataset is identified by a **file number** (e.g., `11` corresponds to `F1_RL_00011.txt` and `C2_RL_00011.txt`).

---

## How to Run the Script

1. Open your terminal or command prompt.
2. Navigate to the folder containing `process_photodiode.py`.
3. Run the script with the following command:

```bash
python process_photodiode.py --year 2025 --month 06 --date 07 --file 11
```

⸻

Command-Line Arguments

Flag	Description	Example
--year	Year of the data folder	2025
--month	Month of the data folder 06
--date	Day of the data folder	07
--file	File number to process (e.g., 11 → 00011) 11


⸻

What the Script Does
	•	Loads the ramp data and finds timing markers (pulses).
	•	Loads photodiode data and extracts signal during the pulses.
	•	Computes transmission using:
 
```T = (WithAtoms - Background) / (WithoutAtoms - Background)```

	•	Fits the result to a model:

	•	Displays:
	•	Fitted transmission vs. detuning
	•	Raw photodiode signals with and without atoms
	•	Prints the estimated Optical Depth (OD).

⸻

Requirements

Make sure the following Python packages are installed:

```pip install numpy pandas matplotlib scipy```

Also ensure AOM_calibration.py is in the same directory or importable, and contains the following variables:
```
LockingFrequencyProbe = ...
SPassProbe = ...
```

⸻

Example

```python process_photodiode.py --year 2025 --month 06 --date 07 --file 11```

This will process:
```
data/2025/06/07/F1_RL_00011.txt
data/2025/06/07/C2_RL_00011.txt
```

⸻

Optional Enhancements
	•	Save results (fit parameters, processed arrays) to CSV
	•	Add a ```--no-plot``` flag for headless use
	•	Batch processing over multiple files
