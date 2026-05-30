from math import ceil
from fractions import Fraction

def calculate_full_usage_note(
    route: str, times: int, dose: str, usage_unit: str, usage_note: str
) -> str:
    return "{} ngày {} lần, lần {} {} ({})".format(
        route, times, dose, usage_unit, usage_note
    )


def calculate_medicine_quantity(
    times: int, dose: str, usage_unit: str, selling_unit: str, days: int
) -> int:
    if usage_unit != selling_unit:
        return 1
    else:
        if "/" in dose:
            numer, denom = [int(i) for i in dose.strip().split("/", 1)]
            return ceil(times * Fraction(numer, denom) * days)
        else:
            return ceil(times * float(dose.strip()) * days)
