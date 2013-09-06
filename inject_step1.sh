#!/bin/bash

# Submit 500 signal injection toy jobs for each limit type.

find limits -type d  -exec fs setacl -dir '{}' -acl condor-hosts rlidkw \;

for type in cmb #llt cmb ltt 4l;
do
  echo "Submitting $type"
  echo "FIXME I'm skipping 110"
  # For now, filter out 110 GeV, since it isn't in the all hadronic cards.
  ls limits/$type/* -d | grep -v 110 | xargs submit.py --injected --condor --toys 500 --bunch-masses 10 --printOnly
done
