from db_connection import get_db_driver, close_driver
import networkx as nx
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def run_query(cypher_query, parameters=None):
    """
    Execute a Cypher query on the Neo4j database.
    """
    driver = get_db_driver()
    try:
        with driver.session(database="neo4j") as session:
            result = session.run(cypher_query, parameters or {})
            return [record for record in result]
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        close_driver(driver)

def fetch_graph_data():
    """
    Fetch nodes and relationships from Neo4j.
    """
    # Fetch nodes
    nodes_query = "MATCH (n:Author) RETURN id(n) AS id, n.name AS name"
    nodes = run_query(nodes_query)
    nodes_data = [(record["id"], {"name": record["name"]}) for record in nodes]

    # Fetch relationships
    rels_query = "MATCH (a:Author)-[r:COLLABORATED]->(b:Author) RETURN id(a) AS source, id(b) AS target"
    relationships = run_query(rels_query)
    edges_data = [(record["source"], record["target"]) for record in relationships]

    return nodes_data, edges_data

def create_networkx_graph(nodes_data, edges_data):
    """
    Create a NetworkX graph from nodes and edges.
    """
    graph = nx.Graph()  # Undirected graph
    graph.add_nodes_from(nodes_data)
    graph.add_edges_from(edges_data)
    return graph

def generate_node2vec_embeddings(graph, dimensions=4, walk_length=10, num_walks=200, p=1, q=1):
    """
    Generate Node2Vec embeddings using the NetworkX graph with tunable parameters.
    """
    node2vec = Node2Vec(graph, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=4, p=p, q=q)
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    embeddings = {str(node): model.wv[str(node)] for node in graph.nodes()}
    return embeddings

def compute_cosine_similarity(embeddings):
    """
    Compute cosine similarity between all nodes using their embeddings.
    """
    # Convert embeddings dictionary to a matrix
    embedding_matrix = np.array(list(embeddings.values()))
    node_ids = list(embeddings.keys())

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(embedding_matrix)

    def recommend_similar_nodes(node_id, top_k=5):
        """
        Recommend top-k similar nodes for a given node based on cosine similarity.
        """
        node_index = node_ids.index(str(node_id))
        similarities = similarity_matrix[node_index]
        similar_indices = similarities.argsort()[-(top_k + 1):-1][::-1]
        similar_nodes = [(node_ids[i], similarities[i]) for i in similar_indices]
        return similar_nodes

    return recommend_similar_nodes

if __name__ == "__main__":
    # Step 1: Fetch graph data from Neo4j
    print("Fetching graph data from Neo4j...")
    nodes_data, edges_data = fetch_graph_data()
    print(f"Retrieved {len(nodes_data)} nodes and {len(edges_data)} edges.")

    # Step 2: Create a NetworkX graph
    print("Creating NetworkX graph...")
    graph = create_networkx_graph(nodes_data, edges_data)

    # Step 3: Generate Node2Vec embeddings
    print("Generating Node2Vec embeddings...")
    embeddings = generate_node2vec_embeddings(graph, 
                                              dimensions=4, 
                                              walk_length=10, 
                                              num_walks=200, 
                                              p=1, 
                                              q=1)

    # Step 4: Compute cosine similarity and get recommendations
    print("Computing cosine similarity...")
    recommend_similar_nodes = compute_cosine_similarity(embeddings)

    # Example: Recommend similar nodes for a given node ID
    example_node = list(embeddings.keys())[0]  # Take the first node as an example
    print(f"Recommendations for Node {example_node}:")
    recommendations = recommend_similar_nodes(example_node, top_k=5)
    for node, similarity in recommendations:
        print(f"Node: {node}, Similarity: {similarity}")
