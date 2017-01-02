#!/usr/bin/python
import sys,os,re,optparse,tarfile,uuid,math,glob
from arguments_RAxML import *

def TF(inputTF):
    if( inputTF != None and inputTF!=False ): return "True"
    return "False"


'''
Builds the submit file for RAxML runs
'''

def main():

    current_version = "#version 1.0.1"    #1.0.1 added code for RAxML flag -#
    current_RAxML_version = "raxmlHPC"
    
    instanceID = uuid.uuid4()
    
    parser = getParser()
    options, remainder = parser.parse_args()

    noErrors = 1
    print("\n")
    #__________________________
    #fetch the working directory    
    #__________________________
    try:
        working_dir = os.path.dirname(os.path.realpath(__file__))
    except:
        print("ERROR: problem determining working directory")
        noErrors = 0

    #__________________________
    #  Work on data directory
    #__________________________
    data_dir = remainder[0]
    if( data_dir == None ):
        print("ERROR:   no data directory provided.  First argument after set_up_RAxML should be data directory")
        noErrors = 0
    else:
        if os.path.isdir(data_dir) != True :
            print("ERROR:   data directory (" + data_dir + ") does not exist.")
            noErrors = 0

    if noErrors == 1:
        myGenes = []
        myFiletypes = []
        filetypes = ('*.phy', '*.nex') # the tuple of file types
        for filetype in filetypes:
            for file in glob.glob(data_dir + "/" + filetype):
                if filetype == "*.nex" :
                    phyFilename = os.path.splitext(os.path.basename(file))[0] + ".phy"
                    if os.path.isfile(data_dir + "/" + phyFilename):
                        print("ERROR: phylip file already exists for a nexus file("+file+").  Data would be overwritten when nexus file created.")
                        noErrors = 0
                myGenes.append(os.path.basename(file))
                myFiletypes.append(filetype)

        if len(myGenes) == 0 :
            print "ERROR:   no phylip (*.phy) or nexus (*.nex) files found in data directory."
            noErrors = 0
        else:
            print "CHECKED: Found ", len(myGenes), "phylip files in directory:", working_dir+"/" + data_dir+"/."

    #__________________________
    #  Work on LOG/ERR/OUT directories
    #__________________________
    if( os.path.isdir("log") ):
        print "CHECKED: - log/ directory exists."
    else:
        os.makedirs("log")
        print "ACTION:   - log/ directory created."

    if( os.path.isdir("err") ):
        print "CHECKED: - err/ directory exists."
    else:
        os.makedirs("err")
        print "ACTION:   - err/ directory created."

    if( os.path.isdir("out") ):
        print "CHECKED: - out/ directory exists."
    else:
        os.makedirs("out")
        print "ACTION:   - out/ directory created."


    #If any errors prior to this point, stop
    if noErrors == 0 : sys.exit()

    #Build run_RAxML.dag which lists the individual genes to run
    st  = "#instanceID="+str(instanceID)+"\n"
    st += "#This dag runs the individual genes through RAxML\n\n"
    whichGene = 0
    for file in myGenes:
        whichGene += 1
        basename = os.path.splitext(file)[0]
        st += 'JOB         run_RAxML_' + str(whichGene) + ' run_RAxML.submit\n'
        st += 'VARS        run_RAxML_' + str(whichGene) + ' filename="' + file + '" basename = "' + basename + '"\n'
        st += 'SCRIPT POST run_RAxML_' + str(whichGene) + ' pos_RAxML.py $RETURN ' + basename+ '\n\n'

    submit_file = open('run_RAxML.dag', 'w')
    submit_file.write(st)
    submit_file.close()

    #_________________________
    #Build run_RAxML.submit
    #- This job file submits each individual gene
    #_________________________
    st  = "#instanceID="+str(instanceID)+"\n"
    st += "#Submit file for RAxML.\n\n"

    st += "universe = Vanilla\n\n"
    st += "executable = run_RAxML.py\n\n"
    st += "DDIR  = " + working_dir + "/" + data_dir + "\n"
    st += "should_transfer_files   = YES\n"
    st += "when_to_transfer_output = ON_EXIT\n\n"
    st += "transfer_input_files = run_RAxML.py, nexusToPhylip.py, raxmlHPC, $(DDIR)/$(filename)\n\n"
    st += "log    = log/raxml.$(basename).log\n"
    st += "error  = err/raxml.$(basename).err\n"
    st += "output = out/raxml.$(basename).out\n\n"
    st += "request_cpus   = 1\n"
    st += "request_disk   = 5000\n"
    st += "request_memory = 1000\n\n"
    #st += "+wantFlocking = true\n"
    #st += "+wantGlidein = true\n\n"

    st += 'arguments = "' + buildArgList("R", options) + " "
    st += '-s $(filename) -n $(basename)"\n'
    st += "queue \n\n"

    submit_file = open('run_RAxML.submit', 'w')
    submit_file.write(st)
    submit_file.close()

    print "\n\nProgram set_up finished successfully."
    print "run_RAxML.dag has been created.\n\n"
    


main()



