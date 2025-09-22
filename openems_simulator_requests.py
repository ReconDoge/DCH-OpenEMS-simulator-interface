import requests
import json
import pandas as pd


# Load input CSV file
csv_file_path = "./data/simulation_input.csv"
df = pd.read_csv(csv_file_path, skiprows=1)

df_clean = df.iloc[:, [1, 2]].copy()
df_clean.columns = ["Electricity Consumption (kW)", "Electricity Generation (kW)"]
df_clean = df_clean.apply(pd.to_numeric, errors="coerce")

# Convert to kilowatts
df_clean *= 1000

# Convert to NumPy arrays
electricity_consumption = df_clean.iloc[:, 0].values
electricity_generation = df_clean.iloc[:, 1].values

# Print first few values to check
# print(electricity_consumption[:5], electricity_generation[:5])

# import matplotlib.pyplot as plt

# plt.plot(electricity_consumption)
# plt.plot(-1*electricity_generation)
# plt.show()


# OpenEMS Edge JSON-RPC endpoint
url = "http://localhost:8084/jsonrpc"

# JSON-RPC request payload
payload = {
   "method":"componentJsonApi",
   "params":{
      "componentId":"_simulator",
      "payload":{
         "method":"executeSimulation",
         "params":{
            "components":[
               {
                  "factoryPid":"Scheduler.AllAlphabetically",
                  "properties":[
                     {
                        "name":"id",
                        "value":"scheduler0"
                     }
                  ]
               },
               {
                  "factoryPid":"Simulator.GridMeter.Reacting",
                  "properties":[
                     {
                        "name":"id",
                        "value":"meter0"
                     }
                  ]
               },
               {
                  "factoryPid":"Simulator.NRCMeter.Acting",
                  "properties":[
                     {
                        "name":"id",
                        "value":"meter1"
                     },
                     {
                        "name":"alias",
                        "value":"Consumption"
                     },
                     {
                        "name":"datasource.id",
                        "value":"_simulator"
                     }
                  ]
               },
               {
                  "factoryPid":"Simulator.ProductionMeter.Acting",
                  "properties":[
                     {
                        "name":"id",
                        "value":"meter2"
                     },
                     {
                        "name":"alias",
                        "value":"South Roof"
                     },
                     {
                        "name":"datasource.id",
                        "value":"_simulator"
                     }
                  ]
               },
               {
                  "factoryPid":"Simulator.EssSymmetric.Reacting",
                  "properties":[
                     {
                        "name":"id",
                        "value":"ess0"
                     },
                     {
                        "name":"maxApparentPower",
                        "value":10000
                     },
                     {
                        "name":"capacity",
                        "value":10200
                     },
                     {
                        "name":"initialSoc",
                        "value":50
                     }
                  ]
               },
               {
                  "factoryPid":"Controller.Symmetric.Balancing",
                  "properties":[
                     {
                        "name":"id",
                        "value":"ctrlBalancing0"
                     },
                     {
                        "name":"ess.id",
                        "value":"ess0"
                     },
                     {
                        "name":"meter.id",
                        "value":"meter0"
                     }
                  ]
               },
               {
                  "factoryPid":"Controller.Symmetric.PeakShaving",
                  "properties":[
                     {
                        "name":"id",
                        "value":"ctrlPeakShaving0"
                     },
                     {
                        "name":"ess.id",
                        "value":"ess0"
                     },
                     {
                        "name":"meter.id",
                        "value":"meter0"
                     }
                  ]
               }
            ],
            "clock":{
               "start":"2000-01-01T00:00:00.00Z",
               "end":"2000-01-08T00:00:00.00Z",
               "timeleapPerCycle":900000,
               "executeCycleTwice":True
            },
            "profiles":{
               "meter1/ActivePower": list(electricity_consumption),     # Building power consumption
               "meter2/ActivePower": list(-1*electricity_generation)    # PV power generation
            },
            "collect":[
               "_sum/GridActivePower",
               "_sum/EssActivePower",
               "_sum/ProductionActivePower",
               "_sum/ConsumptionActivePower",
               "_sum/EssSoc"
            ]
         }
      }
   }
}
# Headers for JSON-RPC request
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic YWRtaW46YWRtaW4="
}

# Send the request
response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Response Code:", response.status_code)

if response.status_code == 200:

   response_json = response.json()

   with open("./data/simulation_response.json", "w") as file:
      json.dump(response_json, file, indent=4)

      print("JSON saved in 'data/simulation_response.json'")

# print("Response:", response.json())
