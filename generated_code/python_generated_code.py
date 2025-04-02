from decimal import Decimal
def calculate_roi(initial_investment: Decimal, final_value: Decimal) -> Decimal:
    if initial_investment <= 0:
        return Decimal('NaN')
    return (final_value - initial_investment) / initial_investment