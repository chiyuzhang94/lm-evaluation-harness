#!/bin/bash
#SBATCH --account=def-mageed
#SBATCH --gpus-per-node=v100l:1
#SBATCH --mem=128G
#SBATCH --time=0-36:00
#SBATCH --cpus-per-task=32

bash /home/khaidoan/projects/def-mageed/khaidoan/chiyu/lm-evaluation-harness/run_19.sh >> /home/khaidoan/projects/def-mageed/khaidoan/chiyu/lm-evaluation-harness/log_19.txt 2>&1