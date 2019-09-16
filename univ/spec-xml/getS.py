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

#prov.append(["beijing","00","10003"])
#prov.append(["hubei","01","10021"])
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


#####to do i


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

def download(url,path):
	try:
		src=spiderPage(url)
		if re.search("flash",src):   # 404.htm, error
			return
		output=file(path,"w")
		output.write(src)
	except AttributeError:
		return


def search(num,group):
	global fo
	global type
	global place
	global name
	global area_no
	global tags
	tags=[]
	xml_li = "http://gkcx.eol.cn/commonXML/schoolSpecialPoint/schoolSpecialPoint"+str(num)+"_"+area_no+"_10035.xml"
	xml_wen = "http://gkcx.eol.cn/commonXML/schoolSpecialPoint/schoolSpecialPoint"+str(num)+"_"+area_no+"_10034.xml"	
	dld_li="data/schoolSpecialPoint"+str(num)+"_"+area_no+"_10035.xml"
	dld_wen="data/schoolSpecialPoint"+str(num)+"_"+area_no+"_10034.xml"
	download(xml_li,dld_li)
	download(xml_wen,dld_wen)


	
for p in prov:	
	print p[0]
	area=p[0]
	area_saved=p[1]
	area_no=p[2]

	
	getnum(1,20,search)
	getnum(2,20,search)
	#getnum(3,20,search)
