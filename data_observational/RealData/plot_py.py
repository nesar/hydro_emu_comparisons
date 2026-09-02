import matplotlib.pyplot as plt
import pandas as pd

# Load the data from the files
reid_data = pd.read_csv('reid_DR7.txt', delim_whitespace=True, comment='#')
wmap_data = pd.read_csv('wmap_act.txt', delim_whitespace=True, comment='#')

# Extract the relevant columns including error bars
reid_k = reid_data.iloc[:, 0]
reid_Pk = reid_data.iloc[:, 1]
reid_error = reid_data.iloc[:, 2]

wmap_k = wmap_data.iloc[:, 0]
wmap_Pk = wmap_data.iloc[:, 1]
wmap_Pk_upper = wmap_data.iloc[:, 2]

# Calculate the error for WMAP ACT as the difference between upper and main value
wmap_error = wmap_Pk_upper - wmap_Pk

# Plot the data with error bars
plt.figure(figsize=(10, 6))
plt.errorbar(reid_k, reid_Pk, yerr=reid_error, fmt='o', label='Reid DR7')
plt.errorbar(wmap_k, wmap_Pk, yerr=wmap_error, fmt='x', label='WMAP ACT')

plt.xlabel('k (h/Mpc)')
plt.ylabel('P(k) (Mpc/h)^3')
plt.title('Matter Power Spectrum P(k) vs k with Error Bars')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.show()