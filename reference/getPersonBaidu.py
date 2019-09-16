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

cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urlhead="http://top.baidu.com/buzz?b="
filehead="/search/odin/zhaozshuo/data/person/"
urltag=["258&c=9&fr=topbuzz_b255_c9","618&c=9&fr=topbuzz_b258_c9","18&c=9&fr=topbuzz_b618_c9","17&c=9&fr=topbuzz_b18_c9","1395&c=9&fr=topbuzz_b17_c9","16&c=9&fr=topbuzz_b1395_c9","15&c=9&fr=topbuzz_b16_c9","1396&c=9&fr=topbuzz_b259_c9","260&c=9&fr=topbuzz_b1396_c9","454&c=9&fr=topbuzz_b260_c9","255&c=9&fr=topbuzz_b255_c9","3&c=9&fr=topbuzz_b255_c9","22&c=9&fr=topbuzz_b3_c9","493&c=9&fr=topbuzz_b22_c9","491&c=9&fr=topbuzz_b493_c9","261&c=9&fr=topbuzz_b491_c9","257&c=9&fr=topbuzz_b261_c9","259&c=9&fr=topbuzz_b15_c9","612&c=9&fr=topbuzz_b259_c9"]
filetag=["hot","ent","actress_female","actor_male","actor","singer_female","singer_male","singer","celebrity","host","athlete","beauty","handsome","singer_tvshow","star_Europe_America","finance","internet","history","public_welfare"]
urlperson="http://top.baidu.com/"

#fo=open(file,"w")

def replacebr(x):
	replaceBR=re.compile('</p><p>')
	x=re.sub(replaceBR,"",x)
	return x.strip()

def spider(url):
        req=urllib2.Request(url)
        event=urllib2.urlopen(req)
        str0=event.read()
        search(str0)

def search(str1):
	regex=re.compile(r'<a class="list-title" target="_blank" href=".*?" href_top=".*?">.*?</a>.*?<a href=".(.*?)" class="icon-search',re.S)
	for i in regex.finditer(str1):
		try:
			t=1+random.randint(0,10)
			urlp=urlperson+i.group(1).strip()
			#print urlp
			req2=urllib2.Request(urlp)
			event2=urllib2.urlopen(req2)
			str2=event2.read()
			search2(str2)
			time.sleep(t)
		except Exception, e:
                	#print >> sys.stderr, "exception:\t" + url
                	print >> sys.stderr, e
def search2(str2):
        html=etree.HTML(str2.decode('gb2312',"ignore"))
        name=html.xpath('//div[@class="top-title"]/h2')
        if(name):
                fo.write(name[0].text.encode('utf-8')+"\t")
        else:
                fo.write("\t")
        regex=re.compile(r'<img onload=.*? src="(.*?)" /></a>',re.S)
        if(regex.search(str2)):
                fo.write(regex.search(str2).group(1).strip()+"\t")
        else:
                fo.write("\t")
        summary=html.xpath('//p[@class="text"]')
        if(summary):
                fo.write(summary[0].text.encode('utf-8')+"\n")
        else:
                fo.write("\n")


for i in range(0,len(urltag)):
        url=urlhead+urltag[i]
	file=filehead+filetag[i]
        fo=open(file,"w")
	print url
	print file
	try:
		spider(url)
    	except Exception, e:
        	print >> sys.stderr, "exception:\t" + url
        	print >> sys.stderr, e
	fo.close()
