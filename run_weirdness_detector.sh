#!/bin/bash
#SBATCH --job-name=run_weirdness_detector
#SBATCH --output=/home/angelos.toutsios.gr/data/Thesis_dev/weirdness_detector/logs/log_%j.out  # Output log file
#SBATCH --error=/home/angelos.toutsios.gr/data/Thesis_dev/weirdness_detector/logs/log_%j.err   # Error log file
#SBATCH -N 1
#SBATCH --mem=60G
#SBATCH --cpus-per-task=64
#SBATCH --time=80:00:00              # Time limit (hh:mm:ss)
#SBATCH --partition=beards            # Specify the partition
#SBATCH --gres=gpu:1                 # Request 1 GPU

eval "$(pixi shell-hook -s bash)"

# pixi run python ollama-model.py
# pixi run python ollama-model-batch-structured.py
# pixi run python ollama-model-batch.py


pixi run python ollama-model-parallel.py