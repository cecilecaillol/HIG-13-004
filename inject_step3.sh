#!/bin/bash

# Plot all the injected results.

pushd limits/

for type in llt cmb ltt 4l;
do
  echo "Plotting $type"
  plot --injected $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_injected_layout.py $type/
done

popd
