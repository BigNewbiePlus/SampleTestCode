#!/usr/bin/env python
#coding:utf-8

'''
created on 2018/03/20
@author fangdenghui
功能: 爬取所有明星名字
思路: 1: 百度搜索“明星姓名大全”，网页第一项（本人使用Chrome浏览器）
      2: 检测网页代码源：因为展现是slider模型，点击切换不同页面观察加载数据情况，发现包含姓名只有一项(js文件)，明星图片多项(忽略)
      3: 只观察js文件，发现不同页面只有pn和rn两个变量值发生改变，通过多次切换吗，发现pn表示起始位置，rn表示返回数量(return number)
      4: 观察Header，请求给予GET，使用python的urllib即可发送请求
      5: 查看Response，为json文件结果，使用json库解析即可
'''

print(__doc__)

import urllib
import urllib2
import json
import sys


def craw_starname(filename):
    '''
    Desc 爬取明星姓名

    Args:
        filename 爬取后数据保存文件名
    '''

    # 爬取数据的起始和爬取量
    pn = 0 #爬取起始位置
    rn = 100 #爬取量
    rep_num = 0 # 获取数据重复为0个数（5次停止）

    names = list() #  存放爬取的明星姓名
    while rep_num <= 5:
        url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E5%A5%B3%E6%98%8E%E6%98%9F&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn="+str(pn)+"&rn="+str(rn)+"&cb=jQuery11020524022681936074_1521457071677&_=1521457071746"
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

        trun_res = res[len('jQuery11020524022681936074_1521457071677')+1:-1]
        res_dic = json.loads(trun_res)

        # 没有明星数据了
        if not res_dic['data'] or not res_dic['data'][0]:
            rep_num += 1
            print 'zero in ',pn
            print res_dic['data']
            continue
        else:
            rep_num = 0
        stars = res_dic['data'][0]['result']
        for star in stars:
            names.append(star['ename'].encode('utf8'))


        # pn下标递增
        pn += rn

        # 每爬取1000个姓名报告一次
        if pn%1000==0:
            print 'craw star name number:',pn
            sys.stdout.flush()

    # 保存
    fw = open(filename, 'w')
    for name in names:
        fw.write(name+'\n')
    fw.close()
def main():
    filename = 'starname.txt'
    craw_starname(filename)

if __name__ == '__main__':
    main()
