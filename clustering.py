import MeCab
import logging
from split import split
from scipy.cluster.hierarchy import linkage,dendrogram
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from tqdm import tqdm

import gensim
from gensim.models.word2vec import Word2Vec

infile = "201/N2267BE.txt"

def keitaiso(infile):
    mecab = MeCab.Tagger('-Owakachi')
    with open(infile, 'r', encoding="utf8", errors='ignore') as it:
        text = it.read()
    tx = text.split('\n')
    words = []
    for line in tx:
        word = mecab.parse(line).split('\n')
#        print(word)
        words.extend(word)
        word.clear()

    return words

def cluster_hier(word, wv):

    print(word)
    fp = FontProperties(fname=r"TaipeiSansTCBeta-Light.ttf")

    l = linkage(wv, metric="correlation", method="average")
    fig = plt.figure(figsize=(25,9))
    dendrogram(l, labels=word)
    for l in plt.gca().get_xticklabels():
        l.set_fontproperties(fp)
    fig.savefig("heirratical.jpg")

def aftertrain(word):

    model = Word2Vec.load("201model")
    model.build_vocab(word, update=True)
    model.train(word,total_examples=model.corpus_count, epochs=model.epochs)
    return model
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
def cluster(word, wv):
    model = KMeans(n_clusters= 4 ).fit(wv)
    labels = model.labels_
    print(labels)

    df = pd.DataFrame(wv)
    df["word"] = word
    df["cluster"] = labels

    pca = PCA(n_components=2)
    pca.fit(df.iloc[:,:-2])
    feature = pca.transform(df.iloc[:,:-2])

    fp = FontProperties(fname=r"TaipeiSansTCBeta-Light.ttf")
    color = {0:"green",1:"red",2:"yellow",3:"blue"}
    colors = [color[x] for x in labels]
    fig = plt.figure(figsize=(6, 6 ))
    for x,y,name in zip(feature[:,0], feature[:,1], word):
        plt.text(x, y, name, fontproperties = fp)

    plt.scatter(feature[:,0], feature[:,1], color = colors)
    plt.show()
    fig.savefig("scatter.jpg")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("処理を開始します。")

word = keitaiso(infile)
model = aftertrain(word)
wd = {}
for w in tqdm(word):
    if( w not in wd):
        wd[w] = 1
    else:
        wd[w] += 1

thirty_word = sorted(wd.items(), key=lambda x: x[1], reverse=True)
twd = dict(thirty_word[:256])
tw = list(twd.keys())
wv = []
s = set(tw)&set(model.wv.key_to_index)
ll = list(s)
for w in tqdm(ll):
    wv.append(model.wv[w])

print(ll)
with open('RE_word_vec', 'w') as f:
    f.write(str(wv))


 
cluster_hier(ll, wv)
cluster(ll, wv)
