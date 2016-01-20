#coding:utf-8

import requests
import re
import os
import urllib
import time
import base64
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf8')

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Host' : 'www.u17.com',
    'DNT' : '1'
}

def getPageTree(targeturl):

    response = requests.get(targeturl, headers = headers)
    page = response.content
    #将html变为树状图结构
    tree = etree.HTML(page)
    return tree


def analyze_manga(targeturl):

    tree = getPageTree(targeturl)
    #chapter url
    chapterurl = tree.xpath('//*[@id="chapter"]/li/a/@href')
    
    #chapter title
    chaptertitle = tree.xpath('//*[@id="chapter"]/li/a/@title')
    #print chapterurl, picnum, chaptertitle
    items = zip(chapterurl, chaptertitle)
    return items

def analyze_chapter():
    #此处输入你想要爬取的微漫画地址
    itemss = analyze_manga('http://www.u17.com/comic/3166.html')
    items = itemss[6:11]
    print len(items)
    for i in xrange(len(items)):
        #items[i][0]:url, items[i][1]:title
        pages = []
        response = requests.get(items[i][0], headers = headers)
        p = response.content
        titles = items[i][1].replace('！', '')
        titles = titles.replace(' ', '')
        titles = delextra(titles)
        #获取所有的漫画url
        images = re.findall('"src":"(.*?)"', p)
        images = [unicode(base64.b64decode(i)) for i in images]
        for url in images:
            #对漫画url进行处理，获取到真正的漫画链接
            pages.append(url)
        #print titles, type(titles)
        mkdir(titles)
        print len(pages), titles
        for y in xrange(len(pages)):
            saveImg(pages[y], titles, y)
            time.sleep(0.5)


def delextra(picnum):
    pattern = re.compile(r'\:|\\', re.I|re.M|re.S)
    pic = pattern.sub('', picnum)
    return pic  

#传入图片地址，文件名，保存单张图片
def saveImg(imageURL,name, number):
    num = '%03d'%number
    print num
    fileNames = "d:/queue" + "/" +name + "/" + str(num) + ".jpg"
    #u = urllib.urlopen(imageURL)
    #data = u.read()
    u = requests.get(imageURL)
    data = u.content
    f = open(fileNames, 'wb')
    f.write(data)
    f.close()
 
#创建新目录
def mkdir(path):
    path = path.strip()
    path = os.path.join('d:/queue',path)
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
