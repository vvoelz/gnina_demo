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

## We will use DockRMSD to compute RMSD to xtal pose for donepezil
if not os.path.exists('./DockRMSD'):
    run_cmd('wget https://seq2fun.dcmb.med.umich.edu//DockRMSD/DockRMSD.gz')
    run_cmd('gunzip DockRMSD.gz')
    run_cmd('chmod +x ./DockRMSD')

# DockRMSD only works with *.mol2 files. So we need to
# ...convert the xtal structure pose to mol2
run_cmd('obabel input_files/donepezil_xtal.pdb  -O input_files/donepezil_xtal.mol2 --ff GAFF')

# ... and convert # convert our docking poses to mol2
run_cmd('obabel docking_results/smina_donepezil.sdf -O docking_results/smina_donepezil.mol2 -m')
#run_cmd('obabel docking_results/gnina_rescore_donepezil.sdf -O docking_results/gnina_rescore_donepezil.mol2 -m')
#run_cmd('obabel docking_results/gnina_refinement_donepezil.sdf -O docking_results/gnina_refinement_donepezil.mol2 -m')

for ligand in ['donepezil', 'galantamine', 'huperzine', 'rivastigmine', 'AC6']:


#############
### ANALYSIS: docking score versus RMSD-to-xtal

# resultname = 'smina_donepezil'
resultname = 'gnina_rescore_donepezil'
# resultname = 'gnina_refinement_donepezil'

# To get the docking score(s), we need to parse the 'docking_results/gnina_donepezil.sdf' file using rdkit

import rdkit
from rdkit import Chem

# Load the SDF file
sdf_file = Chem.SDMolSupplier(f'docking_results/{resultname}.sdf')

minimizedAffinity_values = []
CNNscore_values = []
CNNaffinity_values = []

# Iterate over the molecules in the file
for mol in sdf_file:

    # get the smina affinity
    minimizedAffinity = mol.GetProp('minimizedAffinity')
    minimizedAffinity_values.append(float(minimizedAffinity))
    print('minimizedAffinity', minimizedAffinity, end=' ')

    # get the gnina CNN affinities
    if resultname.count('smina') == 0:
      CNNscore = mol.GetProp('CNNscore')
      CNNaffinity = mol.GetProp('CNNaffinity')
      CNNscore_values.append(float(CNNscore))
      CNNaffinity_values.append(float(CNNaffinity))
      print('CNNscore', CNNscore, 'CNNaffinity', CNNaffinity, end='')
    print()

import subprocess

# resultname = 'smina_donepezil'
resultname = 'gnina_rescore_donepezil'
# resultname = 'gnina_refinement_donepezil'

# To get the rmsd-to-xtal of the docked pose, we need to parse the output of DockRMSD
posed_mol2files = [f'docking_results/{resultname}{i}.mol2' for i in range(1,10)]
rmsd_values = []
for posed_mol2file in posed_mol2files:

    try:
      # Create a subprocess to run the 'ls' command
      xtal_mol2 = 'input_files/donepezil_xtal.mol2'
      output = subprocess.check_output(['./DockRMSD', xtal_mol2, posed_mol2file], text=True)

      # parse the RMSD from the line "Calculated Docking RMSD: ##.###\n"
      lines = [line for line in output.split('\n') if line.count("Calculated Docking RMSD:") > 0]
      rmsd = float(lines[0].strip().split()[-1])
      rmsd_values.append(rmsd)
    except:
      rmsd_values.append(None)

print('rmsd_values', rmsd_values)
print()

if resultname.count('smina') > 0:
    print('RMSD-to-xtal (A), minimizedAffinity_values (kcal/mol)')
    for i in range(len(minimizedAffinity_values)):
        print(f'pose {i}: {rmsd_values[i]},  {minimizedAffinity_values[i]}')

else:
    print('RMSD-to-xtal (A), CNNaffinity (pKd)')
    for i in range(len(minimizedAffinity_values)):
        print(f'pose {i}: {rmsd_values[i]},  {CNNaffinity_values[i]}')

