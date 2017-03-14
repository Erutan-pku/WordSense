#coding=utf-8
#-*- coding: UTF-8 -*- 
import sys
import nltk
import random
random.seed(1337)
import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic, genesis
from dataAnalysis import getWordPairs, evalueSpearman
#nltk.download()

# http://www.nltk.org/howto/wordnet.html
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
genesis_ic = wn.ic(genesis, False, 0.0)

global average
sum_None = lambda xs : sum([(x if not x is None else 0) for x in xs])
len_None = lambda xs : sum([(1 if not x is None else 0) for x in xs])
average = lambda x : sum_None(x)/len_None(x)

global topN
def topN(xs, n=3) :
    newList = []
    for x in xs :
        if not x is None :
            newList.append(x)
    newList = sorted(newList, reverse=True)
    print newList
    sum_score = 0
    for i in range(min(n, len(newList))) :
        sum_score += newList[i]
    return sum_score / n

# 1/path
#0.292690091424     0.311689149344      0.242355433886
#simFunction = wn.path_similarity
# Leacock-Chodorow Similarity:  -log(p/2d) where p is the shortest path length and d the taxonomy depth.
# 不同词性的直接认为值为0
#0.303463230095     0.33365080482       0.243127578189
#simFunction = lambda x,y : wn.lch_similarity(x, y) if x.pos()==y.pos() else 0
# based on the depth of the two senses in the taxonomy and that of their Least Common Subsumer 
#0.331197865969     0.35898821251       0.258938723468
#simFunction = wn.wup_similarity

# -log P(LCS(c1,c2))
#0.332605157422     0.378351460201      0.237095177379
#simFunction = lambda x,y : wn.res_similarity(x,y,brown_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
#0.333519003413     0.382270850924      0.237229430736
#simFunction = lambda x,y : wn.res_similarity(x,y,semcor_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
#0.327047195075     0.378426849209      0.226561164029
simFunction = lambda x,y : wn.res_similarity(x,y,genesis_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
 
# 1/(IC(s1) + IC(s2) - 2 * IC(lcs))
#0.283453351637     0.364845938375      0.158729843246
#simFunction = lambda x,y : wn.jcn_similarity(x,y,brown_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
#0.17733734237      0.272078927265      0.0570884272107
#simFunction = lambda x,y : wn.jcn_similarity(x,y,semcor_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
#0.131891595045     0.215981129294      0.0797506187655
#simFunction = lambda x,y : wn.jcn_similarity(x,y,genesis_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0

# 2 * IC(lcs) / (IC(s1) + IC(s2))
#0.299336498295     0.360000100519      0.197707567689
#simFunction = lambda x,y : wn.lin_similarity(x,y,brown_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
#0.216159121464     0.273284313725      0.12954361359
#simFunction = lambda x,y : wn.lin_similarity(x,y,semcor_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0
#0.197001229283     0.243409325453      0.159964749119
#simFunction = lambda x,y : wn.lin_similarity(x,y,genesis_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0

def getWordNetSim(Data, simFunction=simFunction, dataSet='All', covert=average) :
    assert dataSet in ['All', 'set1', 'set2']
    scores = []
    for data in Data:
        synset1 = wn.synsets(data[0])
        synset2 = wn.synsets(data[1])
        maxScore = covert([simFunction(x,y) for x in synset1 for y in synset2]+[0])
        maxScore = min(maxScore, 5.2)
        scores.append(maxScore)
    
    if dataSet=='All' :
        return scores
    elif dataSet == 'set1' :
        return scores[:153]
    elif dataSet == 'set2' :
        return scores[153:]

def main(simFunction) :
    Data = getWordPairs()
    setAll = getWordNetSim(Data, simFunction)
    scores = (evalueSpearman(setAll), evalueSpearman(setAll[:153],dataSet='set1'), evalueSpearman(setAll[153:],dataSet='set2'))
    print '%f\t\t%f\t\t%f'%scores

if __name__ == '__main__':
    main(wn.path_similarity)
    main(lambda x,y : wn.lch_similarity(x, y) if x.pos()==y.pos() else 0)
    main(wn.wup_similarity)

    wn_Infor = [wn.rl_similarity, wn.jcn_similarity, wn.lin_similarity]
    ic_Infor = [brown_ic, semcor_ic, genesis_ic]
    [main(lambda x,y:t1(x,y,t2)if x.pos()==y.pos()and not x.pos()in['a','s']else 0)for t1 in wn_Infor for t2 in ic_Infor]
#main(simFunction)


# supervised used:
wup_max = lambda data : getWordNetSim(data, simFunction=wn.wup_similarity, covert=max)
res_ave_genesis = lambda data : getWordNetSim(data, simFunction=lambda x,y : wn.res_similarity(x,y,genesis_ic)if x.pos()==y.pos() and not x.pos()in['a','s'] else 0, covert=average)
"""
max :
0.292690        0.311689        0.242355
0.303463        0.333651        0.243128
0.331198        0.358988        0.258939
0.332605        0.378351        0.237095
0.333519        0.382271        0.237229    semcor_ic
0.327047        0.378427        0.226561
0.283453        0.364846        0.158730    brown_ic
0.177337        0.272079        0.057088
0.131892        0.215981        0.079751
0.299336        0.360000        0.197708    brown_ic
0.216159        0.273284        0.129544
0.197001        0.243409        0.159965

average:
0.244259        0.237357        0.219978
0.173875        0.284668        0.076100
0.296517        0.307310        0.243068
0.361846        0.385245        0.293645
0.361034        0.399594        0.275554
0.373279        0.417581        0.284367     ***. genesis_ic
0.292642        0.443521        0.121428    brown_ic
0.176178        0.329483        0.003367
0.105656        0.202480        0.036422
0.328972        0.367325        0.253186    brown_ic
0.224770        0.261762        0.153170
0.201050        0.262023        0.161262

topN n=3
0.208569        0.208334        0.202608
0.138327        0.146694        0.136479
0.174386        0.169201        0.157879
0.280307        0.312543        0.203300
0.278864        0.314704        0.197069
0.268741        0.336484        0.168242
0.227641        0.328316        0.109784
0.136733        0.250245        0.009784
0.088984        0.178617        0.031574
0.240359        0.289037        0.149580
0.172097        0.246265        0.083449
0.162308        0.222622        0.113164


##########  seed = 1337
random_max
0.292690        0.311689        0.242355
0.303450        0.333651        0.243128
0.331198        0.358988        0.258939
0.332091        0.374636        0.238705
0.333690        0.379646        0.239383
0.326478        0.375122        0.227757
0.283036        0.363748        0.158719
0.172369        0.263407        0.054691
0.095196        0.158580        0.063092
0.296426        0.351964        0.197381
0.202845        0.246633        0.125397
0.131644        0.138511        0.134595

random_average
0.244259        0.237357        0.219978
0.173673        0.284411        0.076211
0.296517        0.307310        0.243068
0.361510        0.381122        0.296090
0.361251        0.396155        0.277749
0.372949        0.417269        0.283870
0.292629        0.440970        0.121784
0.162716        0.308785        -0.003912
0.067276        0.145863        0.019710
0.327334        0.359859        0.256199
0.212778        0.233976        0.152313
0.115076        0.133561        0.112015
"""
