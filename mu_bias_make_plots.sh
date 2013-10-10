#!/bin/bash

#DIRS="limits/mmt/125 limits/emt/125 limits/eet/125 limits/mtt/125 limits/ett/125 limits/vhtt_wh/125 limits/vhtt_wh_had/125 limits/vhtt_zh/125"
DIRS="limits/mmt/125 limits/mmt_7TeV/125 limits/mmt_8TeV/125 limits/mmt_8TeV_low/125 limits/mmt_8TeV_high/125 limits/emt/125 limits/vhtt_wh/125 limits/eet/125"

for dir in $DIRS; do
    nicename=`echo $dir | sed "s|limits/||" | sed "s|/125||"`
    echo $dir
    ./mu_bias_plot_toys.py $nicename mu_toys_$nicename.pdf \
        $dir/higgsCombineTest.MaxLikelihoodFit.mH125.root \
        $dir/higgsCombineTest.MaxLikelihoodFit.mH125.*[0-9]*root
    # pushd $dir
    # hadd -f mlfit_toys.root out/*/mlfit.root
    # the_macro="$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/plotParametersFromToys.C+"
    # root -q -b "$the_macro(\"mlfit_toys.root\", \"out/mlfit.root\", \"\", \"mu < -5\")"
    # # root -q -b "$the_macro(\"mlfit_toys.root\", \"\", \"\", \"mu < -5\")"
    # popd
done
