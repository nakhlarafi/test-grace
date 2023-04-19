#!/bin/bash
SBATCH -J Test-GPUs --mem=100M --account=r_mdnakh
SBATCH --gpus=40gb:1
python3 runtotal.py Time
nvidia-smi -L
sleep 20