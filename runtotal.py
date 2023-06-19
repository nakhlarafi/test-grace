import subprocess
from tqdm import tqdm
import os, sys
import pickle

project = sys.argv[1]
lst = list(range(len(pickle.load(open(project + '.pkl', 'rb')))))
singlenums = {'Time':5, 'Math':2, "Lang":10, "Chart":3, "Mockito":4, "Closure":1}
singlenum = singlenums[project]
lr = 1e-2
seed = 0
batch_size = 60

# calculate total number of jobs for each GPU
totalnum = len(lst)
gpu_count = 1  # You mentioned you have 3 GPUs

# Iterate through all jobs
for i in tqdm(range(totalnum)):
    # Calculate which GPU to use for this job
    gpu_id = i % gpu_count

    # Start the job on the selected GPU
    command = "CUDA_VISIBLE_DEVICES=%d python run.py %d %s %f %d %d" % (gpu_id, lst[i], project, lr, seed, batch_size)
    p = subprocess.Popen(command, shell=True)

    # Wait for the job to finish before continuing
    p.wait()

# Run the summation and watch scripts after all jobs are done
p = subprocess.Popen("python sum.py %s %d %f %d" % (project, seed, lr, batch_size), shell=True)
p.wait()

subprocess.Popen("python watch.py %s %d %f %d" % (project, seed, lr, batch_size), shell=True)
