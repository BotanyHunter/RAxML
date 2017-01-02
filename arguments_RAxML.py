#Arguments_RAxML.py
#version 1.0.1

#  For use with runRAxML.py
#  Only very limited options have been coded.

import os, optparse

def getParser():
    parser = optparse.OptionParser()
    #general options
    #parser.add_option('-x', dest = 'rapidBootstrapRandomNumberSeed', type='int', default = 12345, help = 'Random seed for rapid bootstrap.')
    #parser.add_option('-p', dest = 'parsimonyRandomSeed'           , type='int', default = 12345, help = 'Random seed for parsimony.')
    #parser.add_option('-N', dest = 'numberOfRuns'                  , type='int', default = 1    , help = 'Number of runs.')
    #parser.add_option('-k', dest = 'BLOnBootstrapTrees'            ,             default = None , help = 'Output Bootstrap as branch length')
    #parser.add_option('-f', dest = 'algorithm'                     ,             default = "a"  , help = 'Algorithm to use')
    #parser.add_option('-m', dest = 'substitutionModel'             ,             default = "GTRGAMMA"  , help = 'Substitution model')
    #parser.add_option('-s', dest = 'filename'                      ,             default = None , help = 'filename of data.')
    #parser.add_option('-n', dest = 'outputFilename'                ,             default = None , help = 'Output filename.')
    parser.add_option('-R', dest = 'RAxMLCommand'                  ,             default = "-f a" , help = 'RAxML command in quotes.')
    
    return parser

def buildArgList(whichArgs, options):
    #build arguments for later submit files
    args = ""

    if( "R" in whichArgs ): 
        args += options.RAxMLCommand
        return args

    #if( "x" in whichArgs ):  args += " -x " + str(options.rapidBootstrapRandomNumberSeed)
    #if( "p" in whichArgs ):  args += " -p " + str(options.parsimonyRandomSeed)
    #if( "N" in whichArgs ):  args += " -N " + str(options.numberOfRuns)
    #if( "k" in whichArgs ):  args += " -k"
    #if( "f" in whichArgs ):  args += " -f " + options.algorithm
    #if( "m" in whichArgs ):  args += " -m " + options.substitutionModel
    #if( "n" in whichArgs ):  args += " -s " + options.filename
    #if( "s" in whichArgs ):  args += " -n " + options.outputFilename

    return args
    


