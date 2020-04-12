#! /usr/bin/env python
#coding=utf-8
import operator

EventIndex = []
Occurce ={}


def hasElement(element):
    
    for e in EventIndex:
        if e == element:
            return True
        
    return False

def getIndex(element):
    
    for i, e in enumerate(EventIndex):
        if e == element:
            return i
    return -1

def readEvent(lines):
    counter = 0
    for line in lines:
        line = line.strip()
        cause, effect = line.split('\t\t')

        if not hasElement(cause):
            EventIndex.append(cause)
            Occurce[cause]=1
        else:
            Occurce[cause] += 1
        if not hasElement(effect):
            EventIndex.append(effect)
            Occurce[effect]=1
        else:
            Occurce[effect] += 1
            

def Event2Index(infile, outfile):
    input = open(infile, 'r')
    lines = input.readlines()
    input.close()
    output = open(outfile, 'w')
    
    for line in lines:
        line = line.strip()
        cause, effect = line.split('\t\t')
        causeindex = "%05d" %(getIndex(cause))
        effectindex = "%05d" %(getIndex(effect))
        newline = causeindex+"\t\t"+effectindex
        output.writelines(newline + '\n')

    output.close()
    
    
def turnIndex():
    
    input = open('up_synet/upCausalityTrain.txt')
    lines = input.readlines()
    readEvent(lines)
    
    Event2Index('up_synet/upCausalityTrain.txt', 'up_synet/NYT_data/NYT-causality-synet-train.txt')
    Event2Index('up_synet/upCausalitytest.txt', 'up_synet/NYT_data/NYT-causality-synet-test.txt')
    Event2Index('up_synet/upCausalityvalid.txt', 'up_synet/NYT_data/NYT-causality-synet-valid.txt')
    
    
    #write deifiniton file        
    output = open('up_synet/NYT_data/NYT-causality-synet-definition.txt','w')
    print len(EventIndex)
    
    for i, e in enumerate(EventIndex):
        index = "%05d" %(i)
        text = e.split('\t')[0]+" "+e.split('\t')[1]
        output.writelines(index+"\t"+text+"\t"+'EVENT_%d\n' %i)
    output.close()
    
if __name__=='__main__':
    
    input = open('data/NYT-causality-synet-train.txt')
    lines = input.readlines()
    readEvent(lines)
    
    Event2Index('data/NYT-causality-synet-train.txt', 'data/NYT-causality-synet-train-index.txt')
    Event2Index('data/NYT-causality-synet-test.txt', 'data/NYT-causality-synet-test-index.txt')
    Event2Index('data/NYT-causality-synet-valid.txt', 'data/NYT-causality-synet-valid-index.txt')
 

    #write deifiniton file        
    output = open('data/NYT-causality-synet-definition.txt','w')
    print len(EventIndex)

    for i, e in enumerate(EventIndex):
        index = "%05d" %(i)
        text = e.split('\t')[0]+" "+e.split('\t')[1]
        output.writelines(index+"\t"+text+"\t"+'EVENT_%d\n' %i)
    output.close()
        
        
        