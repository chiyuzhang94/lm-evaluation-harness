#!/bin/bash
#SBATCH --account=def-mageed
#SBATCH --gpus-per-node=v100l:1
#SBATCH --mem=128G
#SBATCH --time=0-24:00
#SBATCH --cpus-per-task=32

bash /home/chiyu.zhang/chiyu/lm-evaluation-harness/run_cscc.sh >> /home/chiyu.zhang/chiyu/lm-evaluation-harness/log_cscc.txt 2>&1