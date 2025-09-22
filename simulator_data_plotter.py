import json
import matplotlib.pyplot as plt
import datetime
import numpy as np

LEGEND = {
    "ConsumptionActivePower": ["Consumption", "black"],
    "EssActivePower": ["Battery Output", "blue"],
    "EssSoc": ["Battery Capacity", "green"],
    "GridActivePower": ["Grid Power", "red"],
    "ProductionActivePower": ["Production", "orange"]
}

# Load output JSON file
file_path = './data/simulation_response.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Extract data
timestamps = data["result"]["timestamps"]
times = [datetime.datetime.fromisoformat(ts.replace("Z", "")) for ts in timestamps]

# Extract all fields
data_fields = data["result"]["data"].keys()

# Load baseline data with no controller JSON file
file_path_base = './data/simulation_response_baseline.json'
with open(file_path_base, 'r') as f:
    data_base = json.load(f)

# Compare grid power draw with baseline 
gridActivePower = data["result"]["data"]["_sum/GridActivePower"]
gridActivePower_base = data_base["result"]["data"]["_sum/GridActivePower"]

gridActivePower = np.array(gridActivePower)
gridActivePower_base = np.array(gridActivePower_base)

gridPowerDrawTotal = sum(gridActivePower[gridActivePower > 0])
gridPowerDrawTotal_base = sum(gridActivePower_base[gridActivePower_base > 0])

print("Total Grid Power Draw:", gridPowerDrawTotal)
print("Total Grid Power Draw Baseline:", gridPowerDrawTotal_base)
print(f"Percentage Reduction: {(1-(gridPowerDrawTotal/gridPowerDrawTotal_base)) * 100}%")


fig, ax1 = plt.subplots(2, figsize=(12, 6))
ax2 = ax1[0].twinx()
lines = []
labels = []

for field in data_fields:
    field_label = field.split("/")[1]
    label, color = LEGEND[field_label]
    if label == "Battery Capacity":
        line, = ax2.plot(times, (np.array(data["result"]["data"][field]) / 100) * 10200, label=label, c=color)
        ax2.set_ylim([-40000, 40000])
        ax2.set_xlim([times[0], times[150]])
    else:
        line, = ax1[0].plot(times, data["result"]["data"][field], label=label, c=color)

    lines.append(line)
    labels.append(label)

power_draw = gridActivePower.copy()
power_draw_base = gridActivePower_base.copy()
power_draw[power_draw < 0] = 0
power_draw_base[power_draw_base < 0] = 0

ax1[1].plot(times, power_draw, label="Battery Controller", c='r')
ax1[1].plot(times, power_draw_base, label="No Battery Controller", c='r', linestyle='dashed')

ax1[0].set_xlabel("Time")
ax1[0].set_ylabel("Power (Watts)")
ax1[1].set_ylabel("Power (Watts)")
ax2.set_ylabel("Capacity (Watt Hours)")

ax1[0].set_xlim([times[0], times[150]])
ax1[1].set_xlim([times[0], times[150]])

ax1[0].set_title("Simulation Data With Peak Shaving Battery Controller (Hottest Week)")
ax1[1].set_title("Grid Power Draw Comparison")

ax1[0].legend(lines, labels, loc="upper left", prop={'size': 6})
ax1[1].legend(loc="upper left", prop={'size': 6})
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()