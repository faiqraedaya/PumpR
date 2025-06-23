import numpy as np

class PumpPerformance:
    @staticmethod
    def calculate_pump_performance(Q, H, rho, mu, D_imp, N, eta_pump=0.75):
        """Calculate pump performance parameters"""
        # Flow coefficient
        phi = Q / (N * D_imp**3)
        
        # Head coefficient
        psi = 9.81 * H / (N**2 * D_imp**2)
        
        # Reynolds number
        Re = rho * N * D_imp**2 / mu
        
        # Power calculation
        P_hydraulic = rho * 9.81 * Q * H  # Hydraulic power (W)
        P_shaft = P_hydraulic / eta_pump   # Shaft power (W)
        
        # Specific speed
        Ns = N * np.sqrt(Q) / (9.81 * H)**(3/4)
        
        # NPSH calculation (simplified)
        NPSH_required = 0.2 * (N * np.sqrt(Q) / 1000)**2
        
        return {
            'phi': phi,
            'psi': psi,
            'Re': Re,
            'P_hydraulic': P_hydraulic,
            'P_shaft': P_shaft,
            'Ns': Ns,
            'NPSH_req': NPSH_required,
            'eta_pump': eta_pump
        } 