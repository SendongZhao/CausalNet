#! /usr/bin/env python
#coding=utf-8
from UpCausality import *
from LanguageModel import *
from Index import *

if __name__ == '__main__':
    generateLanguageModel()
    print "generate LanguageModel Done ..."
    processUpNode()
    print "processUpNode Done ..."
    runSample()
    print "Sample Done ..."
    turnIndex()
    print "Index Done ..."
    