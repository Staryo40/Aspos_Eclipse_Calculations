from enum_types import *
from utils import *
import math

def lunation_number(year_float, moon_phase: MoonPhase = MoonPhase.NEW_MOON):
    k = (year_float - 2000) * 12.368_5

    if moon_phase == MoonPhase.NEW_MOON:
        add = 0
    elif moon_phase == MoonPhase.FIRST_QUARTER:
        add = 0.25
    elif moon_phase == MoonPhase.FULL_MOON:
        add = 0.5
    else:
        add = 0.75
    
    return math.floor(k) + add

def base_lunation_number(year_float):
    return lunation_number(year_float)

def julian_century_time(k):
    return k / 1_235.85

def lunar_jde(k):
    T = julian_century_time(k)
    jde = 2_451_550.097_66 + 29.530_588_861 * k + 0.000_154_37 * (T**2) - 0.000_000_150 * (T**3) + 0.000_000_000_73 * (T**4)
    return jde

def excentric_anomaly(T):
    return 1 - 0.002_516 * T - 0.000_007_4 * T**2

def solar_mean_anomaly(k):
    T = julian_century_time(k)
    Ms = 2.553_4 + 29.105_356_70 * k - 0.000_001_4 * T**2 - 0.000_000_11 * T**3
    return Ms

def lunar_mean_anomaly(k):
    T = julian_century_time(k)
    Mm = 201.564_3 + 385.816_935_28 * k + 0.010_758_2 * T**2 + 0.000_012_38 * T**3 - 0.000_000_058 * T**4
    return Mm

def lunar_argument_of_latitude(k):
    T = julian_century_time(k)
    F_deg = 160.710_8 + 390.670_502_84 * k - 0.001_611_8 * T**2 - 0.000_002_27 * T**3 + 0.000_000_011 * T**4
    
    F_deg = F_deg % 360.0
    return math.radians(F_deg)

def eccentricity_factor(k):
    T = julian_century_time(k)
    return 1 - 0.002_516 * T - 0.000_0074 * (T ** 2)

def lunar_longitude_of_ascending_node(k):
    T = julian_century_time(k)
    omega_deg = 124.774_6 - 1.563_755_88 * k + 0.002_067_2 * T**2 + 0.000_002_15 * T**3
    return math.radians(omega_deg)

def calculate_f1(k):
    F = lunar_argument_of_latitude(k)
    OMEGA = lunar_longitude_of_ascending_node(k)
    return F - 0.026_65 * math.sin(OMEGA)

def calculate_a1(k):
    T = julian_century_time(k)
    return 299.77 + 0.107_408 * k - 0.009_173 * T**2

def corr_jde_solar(Mm, Ms, F1, E, A1, Omega):
    Mm_rad = math.radians(Mm)
    Ms_rad = math.radians(Ms)
    A1_rad = math.radians(A1)
    F1_rad = math.radians(F1)
    Omega_rad = math.radians(Omega)

    return (
        -0.4075 * math.sin(Mm_rad)
        + 0.1721 * E * math.sin(Ms_rad)
        + 0.0161 * math.sin(2 * Mm_rad)
        - 0.0097 * math.sin(2 * F1_rad)
        + 0.0073 * E * math.sin(Mm_rad - Ms_rad)
        - 0.0050 * E * math.sin(Mm_rad + Ms_rad)
        - 0.0023 * math.sin(Mm_rad - 2 * F1_rad)
        + 0.0021 * E * math.sin(2 * Ms_rad)
        + 0.0012 * math.sin(Mm_rad + 2 * F1_rad)
        - 0.0006 * E * math.sin(2 * Mm_rad + Ms_rad)
        - 0.0004 * math.sin(3 * Mm_rad)
        + 0.0003 * E * math.sin(Ms_rad + 2 * F1_rad)
        + 0.0003 * math.sin(A1_rad)
        + 0.0002 * E * math.sin(Ms_rad - 2 * F1_rad)
        + 0.0002 * math.sin(2 * Mm_rad + Ms_rad)
        - 0.0002 * math.sin(Omega_rad)
    )

def corr_jde_lunar(Mm, Ms, F1, E, A1, Omega):
    Mm_rad = math.radians(Mm)
    Ms_rad = math.radians(Ms)
    A1_rad = math.radians(A1)
    F1_rad = math.radians(F1)
    Omega_rad = math.radians(Omega)

    return (
        -0.4065 * math.sin(Mm_rad)
        + 0.1727 * E * math.sin(Ms_rad)
        + 0.0161 * math.sin(2 * Mm_rad)
        - 0.0097 * math.sin(2 * F1_rad)
        + 0.0073 * E * math.sin(Mm_rad - Ms_rad)
        - 0.0050 * E * math.sin(Mm_rad + Ms_rad)
        - 0.0023 * math.sin(Mm_rad - 2 * F1_rad)
        + 0.0021 * E * math.sin(2 * Ms_rad)
        + 0.0012 * math.sin(Mm_rad + 2 * F1_rad)
        - 0.0006 * E * math.sin(2 * Mm_rad + Ms_rad)
        - 0.0004 * math.sin(3 * Mm_rad)
        + 0.0003 * E * math.sin(Ms_rad + 2 * F1_rad)
        + 0.0003 * math.sin(A1_rad)
        + 0.0002 * E * math.sin(Ms_rad - 2 * F1_rad)
        + 0.0002 * math.sin(2 * Mm_rad + Ms_rad)
        - 0.0002 * math.sin(Omega_rad)
    )

def maximum_eclipse_time(k, eclipse_type: EclipseType):
    JDE = lunar_jde(k)
    Mm = lunar_mean_anomaly(k)
    Ms = solar_mean_anomaly(k)
    F1 = calculate_f1(k)
    E = eccentricity_factor(k)
    A1 = calculate_a1(k)
    OMEGA = lunar_longitude_of_ascending_node(k)

    if eclipse_type == EclipseType.SOLAR:
        return JDE + corr_jde_solar(Mm, Ms, F1, E, A1, OMEGA)
    elif eclipse_type == EclipseType.LUNAR:
        return JDE + corr_jde_lunar(Mm, Ms, F1, E, A1, OMEGA)

def calculate_p(k):
    Mm = lunar_mean_anomaly(k)
    Ms = solar_mean_anomaly(k)
    F1 = calculate_f1(k)
    E = eccentricity_factor(k)

    return (
        + 0.2070 * E * math.sin(Ms)
        + 0.0024 * E * math.sin(2 * Ms)
        - 0.0392 * math.sin(Mm)
        + 0.0116 * math.sin(2 * Mm)
        - 0.0073 * E * math.sin(Mm + Ms)
        + 0.0067 * E * math.sin(Mm - Ms)
        + 0.0118 * math.sin(2 * F1)
    )

def calculate_solar_u(k):
    '''
    u is umbra radius for solar eclipse in EARTH RADIUS units

    solar eclipse: u = Moon's umbral radius on the fundamental plane
    Lunar eclipse: u = correction term used to compute Earth's shadow radii (σ, ρ)
    
    k: lunation number
    '''
    Mm = lunar_mean_anomaly(k)
    Ms = solar_mean_anomaly(k)
    E = eccentricity_factor(k)

    return (
        0.0059
        + 0.0046 * E * math.cos(Ms)
        - 0.0182 * math.cos(Mm)
        + 0.0004 * math.cos(2 * Mm)
        - 0.0005 * math.cos(Ms + Mm)
    )

def calculate_u_correction(k):
    Mm = lunar_mean_anomaly(k)
    Ms = solar_mean_anomaly(k)
    E = eccentricity_factor(k)

    return (
        0.0059
        + 0.0046 * E * math.cos(Ms)
        - 0.0182 * math.cos(Mm)
        + 0.0004 * math.cos(2 * Mm)
        - 0.0005 * math.cos(Ms + Mm)
    )

def calculate_q(k):
    Mm = lunar_mean_anomaly(k)
    Ms = solar_mean_anomaly(k)
    E = eccentricity_factor(k)

    return (
        + 5.2207
        - 0.0048 * E * math.cos(Ms)
        + 0.0020 * E * math.cos(2 * Ms)
        - 0.3299 * math.cos(Mm)
        - 0.0060 * E * math.cos(Mm + Ms)
        + 0.0041 * E * math.cos(Mm - Ms)
    )

def solar_eclipse_umbra_radius(k):
    return calculate_solar_u(k)

def solar_eclipse_penumbra_radius(k):
    return calculate_solar_u(k) + 0.546_1

def eclipse_type_omega(gamma):
    return 0.004_64 * math.sqrt(1 - gamma**2)

def calculate_w(k):
    F1 = calculate_f1(k)
    return abs(math.cos(F1))

def calculate_gamma(k):
    P = calculate_p(k)
    Q = calculate_q(k)
    F1 = calculate_f1(k)
    W = calculate_w(k)

    return (P * math.cos(F1) + Q * math.sin(F1)) * (1 - 0.004_8 * W)

def calculate_magnitude(k):
    u = calculate_solar_u(k)
    GAMMA = calculate_gamma(k)

    return (1.543_3 + u - abs(GAMMA)) / (0.546_1 + 2 * u)

# === LUNAR ECLIPSE ===
def lunar_eclipse_penumbra_radius(k):
    u = calculate_u_correction(k)
    rho = 1.284_8 + u
    return rho

def lunar_eclipse_umbra_radius(k):
    u = calculate_u_correction(k)
    sigma = 0.740_3 - u
    return sigma

def lunar_eclipse_penumbra_magnitude(k):
    GAMMA = calculate_gamma(k)
    u = calculate_u_correction(k)
    return (1.557_3 + u - abs(GAMMA)) / 0.545_0

def lunar_eclipse_umbra_magnitude(k):
    GAMMA = calculate_gamma(k)
    u = calculate_u_correction(k)
    return (1.012_8 + u - abs(GAMMA)) / 0.545_0

def lunar_semidurations(k):
    gamma = calculate_gamma(k)
    u = calculate_u_correction(k)
    Mm = math.radians(lunar_mean_anomaly(k))

    n = 0.5458 + 0.0400 * math.cos(Mm)

    S_penumbral = (1 / n) * safe_sqrt((1.5573 + u)**2 - gamma**2)
    S_partial   = (1 / n) * safe_sqrt((1.0128 + u)**2 - gamma**2)
    S_total     = (1 / n) * safe_sqrt((0.7403 - u)**2 - gamma**2)

    return S_total, S_partial, S_penumbral

def lunar_contacts(k):
    jde_corr = maximum_eclipse_time(k, EclipseType.LUNAR)

    S_total, S_partial, S_penumbral = lunar_semidurations(k)

    P1 = jde_corr - S_penumbral
    U1 = jde_corr - S_partial
    U2 = jde_corr - S_total
    MAX = jde_corr
    U3 = jde_corr + S_total
    U4 = jde_corr + S_partial
    P4 = jde_corr + S_penumbral

    return P1, U1, U2, MAX, U3, U4, P4
