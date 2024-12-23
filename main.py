from data_preparation import data_download
from data_visualization import data_preview
from experiments import citation_graph_local_run

if __name__ == "__main__":
    
    # Download and extract the raw data
    data_download.download_and_extract()

    # Draw Preview graphs
    data_preview.draw_all_graphs()
    
    # Print the max and min citation counts
    data_preview.max_and_min_in_degree_citation()
    data_preview.max_and_min_out_degree_citation()

    # Experiments with random samples citation network 
    # paper recommendation
    citation_graph_local_run.run_citation_recommender()