#coding = utf8
import os
import sys
import re
#import thread
import time


#Hash table with triggers
Trigger = {}

#Trigger list
Trigger_List = []

filecount = 0

WalkHash = {}



p_after = re.compile(r"After ([a-zA-Z\'\- ]+?),\s([\w\'\- ]+)\s?[\.,\?]")
p_because = re.compile(r"([\w\'\- ]+?)because(?!\sof) ([\w\'\- ]+)\s?[\.,\?]")
p_due_to_1 = re.compile(r"([\w\'\- ]+)[was|were|is|are]?due to\s([\w\'\- ]+)\s?[\.,\?]")
p_due_to_2 = re.compile(r"([\w\'\- ]+),\sdue to\s([\w\'\- ]+)\s?[\.,\?]")
p_because_of_1 = re.compile(r"Because of ([\w\'\- ]+?),\s([\w\'\- ]+)\s?[\.,\?]")
p_because_of_2 = re.compile(r"([\w\'\- ]+)because of\s([\w\'\- ]+)\s?[\.,\?]")
p_cause = re.compile(r"([\w\'\- ]+)\scause(?!\sby)\s([\w\'\- ]+)\s?[\.,\?]")
p_caused_by = re.compile(r"([\w\'\- ]+)[was|were|is|are]?caused by\s([\w\'\- ]+)\s?[\.,\?]")
p_lead_to = re.compile(r"([\w\'\- ]+)lead to ([\w\'\- ]+)\s?[\.,\?]")

#p_because = re.compile(r"([\w\'\- ]+?)because(?!\sof) ([\w\'\- ]+)\s?[\.,\?]")
p_as_a_consequence=re.compile(r"([\S ]+?)as a consequence(?!\sof) ([\S ]+)\s?[\.,\?]")
p_as_a_result=re.compile(r"([\S ]+?)as a result(?!\sof) ([\S ]+)\s?[\.,\?]")
p_for_reason = re.compile(r"([\S ]+?)for reason(?!\sthat) ([\S ]+)\s?[\.,\?]")

def test():
    
    line = r"after wesd Afghan vote, comp-laints because lead-to that' of fraud, surfacev ? jadsklfj?"

    match = p_because.search(line)
    
    if match:
        print "Match Rex ..."
        print match.group(0)
        print match.group(1)
        print match.group(2)
    else:
        print "Cannot Match ..."
   
"""   
    qq = re.findall("[aA]fter ([\w ]+?),\s([\w ]+)\s?[\.,\?]", line)
    #qq = re.findall("after (.+?),\s(.+?)\s?\.",line)
    #print qq
    #print qq[0]
    for q in qq:
        print q        
"""

#Read triggers to a hash table
def TriggerHashRead(triggerfile):
    
    fp = open(triggerfile,'r')
    triggers = fp.readlines()
    fp.close()
    
    for trigger in triggers:
        if Trigger.has_key(trigger):
            continue
        else:
            Trigger[trigger.rstrip()]=1
            
#Read triggers to a list
def TriggerListRead(triggerfile):   
    
    fp = open(triggerfile, 'r')
    triggers = fp.readlines()
    fp.close()
    
    for trigger in triggers:
        Trigger_List.append(trigger.rstrip())

        
#Segement sentence
def Tokenlization(document, sentencefile):
    
    input = open(document, 'r')
    all_the_text = input.read()
    input.close()
    
    text = all_the_text.rstrip()
    text = " ".join(text.split())
    
    #Math the end of sentences
    end = re.compile(r"[.!?.]+")
    sentences = re.split(end, text)
    
    output = open(sentencefile, 'w')
    for sentence in sentences:
        output.writelines(sentence+'.'+'\n')
    
    output.close()
    

# Extract cause and effect mention using Rex 

def CausalMentionUseRex(sentencefile, causalityfile):
    
    input = open(sentencefile, 'r')
    sentences = input.readlines()
    input.close()
    os.remove(sentencefile)
    
    output = open(causalityfile,'w')    
    
    for i, sentence in enumerate(sentences):
        
        Cause = False
        
        
        match = p_after.search(sentence)
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(1)+'\t'+match.group(2)+'\n')
            #print match.group(1)+"\t"+match.group(2)
            
        match = p_because.search(sentence)    
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n')
            Cause = True
        
        match = p_due_to_1.search(sentence)   
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n')
            Cause = True
            
        match = p_due_to_2.search(sentence)
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n')
            Cause = True
            
        match = p_because_of_1.search(sentence)
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n')
            Cause = True
            
        match = p_because_of_2.search(sentence)    
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n')
            Cause = True
            
        match = p_cause.search(sentence)    
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(1)+'\t'+match.group(2)+'\n')
            Cause = True
            
        match = p_caused_by.search(sentence)    
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n')
            Cause = True
        
        match = p_lead_to.search(sentence)            
        if match:
            output.writelines("Sentence#"+str(i)+":"+sentence)
            output.writelines(match.group(2)+'\t'+match.group(1)+'\n') 
            Cause = True
        
        if Cause:
            print "Match a pattern ..."

    output.close()
    
    
#Extract sentences which contain causal triggers
def CausalMentionUseHash(sentencefile, causalityfile):
    input = open(sentencefile,'r')
    sentences = input.readlines()
    input.close()
    os.remove(sentencefile)
    
    output = open(causalityfile,'w')
    
    for sentence in sentences:

        Cause = False        

        words = sentence.split(' ')
        for word in words:
            if Trigger.has_key(word):
                Cause = True
                print "Match a case ..."
                break
            else:
                #print "No Match ..."
                continue
        
        if Cause:
            output.writelines(sentence)
        else:
            continue

    output.close()
      
      
def CausalMentionUseList(sentencefile, causalityfile):
    
    input = open(sentencefile,'r')
    sentences = input.readlines()
    input.close()
    os.remove(sentencefile)
    #output_because = open("./triggerfile/because.txt",'a')
    output_as_a_consequence= open("./triggerfile/as_a_consequence.txt",'a')
    output_as_a_result= open("./triggerfile/as_a_result.txt",'a')
    output_for_reason = open("./triggerfile/for_reason.txt",'a')
    
    for sentence in sentences:
        #match = p_because.search(sentence)
       # if match:
       #     output_because.writelines(sentence)
        #    continue
        match = p_as_a_consequence.search(sentence)
        if match:
            output_as_a_consequence.writelines(sentence)
            continue
        match = p_as_a_result.search(sentence)     
        if match:
            output_as_a_result.writelines(sentence)
            continue
        match = p_for_reason.search(sentence)
        if match:
            output_for_reason.search(sentence)
            continue

    #output_because.close()
    output_as_a_consequence.close()
    output_as_a_result.close()
    output_for_reason.close()

    
"""    
    for trigger in Trigger_List:
        
        output = open(path+"\\triggerfile\\"+str(trigger)+".txt",'a')
        for sentence in sentences:
            if sentence.find(trigger)!=-1:
                output.writelines(sentence)
            else:
                continue
        output.close()
"""    
    
"""    
    output = open(causalityfile,'w')
    
    for sentence in sentences:
        
        Cause = False
        for trigger in Trigger_List:
            if sentence.find(trigger)!=-1:
                Cause = True
                print "Match a case ..."
                break
            else:
                continue
        if Cause:
            output.writelines(sentence)
        else:
            continue
        
    output.close()
"""    
 
def FileWalk(rootdir):
    
    filecount = 0
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            
            if WalkHash.has_key(filename):
                continue
            else:
                filecount+= 1
                WalkHash[filename] =1
                sentencefile = "./sentence/"+str(filecount)+".sentences.txt"
                causalityfile = "./causalmention/"+str(filecount)+".causalmention.txt"
                                          
                Tokenlization(os.path.join(parent, filename), sentencefile)
                CausalMentionUseList(sentencefile, causalityfile) 
                #CausalMentionUseRex(sentencefile, causalityfile)
    print "Total file num: " + str(filecount)
                
    
if __name__=="__main__":
    
    #test()
    
    #TriggerHashRead('trigger.txt')

    rootdir = r"../../20061020_20131126_bloomberg_news"
    #path = 'F:\CausalEventLearning\data'
    #TriggerListRead(path+'\\trigger.txt')
    FileWalk(rootdir)
    
    
    
    
