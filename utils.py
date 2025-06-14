def yes_no_prompt(prompt: str) -> bool:
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please answer yes or no.")

def plate_calculator(target_weight, unit="lb", bar_weight=None):
    """
    Returns a list of plates per side needed to reach the target_weight (including bar).
    If bar_weight is None, defaults to 45 lb or 20 kg.
    Returns a dict: {plate_size: count_per_side}
    """
    if unit == "lb":
        plate_sizes = [45, 35, 25, 10, 5, 2.5]
        bar_weight = bar_weight or 45
    else:
        plate_sizes = [25, 20, 15, 10, 5, 2.5, 1.25]
        bar_weight = bar_weight or 20

    if target_weight < bar_weight:
        return {}

    per_side = (target_weight - bar_weight) / 2
    result = {}
    for plate in plate_sizes:
        count = int(per_side // plate)
        if count > 0:
            result[plate] = count
            per_side -= plate * count
    # If per_side is not zero, it's not possible to match exactly
    if round(per_side, 2) > 0:
        result['unmatched'] = round(per_side, 2)
    return result

# Example usage:
# print(plate_calculator(225, "lb"))  # {45: 2}
# print(plate_calculator(100, "kg"))  # {20: 1, 15: 1, 2.5: 1}
