#%%
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import re

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


#%%
baseCase = firstDay.iloc[0:3600]
plt.plot(firstDay['voltage'], label='17_06_2025')
plt.plot(baseCase['voltage'])
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()
#%%
plt.plot(firstDay['voltage'], label='17_06_2025')
plt.plot(secondDay['voltage'], label='18_06_2025')
plt.plot(thirdDay['voltage'], label='26_06_2025')
plt.plot(fourthDay['voltage'], label='30_06_2025')
plt.plot(fifthDay['voltage'], label='01_07_2025')
plt.plot(sixthDay['voltage'], label='02_  07_2025')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()


