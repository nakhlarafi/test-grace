#!/bin/bash
SBATCH -J Grace --mem=120GB --account=r_mdnakh
SBATCH --gpus=40gb:1
python3 runtotal.py Time
nvidia-smi -L
sleep 20