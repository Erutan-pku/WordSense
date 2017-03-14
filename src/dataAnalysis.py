import pandas as pd
import numpy as np
import random

def getWordPairs(dataSet='All') :
    assert dataSet in ['All', 'set1', 'set2']
    data1 = pd.read_table('../wordsim353/set1.tab', encoding='utf-8')
    data2 = pd.read_table('../wordsim353/set2.tab', encoding='utf-8')
    data1_word1 = list(data1['Word 1'])
    data1_word2 = list(data1['Word 2'])
    human_mean1 = list(data1['Human (mean)'])
    data2_word1 = list(data2['Word 1'])
    data2_word2 = list(data2['Word 2'])
    human_mean2 = list(data2['Human (mean)'])

    word1, word2, human_mean = [], [], []
    if dataSet == 'All' :
        word1 = data1_word1+data2_word1
        word2 = data1_word2+data2_word2
        human_mean = human_mean1+human_mean2
    elif dataSet == 'set1' :
        word1 = data1_word1
        word2 = data1_word2
        human_mean = human_mean1
    elif dataSet == 'set2' :
        word1 = data2_word1
        word2 = data2_word2
        human_mean = human_mean2
    assert len(word1) == len(word2)

    return [[word1[i], word2[i], human_mean[i]] for i in range(len(word1))]

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

def evalueSpearman(xs, dataSet='All', data=None) :
    if not data is None :
        dataSet = None
    assert dataSet in ['All', 'set1', 'set2', None]
    data_mean1 = pd.read_table('../wordsim353/set1.tab', encoding='utf-8')['Human (mean)'].values
    data_mean2 = pd.read_table('../wordsim353/set2.tab', encoding='utf-8')['Human (mean)'].values

    if dataSet == 'All' :
        data = list(data_mean1)+list(data_mean2)
    elif dataSet == 'set1' :
        data = data_mean1
    elif dataSet == 'set2' :
        data = data_mean2

    return countSpearman(xs, data)    

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
            matrix1[i][j] = "%.4f"%countSpearman(data_i, data1[str(j+1)].values)
        meanScore1.append(countSpearman(data_i, [(data1_mean[j]*13-data_i[j])/12 for j in range(len(data_i))]))
    matrix2 = np.zeros([16,16])
    for i in range(16) :
        data_i = data2[str(i+1)].values
        for j in range(16) :
            matrix2[i][j] = "%.4f"%countSpearman(data_i, data2[str(j+1)].values)
        meanScore2.append(countSpearman(data_i, [(data2_mean[j]*16-data_i[j])/15 for j in range(len(data_i))]))

    print matrix1
    print matrix2
    """
    [[ 1.      0.7126  0.746   0.688   0.6546  0.6495  0.7034  0.7466  0.7915   0.7935  0.5984  0.7116  0.6744]
     [ 0.7126  1.      0.7292  0.7487  0.5808  0.541   0.7114  0.7536  0.7029   0.7526  0.5712  0.7459  0.6978]
     [ 0.746   0.7292  1.      0.8138  0.6281  0.7202  0.7692  0.7987  0.7113   0.744   0.6178  0.7242  0.7496]
     [ 0.688   0.7487  0.8138  1.      0.679   0.6513  0.7677  0.7305  0.6519   0.7045  0.6064  0.6972  0.748 ]
     [ 0.6546  0.5808  0.6281  0.679   1.      0.6076  0.6755  0.6105  0.6178   0.6324  0.5536  0.6301  0.713 ]
     [ 0.6495  0.541   0.7202  0.6513  0.6076  1.      0.6308  0.593   0.6072   0.6036  0.4182  0.5592  0.6222]
     [ 0.7034  0.7114  0.7692  0.7677  0.6755  0.6308  1.      0.7406  0.7068   0.7246  0.5218  0.7705  0.7559]
     [ 0.7466  0.7536  0.7987  0.7305  0.6105  0.593   0.7406  1.      0.7131   0.7481  0.6046  0.7672  0.7215]
     [ 0.7915  0.7029  0.7113  0.6519  0.6178  0.6072  0.7068  0.7131  1.       0.7762  0.5754  0.7428  0.7771]
     [ 0.7935  0.7526  0.744   0.7045  0.6324  0.6036  0.7246  0.7481  0.7762   1.      0.6469  0.7768  0.7462]
     [ 0.5984  0.5712  0.6178  0.6064  0.5536  0.4182  0.5218  0.6046  0.5754   0.6469  1.      0.6335  0.6254]
     [ 0.7116  0.7459  0.7242  0.6972  0.6301  0.5592  0.7705  0.7672  0.7428   0.7768  0.6335  1.      0.7499]
     [ 0.6744  0.6978  0.7496  0.748   0.713   0.6222  0.7559  0.7215  0.7771   0.7462  0.6254  0.7499  1.    ]]

    [[ 1.      0.6213  0.6559  0.6759  0.4382  0.6342  0.622   0.6443  0.6419   0.5557  0.593   0.6283  0.658   0.4166  0.5675  0.6709]
     [ 0.6213  1.      0.5988  0.623   0.3839  0.5281  0.6064  0.6963  0.6631   0.4874  0.6193  0.5931  0.6344  0.2904  0.6591  0.5692]
     [ 0.6559  0.5988  1.      0.7059  0.5255  0.6745  0.6612  0.6944  0.6529   0.5692  0.6461  0.6234  0.7018  0.4404  0.6418  0.6369]
     [ 0.6759  0.623   0.7059  1.      0.4693  0.5598  0.6259  0.7215  0.6556   0.58    0.6914  0.629   0.6691  0.4272  0.6484  0.6323]
     [ 0.4382  0.3839  0.5255  0.4693  1.      0.4381  0.4497  0.51    0.4774   0.4466  0.5038  0.5361  0.4441  0.4051  0.4657  0.4516]
     [ 0.6342  0.5281  0.6745  0.5598  0.4381  1.      0.5617  0.5807  0.5611   0.5429  0.4505  0.5502  0.5844  0.4438  0.5429  0.7021]
     [ 0.622   0.6064  0.6612  0.6259  0.4497  0.5617  1.      0.6135  0.5916   0.53    0.589   0.5193  0.6181  0.3443  0.6633  0.6191]
     [ 0.6443  0.6963  0.6944  0.7215  0.51    0.5807  0.6135  1.      0.6794   0.5662  0.6892  0.6341  0.6848  0.4349  0.6076  0.6383]
     [ 0.6419  0.6631  0.6529  0.6556  0.4774  0.5611  0.5916  0.6794  1.       0.5977  0.6384  0.6341  0.669   0.3796  0.6067  0.6502]
     [ 0.5557  0.4874  0.5692  0.58    0.4466  0.5429  0.53    0.5662  0.5977   1.      0.5068  0.5419  0.5233  0.515   0.518   0.5891]
     [ 0.593   0.6193  0.6461  0.6914  0.5038  0.4505  0.589   0.6892  0.6384   0.5068  1.      0.5862  0.606   0.2957  0.6017  0.5229]
     [ 0.6283  0.5931  0.6234  0.629   0.5361  0.5502  0.5193  0.6341  0.6341   0.5419  0.5862  1.      0.6356  0.3882  0.574   0.6332]
     [ 0.658   0.6344  0.7018  0.6691  0.4441  0.5844  0.6181  0.6848  0.669    0.5233  0.606   0.6356  1.      0.3864  0.6301  0.5827]
     [ 0.4166  0.2904  0.4404  0.4272  0.4051  0.4438  0.3443  0.4349  0.3796   0.515   0.2957  0.3882  0.3864  1.      0.3807  0.3852]
     [ 0.5675  0.6591  0.6418  0.6484  0.4657  0.5429  0.6633  0.6076  0.6067   0.518   0.6017  0.574   0.6301  0.3807  1.      0.5879]
     [ 0.6709  0.5692  0.6369  0.6323  0.4516  0.7021  0.6191  0.6383  0.6502   0.5891  0.5229  0.6332  0.5827  0.3852  0.5879  1.    ]]
    """
    # 0.7988 [0.8208, 0.8178, 0.8454, 0.8167, 0.7194, 0.6848, 0.8214, 0.8325, 0.8122, 0.8627, 0.6790, 0.8298, 0.8421]
    # 0.7286 [0.7743, 0.7247, 0.8121, 0.7989, 0.5761, 0.7173, 0.7307, 0.8128, 0.7817, 0.7011, 0.7269, 0.7344, 0.7716, 0.5016, 0.7395, 0.7542]
    print sum(meanScore1)/len(meanScore1), meanScore1
    print sum(meanScore2)/len(meanScore2), meanScore2

    # -0.0032777465053      -0.0162739068477        -0.00387015379948
    random.seed(1337)
    ran_score1 = [random.random() for i in range(len(data1_mean))]
    ran_score2 = [random.random() for i in range(len(data2_mean))]
    print evalueSpearman(ran_score1, dataSet = 'set1')
    print evalueSpearman(ran_score2, dataSet = 'set2')
    print evalueSpearman(ran_score1+ran_score2)


