#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import codecs
import numpy as np
from dataAnalysis import getWordPairs, evalueSpearman
from tools.NNData_Tools import nf_dataSep
from tools.IO import loadLists
from wordNetSimilarity import wup_max, res_ave_genesis
from GoogleSimilarity import getBingScores
from wikiCooccurance import getWikiScores
from gloveSim import getGolveCos

def normalization(x) :
    x = np.array(x)
    x -= min(x)
    x /= max(x)
    return x
def writeSVMFile(filename, dataqidDict):
    assert type(dataqidDict) is list
    
    #filename = '../data/'+filename
    filename = '../../svm_rank/'+filename
    output = codecs.open(filename, "w", "utf-8")

    for datas in dataqidDict:
        assert 'qid' in datas.keys() and 'data' in datas.keys()
        for data in datas['data'] :
            output.write('%.3f qid:%d'%(data[2], datas['qid']))
            for i in range(3, len(data)) :
                if data[i] < 0.00005 :
                    continue
                output.write(' %d:%.4f'%(i-2, data[i]))
            output.write('\n')
    output.flush()
    output.close()

def getDataSet_all() :
    data = getWordPairs()
    #label_wup_max = wup_max(data)
    label_res_ave_genesis = res_ave_genesis(data)
    label_Bing_NGD = getBingScores(dataSet='All')
    label_Wiki_Blank = getWikiScores(dataSet='All')
    label_Glove_cos = getGolveCos(data)
    label_all = [label_res_ave_genesis, label_Bing_NGD, label_Wiki_Blank, label_Glove_cos]
    label_all = [normalization(label) for label in label_all]

    """
    print evalueSpearman(label_wup_max)
    print evalueSpearman(label_res_ave_genesis)
    print evalueSpearman(label_Bing_NGD)
    print evalueSpearman(label_Wiki_Blank)
    print evalueSpearman(label_Glove_cos)
    print evalueSpearman([sum([label[i] for label in label_all]) for i in range(len(data))])
    #"""

    dataset_all = [(data[i]+[label[i] for label in label_all])for i in range(len(data))]

    set1 = dataset_all[:153]
    set2 = dataset_all[153:]
    useless1, useless2, DetailedData = nf_dataSep([set1, set2], nflod=5, needDetail=True)

    return dataset_all, DetailedData

def supervisedDataGenerate(dataset_all, DetailedData) :
    set1 = dataset_all[:153]
    set2 = dataset_all[153:]
    
    writeSVMFile(filename='set1_all', dataqidDict=[{'qid':1,'data':set1}])
    writeSVMFile(filename='set2_all', dataqidDict=[{'qid':2,'data':set2}])
    for i in range(5) :
        writeSVMFile(filename='set1_validation_train'+str(i), dataqidDict=[{'qid':1,'data':DetailedData[0]['Train'][i]}])
        writeSVMFile(filename='set1_validation_test'+str(i), dataqidDict=[{'qid':2,'data':DetailedData[0]['Test'][i]}])
        writeSVMFile(filename='set2_validation_train'+str(i), dataqidDict=[{'qid':1,'data':DetailedData[1]['Train'][i]}])
        writeSVMFile(filename='set2_validation_test'+str(i), dataqidDict=[{'qid':2,'data':DetailedData[1]['Test'][i]}])
    for i in range(5) :
        writeSVMFile(filename='all_validation_train'+str(i), dataqidDict=[{'qid':1,'data':DetailedData[0]['Train'][i]},{'qid':2,'data':DetailedData[1]['Train'][i]}])
        writeSVMFile(filename='all_validation_test'+str(i), dataqidDict=[{'qid':3,'data':DetailedData[0]['Test'][i]},{'qid':4,'data':DetailedData[1]['Test'][i]}])

def evaluation(truthDatas, predictFileList) :
    getHuman = lambda x : [xi[2] for xi in x]
    predict_x = [xt for pf in predictFileList for xt in loadLists('../../svm_rank/'+pf,convert=float)]
    truth_x = [xt for td in truthDatas for xt in getHuman(td)]
    return evalueSpearman(predict_x, data=truth_x)

if __name__ == '__main__':
    dataset_all, DetailedData = getDataSet_all()
    supervisedDataGenerate(dataset_all, DetailedData)

    set1 = dataset_all[:153]
    set2 = dataset_all[153:]
    predict_name_set1 = ['predition_set1_validation_test'+str(i) for i in range(5)]
    predict_name_set2 = ['predition_set2_validation_test'+str(i) for i in range(5)]
    predict_name_all  = ['predition_all_validation_test'+str(i) for i in range(5)]
    set_validation_all = [DetailedData[j]['Test'][i] for i in range(5) for j in range(2)]

    #print 'predition_set1_all'
    print evaluation([set1], ['predition_set1_all'])

    #print 'predition_set2_all'
    print evaluation([set2], ['predition_set2_all'])

    #print 'predition_set1+2_all'
    print evaluation([set1, set2], ['predition_set1_all', 'predition_set2_all'])
    print 

    #print 'set1_validation'
    print evaluation(DetailedData[0]['Test'], predict_name_set1)

    #print 'set2_validation'
    print evaluation(DetailedData[1]['Test'], predict_name_set2)

    #print 'set1+2_validation'
    print evaluation(DetailedData[0]['Test']+DetailedData[1]['Test'], predict_name_set1+predict_name_set2)
    print 

    #print 'all_validation'
    print evaluation(set_validation_all, predict_name_all)
"""
1 1:0.52561176 2:0.8987509 3:3.2789834 4:4.405395 #
1 1:1.4645686 2:1.9386984 3:2.174679 4:5.1021175 #

c=1
0.772291691796
0.692836570914
0.751440983514

0.763088369319
0.671481287032
0.631314124039

0.760986544455
"""


