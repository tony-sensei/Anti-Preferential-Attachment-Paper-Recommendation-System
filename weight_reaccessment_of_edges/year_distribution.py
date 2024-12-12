from collections import Counter
import matplotlib.pyplot as plt

"""
This file mainly works on analyzing the publication year of articles.

Including generating the plot of the publication year distribution of the whole dataset and top 100 cited papers.

@Author Kristy He

"""


def generate_year_dictionary(file):
    year_dic = {}
    with open(file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                article_id = parts[0]
                year = parts[2]
                if year != "":
                    year_dic[article_id] = year
    return year_dic


def analyze_year_distribution(dictionary):
    years = list(dictionary.values())
    year_distribution = Counter(years)
    sorted_year_distribution = dict(sorted(year_distribution.items()))

    plt.figure(figsize=(10, 6))
    plt.bar(sorted_year_distribution.keys(), sorted_year_distribution.values(), color='#ec9ba2')
    plt.xlabel('Year')
    plt.ylabel('Number of Articles')
    plt.title('Publication Year Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def top_citation_paper(file):
    article_dict = {}
    with open(file, 'r') as file:
        for line in file:
            year, articles_count = line.strip().split(", ")
            article_dict[year] = int(articles_count)
    sorted_dict = sorted(article_dict.items(), key=lambda x: x[1], reverse=True)
    years = [year for year, count in sorted_dict]
    article_counts = [count for year, count in sorted_dict]

    plt.bar(years, article_counts, color='#ec9ba2')

    plt.title('Number of Articles by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Articles')
    plt.xticks(rotation=45)

    plt.show()


if __name__ == "__main__":
    paper_ids = "paper_ids.txt"
    id_to_year = generate_year_dictionary(paper_ids)

    analyze_year_distribution(id_to_year)

    top_article_file = "top_100_articles_year_distribution.txt"
    top_citation_paper(top_article_file)



