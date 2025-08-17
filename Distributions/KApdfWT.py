import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from scipy.spatial.distance import jensenshannon

import matplotlib.pyplot as plt

# Read the Excel file and the 'WT' sheet
df = pd.read_excel('vesicle_data.xlsx', sheet_name='WT')

# Extract the required columns
stiffness = df['Linear stiffness mN/m']
stiffness_std = df['Linear stiffness STD mN/m']
stiffness_plus_std = stiffness + stiffness_std
stiffness_minus_std = stiffness - stiffness_std

# Prepare data for KDE
data_list = [stiffness, stiffness_plus_std, stiffness_minus_std]
labels = ['Stiffness', 'Stiffness + STD', 'Stiffness - STD']
colors = ['blue', 'green', 'red']

plt.figure(figsize=(8, 5))
x_min = min([data.min() for data in data_list])
x_max = max([data.max() for data in data_list])
x_grid = np.linspace(x_min, x_max, 500)

for data, label, color in zip(data_list, labels, colors):
    kde = gaussian_kde(data)
    plt.plot(x_grid, kde(x_grid), label=label, color=color)

plt.xlabel('Linear stiffness (mN/m)')
plt.ylabel('PDF')
plt.title('PDF of Stiffness (WT)')
plt.legend()
plt.tight_layout()
# plt.savefig('example_KApdfWT.png')
plt.show()
# Calculate the sum of each column
# Evaluate KDEs on the grid
pdfs = [gaussian_kde(data)(x_grid) for data in data_list]

# Normalize PDFs to sum to 1 (so they are proper probability distributions)
pdfs = [pdf / pdf.sum() for pdf in pdfs]

# Calculate Jensen-Shannon divergence between each pair
jsd_01 = jensenshannon(pdfs[0], pdfs[1])
jsd_02 = jensenshannon(pdfs[0], pdfs[2])
jsd_12 = jensenshannon(pdfs[1], pdfs[2])

print(f"Jensen-Shannon divergence (Stiffness vs Stiffness + STD): {jsd_01:.4f}")
print(f"Jensen-Shannon divergence (Stiffness vs Stiffness - STD): {jsd_02:.4f}")
print(f"Jensen-Shannon divergence (Stiffness + STD vs Stiffness - STD): {jsd_12:.4f}")