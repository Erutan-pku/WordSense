#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import random
import numpy as np

# return a list of num empty lists
def nEmptyList(num) :
    ret = []
    for i in range(num) :
        ret.append([])
    return ret

# n-flod cross-validation
def nf_dataSep(datasets, nflod, seed=1337, needDetail=False) :
    # datasets = list of (list of Jsons)
    assert(type(datasets) is list)
    random.seed(seed)

    allTrains = nEmptyList(nflod)
    allTests = nEmptyList(nflod)
    DetailedData = []

    for dataset in datasets :
        Train_t = nEmptyList(nflod)
        Test_t = nEmptyList(nflod)

        index = range(len(dataset))
        random.shuffle(index)
        for i in range(len(dataset)) :
            tempData = dataset[index[i]]
            for jj in range(nflod) :
                if i % nflod == jj :
                    Test_t[jj].append(tempData)
                else :
                    Train_t[jj].append(tempData)

        for i in range(nflod):
            allTrains[i] += Train_t[i]
            allTests[i] += Test_t[i]
        DetailedData.append({'Train':Train_t, 'Test':Test_t})

    if needDetail :
        return allTrains, allTests, DetailedData
    else :
        return allTrains, allTests

# convert data from m * n * Object -> n * m * Object
def DataConvert(Input) :
    n = len(Input[0])
    output = nEmptyList(n)
    for data in Input :
        for i in range(n) :
            output[i].append(data[i])
    return output

