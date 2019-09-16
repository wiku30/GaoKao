#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import time
import random
import sys
from lxml import etree
import z1
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D)'}
tencenthead="http://v.qq.com/x/varietylist/?itype=-1&offset=0&isource=-1&iarea=-1&sort=5"
filehead="/search/odin/zhaozshuo/data/"
urltag=["04","07","10","13","00"]
filetag=["qinggan","yishu","tuokouxiu","zhenrenxiu","fangtan"]
pageno=[7,8,9,26,6]
urltail1="_p3_p4_p5_p6_p73_p8_p9_2d1_p10"
urltail2="_p110_p12_p131.html"
#name pic -- url des tag
urllist = {}
#first page url
dict_areaid={"浙江":"iarea=5","江苏":"iarea=3","东方":"iarea=4","湖南":"iarea=2","北京":"iarea=12","安徽":"iarea=9","深圳":"iarea=11","天津":"iarea=6","台湾":"iarea=7","韩国":"iarea=75","欧美":"iarea=73"}
#domestic
domestic=["浙江","江苏","东方","湖南","北京","安徽","深圳","天津"]
taiwan=["台湾"]
foreign=["韩国","欧美"]
def replace(x):
        replaceBR=re.compile('\s+')
        x=re.sub(replaceBR,"",x)
        return x.strip()
def spider(url):
	t=1+random.randint(0,10)
        req=urllib2.Request(url)
        event=urllib2.urlopen(req)
        str0=event.read()
        search(str0)
	time.sleep(t)
def spiderPage(url):
        req2=urllib2.Request(url)
        event2=urllib2.urlopen(req2)
        str0=event2.read()
        return str0
def spiderPage1(url):
        req3=urllib2.Request(url)
        event3 = urllib2.urlopen(req3)
        str0 = event3.read()
        return str0
def GetRequest(url, headers = {}):
	response = None
	try:
		if len(headers) > 0:
			response = requests.get(url, headers = headers)
		else:
			response = requests.get(url)
		if response and response.status_code == 200:
			return response.text
	except:
		return ''
	return ''

def getdestag(url):
    print "Enter des\n"
    str1 = spiderPage1(url)
    #print str1
    regex = re.compile(r'<div class="album_intro">.*?<span class="label">简介：</span>(.*?)</div>',re.S)
    des = ""
    tag = ""
    if regex.search(str1):
         print "des match\n"
         des = regex.search(str1).group(1).strip()
         print "des:%s" % des
    #regex1 = re.compile(r'<div class="video_tags">.*?<a _stat.*?>(.*?)</a>',re.S)
    regex1 = re.compile(r'<div class="video_tags">(.*?)</div>',re.S)
    if regex1.search(str1):
         tagstr = regex1.search(str1).group(1).strip()
         regex2 = re.compile(r'<a _stat.*?>(.*?)</a>',re.S)
         ll = list(regex2.finditer(tagstr))
         tagline = ""
         for i in xrange(len(ll)):
             tag = ll[i].group(1).strip()
             if i == 0:
                tagline = tag
             else:
                tagline = tagline +"|"+tag
         print "tag:%s" % tagline
    return des+"\t"+tag
def fetchlatestTvshow(url,fo,region):
    str0 = spiderPage(url)
    print "Enter latest\n"
    urlhead="http://v.qq.com/x/cover/"
    regex = re.compile(r'<ul class="figures_list">(.*?)</ul>',re.S)
    if regex.search(str0):
        #print str0
        print "match"
        ulstr = regex.search(str0).group(1).strip()
        #print "ulstr:%s" % ulstr
        regex1 = re.compile(r'<li class="list_item.*?data-trigger-class="list_item_hover">(.*?)</li>',re.S)
        ll = list(regex1.finditer(ulstr))
        print "ll len:%d" % len(ll)
        for i in xrange(len(ll)):
            listr = ll[i].group(1).strip()
            #print "listr:%s" % listr
            regex2 = re.compile(r'<a.*?_boss="film".*?href="(.*?)".*?target="_blank".*?class="figure".*?tabindex="-1".*?>.*?<img.*?src="(.*?)".*?alt="(.*?)".*?>',re.S)
            url = ""
            pic = ""
            name = ""
            des = ""
            tag = ""
            if regex2.search(listr):
                url = regex2.search(listr).group(1).strip()
                pic = regex2.search(listr).group(2).strip()
                name = regex2.search(listr).group(3).strip()
                urlarr = url.split("/")
                url = urlhead + urlarr[5]
                print "url:%s" % url
                destag = getdestag(url)
                destagarr = destag.split('\t')
                des = destagarr[0]
                tag = destagarr[1]
                if tag == "":
                   tag = "最新"
                else:
                   tag = tag + "|" + "最新"
                #print "name:%s,pic:%s,,url:%s,des:%s" % (name,pic,url,des)
                line = name +"\t"+pic+"\t"+region+"\t"+tag+"\t"+des
                fo.write(line+"\n")
                #str1 = z1.fetchPage(url) 
                #print "str1:%s" % str1
def fetchdestag():
    print "enter fetchdes\n"
    for key in urllist:
        url = urllist[key]
        str1 = z1.fetchPage("http://v.qq.com/x/cover/tle3vwzho4pvcu1.html")
        print "str1:%s" % str1            

def search(str0):
	html=etree.HTML(str0)
	lis=html.xpath('//ul[@class="st-list cfix"]/li')
	for i in range(0,len(lis)):

		title=lis[i].xpath('.//strong/a/@title')
                if(title):
                        t="".join(title).encode('utf-8')
                        fo.write(t+"\t")
                else:
                        fo.write("\t")

		pic=lis[i].xpath('.//div[@class="st-pic"]/a/img/@src')
                if(pic):
                        p="".join(pic)
                        fo.write(p+"\t")
                else:
                        fo.write("\t")
		
		years=lis[i].xpath('.//p[@class="col3a lh-area"]/a')
		if(years):
                        year=""
                        for j1 in range(0,len(years)-1):
                                year+=years[j1].text
                                year+="\001"
                        year+=years[len(years)-1].text
                        fo.write(year.encode('utf-8')+"\t")
                else:
                        fo.write("\t")

		tags=lis[i].xpath('.//p[@class="lh-type"]/a')
		if(tags):
                        tag=""
                        for j2 in range(0,len(tags)-1):
                                tag+=tags[j2].text
                                tag+="\001"
                        tag+=tags[len(tags)-1].text
                        fo.write(tag.encode('utf-8')+"\t")
                else:
                        fo.write("\t")

		stars=lis[i].xpath('.//p[@class="lh-zy"]/a')
		if(stars):
                        star=""
                        for j3 in range(0,len(stars)-1):
                                star+=stars[j3].text
                                star+="\001"
                        star+=stars[len(stars)-1].text
                        fo.write(star.encode('utf-8')+"\t")
                else:
                        fo.write("\t")
		summary=lis[i].xpath('.//p[@class="lh-info"]/text()')
                if(summary):
                        s="".join(summary)
                        s2=replace(s)
                        fo.write(s2.encode('utf-8')+"\n")
                else:
                        fo.write("\n")


def fetchallTvshow():
    file="/search/odin/yangt/data/tvshow/latestTencent"
    fo=open(file,"w")
    for key in dict_areaid:
        region = ""
        if key in domestic:
            region = "内地" + "|" + key
        elif key in taiwan:
            region = "台湾"
        elif key in foreign:
            region = key
        index = 0
        while (index < 5):
            url = "http://v.qq.com/x/varietylist/?itype=-1&offset="+str(index*20)+"&isource=-1&"+dict_areaid[key]+"&sort=5" 
            fetchlatestTvshow(url,fo,region)
    fo.close()

fetchallTvshow()

