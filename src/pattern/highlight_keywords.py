#!/usr/bin/env python
#coding=utf-8

'''
created on 2018/03/20
@author fangdenghui
功能: 基于倒排的关键字匹配，匹配效率大致为O（m+n）（空间换时间，m为文本长度，n为关键字最大长度，和关键字个数无关）
参考: 本代码严格参考http://blog.csdn.net/sinat_22013331/article/details/51613394
'''


def read_keywords(filepath):
    '''
    Desc 从文件读取关键字，每个关键字单独一行

    Args:
        filepath 文件路径

    Returns:
        keywords 关键字
    '''
    keywords = list()

    fr = open(filepath)

    for line in fr.readlines():
        keywords.append(line.strip())
    fr.close()
    return keywords

class KeywordDict(object):
    '''
    Desc 根据关键字创建倒排词典，主要包括三种存储类型
    '''

    def __init__(self):
        # 关键词最大长度
        self.MAX_WORD_LENGTH = 15
        self.MAX_CHAR_VALUE = 256

        # 倒排存放每个字节关键词集合
        self.words = [set()] * self.MAX_CHAR_VALUE #ascii码最大值作为list大小

        # 关键字最大和最小长度
        self.maxStoreWordLength = 0
        self.minStoreWordLength = 9999

        # 倒排存放每个字节对应关键字位置集合
        self.fastPositionCheck = [0] * self.MAX_CHAR_VALUE

        # 倒排存放每个首字节对应关键字长度
        self.fastLengthCheck = [0] * self.MAX_CHAR_VALUE

    def add_keyword(self, word):
        '''
        Desc 添加关键词

        Args:
            word 关键词
        '''

        # 将字符串转化为ascii序列
        ascii_word = map(ord, word)

        self.maxStoreWordLength = max(self.maxStoreWordLength, len(ascii_word))
        self.minStoreWordLength = min(self.minStoreWordLength, len(ascii_word))

        # 记录以每个字节开始的对应关键字位置
        for i in range(len(ascii_word)):
            self.fastPositionCheck[ascii_word[i]] |= (1<<i)

        # 添加入长度记录列表中，倒排
        self.fastLengthCheck[ascii_word[0]] |= (1<<(len(ascii_word)-1))

        # 添加入词典倒排集合中
        if word not in self.words[ascii_word[0]]:
            self.words[ascii_word[0]].add(word)

class KeywordManager(object):
    '''
    Desc 关键词管理器，包含添加关键词词典，匹配文本
    '''

    def __init__(self, keywords_dict):
        '''
        Desc 初始化，将关键词词典加入

        Args:
            keywords_dict关键词词典实例
        '''
        self.keywords_dict = keywords_dict

    def add_keywords_by_file(self, filepath):
        '''
        Desc 从文件读取关键字，添加到库中
        '''

        keywords = read_keywords(filepath)
        for keyword in keywords:
            #print keyword
            self.keywords_dict.add_keyword(keyword)

    def text_pattern(self, text):
        '''
        Desc 模式匹配文本text

        Args:
            text 要匹配的文本

        Returns:
            keywords 匹配到的关键词
        '''

        keywords = list()
        ascii_text = map(ord, text)

        index=0
        while index < len(ascii_text):
            # 首先判断当前字符是否是某关键字的第一个字符，不是就继续遍历
            while index<len(ascii_text) and (self.keywords_dict.fastPositionCheck[ascii_text[index]] & 1) == 0:
                index += 1

            if index>=len(ascii_text):
                break

            # 此时判断，当前字符会出现在关键词的第一位上
            begin = ascii_text[index]
            jump = 1
            h = min(self.keywords_dict.maxStoreWordLength, len(ascii_text) - index)
            for j in range(h):
                current = ascii_text[index+j]

                # 判断当前字符是否出现关键字的对应位上，实现快速判断
                if (self.keywords_dict.fastPositionCheck[current] & (1<<min(j, self.keywords_dict.maxStoreWordLength))) == 0:
                    break

                # 当前判决的长度大于关键字的最小长度时，当前的截取字符串可能就是关键字，做详细判定
                if j+1 >= self.keywords_dict.minStoreWordLength:

                    # 存在起始begin且长度为j的关键字，可能是
                    if (self.keywords_dict.fastLengthCheck[begin] & (1<<min(j, self.keywords_dict.maxStoreWordLength))) >0 :
                        sub = text[index:index+j+1]

                        if sub in self.keywords_dict.words[begin]:
                            jump = len(sub)
                            keywords.append(sub)

            index += jump
        return keywords

if __name__ == '__main__':
    keyword_dict = KeywordDict()
    keyword_manager = KeywordManager(keyword_dict)
    keyword_manager.add_keywords_by_file('../crawler/starname.txt')

    import time
    start = time.time()
    res = keyword_manager.text_pattern(' 韩雨芹 刘亦菲 周星驰 刘德华Jessie J 曹高波 徐黄丽 关晓彤  苏诗丁  倪妮 柳岩 姚明 杨洋 成龙 李易峰  李小璐 吴亦凡  王源 张国荣 张歆艺 佟丽娅 张翰，何炅太你好，哼爱心，王家卫时是不是亚')
    end = time.time()
    print end-start
    for i in res:
        print i
