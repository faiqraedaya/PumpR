import CoolProp.CoolProp as CP

class PumpSimulator:
    def __init__(self):
        self.components = []
        self.mole_fractions = []
        self.mass_fractions = []
        
    def add_component(self, fluid, mole_fraction):
        """Add component to mixture"""
        self.components.append(fluid)
        self.mole_fractions.append(mole_fraction)
        
    def normalize_fractions(self):
        """Normalize mole fractions to sum to 1"""
        total = sum(self.mole_fractions)
        if total > 0:
            self.mole_fractions = [x/total for x in self.mole_fractions]
            
    def calculate_mixture_properties(self, T, P):
        """Calculate mixture properties using CoolProp"""
        try:
            if len(self.components) == 1:
                # Pure component
                fluid = self.components[0]
                rho = CP.PropsSI('D', 'T', T, 'P', P, fluid)
                mu = CP.PropsSI('V', 'T', T, 'P', P, fluid)
                cp = CP.PropsSI('C', 'T', T, 'P', P, fluid)
                k = CP.PropsSI('L', 'T', T, 'P', P, fluid)
                return rho, mu, cp, k
            else:
                # Mixture - simplified approach
                rho_mix = 0
                mu_mix = 0
                cp_mix = 0
                k_mix = 0
                
                for i, (fluid, x_i) in enumerate(zip(self.components, self.mole_fractions)):
                    try:
                        rho_i = CP.PropsSI('D', 'T', T, 'P', P, fluid)
                        mu_i = CP.PropsSI('V', 'T', T, 'P', P, fluid)
                        cp_i = CP.PropsSI('C', 'T', T, 'P', P, fluid)
                        k_i = CP.PropsSI('L', 'T', T, 'P', P, fluid)
                        
                        rho_mix += x_i * rho_i
                        mu_mix += x_i * mu_i
                        cp_mix += x_i * cp_i
                        k_mix += x_i * k_i
                    except:
                        continue
                        
                return rho_mix, mu_mix, cp_mix, k_mix
        except Exception as e:
            raise Exception(f"Property calculation failed: {str(e)}") 