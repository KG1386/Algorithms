# Example of Naive Bayes implemented from Scratch in Python. Works as a classification technique based on
# Bayes Theorem with an assumption of independence among predictors
# based on http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

import csv
import random
import math

# Retreive contents of the csv. file into list
def loadCsv(filename):
    lines = csv.reader(open(filename, "rb"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset

# Receives dataset list and based on splitRatio variable set in the main separates train and test data
def splitDataset(dataset, splitRatio):
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    copy = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return [trainSet, copy]

# Separates dataset based on the last value in the entry(row) which stands for class variable(or Y, the output)
def separateByClass(dataset):
    separated = {}                          # List with classes as keys
    for i in range(len(dataset)):
        vector = dataset[i]                 #Save current entry(row) into vector
        if (vector[-1] not in separated):   # If class value(0 or 1) is not yet in the list as the key, put it there
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)# Record the entry corresponding to the class it belongs to
    return separated

# Find the mean of the attribute received
def mean(numbers):
    return sum(numbers) / float(len(numbers))

# Find the standard deviation of the attribute
def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)

# Takes each column of data with attributes of entries and calculates mean and standard deviation for each, returns tuple(2) for each attribute
def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)] # Zip retreives entire column and passes it to mean and std.dev function
    del summaries[-1]   # Delete the last column
    return summaries

# Summarize mean and standard deviation for each attribute and group into classes
def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.iteritems():
        summaries[classValue] = summarize(instances)
    return summaries

# Use the Bayes formula to calculate
def calculateProbability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

# Calculate probability for class
def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities

# Obtain mean and standard deviation for each class list and training list and find the largest probability
def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel

# Iterate over entire test set and save as a predictions list
def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
    return predictions

# Check the accuracy of the predictions by counting the number of correct guesses and dividing it by the total number of entries in test set
def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0

# Main process function
def main():
    filename = 'pima-indians-diabetes.data.csv'
    splitRatio = 0.7
    dataset = loadCsv(filename)
    trainingSet, testSet = splitDataset(dataset, splitRatio)
    print('Split {0} rows into train={1} and test={2} rows').format(len(dataset), len(trainingSet), len(testSet))
    # prepare model
    summaries = summarizeByClass(trainingSet)
    # test model
    predictions = getPredictions(summaries, testSet)
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: {0}%').format(accuracy)

# Call the main function
main()