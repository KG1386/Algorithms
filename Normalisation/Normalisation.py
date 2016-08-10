# Library for performing normalisation tasks


def extractColumns(data_list):
    columnsList = []
    for x in range(len(data_list[0])):
        columnsList.append(zip(*data_list)[x])
    return columnsList

def normaliseColumns(columnsList):
    temp_list = []
    normalised_list = []
    for item in columnsList:
        if str(item[0]).isdigit() == True:
            min_val = float(min(item))
            max_val = float(max(item))
            for x in item:
                normalised_value = (x - min_val)/(max_val - min_val)
                temp_list.append(normalised_value)
            normalised_list.append(temp_list)
            temp_list = []
        else:
            for x in item:
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
    print standardConversion(normalised_list)
    return standardConversion(normalised_list)

data_list=[[11,7,1,5,"item1"],[8,19,13,13,"item2"],[21,22,23,2,"item3"],[3.5,13,42,73,"item4"],[2.5,1.3,4.2,2.3,"item5"]]

normaliseList(data_list)