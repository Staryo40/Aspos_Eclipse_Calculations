import datetime
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from collections import Counter
from models import *
import os, math

def colorize(text, color):
    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m",
    }
    return f"{COLORS[color]}{text}{COLORS['reset']}"

def ensure_output_dir_solar(base, start_date: str, n_years: int) -> str:
    start_year = int(start_date[:4])
    folder = f"solar_eclipse_{base}_{start_year}_{n_years}"
    os.makedirs(folder, exist_ok=True)
    return folder

def safe_sqrt(x):
    return math.sqrt(x) if x > 0 else 0.0

# TIME UTILITY
def jde_to_datetime_str(JD: float) -> str:
    """
    Convert Julian Day (JD or JDE) to YYYY-MM-DD HH:MM:SS UT.
    """

    JD += 0.5
    Z = int(JD)
    F = JD - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day_decimal = B - D - int(30.6001 * E) + F
    day = int(day_decimal)
    frac = day_decimal - day

    # Month & Year
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715

    # Time
    total_seconds = frac * 86400
    hour = int(total_seconds // 3600)
    minute = int((total_seconds % 3600) // 60)
    second = int(round(total_seconds % 60))

    # Fix rounding overflow
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0
        day += 1

    # Use datetime to safely normalize days and months
    dt = datetime.datetime(year, month, day, hour, minute, second)

    return dt.strftime("%Y-%m-%d %H:%M:%S UT")


def fraction_of_year(date_str: str) -> float:
    dt = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d")
    start = datetime.datetime(dt.year, 1, 1)
    end = datetime.datetime(dt.year + 1, 1, 1)
    return (dt - start).total_seconds() / (end - start).total_seconds()

def days_to_hms(days: float) -> str:
    total_seconds = int(round(days * 86400))
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# PRINT UTILITY
def eclipse_color(e_type: str) -> str:
    if "Total" in e_type:
        return "red"
    if "Annular" in e_type:
        return "yellow"
    if "Hybrid" in e_type:
        return "magenta"
    if "Partial" in e_type:
        return "cyan"
    return "green"

def print_export_summary(records: list[EclipseRecord]):
    if not records:
        print("(No solar eclipses found)")
        return

    print("\n=== Solar Eclipses Summary ===")
    for r in records:
        print(f"{r.datetime} | {colorize(r.eclipse_type, eclipse_color(r.eclipse_type))}")


from matplotlib.lines import Line2D

def plot_eclipse_timeline(
    records: list[EclipseRecord],
    title: str,
    filename="eclipses_timeline.png"
):
    if not records:
        print("No data to plot (timeline).")
        return

    years = [int(r.datetime[:4]) for r in records]
    y_frac = [fraction_of_year(r.datetime) for r in records]
    types = [r.eclipse_type for r in records]

    # === UNIVERSAL COLOR MAP ===
    color_map = {
        # Solar
        "Total Solar Eclipse": "red",
        "Total Solar Eclipse (Non-central)": "darkred",
        "Annular Solar Eclipse": "orange",
        "Hybrid Solar Eclipse (Annular–Total)": "magenta",
        "Partial Solar Eclipse": "blue",

        # Lunar
        "Total Lunar Eclipse": "red",
        "Partial Lunar Eclipse": "orange",
        "Penumbral Lunar Eclipse": "blue",
    }

    colors = [color_map.get(t, "black") for t in types]

    plt.figure(figsize=(12, 5))
    plt.scatter(years, y_frac, c=colors, s=80)

    plt.yticks(
        [0, 0.25, 0.5, 0.75, 1.0],
        ["Jan", "Apr", "Jul", "Oct", "Dec"]
    )

    plt.xlabel("Year")
    plt.ylabel("Time of Year")
    plt.title(title)
    plt.grid(True, axis="y", linestyle="--", alpha=0.5)

    # === LEGEND (only types that appear) ===
    used_types = sorted(set(types))
    legend_elements = [
        Line2D(
            [0], [0],
            marker="o",
            color="w",
            label=t,
            markerfacecolor=color_map.get(t, "black"),
            markersize=8
        )
        for t in used_types
    ]

    plt.legend(
        handles=legend_elements,
        title="Eclipse Type",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0.0
    )

    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()


def plot_eclipse_type_distribution(records: list[EclipseRecord], title: str, filename="eclipse_types.png"):
    if not records:
        print("No data to plot (type distribution).")
        return

    counter = Counter(r.eclipse_type for r in records)

    plt.figure(figsize=(8, 5))
    plt.bar(counter.keys(), counter.values())
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Count")
    plt.title(title)

    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()