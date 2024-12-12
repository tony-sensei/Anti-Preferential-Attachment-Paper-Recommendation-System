import re

"""
Function to calculate the average similarity difference.

This function computes the difference between the maximum and minimum cosine similarities.

The main function compute the different between baseline model and improved model.

@Author: Kristy He
"""


def calculate_similarity_difference(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regular expression pattern to match cosine similarity values (formatted as float with 4 decimal places)
    similarity_pattern = re.compile(r'(\d+\.\d{4})')
    similarity_differences = []
    for line in lines:
        similarities = similarity_pattern.findall(line)
        similarities = [float(sim) for sim in similarities]

        min_similarity = min(similarities)
        max_similarity = max(similarities)

        similarity_difference = max_similarity - min_similarity
        similarity_differences.append(similarity_difference)

    average_difference = sum(similarity_differences) / len(similarity_differences) if similarity_differences else 0
    return average_difference, max(similarity_differences), min(similarity_differences)


if __name__ == "__main__":
    # File paths for the baseline and modified models
    # Please replace your own path of recommendation results file before running!
    file_path1 = 'baseline_top10_with_similarity.txt'
    file_path2 = 'weighted_top10_p=0.5_q=0.25.txt'

    # Calculate the average similarity difference for the baseline model
    average_diff1, max_diff1, min_diff1 = calculate_similarity_difference(file_path1)
    print(f"Baseline Model: Minimum Similarity Difference:{min_diff1}")
    print(f"Baseline Model: Average Similarity Difference: {average_diff1}")
    print(f"Baseline Model: Maximum Similarity Difference:{max_diff1}")
    print()

    # Calculate the average similarity difference for our modified model
    average_diff2, max_diff2, min_diff2 = calculate_similarity_difference(file_path2)
    print(f"Our Model: Minimum Similarity Difference: {min_diff2}")
    print(f"Our Model: Average Similarity Difference: {average_diff2}")
    print(f"Our Model: Maximum Similarity Difference: {max_diff2}")

