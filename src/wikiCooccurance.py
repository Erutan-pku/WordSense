#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import urllib
import codecs
import random
import pandas as pd
from dataAnalysis import getWordPairs, evalueSpearman
random.seed(1322)

def WikiCount(page, word) :
    response_str = urllib.urlopen('https://en.wikipedia.org/wiki/'+page).read().lower()
    ret = {'wordCnt':response_str.count(word.lower()), 'blank':response_str.count(' '), 'len':len(response_str), 'pnCnt':response_str.count(page.lower())}

    #time.sleep(3)
    return ret

def getWikiCount(Data) :
    outputFile = codecs.open('../data/WikiPageCount.tab', "w", "utf-8")
    outputFile.write('\t'.join(['word1','word2','cnt1@2','cnt2@1','blank1','blank2','len1','len2','cnt1@1','cnt2@2',])+'\n')
    for data in Data :
        ret_1in2 = WikiCount(page=data[1], word=data[0])
        ret_2in1 = WikiCount(page=data[0], word=data[1])
        outputFile.write('%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n'%(data[0],data[1],ret_1in2['wordCnt'],ret_2in1['wordCnt'],ret_2in1['blank'],ret_1in2['blank'],ret_2in1['len'],ret_1in2['len'],ret_2in1['pnCnt'],ret_1in2['pnCnt']))
    outputFile.flush()
    outputFile.close()

def getBingScores(dataSet='All') :
    assert dataSet in ['All', 'set1', 'set2']

    getP = lambda x,y,b : float(x)/(y-b)
    getScore = lambda cn1,all1,cn2,all2:getP(cn1,all1,0)+getP(cn2,all2,0)#+random.random()/10000

    Data = pd.read_table('../data/WikiPageCount.tab', encoding='utf-8')
    """
    min(Data['blank1'])   = 1159
    min(Data['blank2'])   = 1045
    min(Data['len1'])     = 24331
    min(Data['len2'])     = 24410
    """
    #0.582384658573     0.634910303834      0.481524038101
    #scores = [getScore(Data['cnt1@2'][i],Data['len2'][i],Data['cnt2@1'][i],Data['len1'][i]) for i in range(len(Data))]
    #0.582585242277     0.635005796577      0.481627165679
    scores = [getScore(Data['cnt1@2'][i],Data['blank2'][i],Data['cnt2@1'][i],Data['blank1'][i]) for i in range(len(Data))]
    #0.566952126174     0.619619737847      0.469664741619
    #scores = [getScore(Data['cnt1@2'][i],Data['cnt2@2'][i],Data['cnt2@1'][i],Data['cnt1@1'][i]) for i in range(len(Data))]

    if dataSet=='All' :
        return scores
    elif dataSet == 'set1' :
        return scores[:153]
    elif dataSet == 'set2' :
        return scores[153:]


if __name__ == '__main__' :
    Data = getWordPairs()
    #getWikiCount(Data)

    setAll = getBingScores()
    print evalueSpearman(setAll)
    print evalueSpearman(setAll[:153], dataSet='set1')
    print evalueSpearman(setAll[153:], dataSet='set2')





 