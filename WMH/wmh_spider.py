#coding:utf-8

import requests
import re
import os
import urllib
import time
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf8')

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Host' : 'manhua.weibo.com',
    'DNT' : '1'
}

def getPageTree(targeturl):

    response = requests.post(targeturl, headers = headers)
    page = response.content
    #将html变为树状图结构
    tree = etree.HTML(page)
    return tree


def analyze_manga(targeturl):

    tree = getPageTree(targeturl)
    #chapter url
    chapterurl = tree.xpath("/html/body/div[3]/div[2]/div[3]/div/div/a/@href")
    #pic num
    picnum = tree.xpath("/html/body/div[3]/div[2]/div[3]/div/div/a/span/text()")
    #chapter title
    chaptertitle = tree.xpath("/html/body/div[3]/div[2]/div[3]/div/div/a/text()")
    #print chapterurl, picnum, chaptertitle
    items = zip(chapterurl, chaptertitle)

    return items

def analyze_chapter():
    #此处输入你想要爬取的微漫画地址
    items = analyze_manga('http://manhua.weibo.com/c/34381')
    print len(items)
    for i in xrange(len(items)):
        #items[i][0]:url, items[i][1]:title
        pages = []
        tree = getPageTree(items[i][0])
        pic = tree.xpath("/html/head/script[2]/text()")
        title = items[i][1]
        titles = delextra(title)
        p = str(pic[0])
        #获取所有的漫画url
        b = re.findall(r'\"imgUrl\"\:\"(.*?)\"\,\"\D', p)
        for x in range(len(b)):
            #对漫画url进行处理，获取到真正的漫画链接
            b[x] = b[x].replace('.jpg', '_big.jpg')
            b[x] = b[x].replace('\\', '')
            pages.append(b[x])
        mkdir(titles)
        print len(pages)
        for y in xrange(len(pages)):
            saveImg(pages[y], titles, y)
            time.sleep(0.5)


def delextra(picnum):
    pattern = re.compile(r'\:|\/', re.I|re.M|re.S)
    pic = pattern.sub('', picnum)
    return pic  

#传入图片地址，文件名，保存单张图片
def saveImg(imageURL,name, number):
    fileNames = "d:/vimpire" + "/" +name + "/" + str(number) + ".jpg"
    u = urllib.urlopen(imageURL)
    data = u.read()
    f = open(fileNames, 'wb')
    f.write(data)
    f.close()
 
#创建新目录
def mkdir(path):
    path = path.strip()
    path = os.path.join('d:/vimpire',path)
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

if __name__ == "__main__":
    analyze_chapter()
