# File that contains all directories used and provides interface to extract necessary strings when required

from os import listdir
from os.path import isfile, join

# Read all the files in the folder
def readAllFiles(folder):
    my_path = 'D:/Projects/Algorithms/Naive_Bayes_text' + "/" + str(folder)
    all_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return all_files

# Open file specified by program folder and file arguments, return string with all words
def readFile(folder, filename):
    file_location = 'D:/Projects/Algorithms/Naive_Bayes_text/' + str(folder) + "/" + str(filename)
    text_file = open(file_location, 'r')
    return text_file.read()