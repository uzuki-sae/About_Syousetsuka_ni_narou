import MeCab

import csv
import os
import gensim
from gensim.models.word2vec import Word2Vec
from tqdm import tqdm
from split import split
import loggings

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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("処理を開始します。")

path = os.listdir("201")
token = []
for ps in tqdm(path):
    infile = "201/{}".format(ps)
    word = keitaiso(infile)
#    print(word)
    token.extend(word)
    word.clear()

#print(token)
model = Word2Vec(token, sg=1, vector_size=64, window=5, min_count=1)
token.clear()
model.save("201model.bin")
print(model)
