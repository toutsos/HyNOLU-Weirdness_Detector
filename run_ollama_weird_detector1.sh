#!/bin/bash
#SBATCH --job-name=run_weirdness_detector
#SBATCH --output=/home/angelos.toutsios.gr/data/Thesis_dev/weirdness_detector/logs/log_%j.out  # Output log file
#SBATCH --error=/home/angelos.toutsios.gr/data/Thesis_dev/weirdness_detector/logs/log_%j.err   # Error log file
#SBATCH -N 1
#SBATCH --mem=120G
#SBATCH --cpus-per-task=64
#SBATCH --time=80:00:00              # Time limit (hh:mm:ss)
#SBATCH --partition=genai            # Specify the partition
#SBATCH --gres=gpu:1                 # Request 2 GPU

eval "$(pixi shell-hook -s bash)"

# Navigate to the Ollama binary directory
cd ~/data/Programs/ollama/bin/

# Set environment variables
export CUDA_VISIBLE_DEVICES=0
export OLLAMA_NUM_PARALLEL=8
export OLLAMA_GPU_OVERHEAD=512
export OLLAMA_FLASH_ATTENTION=true
export PATH=/home/angelos.toutsios.gr/data/Programs/ollama/bin:$PATH

# Source the bashrc to ensure environment settings are applied
source ~/.bashrc

# Start the Ollama server in the background and log output
./ollama serve > ollama.log 2>&1 &

# Give some time for the server to start
sleep 10

# Optionally check if the server is running (example for a process check)
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "Ollama server failed to start. Exiting..." >&2
    exit 1
fi

# Navigate back to the weirdness detector directory
cd ~/data/Thesis_dev/weirdness_detector/

# Run the parallel Python script and redirect output
pixi run python -u ollama-model-parallel1.py > output1.txt