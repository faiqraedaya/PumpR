"""Result reporting: results-panel text and CSV export (no Qt dependency)."""
import csv

from src.core.units import k_to_c, pa_to_kpa, m3s_to_m3h, w_to_kw

# (CSV header, key in the curve-data dict)
CSV_COLUMNS = [
    ('Q (m3/h)', 'Q_m3h'),
    ('Head (m)', 'head'),
    ('Shaft Power (kW)', 'power_kw'),
    ('Efficiency (%)', 'eff_pct'),
    ('NPSH Required (m)', 'npsh_req'),
]


def build_results_text(components, mole_fractions, T, P, Q, H,
                       rho, mu, cp, k, pump, performance):
    """Build the formatted text shown in the results panel.

    components/mole_fractions : mixture composition
    pump : dict with 'D_imp', 'N_rpm', 'eta'
    performance : dict returned by PumpPerformance.calculate_pump_performance
    """
    results = f"""
CENTRIFUGAL PUMP PERFORMANCE ANALYSIS
====================================

MIXTURE COMPOSITION:
{'-'*40}
"""
    for i, (comp, x) in enumerate(zip(components, mole_fractions)):
        results += f"Component {i+1}: {comp:<15} Mole Fraction: {x:.4f}\n"
    results += f"""
OPERATING CONDITIONS:
{'-'*40}
Temperature:           {T:.2f} K ({k_to_c(T):.2f} °C)
Pressure:              {pa_to_kpa(P):.1f} kPa
Flow Rate:             {Q:.4f} m³/s ({m3s_to_m3h(Q):.1f} m³/h)
Head:                  {H:.2f} m

FLUID PROPERTIES:
{'-'*40}
Density:               {rho:.2f} kg/m³
Dynamic Viscosity:     {mu*1000:.4f} mPa·s
Specific Heat:         {cp/1000:.3f} kJ/kg·K
Thermal Conductivity:  {k:.4f} W/m·K

PUMP PARAMETERS:
{'-'*40}
Impeller Diameter:     {pump['D_imp']:.3f} m
Rotation Speed:        {pump['N_rpm']:.0f} rpm
Efficiency:            {pump['eta']*100:.1f}%

PERFORMANCE RESULTS:
{'-'*40}
Flow Coefficient (φ):      {performance['phi']:.6f}
Head Coefficient (ψ):      {performance['psi']:.6f}
Reynolds Number:           {performance['Re']:.0f}
Specific Speed (Ns, dim.): {performance['Ns']:.3f}

NPSH ANALYSIS:
{'-'*40}
NPSH Required:         {performance['NPSH_req']:.2f} m
"""
    npsh_avail = performance['NPSH_avail']
    npsh_margin = performance['NPSH_margin']
    if npsh_avail is not None:
        results += f"NPSH Available:        {npsh_avail:.2f} m\n"
        results += f"NPSH Margin:           {npsh_margin:.2f} m"
        results += "  *** CAVITATION RISK ***\n" if npsh_margin <= 0 else "  (OK)\n"
    else:
        results += "NPSH Available:        N/A (no vapor pressure at this temperature)\n"
    results += f"""
POWER ANALYSIS:
{'-'*40}
Hydraulic Power:       {w_to_kw(performance['P_hydraulic']):.2f} kW
Shaft Power:           {w_to_kw(performance['P_shaft']):.2f} kW
Power Loss:            {w_to_kw(performance['P_shaft']-performance['P_hydraulic']):.2f} kW

DIMENSIONLESS ANALYSIS:
{'-'*40}
Flow Coefficient:      {performance['phi']:.6f}
Head Coefficient:      {performance['psi']:.6f}
Power Coefficient:     {performance['P_coeff']:.6f}
"""
    return results


def write_curves_csv(path, curve_data):
    """Write the performance-curve table to ``path`` as CSV. Returns row count."""
    headers = [h for h, _ in CSV_COLUMNS]
    columns = [curve_data[key] for _, key in CSV_COLUMNS]
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in zip(*columns):
            writer.writerow([f"{v:.6g}" for v in row])
    return len(columns[0])
