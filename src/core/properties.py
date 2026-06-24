"""Fluid property access (CoolProp) with caching, and mixture handling.

This module has no GUI dependencies. A single ``PropertyCache`` is meant to be
created once and injected into the ``Mixture`` objects that need it, so repeated
CoolProp look-ups for the same state are served from the cache.
"""
import CoolProp.CoolProp as CP


class PropertyCache:
    """Caches CoolProp property look-ups keyed on (output, fluid, T, P).

    CoolProp evaluations are relatively expensive; caching avoids re-querying
    the backend for states that recur within and across calculations.
    """

    def __init__(self):
        self._cache = {}

    def prop(self, output, T, P, fluid):
        """Return a single-phase property (e.g. 'D', 'V', 'C', 'L', 'M') at (T, P)."""
        key = (output, fluid, round(T, 6), round(P, 3))
        if key not in self._cache:
            self._cache[key] = CP.PropsSI(output, 'T', T, 'P', P, fluid)
        return self._cache[key]

    def vapor_pressure(self, T, fluid):
        """Saturation pressure (Pa) at temperature T. Raises if no saturation
        state exists at T (e.g. a supercritical / non-condensable component)."""
        key = ('Pvap', fluid, round(T, 6))
        if key not in self._cache:
            self._cache[key] = CP.PropsSI('P', 'T', T, 'Q', 0, fluid)
        return self._cache[key]


class Mixture:
    """A fluid mixture defined by component CoolProp names and mole fractions.

    Property mixing uses mass-fraction weighting (with ideal volume additivity
    for density), so a single component reduces exactly to its pure property.
    """

    def __init__(self, props):
        self.props = props          # injected PropertyCache (shared)
        self.components = []
        self.mole_fractions = []

    def add_component(self, fluid, mole_fraction):
        """Add component to mixture"""
        self.components.append(fluid)
        self.mole_fractions.append(mole_fraction)

    def normalize_fractions(self):
        """Normalize mole fractions to sum to 1"""
        total = sum(self.mole_fractions)
        if total > 0:
            self.mole_fractions = [x / total for x in self.mole_fractions]

    def mass_fractions(self, T, P):
        """Convert mole fractions to mass fractions using component molar masses"""
        molar_masses = [self.props.prop('M', T, P, fluid) for fluid in self.components]
        total = sum(x_i * M_i for x_i, M_i in zip(self.mole_fractions, molar_masses))
        if total <= 0:
            raise ValueError("Sum of (mole fraction x molar mass) is non-positive")
        return [x_i * M_i / total for x_i, M_i in zip(self.mole_fractions, molar_masses)]

    def calculate_properties(self, T, P):
        """Calculate mixture density, viscosity, specific heat and conductivity.

        Density uses ideal volume additivity (1/rho = sum w_i/rho_i); specific
        heat, viscosity and conductivity use mass-weighted averages.
        """
        try:
            w = self.mass_fractions(T, P)
            inv_rho_mix = 0.0
            mu_mix = 0.0
            cp_mix = 0.0
            k_mix = 0.0
            for fluid, w_i in zip(self.components, w):
                rho_i = self.props.prop('D', T, P, fluid)
                mu_i = self.props.prop('V', T, P, fluid)
                cp_i = self.props.prop('C', T, P, fluid)
                k_i = self.props.prop('L', T, P, fluid)
                inv_rho_mix += w_i / rho_i
                mu_mix += w_i * mu_i
                cp_mix += w_i * cp_i
                k_mix += w_i * k_i
            rho_mix = 1.0 / inv_rho_mix
            return rho_mix, mu_mix, cp_mix, k_mix
        except Exception as e:
            raise Exception(f"Property calculation failed: {str(e)}")

    def vapor_pressure(self, T):
        """Estimate mixture vapor pressure at T (Pa) via Raoult's law.

        Returns None if no component has a defined saturation pressure at T
        (e.g. all components supercritical), so NPSH-available is reported N/A.
        """
        p_vap = 0.0
        any_valid = False
        for fluid, x_i in zip(self.components, self.mole_fractions):
            try:
                p_vap_i = self.props.vapor_pressure(T, fluid)
            except Exception:
                # Component has no saturation state at T; skip its contribution.
                continue
            p_vap += x_i * p_vap_i
            any_valid = True
        return p_vap if any_valid else None
