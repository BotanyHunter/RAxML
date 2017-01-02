##################################################
#  Runs RAxML on a directory of .nex or .phy files
##################################################

1)  ________________

set_up_RAxML.py is a python script that creates the Condor DAG and submit files.  To use enter the following command:

                python set_up_RAxML.py data_directory -R "raxml options"

replace data_directory with the path to the directory where your data is located.
replace raxml options with the raxml options to be used.

Example:

               python set_up_RAxML.py data_new -R "–x 12345 –p 12345 – N 200 –k -f a –m GTRGAMMA"

Please do not use the -s and -n options.
    The -s option, the input file, will be set to each of the input files.
    The -n option, the output file, will be set to the same name as the input file (less the .nex or .phy)

2)_______________

running set_up_RAxML.py creates a Condor DAG file "run_RAxML.dag"

3)_______________

Submit the DAG file to condor
             condor_submit_dag run_RAxML.dag

4)_______________

The output will be placed into a tar file: run_RAxML.tar.

Please rename this file so that it is not overwritten.
