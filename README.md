# PumpR

## Overview
*PumpR is a desktop application that estimates the performance of a centrifugal pump handling a pure fluid or a mixture. It gives the duty-point performance, NPSH margin and indicative curves from a few design inputs.*

## Features
- PySide6 GUI with a mixture editor for ten common fluids
- Mixture properties from CoolProp with mass-fraction weighting
- Flow and head coefficients, impeller Reynolds number, specific speed and power coefficient
- Hydraulic and shaft power at the design point
- NPSH required, NPSH available and margin, with a cavitation-risk warning
- Head, power, efficiency and NPSH curves through the design point
- Speed-varying performance maps from the affinity laws
- CSV export of the performance curves

## Install
```bash
git clone https://github.com/faiqraedaya/PumpR
cd PumpR
uv sync
```

## Usage
```bash
uv run main.py
```
Select Water, click Add Component, then click Calculate Performance with the default inputs (298.15 K, 101325 Pa, 0.1 m³/s, 50 m, 0.3 m impeller, 1750 rpm, 75 % efficiency). The Results, Performance Curves and Performance Maps tabs fill in. Click Export Performance Curves (CSV) to save the curve table.

## Technical details
Inputs are entered in the GUI: components with mole fractions, temperature (K), suction pressure (Pa), flow (m³/s), head (m), impeller diameter (m), speed (rpm) and efficiency. Component properties come from CoolProp at the given temperature and pressure. Mixture density uses ideal volume additivity, and viscosity, heat capacity and conductivity use mass-weighted averages. Mixture vapour pressure comes from Raoult's law.

The duty point gives the dimensionless flow coefficient Q/(ND³), head coefficient gH/(N²D²), impeller Reynolds number ρND²/μ, hydraulic power ρgQH, shaft power and power coefficient. Specific speed is the dimensionless form ωQ^0.5/(gH)^0.75. NPSH required is estimated from a fixed suction specific speed of 3.0. NPSH available is (P − Pvap)/(ρg), neglecting velocity head and elevation. The head curve is a parabola with a shutoff head of 1.2 times design head, and efficiency is a parabola peaking at the design flow. Performance maps scale the head curve across 70–130 % of design speed with the affinity laws.

Results appear as a text report and Matplotlib plots in the GUI. The CSV export lists flow (m³/h), head (m), shaft power (kW), efficiency (%) and NPSH required (m) at 50 points from 10 % to 150 % of design flow.

## License
MIT — see [LICENSE](LICENSE).
