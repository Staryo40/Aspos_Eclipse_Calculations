from intermediate_var import *
from typing import Optional

def calculate_simple_w(k):
    F = lunar_argument_of_latitude(k)
    return abs(math.cos(F))

def calculate_simple_gamma(k):
    P = calculate_p(k)
    Q = calculate_q(k)
    F = lunar_argument_of_latitude(k)
    W = calculate_simple_w(k)

    return (P * math.cos(F) + Q * math.sin(F)) * (1 - 0.004_8 * W)

def calculate_simple_magnitude(k: float) -> float:
    u = calculate_solar_u(k)
    gamma = calculate_simple_gamma(k)  

    return (1.5433 + u - abs(gamma)) / 0.546158

def simple_maximum_eclipse_time(k, eclipse_type: EclipseType):
    JDE = lunar_jde(k)
    Mm = lunar_mean_anomaly(k)
    Ms = solar_mean_anomaly(k)
    F = lunar_argument_of_latitude(k)
    E = eccentricity_factor(k)
    A1 = calculate_a1(k)
    OMEGA = lunar_longitude_of_ascending_node(k)

    if eclipse_type == EclipseType.SOLAR:
        return JDE + corr_jde_solar(Mm, Ms, F, E, A1, OMEGA)
    elif eclipse_type == EclipseType.LUNAR:
        return JDE + corr_jde_lunar(Mm, Ms, F, E, A1, OMEGA)