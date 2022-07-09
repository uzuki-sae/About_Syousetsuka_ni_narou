import sys
import json
import os
import numpy as np
import statistics 

text = "co-dic.json"

tf = open(text, 'r')
t_dict = json.load(tf)
tf.close()
t_words = t_dict.keys()
t_uniq = len(t_words)
t_sm = sum(t_dict.values())
i = 0
print("述べ語数：{1}, 異なり語数：{0}, 異語率：{2:-2f}%".format(t_uniq, t_sm, t_uniq / t_sm * 100))
