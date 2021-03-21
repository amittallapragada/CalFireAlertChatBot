#!/bin/bash
echo "Starting background jobs"
nohup python /app/update_jobs.py > /app/bg_jobs.out 2>&1 &