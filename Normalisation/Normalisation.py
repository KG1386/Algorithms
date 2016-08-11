# Library for performing normalisation tasks
import math

def extractColumns(data_list):
    columnsList = []
    for x in range(len(data_list[0])):
        columnsList.append(zip(*data_list)[x])
    return columnsList

def normaliseColumns(columnsList):
    temp_list = []
    normalised_list = []
    for item in columnsList:
        for x in item:
            try:
                x= float(x)
                min_val = float(min(item))
                max_val = float(max(item))
                normalised_value = (x - min_val) / (max_val - min_val)
                normalised_value = round(normalised_value,2)
                temp_list.append(float(normalised_value))
            except:
                temp_list.append(x)

        normalised_list.append(temp_list)
        temp_list = []
    return normalised_list


def standardConversion(normalised_list):
    standardList = []
    for x in range(len(normalised_list[0])):
        standardList.append(zip(*normalised_list)[x])
    return standardList

# Function that normalises lists where numeric data and text fields may occur in the columns
def normaliseList(data_list):
    columns = extractColumns(data_list)
    normalised_list = normaliseColumns(columns)
    return standardConversion(normalised_list)

