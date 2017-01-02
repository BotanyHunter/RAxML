#!/usr/bin/python
import sys,os,re,subprocess
import nexusToPhylip
'''
Runs a series of RAxML calculations
'''

def main():

    current_version        = "#version 1.0.0"
    current_RAxML_version = "raxmlHPC"
    errorAtStep            = None

    #__________________________
    #fetch the working directory    
    #__________________________
    try:
        working_dir = os.path.dirname(os.path.realpath(__file__))
    except:
        print "ERROR: problem determining working directory"
        return 2

    #  We need to accomplish the following steps
    #  1)  write the RAxML command line
    #  2)  if file is nexus, convert to phylip
    #  3)  launch RAxML
    #  4)  clean up.

    #step 1: write command line
    cmd_RAxML  = "./" + current_RAxML_version
    arg_RAxML = ""
    for arg in sys.argv[1:]:
        arg_RAxML += " " + arg
    arg_RAxML = arg_RAxML.strip()

    #get outputfile names
    try:
        outputFilename = re.search('-n ([^\s]+)(?:\s+|$)', arg_RAxML).group(1)
    except:
        print "ERROR: problem finding output name."
        return 3


    #get datafile names
    try:
        dataFilename = re.search('-s ([^\s]+)(?:\s+|$)', arg_RAxML).group(1)
    except:
        print "ERROR: problem finding input data."
        return 4

    try:
        filenameSplit = os.path.splitext(dataFilename)
        fileExtension = filenameSplit[1]
    except:
        print "ERROR: Could not determine filetype of data."
        return 5

    if fileExtension == ".nex" :
        basename = filenameSplit[0]
        retValue = nexusToPhylip.nexusToPhylip(dataFilename, basename + ".phy")
        if retValue != 0 : 
            print "error in conversion to phylip format."
            return 20 + retValue
        arg_RAxML = re.sub(r'\.nex(?:\s+|$)', '.phy ', arg_RAxML)

    # Step 3: run RAxML
    try:
        retValue = subprocess.call(cmd_RAxML+" "+arg_RAxML, shell=True)
    except OSError as e:
        print "Error executing RAxML"
        print "Execution failed:", e
        return 6
    except:
        print "Unknown RAxML execution error"
        return 7

    # Step 5: remove unwanted output
    if retValue == 0:

        try:
           if fileExtension == ".nex": 
               #os.unlink(basename + ".phy")
               if os.path.exists(basename + ".phy.reduced"):
                   os.remove(basename + ".phy.reduced")
        except:
           print "ERROR: problem deleting temporary phylip file."
           return 8

    return 0
    
sys.exit(main())


