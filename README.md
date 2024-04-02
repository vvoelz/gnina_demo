# gnina_demo
A demo and tutorial for Autodock Vina

## Setup
 
If you haven't already, install the latest version of the Anaconda Python distribution [conda](https://docs.conda.io/projects/conda/en/stable/), or [miniconda](https://docs.anaconda.com/free/miniconda/).

NOTE: The installation package is a large `*.sh` file 
[https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh].
You can either download this to your local machine and `scp` to Owlsnest, or download it directly using `wget`.

In the [vina_demo](https://github.com/vvoelz/vina_demo) repository, we created a conda enviroment called `vina` to prepare the receptor and ligands.  We will use this same enviroment for the gnina work here.

### Create and set up your conda environment 

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
conda install -c conda-forge -c bioconda mgltools openbabel zlib --yes

conda install pandas
```

If you don't already have `wget` installed (use `which wget` to check), install it:

```
pip install wget
```

###  Next Steps

NOTE: For each of these steps, make sure to read the _contents_ of each script before you run the script.  This way, you will know what is going on, and can debug if something goes wrong.

1. Follow the instructions in the `runme_setup` document to prepare the receptor
2. Prepare the ligands using `python prepare_ligands.py` 
3. Dock the ligands using `python docking.py` (**IMPORTANT**! This step should be run interactively on one of the nodes of Owlsnest, see below) 
4. Visualize the docking results in ChimeraX (`scp` the `receptor.pdbqt` and `[ligand]_out.pdbqt` files to your personal computer to view them)
5. Analyze the Vina score vs. RMSD-to-xtal using `python analysis.py`  (NOTE: this script downloads and uses a tool called [DockRMSD](https://zhanggroup.org/DockRMSD/) from the Zhang group at University of Michigan to compute RMSD for molecules with symmetry or permuted atom orders.)

### Running interactively on Owlsnest

Running any program that requires substantial computational resources is NOT ALLOWED on Owlsnest.  This applies to our docking calculations as well. Since we're only docking ligands, the overall runtime should be short.  In this case, we can submit an interactive job on the `normal` queue, using

```
qsub -I -q normal
```

This command will submit a queued shell job, and allow you to interact within it for up to 30 minutes (the docking should take less than a minute).  When you are logged into the node, you will be back in your $HOME directory, and in your base conda environment. You will need to change back to your working directory and activate your 'vina' conda environment like so:

```
cd ~/work/git/vina_demo   # or wherever your work is
conda activate vina
```

You now can continue to run scripts on the command line.  The jobs will run on the queued node, not the login node. 

To exit the interactive job, use
```
exit
```


### References

Full documentation of AutoDock Vina can be found here: https://autodock-vina.readthedocs.io/  

Heavily inspired by https://colab.research.google.com/github/pb3lab/workshops/blob/main/tutorials/spb2022/D1_Tutorial2.ipynb#scrollTo=LRlv9MqoCC19 





