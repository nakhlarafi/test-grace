import subprocess
from tqdm import tqdm
import time
import os, sys
import pickle

project = sys.argv[1]
card = [0,1]
lst = list(range(len(pickle.load(open(project + '.pkl', 'rb')))))
singlenums = {'Time':5, 'Math':2, "Lang":1, "Chart":3, "Mockito":4, "Closure":1}
singlenum = singlenums[project]
totalnum = len(card) * singlenum
lr = 1e-2
seed = 0
batch_size = 60
for i in tqdm(range(int(len(lst) / totalnum) + 1)):
    jobs = []
    for j in range(totalnum):
        if totalnum * i + j >= len(lst):
            continue
        cardn =int(j / singlenum)
        # p = subprocess.Popen("CUDA_VISIBLE_DEVICES="+str(card[cardn]) + " python3 run.py %d %s %f %d %d"%(lst[totalnum * i + j], project, lr, seed, batch_size), shell=True)
        p = subprocess.Popen("CUDA_VISIBLE_DEVICES=0,1,2 torchrun --nnodes=1 --nproc_per_node=3 --rdzv_id=100 --rdzv_backend=c10d --rdzv_endpoint=spear01:29405 run.py %d %s %f %d %d"%(lst[totalnum * i + j], project, lr, seed, batch_size), shell=True)
        jobs.append(p)
        time.sleep(10)
    for p in jobs:
        p.wait()
p = subprocess.Popen("python3 sum.py %s %d %f %d"%(project, seed, lr, batch_size), shell=True)
p.wait()
subprocess.Popen("python3 watch.py %s %d %f %d"%(project, seed, lr, batch_size),shell=True)            