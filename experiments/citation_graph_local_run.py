import os
import random
import networkx as nx
import numpy as np
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity

def run_citation_recommender(
    input_file="data/2014/networks/paper_citation_network.txt",
    output_file="experiments/results/baseline_top10_with_similarity.txt",
    num_samples=1000,
    embedding_dim=64,
    walk_length=10,
    num_walks=100,
    p=0.1,
    q=2,
    workers=4,
    seed=42
):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("Step 1: Loading the graph...")
    G = nx.DiGraph()
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if "==>" in line:
                src, dst = line.split("==>")
                src = src.strip()
                dst = dst.strip()
                G.add_edge(src, dst)

    print(f"Total nodes in the graph: {len(G.nodes())}")
    print(f"Total edges in the graph: {len(G.edges())}")

    print("Step 2: Sampling nodes...")
    all_nodes = list(G.nodes())
    random.seed(seed)
    sampled_nodes = random.sample(all_nodes, min(num_samples, len(all_nodes)))
    print("Sampled nodes count:", len(sampled_nodes))

    print("Step 3: Generating node2vec embeddings...")
    node2vec = Node2Vec(
        G,
        dimensions=embedding_dim,
        walk_length=walk_length,
        num_walks=num_walks,
        p=p,
        q=q,
        workers=workers
    )

    print("Fitting the model...")
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    print("Model training completed.")

    print("Extracting embeddings...")
    node_list = model.wv.index_to_key
    embeddings = np.array([model.wv[node] for node in node_list])
    node_to_idx = {node: idx for idx, node in enumerate(node_list)}

    print("Step 4: Generating recommendations...")
    with open(output_file, 'w', encoding='utf-8') as out:
        for i, node in enumerate(sampled_nodes):
            if i % 100 == 0 and i > 0:
                print(f"Processed {i} out of {len(sampled_nodes)} sampled nodes...")
            
            if node not in node_to_idx:
                continue
                
            node_vec = embeddings[node_to_idx[node]].reshape(1, -1)
            # Compute similarity to all other nodes
            sim = cosine_similarity(node_vec, embeddings).flatten()
            
            # Exclude the node itself
            sim_indices = np.argsort(-sim)
            sim_indices = [idx for idx in sim_indices if node_list[idx] != node]
            
            top_10_indices = sim_indices[:10]
            # Pair recommendations with their similarities
            top_10_recommendations = [(node_list[idx], sim[idx]) for idx in top_10_indices]
            
            # Format: Node ==> Rec1:sim1, Rec2:sim2, ...
            rec_str = ", ".join([f"{rec_node}:{similarity:.4f}" for rec_node, similarity in top_10_recommendations])
            out.write(f"{node} ==> {rec_str}\n")

    print(f"Recommendations stored in {output_file}")


def run_citation_recommender_with_weights(
    input_file="experiments/weighted_paper_citation_network.txt",
    baseline_file="experiments/results/baseline_top10_p=0.5_q=0.25.txt",
    output_file="experiments/results/weighted_top10_with_similarity.txt",
    embedding_dim=64,
    walk_length=10,
    num_walks=100,
    p=0.1,
    q=2,
    workers=4,
    seed=42
):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Step 1: Load previously sampled nodes from the baseline file
    print("Loading previously sampled nodes from baseline file...")
    sampled_nodes = []
    with open(baseline_file, 'r', encoding='utf-8') as sf:
        for line in sf:
            line = line.strip()
            if "==>" in line:
                node, _ = line.split("==>")
                node = node.strip()
                sampled_nodes.append(node)
    print(f"Loaded {len(sampled_nodes)} previously sampled nodes.")

    # Step 2: Load the weighted graph
    print("Loading the weighted graph...")
    G = nx.DiGraph()
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if "==>" in line:
                parts = line.split()
                if len(parts) < 4:
                    continue
                src = parts[0].strip()
                dst = parts[2].strip()
                weight = float(parts[3])
                G.add_edge(src, dst, weight=weight)

    print(f"Total nodes in the graph: {len(G.nodes())}")
    print(f"Total edges in the graph: {len(G.edges())}")

    # Filter sampled_nodes to ensure they are in the current graph
    sampled_nodes = [n for n in sampled_nodes if n in G.nodes()]
    print(f"Sampled nodes count (filtered if needed): {len(sampled_nodes)}")

    # Step 3: Generate node2vec embeddings
    random.seed(seed)
    np.random.seed(seed)
    print("Generating node2vec embeddings")
    node2vec = Node2Vec(
        G,
        dimensions=embedding_dim,
        walk_length=walk_length,
        num_walks=num_walks,
        p=p,
        q=q,
        workers=workers
    )

    print("Fitting the model...")
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    print("Model training completed.")

    print("Extracting embeddings...")
    node_list = model.wv.index_to_key
    embeddings = np.array([model.wv[node] for node in node_list])
    node_to_idx = {node: idx for idx, node in enumerate(node_list)}

    # Step 4: Generating top 10 recommendations with similarities
    print("Generating top 10 recommendations with similarities...")
    with open(output_file, 'w', encoding='utf-8') as out:
        for i, node in enumerate(sampled_nodes):
            if i % 100 == 0 and i > 0:
                print(f"Processed {i} out of {len(sampled_nodes)} sampled nodes...")

            if node not in node_to_idx:
                # Node might not have embedding if isolated or removed
                continue

            node_vec = embeddings[node_to_idx[node]].reshape(1, -1)
            sim = cosine_similarity(node_vec, embeddings).flatten()

            # Exclude the node itself
            sim_indices = np.argsort(-sim)
            sim_indices = [idx for idx in sim_indices if node_list[idx] != node]

            # Take top 10 recommendations
            top_10_indices = sim_indices[:10]
            top_10_recommendations = [(node_list[idx], sim[idx]) for idx in top_10_indices]

            # Format: Node ==> Rec1:sim1, Rec2:sim2, ...
            rec_str = ", ".join([f"{rec_node}:{similarity:.4f}" for rec_node, similarity in top_10_recommendations])
            out.write(f"{node} ==> {rec_str}\n")

    print(f"Recommendations stored in {output_file}")



if __name__ == '__main__':
    run_citation_recommender(num_samples=100, num_walks=20, p=0.25, q=0.25, output_file="experiments/results/baseline_top10_p=0.25_q=0.25.txt")
    run_citation_recommender(num_samples=100, num_walks=20, p=0.5, q=0.25, output_file="experiments/results/baseline_top10_p=0.5_q=0.25.txt")
    run_citation_recommender(num_samples=100, num_walks=20, p=1, q=1, output_file="experiments/results/baseline_top10_p=1_q=1.txt")
    run_citation_recommender_with_weights(num_walks=20, p=0.25, q=0.25, output_file="experiments/results/weighted_top10_p=0.25_q=0.25.txt")
    run_citation_recommender_with_weights(num_walks=20, p=0.5, q=0.25, output_file="experiments/results/weighted_top10_p=0.5_q=0.25.txt")
    run_citation_recommender_with_weights(num_walks=20, p=1, q=1, output_file="experiments/results/weighted_top10_p=1_q=1.txt")
    run_citation_recommender(num_samples=100, num_walks=100, p=0.1, q=2, output_file="experiments/results/baseline_top10_p=0.1_q=2.txt")
    run_citation_recommender_with_weights(num_walks=100, p=0.1, q=2, output_file="experiments/results/weighted_top10_p=0.1_q=2.txt")
