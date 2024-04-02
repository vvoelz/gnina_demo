import os, sys

def run_cmd(cmd, testing=False):
    """Run a shell command on the UNIX command line.

    OPTIONS
    testing          If True, just print the cmd. Default: False
    """

    print('>>', cmd)
    if not testing:
        os.system(cmd)


## NOTE: You may have to change the pathname of the script depending on your conda installation
##       Use 'which prepare_receptor4.py' to see the pathname
cmd = 'python2 ~/anaconda3/envs/vina/bin/prepare_receptor4.py -r input_files/4ey7_receptor_prepped.pdb -o ./receptor.pdbqt -U nphs_lps -v'

run_cmd(cmd)


