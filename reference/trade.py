import re

file=open("test/test")

str=file.read()

def divide(str,label,func):
	pat=re.compile(r"<" + label + ".*?>(.*?)</"+ label +">",re.DOTALL)
	res=re.finditer(pat,str)

	for i in res:
		pat2=re.compile(".*<"+ label +".*?>",re.DOTALL)
		str2= i.group(1)
		str2=re.sub(pat2,"",str2)
		proc(str2)

def proc(str):
	print "******************************\n",str


divide(str,"div",proc)
