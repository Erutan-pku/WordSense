#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import re
import time
import urllib
import codecs
from dataAnalysis import getWordPairs

def BingSearch(word1, word2=None) :
    query = word1 if word2 is None else word1+'+'+word2
    cnt_pattern = re.compile(r'[\d,]+ 条结果</span>')

    f = urllib.urlopen('http://cn.bing.com/search?q="%s"&qs=bs&form=QBLH'%(query))
    response_str = f.read()
    match = cnt_pattern.search(response_str)

    cnt = int("".join(match.group().split()[0].split(","))) if match else 0
    #time.sleep(3)
    return cnt
def getSearchCount() :
    outputFile = codecs.open('../data/BingSearchCount', "w", "utf-8")
    outputFile.write('word1\tword2\tcnt1\tcnt2\tcnt12\n')
    Data = getWordPairs()
    for data in Data :
        cnt_word1 = BingSearch(data[0])
        cnt_word2 = BingSearch(data[1])
        cnt_word12 = BingSearch(data[0], data[1])
        outputFile.write('%s\t%s\t%d\t%d\t%d\n'%(data[0], data[1], cnt_word1, cnt_word2, cnt_word12))
    outputFile.flush()
    outputFile.close()

getSearchCount()




 