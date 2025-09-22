OpenEMS Simulation Query Tool

This project provides a Python-based interface to query the OpenEMS Edge
 simulation server hosted locally, retrieve simulation results, and visualize them using graphs.

Folder Structure
project-root/
├── data/
│   ├── simulation_input.csv         # Input data: consumption & generation (W)
│   ├── simulation_response.json     # Output data: OpenEMS response
│   └── simulation_response_baseline.json  # Baseline (uncontrolled) response
├── main.py                          # Core script to send queries and plot results
└── README.md                        # Project documentation

Requirements

OpenEMS Edge
 installed and running locally

WebSocket API must be enabled on the OpenEMS Edge server (http://localhost:8084)

Python 3.7+

Python libraries: websocket-client, matplotlib, pandas, json

Setup Instructions

Run OpenEMS Edge locally
Follow the instructions to configure and launch the simulator:
OpenEMS Simulator README

Prepare input data
Provide your simulation input as a CSV file at:
./data/simulation_input.csv

Format: Timestamps (default: 15-minute intervals), Power Consumption (W), Power Generation (W)

Run the script
Execute the Python script to send queries and plot the returned simulation results:

python main.py

Output Files

./data/simulation_response.json: Standard OpenEMS response to the current simulation input.

./data/simulation_response_baseline.json: Baseline response with no control logic applied. (Note: specific to the current project)

📝 Notes

Ensure the OpenEMS server is fully initialized before running the script to avoid WebSocket connection errors.

The tool assumes OpenEMS is hosted at http://localhost:8084. Update the URL in the script if needed.
