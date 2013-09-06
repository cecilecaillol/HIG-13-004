#!/bin/bash -e

# Run the ML fit and compute all in the information for the pulls.

pushd pulls/125

combineCards.py *.txt > everything.txt

for card in `ls *.txt`
do
  echo "ML fitting $card in $PWD"
  name=`echo $card | sed "s|.txt||"`
  combine -M MaxLikelihoodFit --minimizerStrategy=2 --robustFit=1 --minimizerStrategyForMinos=2 $card -m 125 &> $name.combine.txt
  echo "Generating ML fit reports"
  python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -f html > $name.pulls.html
  python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -a -f html > $name.pulls.all.html
  # requires 1.6 of http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/test/diffNuisances.py?view=log&pathrev=MAIN
  #python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -g $name.pulls.png > $name.pulls.txt
  mv mlfit.root $card.fit.root
done

popd
