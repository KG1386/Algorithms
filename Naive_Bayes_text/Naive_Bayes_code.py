# Takes a number of text files pre-labelled as positive and negative to train the naive bayes algorithm. Upon extracting features, can predict
# result of new files
# based on http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
# http://blog.yhat.com/posts/naive-bayes-in-python.html


import wordFreqTable as wft
import stringExtractor as se
import math
from nltk import PorterStemmer # Library that implements stemming functions

pos_words = se.readFile("vocabulary", "voc_positive.txt")
neg_words = se.readFile("vocabulary", "voc_negative.txt")
linkages = se.readFile("vocabulary", "voc_linkages.txt")
file_counter = 0
vocab = {}
cleaned_word_list = []
test_word_list = []
word_counts = {
    "p": {},
    "n": {}
}
train_distribution = {
    "p": 0.,
    "n": 0.
}
categories = []
# Read all the files in the folder
all_text_files = se.readAllFiles("sample_training_set")
# Having all the files in the folder saved as string, go through each
for text_file in all_text_files:
    if "pos" in text_file:
        category = "p"
    elif "neg" in text_file:
        category = "n"
    file_counter = file_counter + 1
    print file_counter
    # Saves categories of files discovered as a list
    categories.append(category)
    # Counts number of positive and negative texts
    train_distribution[category] += 1
    # Call the function from other file imported to main file(here) to get frequency table for words
    counts = wft.create_freq_table(se.readFile("sample_training_set", str(text_file))) # Get the table with number of occurences from wordFreqTable
    words = wft.extr_words(se.readFile("sample_training_set", str(text_file))) # Get the individual words from the text
    for word, count in counts.items():
        # Make sure that file is longer that 3 letters, is not a stop word and not a digit
        if len(word) >= 3 and word not in linkages and word.isdigit() is False:
            # Transform the word into its basic form (increases recognition rate significantly)
            word = PorterStemmer().stem_word(word)
            # Add transformed word into list
            cleaned_word_list.append(word)
    # Assemble all words into pairs or more groupings(n-grams)
    n_grams = wft.find_bigrams(cleaned_word_list)
    # Get the table with number of occurences from wordFreqTable
    counts = wft.create_freq_table_simp(n_grams)

    for word, count in counts.items():
        # if we haven't seen a word yet, let's add it to our dictionaries with a count of 0
        if word not in vocab:
            vocab[word] = 0.0 # Create a new entry
        if word not in word_counts[category]:
            word_counts[category][word] = 0.0   # Word_counts is the list containing all words that belong to each category
            vocab[word] += count    # Vocabulary of all words irrespective of their category
            # Add occurrence data of the word into the list as well
            word_counts[category][word] += count

# Obtain distribution of positive and negative reviews by finding percentage of each category
a = sum(train_distribution.values())
train_dist_positive = (train_distribution["p"] / sum(train_distribution.values())) # devision of positive number of files/total files
train_dist_negative = (train_distribution["n"] / sum(train_distribution.values()))

all_text_files = se.readAllFiles("sample_test_set")
# Having all the files in the folder saved as string, go through each
suc_counter = 0.0
file_counter = 0.0
vocab_sum_pos = sum(word_counts["p"].values())
vocab_sum_neg = sum(word_counts["n"].values())
vocab_sum = sum(vocab.values())

for text_file in all_text_files:

    log_prob_positive = 0.0 #
    log_prob_negative = 0.0

    # Training data is collected, analyse given sample
    test_counts = wft.create_freq_table(se.readFile("sample_test_set", str(text_file)))  # Get the table with number of occurences from wordFreqTable
    words = wft.extr_words(se.readFile("sample_test_set", str(text_file)))  # Get the individual words from the text

    for word, count in test_counts.items():
        if len(word) >= 3 and word not in linkages and word.isdigit() is False:
            word = PorterStemmer().stem_word(word) # Transform the word into its basic form
            test_word_list.append(word) # Add transformed word into list
    test_n_grams = wft.find_bigrams(test_word_list)
    test_counts = wft.create_freq_table_simp(test_n_grams)  # Get the table with number of occurences from wordFreqTable

    for word, count in test_counts.items():
        # Check if the word is in vocabulary at all, and calculate its score (how often it occurs)
        if word in vocab:
            p_word = vocab[word] / vocab_sum

        # Find probability that word fits to positive or negative category
        p_w_given_positive = word_counts["p"].get(word, 0.0) / vocab_sum_pos
        p_w_given_negative = word_counts["n"].get(word, 0.0) / vocab_sum_neg
        # Depending which of the words is larger, add it to probability log
        if p_w_given_positive > 0:
            log_prob_positive += math.log(count * p_w_given_positive / p_word)
        if p_w_given_negative > 0:
            log_prob_negative += math.log(count * p_w_given_negative / p_word)

    # Goes from logspace to regular, prints filename and score for each file
    pos_score = math.exp(log_prob_positive + math.log(train_dist_positive))
    neg_score = math.exp(log_prob_negative + math.log(train_dist_negative))
    if pos_score > neg_score and "pos" in text_file:
        polarised_flag = True
        suc_counter += 1
    elif pos_score < neg_score and "neg" in text_file:
        polarised_flag = True
        suc_counter += 1
    else:
        polarised_flag = False
    print "File -", text_file, ",scored positive -",pos_score, ",scored negative -", neg_score,"Flag -", polarised_flag

    test_n_grams[:] = []
    test_counts.clear()
    words[:] = []
    log_prob_positive, log_prob_negative = 0,0
    test_word_list[:] = []
    file_counter += 1


print "Successful estimations:",((suc_counter/file_counter)*100),"%"