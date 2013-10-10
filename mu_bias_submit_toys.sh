#!/bin/bash


#DIRS="limits/mmt/125 limits/emt/125 limits/eet/125 limits/mtt/125 limits/ett/125 limits/vhtt_wh/125 limits/vhtt_wh_had/125 limits/vhtt_zh/125 limits/cmb/125"
DIRS="limits/mmt/125 limits/mmt_7TeV/125 limits/mmt_8TeV/125"

for i in `seq 100`; do
    lxb-limit.py --condor --name="condor_toys_$i" \
        --limit-options="--max-likelihood-toys --stable --rMin -30 --rMax 30 --toys 200" \
        $DIRS
done

lxb-limit.py --condor --name="condor_mlfit" \
    --limit-options="--max-likelihood --stable --rMin -30 --rMax 30" \
    $DIRS
