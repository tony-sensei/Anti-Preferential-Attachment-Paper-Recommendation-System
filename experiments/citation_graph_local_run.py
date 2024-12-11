import os
import random
import networkx as nx
import numpy as np
from node2vec import Node2Vec
from sklearn.metrics.pairwise import cosine_similarity

def run_citation_recommender(
    input_file="data/2014/networks/paper_citation_network.txt",
    output_file="experiments/results/baseline_top5.txt",
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
                # If node didn't appear in the wv (rare, but possible), skip
                continue
            node_vec = embeddings[node_to_idx[node]].reshape(1, -1)
            # Compute similarity to all other nodes
            sim = cosine_similarity(node_vec, embeddings).flatten()
            
            # The node itself will have the highest similarity, so skip it
            sim_indices = np.argsort(-sim)
            sim_indices = [idx for idx in sim_indices if node_list[idx] != node]
            
            # Take top 5
            top_5_indices = sim_indices[:5]
            recommendations = [node_list[idx] for idx in top_5_indices]
            
            out.write(f"{node} ==> {', '.join(recommendations)}\n")

    print(f"Recommendations stored in {output_file}")


if __name__ == '__main__':
    run_citation_recommender()
