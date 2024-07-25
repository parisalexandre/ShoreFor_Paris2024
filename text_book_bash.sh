#!/bin/bash

# Bash script to run text_book_par in parallel on an available set of
# MPI "tasks" within an allocated job. The total set of tasks in a job is divided
# up into tiles, each containing the number needed to run the user's executable.

# The script assumes a static scheduling model. Under this model, when
# evaluation number N completes, Dakota launches evaluation N + evaluation_concurrency.
# As such, the tile numbered N % evaluation_concurrency can assumed to be available. 
# Static scheduling of asynchronous evaluations is enabled in Dakota with the keywords
# 'local_evaluation_scheduling static'.

# The names of the Dakota parameters and results files are provided as command
# line arguments
params=$1
results=$2

# Extract the evaluation number from the parameters file name (assumes the file_tag
# keyword is present in the Dakota input file.
num=$(echo $params | awk -F. '{print $NF}')
echo $num


workdir=`pwd`

# -------------------------
# INPUT FILE PRE-PROCESSING
# -------------------------

# This demo does not need file pre-processing, but normally (see
# below) APREPRO or DPREPRO is used to "cut-and-paste" data from the
# params.in.# file written by DAKOTA into the template input file for
# the user's simulation code.

# aprepro run6crh_rigid_template.i temp_rigid.new
# grep -vi aprepro temp_rigid.new > run6crh_rigid.i
# dprepro $1 application_input.template application.in 

cp -rf ../parameters.txt.template .
cp -rf ../objective_function.py .
cp $params application.in
dprepro application.in parameters.txt.template parameters.txt

# -------------------
# RUN SIMULATION CODE
# -------------------


# !!! Requires that APPLIC_PROCS either divide evenly into PPN or be
# !!! an integer multiple of it


cd $workdir
python objective_function.py
# ---------------------------
# OUTPUT FILE POST PROCESSING
# ---------------------------

# Normally any application-specific post-processing to prepare the
# results.out file for Dakota would go here. Here we'll substitute a
# copy command:

#cp rmse.txt $results
#cp nmse.txt $results
#cp bss.txt $results
#cat rmse.txt bss.txt > $results
cp results.txt $results

