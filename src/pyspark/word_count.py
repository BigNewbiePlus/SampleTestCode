#!/usr/bin/env python
# coding=utf-8

'''
created on 2018/3/19
@author fangdenghui
功能: 词频统计，主要练习spark中的API函数使用
'''
import findspark
findspark.init()

import sys
from pyspark import SparkContext
from operator import add
import re

def main():

    sc = SparkContext(appName="wordsCount")
    lines = sc.textFile('file:///data00/home/fangdenghui/SampleTestCode/data/words.txt')
    counts = lines.flatMap(lambda x:x.split(' '))\
                    .map(lambda x:(x, 1))\
                    .reduceByKey(add)

    cnts = counts.collect()
    print cnts

    sc.stop()

if __name__ == '__main__':
    main()


