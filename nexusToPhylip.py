#!/usr/bin/python
#version 1.0.1
import sys,os,re

#Adapted to python from perl script provided by Cecile (6 March 2015)
#  Version 1.0.0
#     find nchar and ntax attributes.
#     reads all lines between "matrix" and ";"
#     If there are ntax of them and they are all nchar long.
#     Then subroutine ends without an error message.
#
#  Version 1.0.1
#     deal with interleaved format.

def nexusToPhylip(inputFilename, outputFilename):
    errorOffset = 0

    if( not os.path.isfile(inputFilename) ):
        print "Error: input file, " + inputFilename + ", is not a file."
        return errorOffset + 1

    try:
        nexusFile = open(inputFilename, 'r')
    except:
        print "Error: could not open input file, " + inputFilename + "."
        return errorOffset + 2

    try:
        phylipFile = open(outputFilename, 'w')
    except:
        print "Error: could not open output file, " + outputFilename + "."
        return errorOffset + 3

    inMatrix    = False;
    nReadNames  = 0;
    ntax        = 0;
    ntaxRead    = 0;
    nchar       = None;
    ncharRead   = 0;
    interleaved = 0;
    lastLine   = False
    for line in nexusFile:

        if inMatrix and re.search('^\s*;', line):    #Matrix section end-marker is a simple semi-colon ";"
            if ntax != ntaxRead:
                print "Error: ntax (" + str(ntax) + ") attribute in nexus file does not match number of taxa found (" + str(ntaxRead) + ")."
                return errorOffset + 4
            else:
                #Matrix is closed properly and taxa line up.
                inMatrix = False
                phylipFile.close()
                nexusFile.close()
                return 0
            
        #if find nexus ntax or nchar attributes, grab them.
	if line.strip() and inMatrix == False:
            ntaxFound = re.search('ntax=(\d+)', line.lower())
            if ntaxFound:
                ntaxRead = int(ntaxFound.group(1))
                        
            #find the number of characters
            ncharFound = re.search('nchar=(\d+)', line.lower())
            if ncharFound:
                ncharRead = int(ncharFound.group(1))

            interleaveFound = re.search('interleave', line.lower())
            if interleaveFound:
                interleaved = 1
                taxaList = []

            if ntaxFound and ncharFound:
                phylipFile.write(" " + str(ntaxRead) + " " + str(ncharRead) + "\n")

            matrixFound = re.search('matrix', line.lower())
            if matrixFound:
                inMatrix = True

        #else in matrix	
        elif line.strip():
            sequence = re.search("([^ ]+)\s+([01A-Z-?]+)", line)    #added 0 and 1 as sequence digits to handle binary data for presence/absence.
            if sequence:
                name = sequence.group(1)
                sequenceData = sequence.group(2)
                sequenceLength = len(sequence.group(2))
                if ncharRead != sequenceLength and interleaved == 0:
                    print "Error: nchar (" + str(ncharRead) + ") attribute in nexus file does not match length of sequences read (" + str(sequenceLength) + ")."
                    return errorOffset + 5
            else:
                print "Error: sequence line not understood."
                print " line = #" + line + "#"
                return errorOffset + 6

            newTaxa = 1
            if interleaved == 1:
                if name in taxaList:
                    newTaxa = 0
                    if taxaList.index(name) == 0 :
                        phylipFile.write("\n")
                else:
                    taxaList.append(name)

            if newTaxa:
                ntax += 1
                phylipFile.write(name + " " + sequenceData + "\n")
            else:
                phylipFile.write(sequenceData + "\n")
                
    
    nexusFile.close()
    phylipFile.close()
    os.unlink(outputFilename)
    print "Error: nexus file ("+inputFilename+") not completely read."
    return errorOffset + 5


