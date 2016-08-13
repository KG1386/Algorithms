# Main file of the algorithm. Contains calls to other functions not included here

# Practical implementation of KNN algorithm with train and test data supplied by .csv
# based on:
# http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

import csv
import random
import math
import operator
import Normalisation as norm

# Function for loading the dataset into list
def loadDataset(filename):
    rawList =[]
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        norm_dataset = norm.normaliseList(dataset)
        for x in range(len(norm_dataset) - 1):
            rawList.append(norm_dataset[x])
    return rawList

# Function for calculating the distance between unknown point and its neighbour using euclidian formula
def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]),2)
    return math.sqrt(distance)

# Saves the neighbouring points and respective distances to them
def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    n_distances = []
    for x in range(k):
        neighbors.append(distances[x][0])
        n_distances.append(distances[x][-1])
    return neighbors,n_distances

# Obtain weighted sum for each category and return the smallest value
def getResponse(neighbors,n_distances):
    # Keeps weighted votes summary
    classCount = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classCount:
            classCount[response] += n_distances[x]
        else:
            classCount[response] = 1
    # Sum all the counts for each class and pass the result
    sortedVotes = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

# Compare predicted label and the actual label
def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


def main(k):
    # Load data from .csv files
    trainingSet = loadDataset('pima-indians-diabetes.Train.csv')
    testSet = loadDataset('pima-indians-diabetes.Test.csv')
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))
    predictions = []
    # Entire dataset is reevaluated for each entry
    for x in range(len(testSet)):
        neighbors,n_distances = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors,n_distances)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%')
    return accuracy

# Loop over specified range to find optimal K
def findK(iter_base,iter_end):
    max_acc = 0
    for x in xrange(iter_base, iter_end):
        acc = int(main(x+1))
        if acc > max_acc:
            max_acc = acc
            best_k = x
    return max_acc, best_k+1

# Specify the starting and ending values of range where optimal k value will be searched for
print "Best accuracy and K value:", findK(50,70)
#main(14)