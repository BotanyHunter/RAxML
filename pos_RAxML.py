#!/usr/bin/python
import sys,os,re,optparse,tarfile,uuid,shutil
'''
Runs a series of RAxML calculations
'''

def main():

    try:
        returnValue = int(sys.argv[1])
    except:
        print "Error: could not find return value from run_RAxML"
        return 2

    try:
        basename = str(sys.argv[2])
    except:
        print "Error: could not find basename from run_RAxML"
        return 3

    if returnValue != 0: 
        print "Error: run_RAxML returned " + str(returnValue) + "."
        return returnValue

    RAxML_outputTypes = ["bootstrap",
                         "info",
                         "bipartitions",
                         "bipartitionsBranchLabels",
                         "bestTree"]

    if os.path.isfile("run_RAxML.tar"):
        if tarfile.is_tarfile("run_RAxML.tar"):
            try:
                myTarfile = tarfile.open("run_RAxML.tar", 'a:')
            except:
                return 4
        else:
            print "Error: file run_RAxML.tar, not recognized as a tar file."
            return 5
    else:
        try:
            myTarfile = tarfile.open("run_RAxML.tar", 'w:')
        except:
            print "Error: could not open RAxML.tar file."
            return 6
            
        for type in RAxML_outputTypes:
            t = tarfile.TarInfo(type)
            t.type = tarfile.DIRTYPE
            t.mode = 0767   #needs testing
            try:
                myTarfile.addfile(t)
            except:
                print "Error: could not add subdirectory to tar file."
                return 7

    for type in RAxML_outputTypes:
        filename = "RAxML_" + type + "." + basename
        if os.path.isfile(filename):
            try:
                myTarfile.add(filename, arcname="/"+type+"/"+basename+"."+type)
            except:
                print "Error: could not add file to tar file"
                return 8

            try:
                os.unlink(filename)
            except:
                print "Error: could not delete RAxML output file."
                return 9

    myTarfile.close()
    return 0
    
sys.exit(main())


