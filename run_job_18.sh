#!/bin/bash
#SBATCH --account=def-mageed
#SBATCH --gpus-per-node=v100l:1
#SBATCH --mem=128G
#SBATCH --time=0-18:00
#SBATCH --cpus-per-task=32

bash /home/khaidoan/projects/def-mageed/khaidoan/chiyu/lm-evaluation-harness/run_18.sh >> /home/khaidoan/projects/def-mageed/khaidoan/chiyu/lm-evaluation-harness/log_18.txt 2>&1