import os, sys
import subprocess
import rdkit
from rdkit import Chem

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


# DockRMSD only works with *.mol2 files. So we need to
# ...convert the xtal structure pose to mol2
run_cmd('obabel input_files/donepezil_xtal.pdb  -O input_files/donepezil_xtal.mol2 --ff GAFF')

methods = ['smina', 'gnina_rescore', 'gnina_refinement']
results = {} # store results in a dictionary

for method in methods:

  # ... and convert # convert our docking poses to mol2
  run_cmd(f'obabel docking_results/smina_donepezil.sdf -O docking_results/{method}_donepezil.mol2 -m')

  for ligand in ['donepezil', 'galantamine', 'huperzine', 'rivastigmine', 'AC6']:

    resultname = f'{method}_{ligand}'
    results[resultname] = {'minimizedAffinity':[], 'CNNscore':[], 'CNNaffinity':[], 'RMSD-to-xtal':[]}

    # Load the SDF file
    sdf_file = Chem.SDMolSupplier(f'docking_results/{resultname}.sdf')

    # Iterate over the molecules in the file
    for mol in sdf_file:

        # get the smina affinity
        minimizedAffinity = mol.GetProp('minimizedAffinity')
        results[resultname]['minimizedAffinity'].append(float(minimizedAffinity))

        # get the gnina CNN affinities
        if method == 'smina':
            results[resultname]['CNNscore'].append(None)
            results[resultname]['CNNaffinity'].append(None)
        else:
            CNNscore = mol.GetProp('CNNscore')
            CNNaffinity = mol.GetProp('CNNaffinity')
            results[resultname]['CNNscore'].append(CNNscore)
            results[resultname]['CNNaffinity'].append(CNNaffinity)

        # fill RMSD-to-xtal fields with Nones
        results[resultname]['RMSD-to-xtal'].append(None)


    # If the ligand is donepezil, fill the RMSD-to-xtal fields
    if ligand == 'donepezil':

        # To get the rmsd-to-xtal of the docked pose, we need to parse the output of DockRMSD
        posed_mol2files = [f'docking_results/{resultname}{i}.mol2' for i in range(1,10)]
        for j in range(len(posed_mol2files)):

              # Create a subprocess to run the 'ls' command
              xtal_mol2 = 'input_files/donepezil_xtal.mol2'
              output = subprocess.check_output(['./DockRMSD', xtal_mol2, posed_mol2files[j]], text=True)

              # parse the RMSD from the line "Calculated Docking RMSD: ##.###\n"
              lines = [line for line in output.split('\n') if line.count("Calculated Docking RMSD:") > 0]
              rmsd = float(lines[0].strip().split()[-1])
              print('rmsd', rmsd)
              results[resultname]['RMSD-to-xtal'][j] = rmsd


    # PRINT and SAVE the results

    csvfile = f'docking_results/{resultname}.csv'
    print('-------------')
    print()
    print(f'Writing to {csvfile} ...')
    fout = open(csvfile, 'w')

    num_poses = 9
    if method == 'smina':

      if ligand == 'donepezil':
          header = 'pose,RMSD-to-xtal (A),minimizedAffinity (kcal/mol)'
          print(header)
          fout.write(header+'\n')
          for j in range(num_poses):
              line = f"{j+1},{results[resultname]['RMSD-to-xtal'][j]}, {results[resultname]['minimizedAffinity'][j]}"
              print(line)
              fout.write(line+'\n')
      else:
          header = 'pose,minimizedAffinity (kcal/mol)'
          print(header)
          fout.write(header+'\n')
          for j in range(num_poses):
              line = f"{j+1},{results[resultname]['minimizedAffinity'][j]}"
              print(line)
              fout.write(line+'\n')


    else:

      if ligand == 'donepezil':
          header = 'pose,RMSD-to-xtal (A),CNNscore,CNNaffinity (pKd)'
          print(header)
          fout.write(header+'\n')
          for j in range(num_poses):
              line = f"{j+1},{results[resultname]['RMSD-to-xtal'][j]}, {results[resultname]['CNNscore'][j]}, {results[resultname]['CNNaffinity'][j]}"
              print(line)
              fout.write(line+'\n')
      else:
          header = 'pose,CNNscore,CNNaffinity (pKd)'
          print(header)
          fout.write(header+'\n')
          for j in range(num_poses):
              line = f"{j+1},{results[resultname]['CNNaffinity'][j]}"
              print(line)
              fout.write(line+'\n')

    fout.close()


