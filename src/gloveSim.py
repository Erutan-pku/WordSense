#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import codecs
import numpy as np
from tools.IO import W2V, line2list, list2line
from dataAnalysis import getWordPairs, evalueSpearman

def simplifyGlove(wordSet, glovePath='../data/glove.840B.300d.txt', outputPath='../data/glove.840B.300d_simple.txt') :
    input = codecs.open(glovePath, encoding='utf-8')
    output = codecs.open(outputPath, "w", "utf-8")
    output.write('Startline\n')
    
    count = 0
    average = None
    for line in input :
        word = line.split(' ')[0]
        if not word in wordSet :
            continue
        output.write(line)
        
        count += 1
        np_t = np.array(line2list(line, convert=float, start=1))
        average = np_t if average is None else average+np_t

        if count == len(wordSet) :
            break
    
    average /= count
    output.write('__NWord__ %s\n'%(list2line(average, convert=lambda x :'%.5f'%(x))))
    output.flush()
    output.close()

def getGolveCos(Data, dataSet='All') :
    assert dataSet in ['All', 'set1', 'set2']
    w2v = W2V(wordVecFile='../data/glove.840B.300d_simple.txt')

    #0.737948131687     0.745359387774      0.668458711468
    scores = [w2v.getCosine(x[0],x[1]) for x in Data]
    #0.588199062515     0.690938576387      0.462343808595
    #scores = [-w2v.getEuclideanDis(x[0],x[1]) for x in Data]

    if dataSet=='All' :
        return scores
    elif dataSet == 'set1' :
        return scores[:153]
    elif dataSet == 'set2' :
        return scores[153:]

if __name__ == '__main__':
    Data = getWordPairs()
    wordSet = set([x for xs in Data for x in xs])

    #simplifyGlove(wordSet)
    setAll = getGolveCos(Data)
    print evalueSpearman(setAll)
    print evalueSpearman(setAll[:153], dataSet='set1')
    print evalueSpearman(setAll[153:], dataSet='set2')