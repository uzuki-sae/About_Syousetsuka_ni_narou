import time
import sys
import json

text=sys.argv[1]
print("open", text)
tt = text.replace('.txt-wakachi', '')
def get_dict():

  large_file_name = str(text)

  word_dict = {}
  with open(large_file_name, 'r') as infile:
    for line in infile:
      word = line[:-1] # remove \n
      if(word not in word_dict):
        word_dict[word] = 1
      else:
        word_dict[word] += 1
    
  with open("freq{}.json".format(tt), 'w') as dic:
    json.dump(word_dict, dic, indent=4)


time0 = time.time()
get_dict()
time = time0 - time.time()
print(time)


