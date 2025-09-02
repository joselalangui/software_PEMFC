#%%
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def read_csv(file_path):
    """Reads a CSV file and returns a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return pd.read_csv(file_path) 
def read_txt(file_path):
    """Reads a TXT file and returns a pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    df = pd.read_csv(file_path, sep='\t', header=None, names=['time', 'voltage', 'current'])
    df['voltage'] = df['voltage'].astype(str).str.replace('V', '').astype(float)
    df['current'] = df['current'].astype(str).str.replace('A', '').astype(float)
    return df

def get_txt_file_from_folder(folder_name):
    folder_path = os.path.join(os.pardir, folder_name)
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            return os.path.join(folder_path, file)
    raise FileNotFoundError(f"No .txt file found in {folder_path}")

def get_month_folders(parent_folder, months=('2025-06', '2025-07')):
    folder_path = os.path.join(os.pardir, parent_folder)
    folders = [
        f for f in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, f)) and any(f.startswith(month) for month in months)
    ]
    return [os.path.join(folder_path, f) for f in folders]

# Example usage:
month_folders = get_month_folders('organized_by_date', months=('2025-06', '2025-07'))

# To get the .txt file from each folder:
powerCharge_paths = [get_txt_file_from_folder(os.path.join('organized_by_date', os.path.basename(folder))) for folder in month_folders]

days_data = [read_txt(path) for path in powerCharge_paths] #day 0 is when i humidify the membrane

#%%
baseCase = days_data[1].iloc[600:11400]
temp30C = days_data[2].iloc[6100:19600]
temp50C = days_data[3].iloc[10000:21900]
temp70C = days_data[3].iloc[39300:50900]
temp90C = days_data[4].iloc[800:12600]
relHum25 = days_data[5].iloc[10500:26500]
relHum50 = days_data[6].iloc[4600:19400]
relHum75 = days_data[7].iloc[6400:18100]
relHum100 = days_data[7].iloc[31100:41900]
press1_5bar = days_data[9].iloc[26500:37000]
press2bar = days_data[9].iloc[14900:25700]
press2_5bar = days_data[9].iloc[4700:14300]
extraCase = days_data[10].iloc[650:4350] #day 11 is with lambda equal to 1 and saturated both sides to 70C
#%%
#%%
variables = [
    ('baseCase', baseCase),
    ('temp30C', temp30C),
    ('temp50C', temp50C),
    ('temp70C', temp70C),
    ('temp90C', temp90C),
    ('relHum25', relHum25),
    ('relHum50', relHum50),
    ('relHum75', relHum75),
    ('relHum100', relHum100),
    ('press1_5bar', press1_5bar),
    ('press2bar', press2bar),
    ('press2_5bar', press2_5bar),
    ('extraCase', extraCase)
]

plt.figure(figsize=(12, 8))
for name, data in variables:
    plt.scatter(data['current'], data['voltage'], label=name)
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.title('All Cases: Voltage vs Current')
plt.show()
#%%
plt.figure(figsize=(10, 6))
plt.scatter(baseCase['current'], baseCase['voltage'], label='day 1')
plt.xlabel('Current (A)') 
plt.ylabel('Voltage (V)')
plt.legend()
plt.show()

#%%

plt.figure(figsize=(10, 6))
for i, day_data in enumerate(days_data):
    plt.plot(day_data['voltage'], label=f'Day {i+1}')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.show()
#%%
plt.figure(figsize=(10, 6))
for i, day_data in enumerate(days_data):
    plt.scatter(day_data['current'],day_data['voltage'], label=f'Day {i+1}')
#plt.scatter(days_data[1]['current'], days_data[1]['voltage'], label='Day 1')
#plt.scatter(days_data[4]['current'], days_data[4]['voltage'], label='Day 4')
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.show()


