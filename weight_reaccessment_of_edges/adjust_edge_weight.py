from collections import defaultdict
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

"""
This file works on re-assessment of edges in the network.
@Author: Kristy He
"""


def generate_year_dictionary(file):

    """
    This function generate a dictionary that contains the publication year of each article
    :param file: The path of file that contains publication info
    :return: The generated dictionary
    """

    year_dic = {}
    with open(file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace('    ', '\t')
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                article_id = parts[0]
                year = parts[2]
                if year != "":
                    year_dic[article_id] = year
    return year_dic


def generate_paper_author_dic(file):

    """
    This function generate the dictionary that contains the author(s) of each article.
    :param file: The path of file that contains author information.
    :return: The generated dictionary
    """

    paper_to_authors = defaultdict(list)
    with open(file, "r") as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            if not line.strip():
                continue
            paper_id, author_id, _ = line.strip().split("\t")
            paper_to_authors[paper_id].append(author_id)
        paper_to_authors = dict(paper_to_authors)
        return paper_to_authors


def generate_community_dic(file):

    """
    This function generate the dictionary that contains community ID of each author.
    :param file: The path of file that contains community information of authors.
    :return: The generated dictionary.
    """

    communities = {}
    with open(file, "r") as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            if not line.strip():
                continue
            author_id, community_id = line.strip().split(", ")
            communities[author_id] = community_id
        return communities


def calculate_weight(citing, cited):

    """
    Calculate the weight of edge.
    :param citing: The paper ID of paper that citing other article.
    :param cited: The paper ID of paper that being cited.
    :return: The value of weight.
    """

    citing_year = id_to_year.get(citing)
    cited_year = id_to_year.get(cited)
    w = time_decay_function(int(cited_year))
    w = annual_publication_normalization(citing_year, w)
    if citing in paper_author_dic and cited in paper_author_dic:
        citing_author = paper_author_dic.get(citing)
        cited_author = paper_author_dic.get(cited)
        if community_boost(citing_author, cited_author):
            w = w * 1.5
    return w


def time_decay_function(t, k=0.1, t_0=2002):
    """
    Calculate the weight by time decay function.
    :param t: The publication year of paper.
    :param k: The time decay factor, controlling the degree of decaying.
    :param t_0: The center year.
    :return: The weight.
    """
    return 1 / (1 + np.exp(-k * (t - t_0)))


def annual_publication_normalization(citing_year, w):

    """
    Calculate the weight through annual publication normalization.
    :param citing_year: The year of citing.
    :param w: Current weight before normalization.
    :return: The value of weight.
    """

    count = year_distribution.get(citing_year)
    return w * 1 / (1 + np.log(count + 1))


def community_boost(citing_author, cited_author):

    """
    Adjust the weight by checking the community information of authors of two paper.s
    :param citing_author: A list of authors of the citing paper.
    :param cited_author: A list of authors of the cited paper.
    :return: The value of weight after boosting.
    """

    citing_communities = {author: community_dic.get(author) for author in citing_author}
    cited_communities = {author: community_dic.get(author) for author in cited_author}
    for author1, community1 in cited_communities.items():
        if community1 is None:
            continue
        for author2, community2 in citing_communities.items():
            if community2 is None:
                continue
            if community1 == community2:
                return True
    return False


def optimize_new_network(in_file):

    """
    Find the optimal threshold that can effectively reduce the degree of "hubs" in the network
    by drawing the plot of threshold v.s. maximum degree in the network
    :param in_file: The original paper citation network file
    :return: None
    """

    median_annual_normalization = 1 / (1 + np.log(np.median(list(year_distribution.values())) + 1))
    time_decay_threshold = [0.4, 0.41, 0.43, 0.45, 0.47, 0.49, 0.5]
    threshold_list = [median_annual_normalization * t for t in time_decay_threshold]
    maximum_degree_dic = {}
    for value in threshold_list:
        paper_weight_dic = {}
        remove_edge_num = 0
        with open(in_file, "r") as infile:
            for line in infile:
                line = line.strip()
                citing_id, cited_id = line.split(" ==> ")
                weight = calculate_weight(citing_id, cited_id)
                if weight < value:
                    remove_edge_num = remove_edge_num + 1
                    continue
                if cited_id not in paper_weight_dic:
                    paper_weight_dic[cited_id] = [weight]
                else:
                    paper_weight_dic[cited_id].append(weight)
        degree_new = [len(weights) for weights in paper_weight_dic.values()]
        maximum_degree_dic[value / median_annual_normalization] = max(degree_new)
    plot_max_degree(maximum_degree_dic)


def plot_max_degree(dic):

    """
    Draw the plot of threshold v.s. maximum degree in the network
    :param dic: The dictionary that contains the threshold and its corresponding maximum degree.
    :return: None
    """

    plt.figure(figsize=(10, 6))
    plt.plot(dic.keys(), dic.values())
    plt.xlabel("Threshold Value")
    plt.ylabel("Maximum Degree")
    plt.title("")
    plt.show()


def generate_new_network(in_file, out_file, threshold):

    """
    Generate the new network by using the optimal threshold.
    Also, compare the CCDF plot of new and old networks.

    :param in_file: The original paper citation network file.
    :param out_file: The new paper citation network file path.
    :param threshold: The optimal threshold.
    :return: None
    """

    paper_weight_dic = {}
    paper_unweight_dic = {}
    remove_edge_num = 0
    total_edge = 0
    with open(in_file, "r") as infile, open(out_file, 'w') as outfile:
        for line in infile:
            total_edge = total_edge + 1
            line = line.strip()
            citing_id, cited_id = line.split(" ==> ")
            weight = calculate_weight(citing_id, cited_id)
            if cited_id not in paper_unweight_dic:
                paper_unweight_dic[cited_id] = [weight]
            else:
                paper_unweight_dic[cited_id].append(weight)
            if weight < threshold:
                remove_edge_num = remove_edge_num + 1
                continue
            if cited_id not in paper_weight_dic:
                paper_weight_dic[cited_id] = [weight]
            else:
                paper_weight_dic[cited_id].append(weight)
            outfile.write(f"{line} {weight}\n")
    for key in paper_unweight_dic.keys():
        if key not in paper_weight_dic:
            paper_weight_dic[key] = [max(paper_unweight_dic[key])]
    old_degree_dic = {key: len(paper_unweight_dic[key]) for key in paper_unweight_dic}
    new_degree_dic = {key: len(paper_weight_dic[key]) for key in paper_weight_dic}
    old_degrees = list(old_degree_dic.values())
    new_degrees = list(new_degree_dic.values())
    old_x, old_ccdf = compute_ccdf(old_degrees)
    new_x, new_ccdf = compute_ccdf(new_degrees)
    plot_ccdf_comparison(old_x, old_ccdf, new_x, new_ccdf)
    print(f"The percentage of removed edge is {remove_edge_num / total_edge}")


def compute_ccdf(degrees):

    """
    Compute complementary cumulative distribution function
    :param degrees: The list of degrees.
    :return: Degree and its corresponding CCDF value.
    """

    degree_counts = Counter(degrees)
    sorted_degrees = sorted(degree_counts.keys())
    total_nodes = sum(degree_counts.values())
    ccdf = []
    cumulative_sum = 0
    for degree in sorted_degrees:
        cumulative_sum += degree_counts[degree]
        ccdf.append(1 - cumulative_sum / total_nodes)
    return sorted_degrees, ccdf


def plot_ccdf_comparison(x1, ccdf1, x2, ccdf2):

    """
    Draw the comparison CCDF plot of new and old network.

    :param x1: degree list of original network.
    :param ccdf1: A list of CCDF values of original network.
    :param x2: degree list of new network.
    :param ccdf2: A list of CCDF values of new network.
    :return: None
    """

    plt.figure(figsize=(10, 6))
    plt.loglog(x1, ccdf1, marker='o', label="Original Network")
    plt.loglog(x2, ccdf2, marker='x', label="After Hub Removal")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("CCDF (log scale)")
    plt.title("CCDF Comparison of Degree Distribution")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    paper_ids = "paper_ids.txt"
    id_to_year = generate_year_dictionary(paper_ids)

    years = list(id_to_year.values())
    year_distribution = Counter(years)

    paper_author = "paper_author_affiliations.txt"
    paper_author_dic = generate_paper_author_dic(paper_author)

    community_file = "community_results.txt"
    community_dic = generate_community_dic(community_file)

    citation_file = "paper_citation_network.txt"
    output_file = "weighted_paper_citation_network.txt"

    optimize_new_network(citation_file)

    final_threshold = 0.43 * 1 / (1 + np.log(np.median(list(year_distribution.values())) + 1))
    generate_new_network(citation_file, output_file, final_threshold)

















