import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_citation_data(file_path):
    """
    Load citation data from a file.

    Parameters:
    - file_path (str or Path): Path to the citation data file.

    Returns:
    - df (pd.DataFrame): DataFrame containing 'Paper_ID' and 'Citations'.
    """
    file_path = Path(file_path)
    df = pd.read_csv(file_path, sep='\t', header=None, names=['Paper_ID', 'Citations'])
    return df

def compute_degree_distribution(df):
    """
    Compute the degree distribution from the citation data.

    Parameters:
    - df (pd.DataFrame): DataFrame containing citation data.

    Returns:
    - unique_degrees (list): Sorted list of unique degrees.
    - probabilities (np.array): Normalized probabilities of degrees.
    - degrees (list): List of all degrees.
    """
    degrees = df['Citations'].tolist()
    unique_degrees = sorted(set(degrees))
    degree_counts = np.array([degrees.count(d) for d in unique_degrees])
    probabilities = degree_counts / len(degrees)
    return unique_degrees, probabilities, degrees

def plot_degree_distribution(unique_degrees, probabilities, degrees, save_dir, image_name_prefix, dot_size=10, dpi=300):
    """
    Plot degree distributions in various scales and save the images.

    Parameters:
    - unique_degrees (list): Sorted list of unique degrees.
    - probabilities (np.array): Normalized probabilities of degrees.
    - degrees (list): List of all degrees.
    - save_dir (str or Path): Directory to save the plots.
    - image_name_prefix (str): Prefix for the image file names.
    - dot_size (int): Size of the dots in the scatter plot (default: 10).
    - dpi (int): Resolution (dots per inch) for saved images (default: 300).
    """
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    # Linear scale
    plt.figure()
    plt.scatter(unique_degrees, probabilities, s=dot_size, marker='o')  
    plt.title(f"{image_name_prefix} - Linear Scale")
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.savefig(save_dir / f"{image_name_prefix}_Linear_Scale.png", bbox_inches='tight', dpi=dpi)
    plt.close()

    # Log-Log scale with Linear Binning
    plt.figure()
    plt.scatter(unique_degrees, probabilities, s=dot_size, marker='o')  
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"{image_name_prefix} - Log-Log Scale with Linear Binning")
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.savefig(save_dir / f"{image_name_prefix}_LogLog_Linear_Binning.png", bbox_inches='tight', dpi=dpi)
    plt.close()

    # Log-Log scale with Logarithmic Binning
    bins = np.logspace(np.log10(max(1, min(degrees))), np.log10(max(degrees)), 12)
    binned_probabilities = []
    bin_centers = []

    degrees = np.array(degrees)
    for i in range(len(bins) - 1):
        bin_min = bins[i]
        bin_max = bins[i+1]
        bin_center = (bin_min + bin_max) / 2
        bin_centers.append(bin_center)
        
        count_in_bin = ((degrees >= bin_min) & (degrees < bin_max)).sum()
        binned_probabilities.append(count_in_bin / len(degrees))

    plt.figure()
    plt.scatter(bin_centers, binned_probabilities, s=dot_size, marker='o')  
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"{image_name_prefix} - Log-Log Scale with Logarithmic Binning")
    plt.xlabel("k")
    plt.ylabel("P(k)")
    plt.savefig(save_dir / f"{image_name_prefix}_LogLog_Logarithmic_Binning.png", bbox_inches='tight', dpi=dpi)
    plt.close()

    # Corrected CCDF
    unique_degrees, ccdf = compute_ccdf(degrees)

    plt.figure()
    plt.scatter(unique_degrees, ccdf, s=dot_size, marker='o')  
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"{image_name_prefix} - CCDF")
    plt.xlabel("k")
    plt.ylabel("CCDF")
    plt.savefig(save_dir / f"{image_name_prefix}_CCDF.png", bbox_inches='tight', dpi=dpi)
    plt.close()

def compute_ccdf(degrees):
    """
    Compute the CCDF from the degree distribution.

    Parameters:
    - degrees (list): List of all degrees.

    Returns:
    - unique_degrees (list): Sorted list of unique degrees.
    - ccdf (list): CCDF values for each unique degree.
    """
    degrees = np.array(degrees)
    unique_degrees = np.sort(np.unique(degrees))

    # Compute CCDF: 1 - CDF (Cumulative Distribution Function)
    ccdf = np.array([np.sum(degrees >= k) / len(degrees) for k in unique_degrees])

    return unique_degrees, ccdf

def draw_all_graphs():
    """
    Load data, compute degree distributions, and plot graphs for both in-degree and out-degree citations.
    """
    in_degree_file_path = "data/2014/paper_incites.txt"
    out_degree_file_path = "data/2014/paper_outcites.txt"

    save_directory = "visualization/preview"

    # In-degree citations
    in_degree_citation_data = load_citation_data(in_degree_file_path)
    in_unique_degrees, in_probabilities, in_degrees = compute_degree_distribution(in_degree_citation_data)
    plot_degree_distribution(in_unique_degrees, in_probabilities, in_degrees, save_directory, "In_Degree_Citation", dot_size=5, dpi=300)

    # Out-degree citations
    out_degree_citation_data = load_citation_data(out_degree_file_path)
    out_unique_degrees, out_probabilities, out_degrees = compute_degree_distribution(out_degree_citation_data)
    plot_degree_distribution(out_unique_degrees, out_probabilities, out_degrees, save_directory, "Out_Degree_Citation", dot_size=5, dpi=300)


def max_and_min_in_degree_citation():
    in_degree_file_path = "data/2014/paper_incites.txt"
    in_degree_citation_data = load_citation_data(in_degree_file_path)
    print("Max and min value of in degree citation: ")
    print(in_degree_citation_data['Citations'].max(), in_degree_citation_data['Citations'].min())
    return

def max_and_min_out_degree_citation():
    out_degree_file_path = "data/2014/paper_outcites.txt"
    out_degree_citation_data = load_citation_data(out_degree_file_path)
    print("Max and min value of out degree citation: ")
    print(out_degree_citation_data['Citations'].max(), out_degree_citation_data['Citations'].min())
    return

if __name__ == "__main__":

    draw_all_graphs()
    max_and_min_in_degree_citation()
    max_and_min_out_degree_citation()