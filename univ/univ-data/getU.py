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

prov=[]

prov.append(["beijing","00","10003"])
prov.append(["hubei","01","10021"])
prov.append(["heilongjiang","02","10031"])
prov.append(["liaoning","03","10027"])

area=""
area_saved="00"
area_no=""

type=""
place=""
name=""
group=0
tags=[]



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




def proc(_str):
	global type
	global place
	global name
	global fo
	global group
	global tags
	try:
		if(_str):
			year=re.search(r"<year>(.*?)</year>",_str).group(1)
			avg=re.search(r"<avgScore>([0-9]*?)</avgScore>",_str).group(1)
			fo.write (str(group)+" "+name +" "+year+" "+type+" "+avg+" # ");
			
			for i in tags:
				fo.write(i+" ")
			fo.write("#\n")
	except AttributeError:
		return

def getnum(type, maxn, func): #type表示批次,maxn是最大页面数
	global area
	global group
	group=type
	for i in range(maxn):
		list_url="http://gkcx.eol.cn/support/cuttingScore/cuttingScore_"+area+"_"+str(type)+"_"+str(i)+".htm"
		lisrc=spiderPage(list_url)
		num_list=re.finditer("/schoolhtm/schoolTemple/school(.*?).htm",lisrc)
		for num1 in num_list:
			num=int(num1.group(1))
			func(num,type)
			print num


def search(num,group):
	global fo
	global type
	global place
	global name
	global area_no
	global tags
	tags=[]
	page = "http://gkcx.eol.cn/schoolhtm/schoolTemple/school" + str(num) + ".htm"
	xml_li = "http://gkcx.eol.cn/schoolhtm/scores/provinceScores" + str(num) +"_"+area_no+"_10035_1003"+str(5+group)+".xml"
	xml_wen = "http://gkcx.eol.cn/schoolhtm/scores/provinceScores" + str(num) +"_"+area_no+"_10034_1003"+str(5+group)+".xml"
	
	pgsrc=spiderPage(page)
	try:
		name=re.search("<h2 class=\"left\">(.*?)</h2>",pgsrc).group(1)  #first h2 is school name
		print name
		_place=re.search("<td width=\"55\" align=\"left\" class=\"gary\">(.*?)</td>",pgsrc,re.DOTALL).group(1)
		place=re.sub("\\s","",_place)
		tags.append(place)
		if(re.search(r'<a href="http://www.eol.cn/html/g/gxmd/985.shtml">985',pgsrc)):
			tags.append('985')
		if(re.search(r'<a href="http://www.eol.cn/html/g/gxmd/211.shtml">211',pgsrc)):
			tags.append('211')
	except AttributeError:
		return
	

	type="S"

	li_data = spiderPage(xml_li)
	divide(li_data,"score",proc)
	
	type="A"
	wen_data=spiderPage(xml_wen)
	divide(wen_data,"score",proc)

for p in prov:	
	print p[0]
	area=p[0]
	area_saved=p[1]
	area_no=p[2]
	fo=file("res-"+area_saved,"w")
	getnum(1,20,search)
	getnum(2,20,search)
	#getnum(3,20,search)
