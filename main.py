import argparse


def get_resistor_values():
    e_series_value = {
        'E6': [1.0, 1.5, 2.2, 3.3, 4.7, 6.8],
        'E12': [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
        'E24': [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1],
        'E48': [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54,
                1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49,
                2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02,
                4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49,
                6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53],
        'E96': [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24,
                1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58,
                1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00,
                2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55,
                2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24,
                3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
                4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23,
                5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65,
                6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
                8.66, 8.87, 9.09, 9.31, 9.53, 9.76]
    }
    return e_series_value


def get_all_resistor_values(base_values, min_val=None, max_val=None):
    """Generate all resistor values by multiplying base values with powers of 10."""
    # Default range: 1 ohm to 10M ohm
    if min_val is None:
        min_val = 1
    if max_val is None:
        max_val = 10e6

    resistors = []
    for exp in range(-1, 8):  # 0.1 to 10M range
        multiplier = 10 ** exp
        for base in base_values:
            value = base * multiplier
            if min_val <= value <= max_val:
                resistors.append(value)
    return sorted(set(resistors))


def format_resistor_value(value):
    """Format resistor value with appropriate unit."""
    if value >= 1e6:
        return f"{value/1e6:.3g}M"
    elif value >= 1e3:
        return f"{value/1e3:.3g}k"
    else:
        return f"{value:.3g}"


def find_best_pairs_by_ratio(resistor_values, target_ratio, top_n=5, min_val=None, max_val=None):
    """Find best resistor pairs for a given ratio R1/R2."""
    pairs = []

    for r1 in resistor_values:
        for r2 in resistor_values:
            # Apply min/max constraints if specified
            if min_val is not None and (r1 < min_val or r2 < min_val):
                continue
            if max_val is not None and (r1 > max_val or r2 > max_val):
                continue

            actual_ratio = r1 / r2
            error = abs(actual_ratio - target_ratio) / target_ratio
            pairs.append({
                'r1': r1,
                'r2': r2,
                'ratio': actual_ratio,
                'error': error
            })

    # Sort by error and return top N
    pairs.sort(key=lambda x: x['error'])
    return pairs[:top_n]


def find_best_pairs_by_voltage_ratio(resistor_values, voltage_ratio, top_n=10, min_val=None, max_val=None):
    """
    Find best resistor pairs for voltage divider.
    Voltage ratio = Vout/Vin = R2/(R1+R2)
    """
    pairs = []

    for r1 in resistor_values:
        for r2 in resistor_values:
            # Apply min/max constraints if specified
            if min_val is not None and (r1 < min_val or r2 < min_val):
                continue
            if max_val is not None and (r1 > max_val or r2 > max_val):
                continue

            actual_voltage_ratio = r2 / (r1 + r2)
            error = abs(actual_voltage_ratio - voltage_ratio) / voltage_ratio
            pairs.append({
                'r1': r1,
                'r2': r2,
                'voltage_ratio': actual_voltage_ratio,
                'error': error
            })

    # Sort by error and return top N
    pairs.sort(key=lambda x: x['error'])
    return pairs[:top_n]


def main():
    parser = argparse.ArgumentParser(
        description="Calculate Resistor Pair for Voltage Divider or Ratio Matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find resistor pairs for 0.5 voltage ratio (Vout/Vin = 0.5)
  python main.py E24 -v 0.5

  # Find resistor pairs for resistor ratio R1/R2 = 2.5
  python main.py E24 -r 2.5

  # With resistor value constraints (1k to 100k)
  python main.py E24 -r 2.5 --min 1000 --max 100000

Voltage Divider Circuit:
  Vin ---[R1]---+---[R2]--- GND
                |
               Vout

  Vout/Vin = R2/(R1+R2)
        """
    )
    parser.add_argument('series', choices=['E6', 'E12', 'E24', 'E48', 'E96'],
                        help='The E series of the resistor value')

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-v', '--voltage-ratio', type=float,
                            help='Voltage divider ratio Vout/Vin (must be between 0 and 1)')
    mode_group.add_argument('-r', '--ratio', type=float,
                            help='Direct resistor ratio R1/R2')

    parser.add_argument('--min', type=float, default=None,
                        help='Minimum resistor value in ohms (e.g., 1000 for 1k)')
    parser.add_argument('--max', type=float, default=None,
                        help='Maximum resistor value in ohms (e.g., 100000 for 100k)')
    parser.add_argument('-n', '--top', type=int, default=5,
                        help='Number of top matches to display (default: 5)')

    args = parser.parse_args()

    # Validate voltage ratio
    if args.voltage_ratio is not None:
        if args.voltage_ratio <= 0 or args.voltage_ratio >= 1:
            parser.error("Voltage ratio must be between 0 and 1 (exclusive)")

    # Validate ratio
    if args.ratio is not None:
        if args.ratio <= 0:
            parser.error("Resistor ratio must be greater than 0")

    # Validate min/max
    if args.min is not None and args.max is not None:
        if args.min >= args.max:
            parser.error("Minimum value must be less than maximum value")

    # Get base E-series values
    base_values = get_resistor_values()[args.series]

    # Generate all resistor values within range
    resistor_values = get_all_resistor_values(base_values, args.min, args.max)

    if len(resistor_values) == 0:
        print("Error: No resistor values available in the specified range.")
        return

    if args.voltage_ratio is not None:
        # Voltage divider mode
        print(f"\nVoltage Divider Mode: Vout/Vin = {args.voltage_ratio}")
        print(f"E-Series: {args.series}")
        if args.min or args.max:
            min_str = format_resistor_value(args.min) if args.min else "none"
            max_str = format_resistor_value(args.max) if args.max else "none"
            print(f"Resistor range: {min_str} - {max_str}")
        print("-" * 60)

        pairs = find_best_pairs_by_voltage_ratio(
            resistor_values, args.voltage_ratio, args.top, args.min, args.max
        )

        if not pairs:
            print("No matching pairs found in the specified range.")
            return

        print(f"{'No.':<4} {'R1':<12} {'R2':<12} {'Vout/Vin':<12} {'Error':<10}")
        print("-" * 60)
        for i, pair in enumerate(pairs, 1):
            r1_str = format_resistor_value(pair['r1'])
            r2_str = format_resistor_value(pair['r2'])
            error_str = f"{pair['error']*100:.4f}%"
            print(f"{i:<4} {r1_str:<12} {r2_str:<12} {pair['voltage_ratio']:<12.6f} {error_str:<10}")

    else:
        # Ratio mode
        print(f"\nResistor Ratio Mode: R1/R2 = {args.ratio}")
        print(f"E-Series: {args.series}")
        if args.min or args.max:
            min_str = format_resistor_value(args.min) if args.min else "none"
            max_str = format_resistor_value(args.max) if args.max else "none"
            print(f"Resistor range: {min_str} - {max_str}")
        print("-" * 60)

        pairs = find_best_pairs_by_ratio(
            resistor_values, args.ratio, args.top, args.min, args.max
        )

        if not pairs:
            print("No matching pairs found in the specified range.")
            return

        print(f"{'No.':<4} {'R1':<12} {'R2':<12} {'R1/R2':<12} {'Error':<10}")
        print("-" * 60)
        for i, pair in enumerate(pairs, 1):
            r1_str = format_resistor_value(pair['r1'])
            r2_str = format_resistor_value(pair['r2'])
            error_str = f"{pair['error']*100:.4f}%"
            print(f"{i:<4} {r1_str:<12} {r2_str:<12} {pair['ratio']:<12.6f} {error_str:<10}")


if __name__ == "__main__":
    main()
