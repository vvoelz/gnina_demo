import os, sys

# Helper function(s)

def run_cmd(cmd, testing=False):
    """Run a shell command on the UNIX command line.

    OPTIONS
    testing          If True, just print the cmd. Default: False
    """

    print('>>', cmd)
    if not testing:
        os.system(cmd)

# Main

if not os.path.exists('./docking_results'):
    os.mkdir('docking_results')

#methods = ['smina', 'gnina_rescore', 'gnina_refinement']
methods = ['gnina_refinement']
for method in methods:

  for ligand in ['donepezil', 'galantamine', 'huperzine', 'rivastigmine', 'AC6']:

    receptor_pdbqt = './receptor.pdbqt'
    ligand_pdbqt   = f'{ligand}/{ligand}.pdbqt' 

    if method == 'smina':
        flag = '--cnn_scoring=none'
    elif method == 'gnina_rescore':
        flag = '--cnn_scoring=rescore'
    else:
        flag = '--cnn_scoring=refinement'

    cmd = f'./gnina {flag} -r {receptor_pdbqt} -l {ligand_pdbqt} --autobox_ligand ./input_files/donepezil_xtal.pdb --seed 1 -o ./docking_results/{method}_{ligand}.sdf'
    run_cmd(cmd)
 

