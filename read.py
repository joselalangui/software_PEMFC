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


def mean_groups_by_voltage_change(data, threshold=0.1):
    voltage = data['voltage'].values
    current = data['current'].values
    groups = []
    start = 0
    for i in range(1, len(voltage)):
        if abs(voltage[i] - voltage[start]) >= threshold:
            groups.append((voltage[start:i], current[start:i]))
            start = i
    # Add last group
    if start < len(voltage):
        groups.append((voltage[start:], current[start:]))
    mean_voltages = [np.mean(v) for v, _ in groups if len(v) > 0]
    mean_currents = [np.mean(c) for _, c in groups if len(c) > 0]
    return mean_voltages, mean_currents

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
variables = [
    ('baseCase', baseCase),
    ('T= 30 C', temp30C),
    ('T = 50 C', temp50C),
    ('T = 70 C', temp70C),
    ('T = 90 C', temp90C),
    ('RH = 25%', relHum25),
    ('RH = 50%', relHum50),
    ('RH = 75%', relHum75),
    ('RH = 100%', relHum100),
    ('P = 1.5 bar', press1_5bar),
    ('P = 2 bar', press2bar),
    ('P = 2.5 bar', press2_5bar),
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
#%%
threshold = 0.01  # Change threshold as needed

plt.figure(figsize=(12, 8))
for name, data in variables:
    mean_voltages, mean_currents = mean_groups_by_voltage_change(data, threshold=threshold)
    plt.plot(mean_currents, mean_voltages, marker='o', linestyle='-', label=name)
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')
plt.title(f'Polarization Curves (ΔV={threshold}V) for All Cases')
plt.legend()
plt.grid(True)
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
#%%
threshold = 0.01  # Use your desired threshold

plt.figure(figsize=(12, 8))
for name, data in variables:
    mean_voltages, mean_currents = mean_groups_by_voltage_change(data, threshold=threshold)
    plt.plot(mean_currents, mean_voltages, marker='o', linestyle='-', label=name)
    # Add arrows to show direction
    for i in range(len(mean_currents) - 1):
        plt.annotate(
            '', 
            xy=(mean_currents[i+1], mean_voltages[i+1]), 
            xytext=(mean_currents[i], mean_voltages[i]),
            arrowprops=dict(arrowstyle='->', color=plt.gca().lines[-1].get_color(), lw=1)
        )
plt.xlabel('Current (A)')
plt.ylabel('Voltage (V)')
plt.title(f'Polarization Curves (ΔV={threshold}V) with Direction Arrows')
plt.legend()
plt.grid(True)
plt.show()

#%%
#%%
threshold = 0.01  # Use your desired threshold

# Define groups (always include baseCase)
groups = {
    'Temperature': [
        ('baseCase', baseCase),
        ('T = 30 C', temp30C),
        ('T = 50 C', temp50C),
        ('T = 70 C', temp70C),
        ('T = 90 C', temp90C)
    ],
    'Relative Humidity': [
        ('baseCase', baseCase),
        ('RH = 25%', relHum25),
        ('RH = 50%', relHum50),
        ('RH = 75%', relHum75),
        ('RH = 100%', relHum100)
    ],
    'Pressure': [
        ('baseCase', baseCase),
        ('P = 1.5 bar', press1_5bar),
        ('P = 2 bar', press2bar),
        ('P = 2.5 bar', press2_5bar)
    ],
    'Extra': [
        ('baseCase', baseCase),
        ('extraCase', extraCase)
    ]
}

for group_name, group_vars in groups.items():
    plt.figure(figsize=(10, 6))
    for name, data in group_vars:
        mean_voltages, mean_currents = mean_groups_by_voltage_change(data, threshold=threshold)
        plt.plot(mean_currents, mean_voltages, marker='o', linestyle='-', label=name)
        # Add arrows to show direction
        for i in range(len(mean_currents) - 1):
            plt.annotate(
                '',
                xy=(mean_currents[i+1], mean_voltages[i+1]),
                xytext=(mean_currents[i], mean_voltages[i]),
                arrowprops=dict(arrowstyle='->', color=plt.gca().lines[-1].get_color(), lw=1)
            )
    plt.xlabel('Current (A)')
    plt.ylabel('Voltage (V)')
    plt.title(f'{group_name} Polarization Curves (ΔV={threshold}V) with Direction Arrows')
    plt.legend()
    plt.grid(True)
    plt.show()


#%%
mean_voltages, mean_currents = mean_groups_by_voltage_change(temp50C, threshold=threshold)
plt.plot(mean_currents, mean_voltages, marker='o', linestyle='-', label=name)