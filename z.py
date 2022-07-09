import sys
import json
import os
import numpy as np
import statistics 

text = sys.argv[1]
genre = sys.argv[2]

tf = open(text, 'r')
t_dict = json.load(tf)
tf.close()
t_words = t_dict.keys()
t_sm = sum(t_dict.values())
zscore = {}

cop_list = [f.name for f in os.scandir(genre) if f.name.startswith('freq')]
word=""        
def cross(word):
    x_field=[]
    for cop in cop_list:
        cop_file = open("301/{}".format(cop), 'r')
        cop_dict = json.load(cop_file)
        cop_file.close()
        key = cop_dict.keys()
        c_sm = sum(cop_dict.values())
        if word in key :
            wd = cop_dict[word] * 1000000 / c_sm
            x_field.append(wd)
        else:
            x_field.append(0)
    
    return x_field

i = 0
for word in t_words:
    i = i + 1
    x_field = cross(word)
    mean = sum(x_field) / len(x_field)
    sd = statistics.stdev(x_field)
    dev = t_dict[word] - mean
    z = round( dev / sd * 10 + 50 , 7 )
    wz = {word:z}
    zscore.update(wz)
    print(wz)
    print("complete:{0:-2f}%".format( i / len(t_words) * 100.0))
print(zscore)
tt = text.replace('freq', '').replace('.json', '')

with open("{}-zscore.csv".format(tt), 'w') as out:
    out.write("形態素, 偏差値\n")
    for k, v in zscore.items():
        out.write("{},{}\n".format(k, v))



