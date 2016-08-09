# Library for performing normalisation tasks

data_list=[[11,7,1,5,"bume"],[8,19,13,13,"text"],[21,22,23,2,"age"]]
normalised_list = []
columnsList = []

def extractColumns(data_list):
    for x in range(len(data_list[0])-1):
        columnsList.append(zip(*data_list)[x])
    return columnsList

def normaliseColumns(columnsList):
    normalised_value = 0.0
    temp_list = []
    for count,item in enumerate(columnsList):
        print item
        print count
        min_val = float(min(item))
        max_val = float(max(item))
        normalised_list.append(count)
        for count_in,x in enumerate(item):
            normalised_value = (x - min_val)/(max_val - min_val)
            print normalised_value
            temp_list.append(normalised_value)
        normalised_list.append(temp_list)
        temp_list = []
    return normalised_list


columns = extractColumns(data_list)
print normaliseColumns(columns)