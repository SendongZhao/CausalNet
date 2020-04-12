#coding=utf-8
import os
import re
import threading
import sys

import random


def GeneRand(lineCount, randline):
    linenum = random.randint(1,9999999999)%lineCount
    if randline.has_key(linenum):
        return linenum+random.randint(1,10)
        #linenum = GeneRand(lineCount)
    else:
        return linenum
    
def Sample(inputfile, outputfile, samplenum, unitnum):
    
    print "Begin Sample ..."

    input = open(inputfile,'r')
    lines = input.readlines()
    linesnum = len(lines)
    print linesnum
    input.seek(0,0)
            
    output = open(outputfile, 'w')
    counter = 0
    randline ={}
            
    for i in range(samplenum):
        linenum = GeneRand(linesnum/4,randline)
        randline[linenum]=1
                
    while True:
        line = input.readline()
        if not line:
            break

        if randline.has_key(counter):
            output.writelines(line)
            for i in range(unitnum-1):
                line = input.readline()
                output.writelines(line)
        else:
            for i in range(unitnum-1):
                line = input.readline()
        counter += 1
    input.close()
    output.close()


def generateTrain(testfile, validfile, allfile, trainfile):
    exit = {}
    test = open(testfile, 'r')
    valid = open(validfile, 'r')
    all = open(allfile, 'r')
    
    train = open(trainfile, 'w')
    
    testlines = test.readlines()
    validlines = valid.readlines()
    alllines = all.readlines()
    
    
    for line in testlines:
        exit[line] = 1
    for line in validlines:
        exit[line] =1
    
    for line in alllines:
        if exit.has_key(line):
            continue
        train.writelines(line)
        
def runSample():
    Sample('up_synet/upCausalityTest.txt','up_synet/upCausalitytest.txt',280,1)
    Sample('up_synet/upCausalityTest.txt','up_synet/upCausalityvalid.txt',280,1)
    generateTrain('up_synet/upCausalitytest.txt', 'up_synet/upCausalityvalid.txt', 'up_synet/upCausalityClean.txt', 'up_synet/upCausalityTrain.txt')
    
            
    
    

if __name__=="__main__": 
    Sample('up_synet/upCausalityTest.txt','up_synet/upCausalitytest280.txt',280,1)
    Sample('up_synet/upCausalityTest.txt','up_synet/upCausalityvalid.txt',280,1)
    generateTrain('up_synet/upCausalityTest280.txt', 'up_synet/upCausalityvalid.txt', 'up_synet/upCausalityClean.txt', 'up_synet/upCausalityTrain.txt')
