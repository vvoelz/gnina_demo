# gnina_demo
A demo and tutorial for docking with GNINA

## Setup
 
If you haven't already, install the latest version of the Anaconda Python distribution [conda](https://docs.conda.io/projects/conda/en/stable/), or [miniconda](https://docs.anaconda.com/free/miniconda/).

NOTE: The installation package is a large `*.sh` file 
[https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh].
You can either download this to your local machine and `scp` to Owlsnest, or download it directly using `wget`.

In the [vina_demo](https://github.com/vvoelz/vina_demo) repository, we created a conda enviroment called `vina` to prepare the receptor and ligands.  We will use this same enviroment for the gnina work here.

## Create and set up your conda environment 

```
conda create --name vina
conda activate vina
```

And install the following packages:
* bioconda
* mgltools
* openbabel
* zlib
* pandas

```
conda install -c conda-forge -c bioconda mgltools openbabel zlib pandas --yes
```

If you don't already have `wget` installed (use `which wget` to check), install it:

```
pip install wget
```

##  Next Steps

NOTE: For each of these steps, make sure to read the _contents_ of each script before you run the script.  This way, you will know what is going on, and can debug if something goes wrong.

### Preparation

1. Load the GCC v8.4 C++ shared libaries using `module load gcc/8.4.0`
2. Run `./download_gnina` to get an executable copy of gnina.
3. Prepare the receptor using `python prepare_receptor.py`
4. Prepare the ligands using `python prepare_ligands.py`

### Docking

**IMPORTANT**! These steps should be run interactively on one of the nodes of Owlsnest, see below!

4. For the "smina" and "gnina_rescore" protocols, dock the ligands using `python docking.py` (use `qsub -I -q normal` )
5. For the "gnina_refinement" protocols, dock the ligands using `python docking_gpu.py` (use `qsub -I -q large` )


### Analysis

6. Run `./runme_before_analysis`.  This will:
   * install rdkit
   * make a PDB for the donepezil xtal pose ("input_files/donepezil_xtal.pdb")
   * install a tool called [DockRMSD](https://zhanggroup.org/DockRMSD/) so we can compute RMSD-to-xtal for molecules with symmetry or permuted atom orders.
7. Analyze the docking scores (and docking score vs. RMSD-to-xtal for donepezil) using `python analysis.py`.  This script will:
   * parse all the output sdf files to get the docking scores 
   * calculate RMSD-to-xtal for donepezil
   * print and save to csv format tables with the results (e.g. "docking_results/gnina_rescore_huperzine.csv")
8. You should visualize the docking results in ChimeraX (`scp` the `receptor.pdbqt` and the `scp -r` the entire `docking_results` folder files to your personal computer)
9. I have provided a jupyter notebook with some example code to plot the results: [plot_results.ipynb](plot_results.ipynb)

### Running interactively on Owlsnest

Running any program that requires substantial computational resources is NOT ALLOWED on Owlsnest.  This applies to our docking calculations as well. Since we're only docking ligands, the overall runtime should be short.  In this case, we can submit an interactive job on the `normal` queue, using

```
qsub -I -q normal
```

This command will submit a queued shell job, and allow you to interact within it for up to 30 minutes (the docking should take less than a minute).  When you are logged into the node, you will be back in your $HOME directory, and in your base conda environment. You will need to change back to your working directory, activate your 'vina' conda environment, and load the GCC libraries, like so:

```
cd ~/work/git/vina_demo   # or wherever your work is
conda activate vina
module load gcc/8.4.0
```

You now can continue to run scripts on the command line.  The jobs will run on the queued node, not the login node. 

To exit the interactive job, use
```
exit
```

### Running a queued job via batch script

If none of the gpu nodes in the `large` queue are free, you can submit a job to the queue using a batch script.  There is lots of good information about the Owlsnest batch system here: https://www.hpc.temple.edu/owlsnest2/batch_system/ 

I have included an example batch script in `batch.sh`, which contains the following text:

```
#!/bin/sh
#PBS -l walltime=1:00:00
#PBS -N docking_gpu 
#PBS -q large
#PBS -l nodes=1:ppn=1
#PBS -m bae
#PBS -M [AccessNetID]@temple.edu
#PBS
cd $PBS_O_WORKDIR

bash ~/.bashrc
conda activate vina
module load gcc/8.4.0
python docking_gpu.py
```

Replace the `[AccessNetID]` with your own Temple email/AccessNet to get an email notification when it's done.

Submit the batch script using
```
qsub batch.sh
```

To check the status of your job, use
```
qstat
```




