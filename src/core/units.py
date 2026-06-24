"""Physical constants and unit conversions shared across the core layer."""
import numpy as np

G = 9.81  # gravitational acceleration (m/s^2)

def rpm_to_rad_s(rpm):
    """Rotational speed: rev/min -> rad/s"""
    return rpm * 2 * np.pi / 60

def rad_s_to_rpm(omega):
    """Rotational speed: rad/s -> rev/min"""
    return omega * 60 / (2 * np.pi)

def m3s_to_m3h(q):
    """Volumetric flow: m^3/s -> m^3/h"""
    return q * 3600.0

def pa_to_kpa(p):
    """Pressure: Pa -> kPa"""
    return p / 1000.0

def w_to_kw(p):
    """Power: W -> kW"""
    return p / 1000.0

def k_to_c(t):
    """Temperature: K -> degC"""
    return t - 273.15
