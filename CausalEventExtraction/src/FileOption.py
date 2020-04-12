#! /usr/bin/env python
#coding=utf-8

import os
import re
import threading
import sys

import random


#sys.path.append('F:\CausalEventLearning\src')
#from CausalMention import TriggerListRead

WriteLock = threading.RLock()

#Trigger list
Trigger_List = []

def MergeFiles(path, outfile):
    output = open(outfile, 'w')
    
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if os.path.join(parent, filename).find("causalmention")!=-1:
                print "Find one ..."
                input = open(os.path.join(parent, filename),'r')
                text_in_eachdoc = input.read()
                input.close()
                os.remove(os.path.join(parent, filename))
                if len(text_in_eachdoc)>1:
                    output.write(text_in_eachdoc+'\n')
            else:
                continue
    output.close()
    
def GeneRand(lineCount, randline):
    linenum = random.randint(1,9999999999)%lineCount
    if randline.has_key(linenum):
        return linenum+random.randint(1,10)
        #linenum = GeneRand(lineCount)
    else:
        return linenum
    
def Sample(path):
    
    #Samplepath = r"F:\CausalEventLearning\data\Sample"
    
    print "Begin Sample ..."
    input = open(path+"because.txt",'r')
    lines = input.readlines()
    linesnum = len(lines)
    print linesnum
    input.seek(0,0)
    output = open(path+"because_sample.txt", 'w')
    counter = 0
    randline ={}
    for i in range(101):
        linenum = GeneRand(linesnum,randline)
        randline[linenum]=1
    while True:
        line = input.readline()
        if not line:
            break
        else:
            counter +=1
            if randline.has_key(counter):
                output.writelines(line)
                print "Match ..."
    input.close()
    output.close()

    
    """
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            input = open(os.path.join(parent, filename),'r')
            lines = input.readlines()
            linesnum = len(lines)
            print linesnum
            input.seek(0,0)
            
            output = open(Samplepath+'\\'+filename, 'w')
            counter = 0
            randline ={}
            
            for i in range(101):
                linenum = GeneRand(linesnum,randline)
                randline[linenum]=1
                
            while True:
                line = input.readline()
                if not line:
                    break
                else:
                    counter +=1
                    if randline.has_key(counter):
                        output.writelines(line)
                        print "Match ..."
            input.close()
            output.close()
       """     
    
    
#Read triggers to a list
def TriggerListRead(triggerfile):   
    
    fp = open(triggerfile, 'r')
    triggers = fp.readlines()
    fp.close()
    
    for trigger in triggers:
        Trigger_List.append(trigger.rstrip())
    
def ExtractCausalEvent(eventfile, causalevent):
    input = open(eventfile, 'r')
    lines = input.readlines()
    input.close()
    output = open(causalevent, 'w')
    
    for line in lines:
        items = line.split('\t')
        for trigger in Trigger_List:
            if items[3].find(trigger)!=-1:
                print "Match one ..."
                output.writelines(items[1]+'\t'+items[2]+'\t'+items[3]+'\t'+items[4]+'\t'+items[11]+'\n')
    output.close()
    
    
def FileClean(inputfile, outputfile):
    input = open(inputfile, 'r')
    lines = input.readlines()
    input.close()
    
    output = open(outputfile, 'w')
    
    for line in lines:
        if len(line)>1:
            output.writelines(line)
            
    output.close()
            
def CauseEffectMention(inputfile, outputfile):
    
    input = open(inputfile, 'r')
    output = open(outputfile,'w')
    while True:
        line = input.readline()
        if not line:
            break
        line = input.readline()
        causality = line.split('\t')
        cause = causality[0]
        effect = causality[1].rstrip()
        if len(cause)<1 or len(effect)<1:
		    continue
        output.writelines("CAUSE: "+cause+".\n")
        output.writelines("EFFECT: "+effect+".\n")
    
    input.close()
    output.close()
    
        

 
if __name__=="__main__":
    
    rootpath = r"F:\CausalEventLearning\data\causalmention_new"
    outfile = '../data/CausalMention.txt'
    cleanfile = '../data/CausalMention_clean.txt'
    revbfile = '../data/CausalMention_revb.txt'
    #path = 'F:\CausalEventLearning\data'
    #CauseEffectMention(cleanfile, revbfile)
    #MergeFiles(rootpath, outfile)
    #FileClean(outfile, cleanfile)
    #Sample(r'./triggerfile/')
 	   
    print "Finished ..."
