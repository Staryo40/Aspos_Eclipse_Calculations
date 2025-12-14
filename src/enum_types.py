from enum import Enum

class MoonPhase(Enum):
    NEW_MOON = "new moon"
    FIRST_QUARTER = "first quarter"
    FULL_MOON = "full moon"
    LAST_QUARTER = "last quarter"

    def iterate_phase(self):
        order = [
            MoonPhase.NEW_MOON,
            MoonPhase.FIRST_QUARTER,
            MoonPhase.FULL_MOON,
            MoonPhase.LAST_QUARTER,
        ]
        idx = order.index(self)
        return order[(idx + 1) % len(order)]
    
class EclipseType(Enum):
    SOLAR = "solar"
    LUNAR = "lunar"