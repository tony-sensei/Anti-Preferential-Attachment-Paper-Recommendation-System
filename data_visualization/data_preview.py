import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def load_citation_data(file_path):

    file_path = Path(file_path)
    df = pd.read_csv(file_path, sep='\t', header=None, names=['Paper_ID', 'Citations'])
    return df

def plot_citation_histogram(df, save_dir, image_name="citation_histogram.png"):

    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.hist(df['Citations'], bins=range(0, df['Citations'].max() + 1), edgecolor='black', alpha=0.7)

    plt.title('Citation Distribution for Papers', fontsize=16)
    plt.xlabel('Number of Citations', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    

    file_path = save_dir / image_name
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()  

    print(f"Histogram saved to: {file_path}")
    return file_path

def draw_all_graphs():
    in_degree_file_path = "data/2014/paper_incites.txt"
    out_degree_file_path = "data/2014/paper_outcites.txt"

    save_directory = "visualization/preview"

    in_degree_citation_data = load_citation_data(in_degree_file_path)
    out_degree_citation_data = load_citation_data(out_degree_file_path)
    
    plot_citation_histogram(in_degree_citation_data, save_directory, image_name="In degree citation")
    plot_citation_histogram(out_degree_citation_data, save_directory, image_name="Out degree citation")
    return

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