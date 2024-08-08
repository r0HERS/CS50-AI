import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = {}
    total_pages = len(corpus)

    if corpus[page]:
        links = corpus[page]
    else:
        links = corpus.keys()

    random_prob = (1 - damping_factor) / total_pages

    for p in corpus:
        probabilities[p] = random_prob

    if corpus[page]:
        link_prob = damping_factor / len(links)
        for link in links:
            probabilities[link] += link_prob
    else:
        link_prob = damping_factor / total_pages
        for p in corpus:
            probabilities[p] += link_prob

    return probabilities

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_rank[current_page] += 1
        transition_probs = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(transition_probs.keys()), weights=transition_probs.values(), k=1)[0]

    for page in page_rank:
        page_rank[page] /= n

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    page_rank = {page: 1 / num_pages for page in corpus}

    converged = False
    while not converged:
        new_pagerank = {}
        for page in corpus:
            new_rank = (1 - damping_factor) / num_pages
            for potential_linking_page in corpus:
                if page in corpus[potential_linking_page]:
                    new_rank += damping_factor * (page_rank[potential_linking_page] / len(corpus[potential_linking_page]))
                if len(corpus[potential_linking_page]) == 0:
                    new_rank += damping_factor * (page_rank[potential_linking_page] / num_pages)
            new_pagerank[page] = new_rank

        converged = all(abs(new_pagerank[page] - page_rank[page]) < 0.001 for page in page_rank)
        page_rank = new_pagerank

    return page_rank

if __name__ == "__main__":
    main()
