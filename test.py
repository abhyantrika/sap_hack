import itertools, nltk, string
import gensim
from itertools import takewhile, tee, izip
import networkx
import collections, math,re
from textract import process as pdf2txt


#Unsupervised methods
def extract_candidate_words(text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize and POS-tag words
    tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
                                                                    for sent in nltk.sent_tokenize(text)))
    # filter on certain POS tags and lowercase all words
    candidates = [word.lower() for word, tag in tagged_words
                  if tag in good_tags and word.lower() not in stop_words
                  and not all(char in punct for char in word)]

    return candidates

#TEXT_RANK
def score_keyphrases_by_textrank(text, n_keywords=0.05):
    # tokenize for all words, and extract *candidate* words
    words = [word.lower()
             for sent in nltk.sent_tokenize(text)
             for word in nltk.word_tokenize(sent)]
    candidates = extract_candidate_words(text)
    # build graph, each node is a unique candidate
    graph = networkx.Graph()
    graph.add_nodes_from(set(candidates))
    # iterate over word-pairs, add unweighted edges into graph
    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(iterable)
        next(b, None)
        return izip(a, b)
    for w1, w2 in pairwise(candidates):
        if w2:
            graph.add_edge(*sorted([w1, w2]))
    # score nodes using default pagerank algorithm, sort by score, keep top n_keywords
    ranks = networkx.pagerank(graph)
    if 0 < n_keywords < 1:
        n_keywords = int(round(len(candidates) * n_keywords))
    word_ranks = {word_rank[0]: word_rank[1]
                  for word_rank in sorted(ranks.iteritems(), key=lambda x: x[1], reverse=True)[:n_keywords]}
    keywords = set(word_ranks.keys())
    # merge keywords into keyphrases
    keyphrases = {}
    j = 0
    for i, word in enumerate(words):
        if i < j:
            continue
        if word in keywords:
            kp_words = list(takewhile(lambda x: x in keywords, words[i:i+10]))
            avg_pagerank = sum(word_ranks[w] for w in kp_words) / float(len(kp_words))
            keyphrases[' '.join(kp_words)] = avg_pagerank
            # counter as hackish way to ensure merged keyphrases are non-overlapping
            j = i + len(kp_words)
    
    return sorted(keyphrases.iteritems(), key=lambda x: x[1], reverse=True)

def getPDFContent(file):
	return re.sub(r'[%s]' % ''.join(map(unichr, range(32) + range(127, 256))), '', pdf2txt(file)), pdf2txt(file) #Needed as it gives structured data



def get_rank_list(ff):
	f = open('Chapter1.txt')
	ff = f.read()
	gg = ff[::]

	rank_list = []
	rank_list = score_keyphrases_by_textrank(str(extract_candidate_words(ff)))
	final_rank = rank_list_new[:10] 
	print final_rank
	f.close()

	print 

	""" Select 5 from old and 5 from new methods & Do not print candidate words! """
	out = open('output.txt','w')
	print len(final_rank)
	for i in (final_rank):
		if len(i[0]) > 3:
			print i[0],i[1]
			out.write('\n'.join(str(i).strip('()')))

FileName = 'Chapter1'

s = getPDFContent(FileName + '.pdf')
with open(FileName + '.txt','w') as g:
	g.write(s[0])
g.close()

with open(FileName + '_structured.txt','w') as h:
	h.write(s[1])
h.close()

print '\n scores => '



