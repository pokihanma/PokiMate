from decimal import Decimal, ROUND_HALF_UP


def round2(x: Decimal | float) -> Decimal:
    if isinstance(x, float):
        x = Decimal(str(x))
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
