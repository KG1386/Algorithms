# Module that takes file, extracts words from it, lowercases, removes punctuation and creates freqency table(how often word occurs in text)

import re
import string

# Removes punctuation from the text
def remove_punctuation(text):
    table = string.maketrans("", "")
    return text.translate(table, string.punctuation)

# Extract separate words out of text and lowercase it
def extr_words(text):
    text = remove_punctuation(text)
    text = text.lower()
    return re.split("\W+", text)

# .Get function looks up the dictionary and if the word is not there, returns 0 if not, 1. Both added to +1 at the end
def create_freq_table(text):
    words = extr_words(text)
    dict = {}
    for word in words:
        dict[word] = dict.get(word, 0.0) + 1.0
    return dict

def create_freq_table_simp(text):
    dict = {}
    for word in text:
        dict[word] = dict.get(word, 0.0) + 1.0
    return dict

# Bigrams has been found to give the best performance
def find_bigrams(input_list):
  bigram_list = []
  for i in range(len(input_list)-1):
      bigram_list.append(str(input_list[i]))
  return bigram_list


