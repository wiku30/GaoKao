import re
from lxml import etree

file=open("test/test.html")

str=file.read()
file.close()

tree=etree.HTML()
aa=tree.xpath("//div")
