#RAxML

HTCondor files to run RAxML on all files in a directory

##Getting Starting

Navigate to your working directory on the HTCondor submit node and type the following command:

git clone https://github.com/BotanyHunter/RAxML.git
which will create a new directory called RAxML and download:

five python scripts
this README file
the RAxML executable, raxmlHPC, version 8.1.15 (1.180.370 bytes)

##Your molecular data

Create a new directory inside the RAxML directory and give it a name such as data.

Place all files on which you would like to run RAxML (in phylip format) into the directory. The file extensions must be ".phylip".

##Set up the HTCondor job

set_up_RAxML.py is a python script that creates the Condor DAG and submit files.  To use enter the following command:

                python set_up_RAxML.py data_directory -R "raxml options"

replace data_directory with the path to the directory where your data is located.
replace raxml options with the raxml options to be used.

Example:

               python set_up_RAxML.py data_new -R "–x 12345 –p 12345 – N 200 –k -f a –m GTRGAMMA"

Please do not use the -s and -n options.
    The -s option, the input file, will be set to each of the input files.
    The -n option, the output file, will be set to the same name as the input file (less the .nex or .phy)

##Run the HTCondor job

running set_up_RAxML.py creates a Condor DAG file "run_RAxML.dag"

Submit the DAG file to condor
             condor_submit_dag run_RAxML.dag

##Output

The output will be placed into a tar file: run_RAxML.tar.

Please rename this file so that it is not overwritten.
