import pandas as pd
import numpy as np

def getWordPairs(dataSet='All') :
    assert dataSet in ['All', 'set1', 'set2']
    data1 = pd.read_table('../wordsim353/set1.tab', encoding='utf-8')
    data2 = pd.read_table('../wordsim353/set2.tab', encoding='utf-8')
    data1_word1 = list(data1['Word 1'])
    data1_word2 = list(data1['Word 2'])
    data2_word1 = list(data2['Word 1'])
    data2_word2 = list(data2['Word 2'])

    word1, word2 = [], []
    if dataSet == 'All' :
        word1 = data1_word1+data2_word1
        word2 = data1_word2+data2_word2
    elif dataSet == 'set1' :
        word1 = data1_word1
        word2 = data1_word2
    elif dataSet == 'set2' :
        word1 = data2_word1
        word2 = data2_word2
    assert len(word1) == len(word2)

    return [[word1[i], word2[i]] for i in range(len(word1))]

def getRank(x) :
    dataPairs = sorted(zip(x, range(len(x))))
    countDup = {}
    for rank, data in enumerate(dataPairs):
        if not countDup.has_key(data[0]) :
            countDup[data[0]] = [0, 0]
        count_t = countDup[data[0]]
        count_t[1] = (count_t[1]*count_t[0]+rank)/(count_t[0]+1.0)
        count_t[0] += 1.0
    dataPairs = {x[1]:countDup[x[0]][1] for x in dataPairs}
    return dataPairs
def countSpearman(x1, x2) :
    assert len(x1) == len(x2)
    xx1, xx2 = getRank(x1), getRank(x2)
    length = len(x1)
    ps = 0
    for i in range(length) :
        ps += (xx1[i]-xx2[i]) ** 2
    ps = 1-6*ps/length/(length**2-1)
    return ps


# Spearman correlation coefficient between labelers
if __name__ == '__main__' :
    data1 = pd.read_table('../wordsim353/set1.tab', encoding='utf-8')
    data2 = pd.read_table('../wordsim353/set2.tab', encoding='utf-8')
    data1_mean = data1['Human (mean)'].values
    data2_mean = data2['Human (mean)'].values

    meanScore1 = []
    meanScore2 = []

    matrix1 = np.zeros([13,13])
    for i in range(13) :
        data_i = data1[str(i+1)].values
        for j in range(13) :
            matrix1[i][j] = countSpearman(data_i, data1[str(j+1)].values)
        meanScore1.append(countSpearman(data_i, [(data1_mean[j]*13-data_i[j])/12 for j in range(len(data_i))]))
    matrix2 = np.zeros([16,16])
    for i in range(16) :
        data_i = data2[str(i+1)].values
        for j in range(16) :
            matrix2[i][j] = countSpearman(data_i, data2[str(j+1)].values)
        meanScore2.append(countSpearman(data_i, [(data2_mean[j]*16-data_i[j])/15 for j in range(len(data_i))]))
    print matrix1
    print matrix2

    print sum(meanScore1)/len(meanScore1), meanScore1
    print sum(meanScore2)/len(meanScore2), meanScore2


