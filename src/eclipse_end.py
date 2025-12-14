# === TUGAS MENGHITUNG GERHANA BULAN DAN MATAHARI ===
# Tentukan gerhana bulan pertama dan gerhana matahari pertama semenjak tahun 2030+i, dimana i = 0, 1, 2, 3, …

import math
from typing import Tuple
from enum_types import *
from utils import *
from intermediate_var import *
from simple_intermediate_var import *
from models import *

def date_to_year_fraction(date_string):
    dt = datetime.datetime.strptime(date_string, "%Y-%m-%d")

    year = dt.year
    month = dt.month
    day = dt.day

    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    days_in_year = 366 if is_leap else 365
    X = 1 if is_leap else 2

    DoY = int(275 * month / 9) - X * int((month + 9) / 12) + day - 30
    year_fraction = year + DoY / days_in_year

    return year_fraction

# =========================================================== SOLAR ECLIPSE 
def determine_solar_eclipse_type(k) -> Optional[str]:
    GAMMA = calculate_gamma(k)
    u = calculate_solar_u(k)
    g = abs(GAMMA)

    if g < 0.997_2:
        if u < 0:
            return "Total Solar Eclipse"
        elif u > 0.004_7:
            return "Annular Solar Eclipse"
        else:
            if u < eclipse_type_omega(GAMMA):
                return "Hybrid Solar Eclipse (Annular–Total)"
            else:
                return "Annular Solar Eclipse"
    elif 0.997_2 < g < 1.543_3 + u:
        if 0.997_2 < g < 0.997_2 + abs(u):
            return "Total Solar Eclipse (Non-central)"  
        else:
            return "Partial Solar Eclipse"
    
    return None

def determine_simple_solar_eclipse(k: float, display=True) -> bool:
    F = lunar_argument_of_latitude(k)
    m1 = abs(math.sin(F))           
    m2 = calculate_simple_magnitude(k)    

    if display:
        print(f"|sin(F)| = {m1:.6f}, MaxMag = {m2:.6f}")

    occ = True
    e_type = None
    if m1 >= 0.36:
        if display:
            print("Eclipse did not occur (|sin(F)| >= 0.36)")
        occ = False

    if m2 < 0:
        if display:
            print("Eclipse did not occur (Negative MaxMag)")
        occ = False

    if m1 < 0.36 and m2 > 0:
        e_type = determine_solar_eclipse_type(k)

    return occ, e_type


def determine_solar_eclipse(k, display=True):
    F1 = calculate_f1(k)
    m1 = abs(math.sin(F1))
    m2 = calculate_magnitude(k)

    if display:
        print(f"|sin(F)| = {m1:.6f}, MaxMag = {m2:.6f}")

    occ = True
    e_type = None
    if m1 >= 0.36:
        if display:
            print("Eclipse did not occur (|sin(F)| >= 0.36)")
        occ = False
    
    if m2 < 0:
        if display:
            print("Eclipse did not occur (Negative MaxMag)")
        occ = False
    
    if m1 < 0.36 and m2 > 0:
        e_type = determine_solar_eclipse_type(k)
    
    return occ, e_type

def determine_first_solar_eclipse(k, simple=True, display=True):
    i = 1
    current_k = k   
    occ = False

    while not occ: 
        if (display):
            print(f"Iteration {i} with k = {current_k}")
        occ, e_type = determine_simple_solar_eclipse(current_k, display) if simple else determine_solar_eclipse(current_k, display) 
        if (occ):
            jde = simple_maximum_eclipse_time(current_k, EclipseType.SOLAR) if simple else maximum_eclipse_time(current_k, EclipseType.SOLAR)
            print(colorize(e_type, eclipse_color(e_type)) + " occured")
            print(f"Occured with k = {current_k}")
            print(f"JDE: {jde:.3f}")
            print(f"Max Eclipse: {jde_to_datetime_str(jde)}")
        
        print("=" * 30)

        i += 1
        current_k += 1

# =========================================================== SOLAR REPORT FUNCTIONS
def find_solar_eclipse_at_k(k, simple=True) -> Optional[EclipseRecord]:
    if simple:
        occ, e_type = determine_simple_solar_eclipse(k, display=False)
    else:
        occ, e_type = determine_solar_eclipse(k, display=False)

    if not occ or e_type is None:
        return None

    jde = simple_maximum_eclipse_time(k, EclipseType.SOLAR) if simple else maximum_eclipse_time(k, EclipseType.SOLAR)

    return EclipseRecord(
        jde=jde,
        datetime=jde_to_datetime_str(jde),
        k=k,
        eclipse_type=e_type
    )


def export_solar_eclipses(start_date: str, n_years: int, simple=True):
    start_year = int(start_date[:4])
    end_year = start_year + n_years - 1

    year_frac = date_to_year_fraction(start_date)
    k = base_lunation_number(year_frac)

    results: list[EclipseRecord] = []

    while True:
        rec = find_solar_eclipse_at_k(k, simple)
        if rec:
            year = int(rec.datetime[:4])
            if year > end_year:
                break
            if start_year <= year <= end_year:
                results.append(rec)
        k += 1

    return results

def find_first_solar_eclipse_in_year(year: int, simple=True) -> Optional[EclipseRecord]:
    start_date = f"{year}-01-01"
    year_frac = date_to_year_fraction(start_date)
    k = base_lunation_number(year_frac)

    while True:
        rec = find_solar_eclipse_at_k(k, simple)
        if rec:
            rec_year = int(rec.datetime[:4])

            if rec_year == year:
                return rec

            if rec_year > year:
                return None

        k += 1

def export_first_solar_eclipse_per_year(start_date: str, n_years: int, simple=True):
    start_year = int(start_date[:4])
    end_year = start_year + n_years - 1

    results: list[EclipseRecord] = []

    for year in range(start_year, end_year + 1):
        rec = find_first_solar_eclipse_in_year(year, simple)
        if rec:
            results.append(rec)

    return results

# =========================================================== LUNAR ECLIPSE
def determine_lunar_eclipse_type(k) -> Optional[str]:
    mag_p = lunar_eclipse_penumbra_magnitude(k)
    mag_u = lunar_eclipse_umbra_magnitude(k)

    if mag_u > 1:
        return "Total Lunar Eclipse"
    elif mag_u > 0:
        return "Partial Lunar Eclipse"
    elif mag_p > 0:
        return "Penumbral Lunar Eclipse"

    return None

def determine_lunar_eclipse(k, display=True) -> Tuple[bool, Optional[str]]:
    mag_p = lunar_eclipse_penumbra_magnitude(k)
    mag_u = lunar_eclipse_umbra_magnitude(k)

    if display:
        print(f"Penumbral Magnitude = {mag_p:.6f}, Umbral magnitude = {mag_u:.6f}")

    occ = True
    e_type = None
    if mag_p < 0:
        if display:
            print("Eclipse did not occur Penumbral Magnitude < 0)")
        occ = False
    else:
        e_type = determine_lunar_eclipse_type(k)
    
    return occ, e_type

def determine_first_lunar_eclipse(k, simple=True, display=True, filename="lunar_eclipse_report.png"):
    i = 1
    current_k = k
    occ = False

    while not occ:
        if display:
            print(f"Iteration {i} with k = {current_k}")

        occ, e_type = determine_lunar_eclipse(current_k)
        if occ:
            jde = simple_maximum_eclipse_time(current_k, EclipseType.LUNAR) if simple else maximum_eclipse_time(current_k, EclipseType.LUNAR)
            print(f"{colorize(e_type, eclipse_color(e_type))} occured")
            print(f"Occured with k = {current_k}")
            print(f"Max Eclipse: {jde_to_datetime_str(jde)}")

            if display:
                lunar_eclipse_report_png(current_k, filename=filename)

        if display:
            print("=" * 30)

        i += 1
        current_k += 1

# =========================================================== LUNAR REPORT FUNCTIONS
def find_lunar_eclipse_at_k(k, simple=True) -> Optional[EclipseRecord]:
    occ, e_type = determine_lunar_eclipse(k, False)

    if not occ or e_type is None:
        return None

    jde = simple_maximum_eclipse_time(k, EclipseType.LUNAR) if simple else maximum_eclipse_time(k, EclipseType.LUNAR)

    return EclipseRecord(
        jde=jde,
        datetime=jde_to_datetime_str(jde),
        k=k,
        eclipse_type=e_type
    )

def export_lunar_eclipses(start_date: str, n_years: int, simple=True):
    start_year = int(start_date[:4])
    end_year = start_year + n_years - 1

    year_frac = date_to_year_fraction(start_date)
    k = lunation_number(year_frac, MoonPhase.FULL_MOON)

    results: list[EclipseRecord] = []

    while True:
        rec = find_lunar_eclipse_at_k(k, simple)
        if rec:
            year = int(rec.datetime[:4])
            if year > end_year:
                break
            if start_year <= year <= end_year:
                results.append(rec)
        k += 1

    return results

def find_first_lunar_eclipse_in_year(year: int, simple=True) -> Optional[EclipseRecord]:    
    start_date = f"{year}-01-01"
    year_frac = date_to_year_fraction(start_date)
    k = lunation_number(year_frac, MoonPhase.FULL_MOON)

    while True:
        rec = find_lunar_eclipse_at_k(k, simple)
        if rec:
            rec_year = int(rec.datetime[:4])

            if rec_year == year:
                return rec
            if rec_year > year:
                return None

        k += 1

def export_first_lunar_eclipse_per_year(start_date: str, n_years: int):
    start_year = int(start_date[:4])
    end_year = start_year + n_years - 1

    results: list[EclipseRecord] = []

    for year in range(start_year, end_year + 1):
        rec = find_first_lunar_eclipse_in_year(year)
        if rec:
            results.append(rec)

    return results

def lunar_eclipse_report_png(k, filename="lunar_eclipse_report.png"):
    gamma = calculate_gamma(k)
    rho = lunar_eclipse_penumbra_radius(k)
    sigma = lunar_eclipse_umbra_radius(k)

    mag_p = lunar_eclipse_penumbra_magnitude(k)
    mag_u = lunar_eclipse_umbra_magnitude(k)

    P1, U1, U2, MAX, U3, U4, P4 = lunar_contacts(k)
    S_total, S_partial, S_penumbral = lunar_semidurations(k)

    semi_penumbral = S_penumbral * 1440  
    semi_partial   = S_partial * 1440
    semi_total     = S_total * 1440

    dur_penumbral = days_to_hms(P4 - P1)
    dur_partial   = days_to_hms(U4 - U1)
    dur_total     = days_to_hms(U3 - U2)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")

    text = f"""
        LUNAR ECLIPSE REPORT

        Full moon (k)      : {k}

        Maximum Eclipse    : {jde_to_datetime_str(MAX)}
        Gamma              : {gamma:.4f}

        Radius Penumbra    : {rho:.4f}°
        Radius Umbra       : {sigma:.4f}°
        Magnitude Penumbra : {mag_p:.4f}
        Magnitude Umbra    : {mag_u:.4f}

        Semiduration Phase:
        Penumbra           : {semi_penumbral:.3f} m
        Partial            : {semi_partial:.3f} m
        Total              : {semi_total:.3f} m

        Eclipse Duration
        Penumbral          : {dur_penumbral}
        Partial            : {dur_partial}
        Total              : {dur_total}

        Contacts (UT):
        P1 : {jde_to_datetime_str(P1)}
        U1 : {jde_to_datetime_str(U1)}
        U2 : {jde_to_datetime_str(U2)}
        MAX: {jde_to_datetime_str(MAX)}
        U3 : {jde_to_datetime_str(U3)}
        U4 : {jde_to_datetime_str(U4)}
        P4 : {jde_to_datetime_str(P4)}
    """

    ax.text(0.02, 0.98, text, va="top", ha="left", family="monospace")
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()

