#!/bin/bash
# Quick reference for submitting and monitoring prime finder jobs

# ============================================================
# SUBMIT JOBS
# ============================================================

# Basic job - runs for 10 minutes
sbatch slurm/prime_finder.slurm

# With checkpointing - resumes on timeout/failure
sbatch slurm/prime_finder_checkpoint.slurm

# ============================================================
# MONITOR JOBS
# ============================================================

# View all your jobs
squeue -u $USER

# View specific job details
squeue -j <job_id>

# View job status/history
sacct -j <job_id>

# Stream job output
tail -f prime_*.log

# ============================================================
# MANAGE JOBS
# ============================================================

# Cancel a job
scancel <job_id>

# Cancel all your jobs
scancel -u $USER

# Hold a job (prevent it from running)
scontrol hold <job_id>

# Release a held job
scontrol release <job_id>

# ============================================================
# USEFUL INFO
# ============================================================

# View cluster status
sinfo

# View your job limits
scontrol show user=$USER

# View completed job info
sacct --user=$USER --format=JobID,JobName,State,Start,End

# View job output
cat prime_*.log

# ============================================================
# CHECKPOINTING TIPS
# ============================================================

# Monitor checkpointing progress
ls -lh prime_checkpoints/

# View current checkpoint
cat prime_checkpoints/prime_checkpoint.json

# Clean up old checkpoints
rm -f prime_checkpoints/prime_checkpoint*.json

# Check requeue chain
scontrol show job <initial_job_id>
