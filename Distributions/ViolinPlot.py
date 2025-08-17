import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

val = "Linear stiffness mN/m"
## Use val = H_nm, Kappa, to make plots for H_nm and Kappa
# Read the Excel file
excel_path = 'vesicle_data.xlsx'
xls = pd.ExcelFile(excel_path)

# Prepare data for plotting
data_list = []
sheet_names = xls.sheet_names
for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    if val in df.columns:
        ka_values = df[val].dropna()
        data_list.append(pd.DataFrame({val: ka_values, 'Document': sheet}))

# Concatenate all data
plot_df = pd.concat(data_list, ignore_index=True)

# Create violin plot
palette = sns.color_palette("husl", len(plot_df['Document'].unique()))
plt.figure(figsize=(10, 6))
sns.violinplot(x='Document', y=val, data=plot_df, inner='box', palette=palette)
plt.title(f'Violin Plot {val}')
plt.ylabel(f'{val}')
plt.xticks(rotation=45)
# plt.savefig('example_voilin_plot.png')
plt.tight_layout()
plt.show()
