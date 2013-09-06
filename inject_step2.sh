#!/bin/bash

# Collect all the results from the signal injection toy jobs and get ready for
# plotting.

for type in llt cmb ltt 4l;
do
  echo "Collecting $type"
  submit.py --injected --condor --collect limits/$type/*
done
