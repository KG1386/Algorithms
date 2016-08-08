# Takes a number of text files pre-labelled as positive and negative to train the naive bayes algorithm.
# Upon extracting features, can predict result of new files
# based on:
# http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
# http://blog.yhat.com/posts/naive-bayes-in-python.html
# Algorithm with the current training set and functions performs better with disabled option of separating stop-words and no n-grams

# Import custom files used with this program
import wordFreqTable as wft
import stringExtractor as se

# Contains linking words, currently unused
linkages = se.readFile("vocabulary", "voc_linkages.txt")
file_counter = 0
vocab = {}

test_word_list = []
word_counts = {
    "p": {},"n": {}
}
train_distribution = {
    "p": 0.,"n": 0.
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
    file_counter += 1
    print file_counter
    # Saves categories of files discovered as a list
    categories.append(category)
    # Counts number of positive and negative texts
    train_distribution[category] += 1
    # Call the function from other file imported to main file(here) to get frequency table for words
    counts = wft.create_freq_table(se.readFile("sample_training_set", str(text_file))) # Get the table with number of occurences from wordFreqTable
    words = wft.extr_words(se.readFile("sample_training_set", str(text_file))) # Get the individual words from the text

    cleaned_word_list = wft.obtainCleanedList(counts)
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

# Find all text files in specified folder
all_text_files = se.readAllFiles("sample_test_set")
# Reset counters for successful predictions and number of files
suc_counter = 0.0
file_counter = 0.0

# Go over all test files in the folder
for text_file in all_text_files:
    # Training data is collected, analyse given sample
    test_counts = wft.create_freq_table(se.readFile("sample_test_set", str(text_file)))  # Get the table with number of occurences from wordFreqTable
    words = wft.extr_words(se.readFile("sample_test_set", str(text_file)))  # Get the individual words from the text
    # Same function as for training
    test_word_list = wft.obtainCleanedList(test_counts)
    # Find n-grams
    test_n_grams = wft.find_bigrams(test_word_list)
    # Obtain frequency table for text
    test_counts = wft.create_freq_table_simp(test_n_grams)  # Get the table with number of occurences from wordFreqTable
    # Obtain probabilities for entire textfile for it being negative or positive
    pos_score,neg_score = wft.obtainProbabilities(test_counts,vocab,word_counts)

    # Find if prediction is correct and count how often its correct
    if pos_score > neg_score and "pos" in text_file:
        polarised_flag = True
        suc_counter += 1
    elif pos_score < neg_score and "neg" in text_file:
        polarised_flag = True
        suc_counter += 1
    else:
        polarised_flag = False
    print "File -", text_file, ",scored positive -",pos_score, ",scored negative -", neg_score,"Flag -", polarised_flag

    # Find how many files have been assessed
    file_counter += 1

# Show how good the prediction was
print "Successful estimations:",((suc_counter/file_counter)*100),"%"
print "Training data distribution:"
print "Positive:", (train_distribution["p"] / sum(train_distribution.values())), "Negative:", (train_distribution["n"] / sum(train_distribution.values()))
