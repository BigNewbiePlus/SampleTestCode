#!/usr/bin/env python
#coding:utf-8

'''
created on 2018/03/22
@author fangdenghui
功能: 爬取网站http://star.yule.com.cn/sports/pn_1/上所有明星姓名
方法: 使用selenium加载网页，分别为pn_1,pn_2, ..., pn_9
      爬取<div id="SearchResult" class="TArea mt10 switch-class"> 下的<a><img alt='张继科'/></a>
      从alt中获取姓名
注意: 1>为了加快检索速度，使用js脚本执行遍历
      2>使用正常chrome爬取，非页面chrome未设置
'''

from selenium import webdriver


def extract_ssnames_by_js(driver, url):
    '''
    Desc 基于js从URL中抽取运动明星姓名

    Args:
        driver 驱动
        url 网页链接

    Returns:
        page_ssnames 单网页运动明星姓名集合
    '''

    page_ssnames = list()

    # 打开网页
    driver.get(url)

    js = """

    var parent = document;
    var div = parent.getElementById('SearchResult');
    var imgs = div.getElementsByTagName('img');

    result= new Array(imgs.length);
    for(var i=0;i<imgs.length;i++){
        result[i] = imgs[i].alt;
    }
    return result;
    """
    page_ssnames = driver.execute_script(js)
    return page_ssnames

def craw_ssname():
    '''
    Desc 爬取网页http://star.yule.com.cn/sports/pn_1/上的所有明星

    Returns:
        ss_names 爬取的所有明星姓名(ss=sport star)
    '''

    ss_names = list()

    driver = webdriver.Chrome('./chromedriver') # 加载驱动

    for i in range(9):
        url = 'http://star.yule.com.cn/sports/pn_'+str(i+1)+'/'
        page_names = extract_ssnames_by_js(driver, url)
        ss_names.extend(page_names)
    print 'craw over!'
    driver.close()
    return ss_names

def savelisttofile(filename, names):
    '''
    Desc 保存列表到文件中

    Args:
        filename 文件路径
        names 姓名列表
    '''

    fw = open(filename, 'w')

    for name in names:
        fw.write(name.encode('utf8')+'\n')

    fw.close()

if __name__ == '__main__':
    filename = 'sstarname.txt'
    names = craw_ssname()
    savelisttofile(filename, names)



