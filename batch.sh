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
 
