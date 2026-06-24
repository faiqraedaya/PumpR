# PumpR

## Overview
PumpR is a simple desktop application for simulating the performance of centrifugal pumps handling pure fluids or mixtures

## Features
- Interactive GUI built with PySide6
- Supports both pure fluids and mixtures using CoolProp (mass-fraction weighted mixing)
- User input for fluid composition, operating conditions, and pump parameters
- Calculates pump performance metrics: flow/head coefficients, impeller Reynolds number, dimensionless specific speed, hydraulic/shaft power, and power coefficient
- NPSH analysis: NPSH required (from suction specific speed), NPSH available (from suction and vapor pressure) and the resulting margin, with a cavitation-risk warning
- Performance curves (head, power, efficiency, NPSH) passing through the design point and speed-varying performance maps derived from the affinity laws
- Export of the computed performance curves to CSV

## Installation
```bash
git clone https://github.com/faiqraedaya/PumpR
cd PumpR
uv sync
```

## Usage
```bash
uv run main.py
```

## License
[MIT](LICENSE)