#coding:utf-8

from pyspark import  SparkContext
myDat=[ [ 1, 3, 4,5 ], [ 2, 3, 5 ], [ 1, 2, 3,4, 5 ], [ 2,3,4, 5 ] ]
sc = SparkContext( 'local', 'pyspark')
myDat=sc.parallelize(myDat) #得到输入数据RDD #myDat.collect(): [[1, 3, 4, 5], [2, 3, 5], [1, 2, 3, 4, 5], [2, 3, 4, 5]]
C1=myDat.flatMap(lambda x: set(x)).distinct().collect() #distinct()是去重操作，对应C1=createC1(myDat) #得到1项集 #[1, 2, 3, 4, 5],
C1=[frozenset([var]) for var in C1] #需要这样做，因为python的代码里需要处理集合操作
D=myDat.map(lambda x: set(x)).collect() #将输入数据RDD转化为set的列表 #[{1, 3, 4, 5}, {2, 3, 5}, {1, 2, 3, 4, 5}, {2, 3, 4, 5}]
D_bc=sc.broadcast(D)
length=len(myDat.collect())
suppData=sc.parallelize(C1).map(lambda x: (x,len([var for var in D_bc.value if x.issubset(var)])/length) if len([var for var in D_bc.value \
            if x.issubset(var)])/length >=0.75 else ()).collect()


print 'suppData:', suppData
