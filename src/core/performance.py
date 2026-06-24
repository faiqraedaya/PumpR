"""Pump performance calculations and parametric curve models (GUI-free)."""
import numpy as np

from src.core.units import G, m3s_to_m3h, rad_s_to_rpm, w_to_kw


class PumpPerformance:
    @staticmethod
    def calculate_pump_performance(Q, H, rho, mu, D_imp, N, eta_pump=0.75,
                                   P_inlet=None, P_vapor=None, Nss=3.0):
        """Calculate pump performance parameters at a single operating point.

        Q       : volumetric flow rate (m^3/s)
        H       : head (m)
        rho     : fluid density (kg/m^3)
        mu      : dynamic viscosity (Pa.s)
        D_imp   : impeller diameter (m)
        N       : rotational speed (rad/s)
        eta_pump: pump efficiency (-)
        P_inlet : pump inlet/suction pressure (Pa), used for NPSH available
        P_vapor : fluid vapor pressure (Pa), used for NPSH available
        Nss     : dimensionless suction specific speed used to estimate NPSH
                  required (~3.0 for a typical centrifugal pump)
        """
        # Validate geometry / operating inputs that would otherwise divide by zero.
        if N <= 0:
            raise ValueError("Rotational speed must be positive")
        if D_imp <= 0:
            raise ValueError("Impeller diameter must be positive")
        if mu <= 0:
            raise ValueError("Viscosity must be positive")
        if eta_pump <= 0:
            raise ValueError("Efficiency must be positive")
        if Q < 0 or H < 0:
            raise ValueError("Flow rate and head must be non-negative")

        # Dimensionless flow and head coefficients
        phi = Q / (N * D_imp**3)
        psi = G * H / (N**2 * D_imp**2)

        # Impeller Reynolds number
        Re = rho * N * D_imp**2 / mu

        # Power calculation
        P_hydraulic = rho * G * Q * H  # Hydraulic power (W)
        P_shaft = P_hydraulic / eta_pump  # Shaft power (W)

        # Power coefficient
        P_coeff = P_shaft / (rho * N**3 * D_imp**5)

        # Dimensionless specific speed (type number): omega*sqrt(Q)/(g*H)^(3/4)
        Ns = N * np.sqrt(Q) / (G * H)**(3/4) if H > 0 else 0.0

        # NPSH required estimated from a fixed suction specific speed:
        #   Nss = omega*sqrt(Q)/(g*NPSHr)^(3/4)  ->  NPSHr = (omega*sqrt(Q)/Nss)^(4/3)/g
        if Q > 0 and Nss > 0:
            NPSH_required = (N * np.sqrt(Q) / Nss)**(4/3) / G
        else:
            NPSH_required = 0.0

        # NPSH available (requires suction pressure and vapor pressure):
        #   NPSHa = (P_inlet - P_vapor)/(rho*g)
        # Velocity head and static elevation at the suction are neglected.
        NPSH_available = None
        NPSH_margin = None
        if P_inlet is not None and P_vapor is not None:
            NPSH_available = (P_inlet - P_vapor) / (rho * G)
            NPSH_margin = NPSH_available - NPSH_required

        return {
            'phi': phi,
            'psi': psi,
            'Re': Re,
            'P_hydraulic': P_hydraulic,
            'P_shaft': P_shaft,
            'P_coeff': P_coeff,
            'Ns': Ns,
            'NPSH_req': NPSH_required,
            'NPSH_avail': NPSH_available,
            'NPSH_margin': NPSH_margin,
            'eta_pump': eta_pump
        }


def head_curve(Q, Q_design, H_design):
    """Synthetic pump head curve passing through the design point.

    Shutoff head (Q=0) is 1.2*H_design and the curve falls parabolically so
    that H(Q_design) = H_design.
    """
    return H_design * (1.2 - 0.2 * (Q / Q_design)**2)


def efficiency_curve(Q, Q_bep, eta_bep):
    """Parabolic efficiency curve peaking at the best-efficiency point.

    eta(Q) = eta_bep * (2*x - x^2) with x = Q/Q_bep, so efficiency is zero at
    zero flow, peaks at eta_bep at Q_bep, and is clamped non-negative.
    """
    x = Q / Q_bep
    return np.maximum(eta_bep * (2 * x - x**2), 0.0)


def compute_curve_data(Q_design, H_design, rho, mu, D_imp, N, eta):
    """Compute head/power/efficiency/NPSH curves over a flow range.

    Returns a dict of numpy arrays (flow in m^3/h) suitable for plotting and CSV
    export, plus the design flow for annotating the design point.
    """
    Q_range = np.linspace(0.1 * Q_design, 1.5 * Q_design, 50)
    heads = []
    powers = []
    efficiencies = []
    npsh_req = []
    for Q in Q_range:
        H = head_curve(Q, Q_design, H_design)
        eta_Q = float(efficiency_curve(Q, Q_design, eta))
        performance = PumpPerformance.calculate_pump_performance(
            Q, H, rho, mu, D_imp, N, eta_Q
        )
        heads.append(H)
        powers.append(w_to_kw(performance['P_shaft']))
        efficiencies.append(eta_Q * 100)
        npsh_req.append(performance['NPSH_req'])
    return {
        'Q_m3h': m3s_to_m3h(Q_range),
        'head': np.array(heads),
        'power_kw': np.array(powers),
        'eff_pct': np.array(efficiencies),
        'npsh_req': np.array(npsh_req),
        'Q_design_m3h': m3s_to_m3h(Q_design),
    }


def compute_map_data(Q_design, H_design, rho, N_design, eta):
    """Compute head/power curve families across a range of speeds via affinity laws.

    Returns a list of per-speed dicts (rpm, flow in m^3/h, head, power in kW).
    """
    N_range = np.linspace(0.7 * N_design, 1.3 * N_design, 5)
    Q_range = np.linspace(0.0, 1.5 * Q_design, 30)
    series = []
    for N in N_range:
        r = N / N_design
        # Affinity laws applied to the design head curve (Q ~ N, H ~ N^2):
        # H_N(Q) = H_design*(1.2*r^2 - 0.2*(Q/Q_design)^2)
        heads = H_design * (1.2 * r**2 - 0.2 * (Q_range / Q_design)**2)
        powers = w_to_kw(rho * G * Q_range * heads / eta)
        series.append({
            'rpm': rad_s_to_rpm(N),
            'Q_m3h': m3s_to_m3h(Q_range),
            'head': heads,
            'power_kw': powers,
        })
    return series
