import requests
from pathlib import Path
import tarfile
from neo4j import GraphDatabase
from collections import defaultdict
import networkx as nx
from py2neo import Graph
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt

uri = "neo4j+s://8df4b24f.databases.neo4j.io"
username = "neo4j"
password = "mbTM6NJ62-cY1Duvdu9J7lk3PhhIrOQwdFe7jwVwM5Q"
database = "neo4j"

def community_detection():
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
    print(partition)

    # Label Propagation
    communities = nx.algorithms.community.label_propagation_communities(G)
    for community in communities:
        print(community)
    # Assign colors to nodes based on their community
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=[partition[node] for node in G.nodes()]
    )
    plt.show()

def filered_community():
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
    from collections import defaultdict
    communities = defaultdict(list)
    for node, community in partition.items():
        communities[community].append(node)

    # Filter communities with more than 10 members
    filtered_communities = {c: nodes for c, nodes in communities.items() if len(nodes) > 100}

    # Print filtered communities
    print("Filtered Communities:")
    for community, nodes in filtered_communities.items():
        print(f"Community {community}: {nodes}")

    # Create a subgraph with nodes from the filtered communities
    filtered_nodes = [node for nodes in filtered_communities.values() for node in nodes]
    filtered_graph = G.subgraph(filtered_nodes)

    # Assign colors to nodes based on their community
    color_map = {node: community for community, nodes in filtered_communities.items() for node in nodes}
    node_colors = [color_map[node] for node in filtered_graph.nodes()]

    # Visualize the filtered graph
    pos = nx.spring_layout(filtered_graph)
    nx.draw(
        filtered_graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        cmap=plt.cm.tab20
    )
    plt.show()

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

    # Now, update Neo4j with community information
    for node, community in partition.items():
        # Assuming you have nodes identified by `name`, and each node needs a `community` property
        neo4j_graph.run("""
            MATCH (n {name: $node_name})
            SET n.community = $community_number
            """, node_name=node, community_number=community)

    print("Community numbers have been updated in Neo4j.")


if __name__ == "__main__":
   update_with_community_number()