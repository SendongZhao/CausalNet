#! /usr/bin/env python
#coding=utf-8

#Extract text element from NYT corpus

import os
import xml.dom.minidom as minidom
import tarfile
import string
    
def Extractext(XMLfile, TXTfile):
    
    dom = minidom.parse(XMLfile)
    root = dom.documentElement
    node = root.getElementsByTagName("p")
    
    for p in node:
        print p.firstChild.data


def Untgz(rootpath):
    n = len("F:\DataSet\nyt_corpus\data\1987")
    print n
    for parent, dirnames, filenames in os.walk(rootpath):
        for filename in filenames:
            name = os.path.join(parent, filename)
            tgz = tarfile.open(name)
            
            #strnset(name,'F:\DataSet\nyt_corpus\untg',n)
            #print name
            tgz.extractall(name[0:31])
            tgz.close()
            
                    

if __name__ == '__main__':
    #Extractext("123.xml", "123.txt")
    Untgz(r"F:\DataSet\nyt_corpus\data")