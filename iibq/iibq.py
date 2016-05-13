#coding:utf-8

from setting import headers, pic_header, picPath, cookies
from lxml import etree

import requests
import time
import re
import os



def chapterList(url):
    """分别得到话、番外、单行本的列表"""

    page = getPage(url)
    tree = etree.HTML(page)
    
    curl = tree.xpath('//*[@id="subBookListAct"]/div/a/@href')
    cname =  tree.xpath('//*[@id="subBookListAct"]/div/a/text()')
    chapter = zip(curl, cname)

    ecurl = tree.xpath('//*[@id="subBookListPs"]/div/a/@href')
    ecname = tree.xpath('//*[@id="subBookListPs"]/div/a/text()')
    extra_chapter = zip(ecurl, ecname)

    ourl = tree.xpath('//*[@id="subBookListVol"]/div/a/@href')
    oname = tree.xpath('//*[@id="subBookListVol"]/div/a/text()')
    offprint = zip(ourl, oname)
    
    return chapter, extra_chapter, offprint


def chapterPic(url):
    """获取每一章节的图片，并下载"""
    chapter, extra_chapter, offprint = chapterList(url)
    #print offprint
    ourl, oname = offprint[-1]
    #print ourl, oname
    page = getPage(ourl)

    picList = resolveJS(page)
    print picList

    if savePic(oname, picList):
        print 'everything is ok'
    else:
        print 'please check error'


def getPage(url):
    """get web page"""

    #response = requests.get(url, headers=headers, cookies=cookies, timeout=5)
    response = requests.get(url, headers=headers, timeout=5)
    page =  response.content
    time.sleep(1)

    return page


def resolveJS(page):
    """解析相应的章节地址，详情见readme.md"""

    sFiles, sPath = re.findall(r'sFiles\=\"(.*?)\"\;var.sPath\=\"(.*?)\"', page)[0]


    x = sFiles[len(sFiles)-1:] # x = 'e'
    d = "abcdefghijklmnopqrstuvwxyz".index(x) + 1 # d = '5'
    e = sFiles[len(sFiles)-d-12:len(sFiles)-d-1] # e = 'documentabs'
    s = sFiles[:len(sFiles)-d-12]
    k = e[:len(e)-1] # k = 'documentab'
    f = e[-1]
    for i in range(len(k)):
        s =  s.replace(k[i], str(i))
    g = s.split(f)
    gif = ""
    for num in g:
        gif += chr(int(num))

    gifs = gif.split('|')

    picList = []
    for jpg in gifs:
        url = pic_header + sPath + jpg
        picList.append(url)

    return picList

def savePic(name, picList):
    """下载并保存图片"""

    cpath = picPath + name
    if os.path.isdir(cpath):
        pass
    else:
        os.mkdir(cpath)

    for pic in enumerate(picList):
        #ppath = cpath + '/%02d.JPG'%pic[0]
        ppath = cpath + '/' + pic[1].split('/')[-1]
        #print ppath
        page = getPage(pic[1])
        with open(ppath, 'wb') as f:
            f.write(page)



if __name__ == "__main__":
    chapterPic('http://www.iibq.com/comic/82012141146/')