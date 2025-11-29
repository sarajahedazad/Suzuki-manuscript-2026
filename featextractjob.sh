#!/bin/bash -l
#$ -N job_featextract

module load miniconda
mamba activate featextract-env
python3 step1_feature_extraction.py $SGE_TASK_ID