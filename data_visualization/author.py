import requests
from pathlib import Path
import tarfile
from neo4j import GraphDatabase
from collections import defaultdict
import networkx as nx
from py2neo import Graph
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt

def community_detection():
    # Connect to the Neo4j graph database
    neo4j_graph = Graph(uri, auth=("neo4j", password))
    output_file = "community_results.txt"  # Specify the output file for results

    # Query the graph to get node relationships (edges)
    query = """
    MATCH (a)-[r]->(b)
    RETURN id(a) AS source_id, id(b) AS target_id
    """
    results = neo4j_graph.run(query)  # Execute the query and fetch the results

    # Create a NetworkX graph to represent the nodes and relationships
    G = nx.Graph()
    for record in results:
        # Add an edge to the graph using node IDs as source and target
        G.add_edge(record["source_id"], record["target_id"])

    # Perform community detection using the Louvain method
    partition = community_louvain.best_partition(G)

    # Calculate the size of each community
    community_sizes = {}
    for community_id in partition.values():
        # Count the number of nodes in each community
        community_sizes[community_id] = community_sizes.get(community_id, 0) + 1

    # Calculate the number of communities and the average community size
    num_communities = len(community_sizes)
    avg_size = sum(community_sizes.values()) / num_communities

    # Print the results of the community detection
    print(f"Community results saved to {output_file}")  # Inform the user about the output file
    print(f"Number of communities: {num_communities}")  # Print the number of communities detected
    print(f"Average community size: {avg_size:.2f}")  # Print the average size of the communities

def filered_community_adjustment_visulization():

    neo4j_graph = Graph(uri, auth=("neo4j", password))

    # Query nodes and relationships
    query = """
        MATCH (a)-[r]->(b)
        RETURN a.name AS source, b.name AS target
    """
    results = neo4j_graph.run(query)

    # Create NetworkX graph
    G = nx.Graph()
    for record in results:
        G.add_edge(record["source"], record["target"])

    # Louvain community detection
    partition = community_louvain.best_partition(G)

    # Group nodes by community
    communities = defaultdict(list)
    for node, community in partition.items():
        communities[community].append(node)

    # Filter communities with more than 100 members
    filtered_communities = {c: nodes for c, nodes in communities.items() if len(nodes) > 100}

    # Create subgraph
    filtered_nodes = [node for nodes in filtered_communities.values() for node in nodes]
    filtered_graph = G.subgraph(filtered_nodes)

    # Assign colors to nodes based on their community
    color_map = {node: community for community, nodes in filtered_communities.items() for node in nodes}
    node_colors = [color_map[node] for node in filtered_graph.nodes()]

    # Layout and visualization
    pos = nx.spring_layout(filtered_graph, k=1.5, iterations=200)
    node_sizes = [filtered_graph.degree(node) * 50 for node in filtered_graph.nodes()]
    nx.draw(
        filtered_graph,
        pos,
        with_labels=False,  # Remove labels to declutter
        node_color=node_colors,
        cmap=plt.cm.tab20,
        node_size=node_sizes,
        alpha=0.8
    )
    plt.show()

def update_with_community_number():
    neo4j_graph = Graph(uri, auth=("neo4j", password))

    # Query the graph for nodes and relationships
    query = """
        MATCH (a)-[r]->(b)
        RETURN a.name AS source, b.name AS target
    """
    results = neo4j_graph.run(query)

    # Create a NetworkX graph from Neo4j data
    G = nx.Graph()

    for record in results:
        G.add_edge(record["source"], record["target"])

    # Perform community detection using Louvain
    partition = community_louvain.best_partition(G)

    from collections import Counter

    # Count the number of nodes in each community
    community_sizes = Counter(partition.values())

    # Print the size of each community
    print("Community Sizes:")
    for community, size in community_sizes.items():
        print(f"Community {community}: {size} nodes")

    # File path to save the output
    output_file = "author_community.txt"

    # Write each author and their community number to the file
    with open(output_file, "w") as f:
        for author, community_number in partition.items():
            f.write(f"{author}, {community_number}\n")  # Write as "author, community_number"

    print(f"Author-community data has been saved to {output_file}.")

    # Now, update Neo4j with community information
    for node, community in partition.items():
        # Assuming you have nodes identified by `name`, and each node needs a `community` property
        neo4j_graph.run("""
            MATCH (n {name: $node_name})
            SET n.community = $community_number
            """, node_name=node, community_number=community)

    print("Community numbers have been updated in Neo4j.")


if __name__ == "__main__":
    community_detection()