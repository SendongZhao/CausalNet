#! /usr/bin/env python
#coding=utf-8
import os
import types

def Label(infile, outfile):
    
    putin = open(infile, 'r')
    linenum = 0
    if os.path.exists(outfile):
        filecount = open(outfile,'r')
        writelines = filecount.readlines()
        linenum = len(writelines)
        filecount.close()

    output = open(outfile, 'a')
	 
    lines = putin.readlines()
    putin.close()

    
    for i, line in enumerate(lines):
        if i<linenum:
            continue
        print line
        a = input("Please input the label: (0 represent 0, 1 represent 1, 2 represent -1): ")

        while True:
            
            if type(a) is not types.IntType:
                a = input("Illegal! Please correct your label: ")
            elif type(a) is types.IntType:
                if a==0 or a==1 or a==2:
                    break
                else:
                    a = input("Illegal! Please correct your label: ")

        if a==1:
            output.writelines("1\t"+line)
        elif a==0:
            output.writelines("0\t"+line)
        elif a==2:
            output.writelines("-1\t"+line)
            
    output.close()
    

if __name__ == '__main__':
    
    path_file = open("./path.txt",'r')
    path = path_file.read()
    path = path.rstrip()
    
    print "Begin ..."

    trigger_file = open("./trigger.txt",'r')
    triggers = trigger_file.readlines()

    for trigger in triggers:
        trigger = trigger.rstrip()
        print "Trigger is ###"+trigger+"###\n" 
        Label(path+trigger+".txt",path+trigger+"_labeled.txt")
    
