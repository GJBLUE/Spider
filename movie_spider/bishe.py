# encoding=utf-8
import urllib
import urllib2
import re,HTMLParser
import tool,urlfilter,douban
#import douban
from lxml import etree
import os
import sys,random,time
import MySQLdb
import threading, Queue, time
#import gevent
#from gevent import monkey

#monkey.patch_all()


reload(sys)
sys.setdefaultencoding('utf-8')
_queue=Queue.Queue()           #构造一个不限制大小的的队列
#_THREAD_NUM=3                        #设置线程的个数


import StringIO
_olderr = sys.stderr
serr = StringIO.StringIO()
sys.stderr = serr


USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

#headers = {'User-Agent':random.choice(USER_AGENTS)}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36','Referer':'http://movie.douban.com/top250'}

#PHP use
ids=int(sys.argv[1])
#ids=2

class WorkerThread(threading.Thread):

    def __init__(self,func):
        #调用父类的构造函数
        super(WorkerThread,self).__init__()  
        #传入线程函数逻辑
        self.func=func

    def run(self):
        self.func()
               

class ThreadPool(object):
    
    def __init__(self, min=4, max=-1):
          
        self.min = min  
        self.max = max 
       
        self._threads = []

        self.get = _queue.get
    
    #@profile
    def start(self):
        """Start the pool of threads."""
        spider=Spider()
        #向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
        if ids==1:
            douban_url=spider.geturl()
            for index in xrange(4):
            #_queue.put(firsturl.format(page=index*25)
                _queue.put(douban_url.format(page=index*25))
        elif ids==2 or ids==3:
            for num in spider.geturl():
                _queue.put(num)
        for i in range(self.min): 
            #thread=WorkerThread(db.savePageInfo)
            thread=WorkerThread(spider.savePageInfo)
            thread.setName("CP Server " + thread.getName())
            self._threads.append(thread)
            # self.thread.setDaemon(True)
            #self._threads.setDaemon(True)
            thread.start()
        for worker in self._threads:
        #     worker.setName("CP Server " + worker.getName())
        #     worker.start()
            worker.join()
        print 'end'


    def put(self, obj):
        _queue.put(obj)
        if obj is _SHUTDOWNREQUEST:
            return
    

    def grow(self, amount):
        for i in range(amount):
            if self.max > 0 and len(self._threads) >= self.max:
                break
            thread=WorkerThread(spider.savePageInfo())
            thread.setName("CP Server " + thread.getName())
            self._threads.append(thread)
            thread.start()
            thread.join()

    

    def shrink(self, amount):
        for t in self._threads:
            if not t.isAlive():
                self._threads.remove(t)
                amount -= 1

        if amount > 0:
            for i in range(min(amount, len(self._threads) - self.min)):
                _queue.put(_SHUTDOWNREQUEST)
    
    def stop(self, timeout=2):

        for worker in self._threads:
            _queue.put(_SHUTDOWNREQUEST)
        

        current = threading.currentThread()
        if timeout and timeout >= 0:
            endtime = time.time() + timeout
        while self._threads:
            worker = self._threads.pop()
            if worker is not current and worker.isAlive():
                try:
                    if timeout is None or timeout < 0:
                        worker.join()
                    else:
                        remaining_time = endtime - time.time()
                        if remaining_time > 0:
                            worker.join(remaining_time)
                        if worker.isAlive():

                            c = worker.conn
                            if c and not c.rfile.closed:
                                try:
                                    c.socket.shutdown(socket.SHUT_RD)
                                except TypeError:

                                    c.socket.shutdown()
                            worker.join()
                except (AssertionError,

                        KeyboardInterrupt), exc1:
                    pass

class noneException(Exception):
    pass

class Spider:
    
    def __init__(self):
        self.tool=tool.Tool()
        conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="douban",charset="utf8")
        cur = conn.cursor()
        sql='select * from rule where id=%s'
        cur.execute(sql,ids)
        self.data = cur.fetchone()
        conn.commit()
        conn.close()

    #获取页面内容
    def getpage(self,url):
        request=urllib2.Request(url,headers=headers)
            #request.get_method = lambda: 'POST'
        response=urllib2.urlopen(request)
        return response.read()

    def geturl(self):
        #获取起始ＵＲＬ
        page=self.getpage(self.data[1])
        #print self.data[1]
        tree=etree.HTML(page)
        #得到全部ＵＲL
        urlnum=tree.xpath(self.data[2])
        l=[]
        l.append(self.data[1])
        if ids==1:
            return self.data[1]
        elif ids==2 or ids==3:
            l.extend(urlnum)
            l=list(sorted(set(l)))
            return l

    def getPage(self):
        #print _queue.qsize()
        if _queue.qsize() != 0:
            url = _queue.get()
            print url
            #time.sleep(5)
            request=urllib2.Request(url,headers=headers)
            #request.get_method = lambda: 'POST'
            response=urllib2.urlopen(request)
            return response.read()

    #获取缩影页面所有信息，list格式。
    def getContents(self):
        #page=self.sp.getPage()
        page=self.getPage()
        if  page is None:
            raise noneException()
        tree=etree.HTML(page)
            #item0 is no,item1is URL,item2 is src,item3 is moive name.
        if ids==1:
            #top
            item0=tree.xpath(self.data[3])
            #print item0
            #movieurl
            item1=tree.xpath(self.data[4])
            #photo
            item2=tree.xpath(self.data[5])
            #title
            item3=tree.xpath(self.data[6])
            #pinfen
            item4=tree.xpath(self.data[7])
            #num
            item5=tree.xpath(self.data[8])
            #brief
            item6=tree.xpath(self.data[9])

            items=zip(item0,item1,item2,item3,item4,item5,item6)
            return items
        elif ids==2 or ids==3:
            #top
            item0=tree.xpath(self.data[3])
            # print item0
            #movieurl
            item1=tree.xpath(self.data[4])
            #photo
            item2=tree.xpath(self.data[5])
            #title
            item3=tree.xpath(self.data[6])
            #pinfen
            item4=tree.xpath(self.data[7])
            # print '@'*10,it
            # item4=["".join(it[0]+it[1])]
            # print '#'*10,item4
            #num
            item5=tree.xpath(self.data[8])
            #brief
            item6=tree.xpath(self.data[9])
            
            items=zip(item0,item1,item2,item3,item4,item5,item6)
            #print '&'*20, [len(locals().get("item%s"%i)) for i in range(7)]
            #print items
            return items

    #获取详细信息，获取到item[1]
    def getDetailPage(self,infoURL):
        request=urllib2.Request(infoURL)
        try:
            response=urllib2.urlopen(request)
        except:
            return -1
        return response

    #获取电影简介
    def getBrief(self,page):
        #strs=str(self.data[7])
        #print self.data[7]
        pattern=re.compile(self.data[10],re.S)
        result=re.search(pattern,page)
        return self.tool.replace(result.group(1))

    #保存简介
    def saveBrief(self,content,name):
        fileName=self.data[11]+name+"/"+name+".txt"
        if isinstance(fileName, unicode):
            fileName = fileName.encode('utf-8')
        # print type(fileName)
        f=open(fileName,"w+")
           # print content
        f.write(content.encode('utf-8'))

    #传入图片地址，文件名，保存单张图片
    def saveImg(self,imageURL,fileName):
        u=urllib.urlopen(imageURL)
        data=u.read()
        # print fileName
        fileName=self.data[11]+fileName
        if isinstance(fileName, unicode):
            fileName = fileName.encode('utf-8')
        f=open(fileName,'wb')
        f.write(data)                
        f.close()

    #保存头像
    def saveIcon(self,iconURL,name):
        splitPath=iconURL.split('.')
        fTail=splitPath.pop()
        fileName=name+"/icon."+fTail
        self.saveImg(iconURL,fileName)

    def mkdir(self,path):
        # 去除首位空格
        path = path.strip()
        #print path
            # 判断路径是否存在
            # 存在     True
            # 不存在   False
        path=os.path.join(self.data[11],path)
        if isinstance(path, unicode):
            path = path.encode('utf-8')
        isExists=os.path.exists(path)
            # 判断结果mkdir
        if not isExists:
             # 如果不存在则创建目录
             # 创建目录操作函数
            os.makedirs(path, mode=0777)
            return True
        else:
                # 如果目录
                #存在则不创建，并提示目录已存在
            return False

    def savePageInfo(self):
        while True:
            #获取第一页排行信息
            fenxi=self.getContents()
            # print fenxi
            if fenxi:
                #print fenxi
                for item in fenxi:
                    #top,movieurl,photo,title,pinfen,num,brief
                    #电影详细页面URL
                    #print '!'*10,item[4]
                    urlfilter.format(item[1])
                    detailURL=item[1]
                        #得到电影详细页面的代码
                    dp=self.getDetailPage(detailURL)
                    if  dp != -1:
                        detailPage=dp.read()
                            #获得电影简介
                        brief=self.getBrief(detailPage)
                        #removeExtraTag=re.compile('[^\d]')
                        #it=re.sub(removeExtraTag,"",item[0])
                        title="top_"+item[0]+item[3]
                        print title
                        try:
                            self.mkdir(title)
                        except Exception,e:
                            print e
                        print serr.getvalue()
                            #保存图片
                            #self.saveImgs(images,title)
                            #保存个人简介
                        self.saveBrief(brief,title)
                            #保存头像
                        print serr.getvalue()
                        self.saveIcon(item[2],title)
                        print serr.getvalue()
                            #print "m:"+num1+"p:"+num2 
            self.dbcon(fenxi)           

    def dbcon(self, contents):
        # import pdb
        # pdb.set_trace()
        conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="douban",charset="utf8")
        cur = conn.cursor() 
        # cur.execute("SELECT VERSION()")
        # data = cur.fetchone()
        # print "Database version : %s " % data       
        try:
            # contents=self.getContents()
            # print contents
            for item in contents:
                #item0 is url,item1pis name,item2 is moive number. 
                value=[item[0], item[1],item[2],item[3],item[4],item[5],item[6]]
                if ids==1:
                    sql = 'INSERT INTO dmovie(top,moive,photo,title,pinfen,num,brief) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                elif ids==2:
                    sql = 'INSERT INTO tmovie(top,moive,photo,title,pinfen,num,brief) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                elif ids==3:
                    sql = 'INSERT INTO china(top,moive,photo,title,pinfen,num,brief) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                try:
                    # 执行sql语句
                    cur.execute(sql,value)
                   # 提交到数据库执行
                    conn.commit()
                except Exception,e:
                   # Rollback in case there is any error
                    conn.rollback()
                    print e
        except noneException,e:
            #print e
            pass
        conn.close()

# if __name__=='__main__':
# spider=Spider()
#spider.dbcon()
#spider.savePageInfo()
#spider.geturl()
t = ThreadPool()
t.start()