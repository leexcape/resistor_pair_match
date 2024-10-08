import numpy
import argparse
from collections import defaultdict
import numpy as np


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


def main():
    parser = argparse.ArgumentParser(description="Calculate Resistor Pair with Given Ratio")
    parser.add_argument('series', choices=['E6', 'E12', 'E24', 'E48', 'E96'], help='The E series of the resistor value')
    parser.add_argument('-r', '--ratio', type=float, help='The desired voltage ratio')

    args = parser.parse_args()

    # Get resistor values
    e_series_values = np.array(get_resistor_values()[args.series])
    resistor_ratio = 0
    voltage_ratio = args.ratio / (1 - args.ratio)
    counter_voltage_ratio_n = 0
    while voltage_ratio <= 0.1 or voltage_ratio >= 10:
        if voltage_ratio <= 0.1:
            voltage_ratio = voltage_ratio * 10
            counter_voltage_ratio_n -= 1
        else:
            voltage_ratio = voltage_ratio / 10
            counter_voltage_ratio_n += 1
    resistor_ratio_list = []
    resistor_pair_dict = defaultdict(lambda: defaultdict())
    pair_index = 0
    for i in range(e_series_values.shape[0]):
        for j in range(e_series_values.shape[0]):
            pair_index += 1
            resistor_ratio = e_series_values[i] / e_series_values[j]
            resistor_ratio_list.append(resistor_ratio)
            resistor_pair_dict[f'pair {pair_index}']['resistor 1'] = e_series_values[i]
            resistor_pair_dict[f'pair {pair_index}']['resistor 2'] = e_series_values[j]
            resistor_pair_dict[f'pair {pair_index}']['resistor ratio'] = resistor_ratio

    resistor_ratio_array = np.array(resistor_ratio_list)
    resistor_ratio_diff = np.abs(resistor_ratio_array - voltage_ratio)
    resistor_ratio_index_sort = np.argsort(resistor_ratio_diff)[:10]
    resistor_pair_dict_keys = list(resistor_pair_dict.keys())
    for i in range(10):
        resistor_1 = resistor_pair_dict[resistor_pair_dict_keys[resistor_ratio_index_sort[i]]]['resistor 1'] * pow(10, counter_voltage_ratio_n)
        resistor_2 = resistor_pair_dict[resistor_pair_dict_keys[resistor_ratio_index_sort[i]]]['resistor 2']
        print('No. %i Match resistor pair: %f Ohms and %f Ohms' % (i+1, resistor_1, resistor_2))

if __name__ == "__main__":
    main()

