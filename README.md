# PumpR

## Overview
PumpR is a desktop application for simulating the performance of centrifugal pumps handling pure fluids or mixtures. The simulator provides detailed pump performance calculations and visualizations based on user-defined fluid properties and pump parameters.

## Features
- Interactive GUI built with PyQt5
- Supports both pure fluids and mixtures (using CoolProp)
- User input for fluid composition, operating conditions, and pump parameters
- Calculates pump performance (flow, head, power, efficiency, specific speed, NPSH, etc.)
- Visualizes performance curves and maps using matplotlib
- Results summary in a clear, readable format

## Requirements 
- Python 3.7+
- [CoolProp](http://www.coolprop.org/)
- PyQt5
- matplotlib
- numpy

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

## File Structure
- `main.py` — Entry point for the application
- `src/gui.py` — Main GUI logic and user interface
- `src/simulator.py` — Fluid property and mixture calculations
- `src/performance.py` — Pump performance calculations
- `src/matplotlib_widget.py` — Embeds matplotlib plots in the GUI

## License
This project is provided under the MIT License.
