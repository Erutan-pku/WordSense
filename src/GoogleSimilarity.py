#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import re
import time
import urllib
import codecs
import math
import random
import pandas as pd
import numpy as np
from dataAnalysis import getWordPairs, evalueSpearman

def BingSearch(word1, word2=None) :
    query = word1 if word2 is None else word1+'+'+word2
    cnt_pattern = re.compile(r'[\d,]+ 条结果</span>')

    response_str = urllib.urlopen('http://cn.bing.com/search?q="%s"&qs=bs&form=QBLH'%(query)).read()
    match = cnt_pattern.search(response_str)

    cnt = int("".join(match.group().split()[0].split(","))) if match else 0
    #time.sleep(3)
    return cnt

def getSearchCount(Data) :
    outputFile = codecs.open('../data/BingSearchCount.tab', "w", "utf-8")
    outputFile.write('word1\tword2\tcnt1\tcnt2\tcnt12\n')
    for data in Data :
        cnt_word1 = BingSearch(data[0])
        cnt_word2 = BingSearch(data[1])
        cnt_word12 = BingSearch(data[0], data[1])
        outputFile.write('%s\t%s\t%d\t%d\t%d\n'%(data[0], data[1], cnt_word1, cnt_word2, cnt_word12))
    outputFile.flush()
    outputFile.close()

def getBingScores(dataSet='All') :
    assert dataSet in ['All', 'set1', 'set2']

    Data = pd.read_table('../data/BingSearchCount.tab', encoding='utf-8')
    #0.45746343252      0.457850006031      0.445134253356
    #getScore = lambda cn1,cn2,cn12 :float(cn12)/(cn1+cn2-cn12)
    #0.472190341318     0.493602823905      0.448374709368
    #getScore = lambda cn1,cn2,cn12 :float(cn12)/min(cn1,cn2) if not cn1*cn2*cn12==0 else 0
    #0.457344214459      0.457726032997      0.445134253356
    #getScore = lambda cn1,cn2,cn12 :2*float(cn12)/(cn1+cn2)
    #0.0.486824426444   0.508372368086    0.46434560864
    getScore = lambda cn1,cn2,cn12 :math.log(float(cn12*100000000.0)/cn1/cn2)if not cn1*cn2*cn12==0 else 0
    #0.510050532635     0.538611736561      0.470365259131
    #getScore = lambda cn1,cn2,cn12 :-(math.log(max(cn1,cn2))-math.log(cn12))/(math.log(100000000.0)-math.log(min(cn1,cn2))) if not cn1*cn2*cn12==0 else 0
    scores = [getScore(Data['cnt1'][i],Data['cnt2'][i],Data['cnt12'][i]) for i in range(len(Data))]
    score_ave = sum(scores) / len(scores)
    random.seed(1223)
    scores = [x if not x == 0 else score_ave for x in scores]
    if dataSet=='All' :
        return scores
    elif dataSet == 'set1' :
        return scores[:153]
    elif dataSet == 'set2' :
        return scores[153:]

if __name__ == '__main__' :
    Data = getWordPairs()
    #getSearchCount(Data)
    setAll = getBingScores()
    print evalueSpearman(setAll)
    print evalueSpearman(setAll[:153], dataSet='set1')
    print evalueSpearman(setAll[153:], dataSet='set2')






 