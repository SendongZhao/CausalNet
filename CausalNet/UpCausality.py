
import os
import operator

toFather = {}
upCausality = {}


def ifCover(p, event):
    
    words_in_p = p.split('\t')
    words_in_event = event.split('\t')
    counter = 0
    
    for word_p in words_in_p:
        for word_e in words_in_event:
            if word_p == word_e:
                counter += 1
                break
            
    if counter == len(words_in_p):
        return True
    else:
        return False


def searchBiPrototype(events, bigrams):
    
    prototype = []
    for bigram in bigrams:
        items = bigram.split('\t')
        bigram = items[0]+'\t'+items[1]
        line = bigram
        for event in events:
            event = event.strip()
            if ifCover(bigram, event):
                if toFather.has_key(event):
                    toFather[event] = toFather[event]+'\t\t'+bigram
                else:
                    toFather[event] = bigram
                    
                #print "Match one ..."
                line = line + '::\t' + event
        prototype.append(line)

    return prototype

def UpNodeProcess(eventfile, bigramfile, outfile):
    
    in_event = open(eventfile, 'r')
    in_bigram = open(bigramfile, 'r')
    
    events = in_event.readlines()
    bigrams = in_bigram.readlines()
    in_event.close()
    in_bigram.close()
    
    upnodes = searchBiPrototype(events, bigrams)
    
    output = open(outfile, 'w')
    for upnode in upnodes:
        output.writelines(upnode+'\n')
        
    output.close()


def readCausalPairs(infile):
    
    input = open(infile, 'r')
    
    causalpairs = []
    
    while True:
        line = input.readline()
        if not line:
            break
        
        cause = line.strip('\t\n')
        line = input.readline()
        effect = line.strip('\t\n')
        causalpair = (cause, effect)
        causalpairs.append(causalpair)
    input.close()
    
    print len(causalpairs)
    
    return causalpairs

        
#generate the causal relation among upnodes

def generateUpCausality(causalpairs):
    for causalpair in causalpairs:
        cause = causalpair[0]
        effect = causalpair[1]
        if toFather.has_key(cause) and toFather.has_key(effect):
            print "Find a clue ..."
            causeupnodes = toFather[cause].split('\t\t')
            effectupnodes = toFather[effect].split('\t\t')
            
            for causenode in causeupnodes:
                for effectnode in effectupnodes:
                    pair = causenode+'\t\t'+effectnode
                    if upCausality.has_key(pair):
                        upCausality[pair] += 1
                    else:
                        upCausality[pair] = 1
                        
def checkUpCausality(lines):
    
    isolate = 0
    Event = {}
    
    #read dict of event
    for line in lines:
        line = line.strip()
        cause, effect = line.split('\t\t')
        if Event.has_key(cause):
            Event[cause] += 1
        else:
            Event[cause] = 1
            
        if Event.has_key(effect):
            Event[effect] += 1
        else:
            Event[effect] = 1
            
    sorted_dict = sorted(Event.iteritems(), key=operator.itemgetter(1), reverse=True)
    print len(sorted_dict)
    
    output1 = open('up_synet/upCausalityClean.txt','w')
    output2 = open('up_synet/upCausalityTest.txt','w')
    
    for line in lines:
        line = line.strip()
        cause, effect = line.split('\t\t')
        
        if Event[cause]<=1 and Event[effect]<=1:
            isolate += 1
            
        if Event[cause]>=2 or Event[effect]>=2:
            output1.writelines(line+'\n')
            
        if Event[cause]>3 and Event[effect]>3:
            output2.writelines(line+'\n')
        
    
    print isolate
    
    return sorted_dict
            
            
        
def processUpNode():
    
    UpNodeProcess('up_synet/Top_Event_of_bigram.txt', 'up_synet/Event_bigram.txt', 'up_synet/upnode.txt')
    
    causalpairs = readCausalPairs('up_synet/Event_class_whole_clean_synet.txt')
    
    generateUpCausality(causalpairs)
    
    sorted_dict = sorted(upCausality.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    output = open('up_synet/upCausality.txt', 'w')
    for p in sorted_dict:
        #output.writelines(p[0]+'\t'+str(p[1])+'\n')
        output.writelines(p[0]+'\n')
    
    output.close()
    
    
    upcausality = open('up_synet/upCausality.txt','r')
    event = open('up_synet/eventintopcausality.txt', 'w')
    
    lines = upcausality.readlines()
    sortedevent = checkUpCausality(lines)
    for p in sortedevent:
        event.writelines(p[0]+'\t'+str(p[1])+'\n')
        #output.writelines(p[0]+'\n')    
            

if __name__ == '__main__':
    processUpNode()
     
    

    
    
    
    
    