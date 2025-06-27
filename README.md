# PumpR

## Overview
PumpR is a simple desktop application for simulating the performance of centrifugal pumps handling pure fluids or mixtures

## Features
- Interactive GUI built with PyQt5
- Supports both pure fluids and mixtures using CoolProp
- User input for fluid composition, operating conditions, and pump parameters
- Calculates pump performance metrics (flow, head, power, efficiency, specific speed, NPSH, etc.)
- Visualizes performance curves and maps using matplotlib

## Requirements 
- Python 3.7+
- [CoolProp](http://www.coolprop.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/faiqraedaya/PumpR
   cd "PumpR"
   ```
2. **Install dependencies:**
   ```bash
   pip install PyQt5 matplotlib numpy CoolProp
   ```

## Usage
1. To launch the application, run:
   ```bash
   python main.py
   ```
2. Set the temperature, inlet & outlet pressure, and feed rate.
3. Select the pure fluid or define a mixture by selecting materials from CoolProp's database.
4. Run the simulation.
5. View and export the pump performance results & plots.

## License
This project is provided under the MIT License.
