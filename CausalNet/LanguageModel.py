import os
import operator

unigram_dict ={}

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
        
def existWord(bigram, unigram):
    words_in_bigram = bigram.split('\t')
    if unigram == words_in_bigram[0] or unigram == words_in_bigram[1]:
        return True
    else:
        return False
             

class LanguageModel(object):
    
    def __init__(self, dict, pattern, topevent):
        self._dict = dict
        self._pattern = pattern
        self._event = topevent
        
    def addDict(self,item):
        if self._dict.has_key(item):
            self._dict[item] = self._dict[item]+1
        else:
            self._dict[item] =1
            
    def sortDict(self):
        sorted_dict = sorted(self._dict.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_dict
    
    def addTopEvent(self, event):
        if self._event.has_key(event):
            self._event[event] = self._event[event] +1
        else:
            self._event[event] = 1
    
    def sortTopEvent(self):
        sorted_event = sorted(self._event.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_event

    def Bigram(self, Unigram, Event):
        
        length = len(Unigram)
        
        #n^2
        for i in range(length):
            for j in range(i+1, length):
                self._pattern.append(Unigram[i]+'\t'+Unigram[j])
                
        for p in self._pattern:
            for event in Event:
                cover = ifCover(p, event)
                if cover:
                    self.addTopEvent(event)
                    self.addDict(p)
                    
    def Trigram(self, Bigram, Unigram, Event):
        length_bigram = len(Bigram)
        print "Length of Bigram", length_bigram
        
        length_unigram = len(Unigram)
        print "Length of Unigram", length_unigram
        
        for i in range(length_bigram):
            for j in range(length_unigram):
                if existWord(Bigram[i], Unigram[j]):
                    continue
                else:
                    self._pattern.append(Bigram[i]+'\t'+Unigram[j])
                    
        for p in self._pattern:
            for event in Event:
                cover = ifCover(p, event)
                if cover:
                    self.addTopEvent(event)
                    self.addDict(p)
            

def hasUnigram(words):
    have_unigram = False
    length = len(words)
    counter = 0
    for word in words:
        if unigram_dict.has_key(word):
            #have_unigram = True
            counter += 1 
            #break
        
    if float(counter/length)<0.3:
        return False
    else:
        return True
    #return have_unigram

def generateLanguageModel():
    
    #read unigram
    print "Begin Read unigram ..."
    unigram = []
    input = open('up_synet/Event_Unigram_synet.txt', 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.strip()
        items = line.split('\t:')
        if int(items[1]) >= 8:
            unigram.append(items[0])
            if not unigram_dict.has_key(items[0]):
                unigram_dict[items[0]] = 1
    
       
    print "Begin Read Event ..."
    #read event
    event = []
    input = open('up_synet/Event_class_whole_clean_synet.txt', 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.strip()
        line = line.strip('\t')
        words = line.split('\t')
        if hasUnigram(words):
            event.append(line)
    
    print len(event)
    
    print "Begin Language ..."
    
    #model
    dict_bigram = {}
    topevent ={}
    pattern_bigram = []
    
    model = LanguageModel(dict_bigram, pattern_bigram, topevent)
    model.Bigram(unigram, event)
    sorted_dict = model.sortDict()
    sorted_event = model.sortTopEvent()
    
    
    
    #write bigram
    #bigram = []
    output = open('up_synet/Event_bigram.txt', 'w')
    
    for p in sorted_dict:
        output.writelines(p[0]+'\t'+str(p[1])+'\n')
        #bigram.append(p[0])
    output.close()
    
    #write top event
    output = open('up_synet/Top_Event_of_bigram.txt', 'w')
    for e in sorted_event:
        output.writelines(e[0]+'\n')
        
    output.close()
        
    
        

if __name__ == '__main__':
    
    input1 = open('up_synet/Top_Event.txt','r')
    input2 = open('up_synet/Event_trigram_2.txt', 'r')
    
    events = input1.readlines()
    print len(events)
    trigrams = input2.readlines()
    print len(trigrams)
    searchPrototype(events, trigrams, 'up_synet/prototype')
    #test()
    """
    #read unigram
    print "Begin Read unigram ..."
    unigram = []
    input = open('up_synet/Event_Unigram_synet.txt', 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.strip()
        items = line.split('\t:')
        if int(items[1]) >= 10:
            unigram.append(items[0])
            if not unigram_dict.has_key(items[0]):
                unigram_dict[items[0]] = 1

       
    print "Begin Read Event ..."
    #read event
    event = []
    input = open('up_synet/Event_class_whole_clean_synet.txt', 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.strip('\t\n')
        words = line.split('\t')
        if hasUnigram(words):
            event.append(line)
    
    print len(event)
    
    print "Begin Language ..."
    
    #model
    dict_bigram = {}
    topevent ={}
    pattern_bigram = []
    
    model = LanguageModel(dict_bigram, pattern_bigram, topevent)
    model.Bigram(unigram, event)
    sorted_dict = model.sortDict()
    sorted_event = model.sortTopEvent()
    
    
    
    #write bigram
    #bigram = []
    output = open('up_synet/Event_bigram.txt', 'w')
    
    for p in sorted_dict:
        output.writelines(p[0]+'\t'+str(p[1])+'\n')
        #bigram.append(p[0])
    output.close()
    
    #write top event
    output = open('up_synet/Top_Event.txt', 'w')
    for e in sorted_event:
        output.writelines(e[0]+'\n')
        
    output.close()
    
    
    #read bigram
    print "Begin Read bigram ..."
    bigram = []
    input = open('up_synet/Event_bigram.txt', 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.strip()
        items = line.split('\t')
        if int(items[2]) >= 4:
            bigram.append(items[0]+'\t'+items[1])

    print "Begin Read Event ..."
    #read event
    event = []
    input = open('up_synet/Top_Event.txt', 'r')
    lines = input.readlines()
    input.close()
    for line in lines:
        line = line.strip()
        event.append(line)
    
    print len(event)
    
    
    print "Begin Language ..."
    
    #model
    dict_trigram = {}
    topevent_trigram ={}
    pattern_trigram = []
    
    model = LanguageModel(dict_trigram, pattern_trigram, topevent_trigram)
    model.Trigram(bigram, unigram, event)
    sorted_dict = model.sortDict()
    sorted_event = model.sortTopEvent()
    
    #write trigram
    #bigram = []
    print "Write Trigram ..."
    output = open('up_synet/Event_trigram.txt', 'w')
    
    for p in sorted_dict:
        output.writelines(p[0]+'\t'+str(p[1])+'\n')
        #bigram.append(p[0])
    output.close()
    
    #write top event
    output = open('up_synet/Tri_Top_Event.txt', 'w')
    for e in sorted_event:
        output.writelines(e[0]+'\n')
        
    output.close()
    """
    
    
            
    
       
    
    
    
    
            
    
    
    
        
        
                