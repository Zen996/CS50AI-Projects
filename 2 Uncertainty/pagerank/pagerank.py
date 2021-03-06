import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(corpus)
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

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, curr_page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    if len(corpus[curr_page]):
        #if page has outgoing links
        prdict = {pages: (
                damping_factor/len(corpus[curr_page]) +(1-damping_factor)/len(corpus) 
                if pages in corpus[curr_page] 
                else (1-damping_factor)/len(corpus))
                for pages in corpus
                }
        #print(prdict)
        
    else:#no outgoing links
        prdict = {pages: 1/len(corpus)
                for pages in corpus
                }
        #print(prdict)

    """
    The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing the probability that a random surfer would choose that page next. The values in this returned probability distribution should sum to 1.
    {page:pr}
    """
    return prdict
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    #random starting page
    r = random.randint(0,len(corpus)-1)
    count=0
    for i in corpus:
        if count == r:
            page = i
            break
        count+=1
    spdict = {pages: 0
              for pages in corpus
             }
    spdict[page] += 1/n

    for j in range(1,n):
        prdict = transition_model(corpus, page, damping_factor)
        r2=random.random()
        #Choosing next page by probability
        for i in prdict:
            r2 = r2 - prdict[i]
            if r2 < 0:
                page = i
                spdict[page] += 1/n
                break
            
    return spdict
    raise NotImplementedError

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ACC_DIFF = 0.001
    corpuscopy = copy.deepcopy(corpus)
    for p in corpuscopy:
        if not len(corpus[p]): #no outgoing links
             corpuscopy[p] = {s for s in corpus}

    itrdict = {pages: 1/len(corpus)
              for pages in corpus
             }

    flag = 0
    while(flag < len(itrdict)):#when all converged
        flag = 0
        itrdict_old = copy.deepcopy(itrdict)
        for p in itrdict:
            #PR(p) = (1-damping_factor)/len(corpus) + damping_factor*sum(PRi)/numLinks(i)
            
            sum_df = 0

            for i in corpuscopy:        #for all pages in corpus,
                if p in corpuscopy[i]:  #look for pages linking to p
                    #print(i,p,"left links to right")
                    sum_df += itrdict_old[i]/len(corpuscopy[i])
            itrdict[p] =  (1-damping_factor)/len(corpuscopy) + damping_factor*sum_df

            if abs(itrdict[p] - itrdict_old[p]) < ACC_DIFF:
                flag+=1
                #print(flag)
                #print(itrdict[p],itrdict_old[p])
            #else:
                #print("noflag",itrdict[p],itrdict_old[p],p)
    #print("converged")
    return itrdict
    raise NotImplementedError


if __name__ == "__main__":
    main()
