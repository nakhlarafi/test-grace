#!/bin/bash
#SBATCH -J Grace --mem=120G --account=r_mdnakh
#SBATCH --gpus=40gb:1
module load anaconda/3.2022.10
python3 runtotal.py Time
