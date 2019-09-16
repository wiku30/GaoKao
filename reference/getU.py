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

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D)'}
tencenthead="http://v.qq.com/x/varietylist/?itype=-1&offset=0&isource=-1&iarea=-1&sort=5"
filehead="/search/odin/zhaozshuo/data/"

fo=file("res0","w")

def replace(x):
    replaceBR=re.compile('\s+')
    x=re.sub(replaceBR,"",x)
    return x.strip()
def spiderPage(url):
		req2=urllib2.Request(url)
		event2=urllib2.urlopen(req2)
		str0=event2.read()
		#time.sleep(0.05*(1+random.randint(0,10)))
		return str0

#####

def divide(str,label,func):
	pat=re.compile(r"<" + label + ".*?>(.*?)</"+ label +">",re.DOTALL)
	res=re.finditer(pat,str)

	for i in res:
		pat2=re.compile(".*<"+ label +".*?>",re.DOTALL)
		str2= i.group(1)
		str2=re.sub(pat2,"",str2)
		func(str2)



#####to do i

type=""
place=""
name=""

num_set=range(3500)

def proc(_str):
	global type
	global place
	global name
	global fo
	if(_str):
		year=re.search(r"<year>(.*?)</year>",_str).group(1)
		avg=re.search(r"<avgScore>(.*?)</avgScore>",_str).group(1)
		fo.write (name+" "+place+" "+year+" "+type+" "+avg+"\n")

def search(num):
	global fo
	global type
	global place
	global name
	
	if(num%200==0):
		fo.close()
		fo=file("res"+str(int(num/200)),"w")
	
	page = "http://gkcx.eol.cn/schoolhtm/schoolTemple/school" + str(num) + ".htm"
	xml_li = "http://gkcx.eol.cn/schoolhtm/scores/provinceScores" + str(num) +"_10003_10035_10036.xml"
	xml_wen = "http://gkcx.eol.cn/schoolhtm/scores/provinceScores" + str(num) +"_10003_10034_10036.xml"
	
	pgsrc=spiderPage(page)
	try:
		name=re.search("<h2 class=\"left\">(.*?)</h2>",pgsrc).group(1)  #first h2 is school name
		_place=re.search("<td width=\"55\" align=\"left\" class=\"gary\">(.*?)</td>",pgsrc,re.DOTALL).group(1)
	except AttributeError:
		return
	place=re.sub("\\s","",_place)

	type="理科"

	li_data = spiderPage(xml_li)
	divide(li_data,"score",proc)
	
	type="文科"
	wen_data=spiderPage(xml_wen)
	divide(wen_data,"score",proc)

for num in num_set:
	search(num)
	if(num%25==0):
		print num

