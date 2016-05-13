>[http://www.iibq.com/](http://www.iibq.com/),这个漫画网站非常有意思，分段把漫画图片信息给出来，最后用js进行组装。

示例网站:http://www.iibq.com/comic/82012141146/viewcomic218792/#p=1&s=1
从爬虫抓取的html可以看到，只能抓取到一个http://comicui.jmmh.net/upfiles/comicpic/41146.jpg的图片链接，而保存下来的画质非常差。
但从chrome的开发者工具里可以看到，还存在一个http://comic.jmydm.com:8080/jmydm2/41146/218792/jmydm0001-68032.JPG的图片链接。
这个链接是动态返回的。
继续寻找，会发现在一个script标签中，存在一个名为sFiles的字符串，这个字符串由许多字母所组成，非常可疑。

再来看下需要的url:http://comic.jmydm.com:8080/jmydm2/41146/218792/jmydm0001-68032.JPG

查看Network可以发现，有一viewhtm.js里面对sFiles进行了处理。
处理应该就在这个里面了：src='"+ getSLUrl(cuD) + sPath + arrFiles[parseInt(sPD)-1] +"' onerror='cerrmsg()' onload='movePage(this);prvLoadNext("+ sPD +")'
src指向的就是高清无码大图地址，所以我们现在需要研究一下viewhtm.js。
sFiles=unsuan(sFiles)，unsuan这个方法对sFiles进行了处理，但整个js中并没有找到这个sFiles。
继续看，在最上面有一段内转义为十六进制的代码：window["\x65\x76\x61\x6c"](...)。推测，unsuan就在其中。
摆弄了半天，并不能将其很好的转义出来。后来发现，在console控制台直接输入unsuan,function就自动出现了。
将其转换成python的字符串处理方法，得到了图片url的部分地址。

最后，由于图片是二进制文件，所以保存需要"wb"。