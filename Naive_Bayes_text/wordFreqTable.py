# Module that deals with text file processing such as: removing punctuation, lowercasing, counting occurences and creating n-grams
import re
import string
from nltk import PorterStemmer # Library that implements stemming functions
import math


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

# Unused at the moment
def find_bigrams(input_list):
  bigram_list = []
  for i in range(len(input_list)-1):
      bigram_list.append(str(input_list[i]))
  return bigram_list

# Function that checks if the word in a text file matches the requirements, converts it to basic form and records new word
def obtainCleanedList (counts):
    cleaned_word_list = []
    for word, count in counts.items():
        # Make sure that file is longer that 3 letters, is not a stop word and not a digit
        if len(word) >= 3 and word.isdigit() is False:
            # Transform the word into its basic form (increases recognition rate significantly)
            word = PorterStemmer().stem_word(word)
            # Add transformed word into list
            cleaned_word_list.append(word)
    return cleaned_word_list

def obtainProbabilities(test_counts,vocab,word_counts):
    log_prob_positive = 0.0  #
    log_prob_negative = 0.0

    pos_score, neg_score = 0,0
    # Pre-calculate sums to save processing time
    vocab_sum_pos = sum(word_counts["p"].values())
    vocab_sum_neg = sum(word_counts["n"].values())
    vocab_sum = sum(vocab.values())

    for word, count in test_counts.items():
        # Check if the word is in vocabulary at all, and calculate its score (how often it occurs)
        if word in vocab:
            p_word = vocab[word] / vocab_sum

        # Find probability that word fits to positive or negative category
        p_w_given_positive = word_counts["p"].get(word, 0.0) / vocab_sum_pos
        p_w_given_negative = word_counts["n"].get(word, 0.0) / vocab_sum_neg

        # Using logarithms allows to keep numbers manageable by python as log function scales them
        if p_w_given_positive > 0:
            log_prob_positive += math.log(count * p_w_given_positive / p_word)
        if p_w_given_negative > 0:
            log_prob_negative += math.log(count * p_w_given_negative / p_word)

        # Exponent helps to get rid of negative numbers
        pos_score = math.exp(log_prob_positive)
        neg_score = math.exp(log_prob_negative)
    return pos_score, neg_score
