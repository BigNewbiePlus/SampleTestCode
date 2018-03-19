#!/usr/bin/python
# -*- coding: UTF-8 -*-
import findspark
findspark.init()
from pyspark import SparkContext,SparkConf
import os

# from pyspark.context import SparkContext
# from pyspark.conf import SparkConf

#from pyspark.sql import DataFrame,SQLContext

sc = SparkContext(conf=SparkConf().setAppName("The first example"))

dirPath = os.path.join('../../data', "files") # dirPath 也可以是hdfs上的文件

if not os.path.exists(dirPath):
    os.mkdir(dirPath)

with open(os.path.join(dirPath, "1.txt"), "w") as file1:
    file1.write("10")
with open(os.path.join(dirPath, "2.txt"), "w") as file2:
    file2.write("20")

dirPath = 'file:///data00/home/fangdenghui/SampleTestCode/data/files'
textFiles = sc.wholeTextFiles(dirPath)
# sorted(textFiles.collect())
print(type(textFiles)) # <class 'pyspark.rdd.RDD'>
print(textFiles.collect())
print(type(textFiles.collect())) # list
# [(u'.../1.txt', u'10'), (u'.../2.txt', u'20')]
print(len(textFiles.collect())) # 2
