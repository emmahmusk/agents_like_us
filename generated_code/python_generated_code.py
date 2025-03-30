from typing import List, Tuple, Dict

def calculate_daily_contributions(contributions: List[Tuple[str, float]]) -> Dict[str, float]:
    """Calculates daily contribution sums from a list of contributions.

    Args:
        contributions: A list of tuples, where each tuple contains (date, contribution_amount).

    Returns:
        A dictionary where keys are dates and values are the total contributions for that date.  Returns an empty dictionary if input is invalid.
    """
    if not isinstance(contributions, list):
        return {}
    if not all(isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], (int, float)) for item in contributions):
        return {}

    daily_sums: Dict[str, float] = {}
    for date, amount in contributions:
        daily_sums[date] = daily_sums.get(date, 0.0) + amount
    return daily_sums