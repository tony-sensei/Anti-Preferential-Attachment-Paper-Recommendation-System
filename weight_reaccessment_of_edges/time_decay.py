import numpy as np
import matplotlib.pyplot as plt

"""
This file works on comparing three different kinds of time decay functions.

@Author: Kristy He
"""


def compare_sigmoid_linear_and_exponential(start_year, end_year, sigmoid_T0, lambda_value, linear_reference_year, slope):

    """
    Compares sigmoid, linear, and exponential decay functions over a range of years.

    Parameters:
    - start_year: The first year in the range.
    - end_year: The last year in the range.
    - sigmoid_T0: The center year where sigmoid decay is centered.
    - lambda_value: The steepness of the sigmoid function.
    - linear_reference_year: The year where linear decay starts at weight 1.
    - slope: The rate of linear decay.
    """

    years = np.arange(start_year, end_year + 1)
    sigmoid_weights = 1 / (1 + np.exp(-lambda_value * (years - sigmoid_T0)))
    print("The average weight is " + str(np.mean(sigmoid_weights)))
    linear_weights = np.maximum(0, 1 - slope * (linear_reference_year - years))
    exponential_weights = np.exp(-lambda_value * np.abs(years - linear_reference_year))

    plt.figure(figsize=(10, 6))
    plt.plot(years, sigmoid_weights, marker='o', label=f"Sigmoid (T0={sigmoid_T0}, lambda={lambda_value})")
    plt.plot(years, linear_weights, marker='x', label=f"Linear (Reference Year={linear_reference_year}, slope={slope})")
    plt.plot(years, exponential_weights, marker='s', label=f"Exponential (Reference Year={linear_reference_year}, lambda={lambda_value})")
    plt.axvline(sigmoid_T0, color='blue', linestyle='--', label=f"Sigmoid T0 = {sigmoid_T0}")
    plt.axvline(linear_reference_year, color='green', linestyle='--', label=f"Linear/Exponential Reference Year = {linear_reference_year}")
    plt.title("Comparison of Sigmoid, Linear, and Exponential Time Decay Weights")
    plt.xlabel("Year")
    plt.ylabel("Weight")
    plt.grid(True)
    plt.legend()
    plt.show()


compare_sigmoid_linear_and_exponential(start_year=1965, end_year=2015, sigmoid_T0=2002, lambda_value=0.1, linear_reference_year=2015, slope=0.02)
