#!/bin/bash


BASE=STANDARD-LIMITS
#BASE=ALL-LIMITS

#limit.py --max-likelihood --rMax 5 --userOpt '--rMin -5 --robustFit=1 --minimizerStrategy=2 --minimizerAlgo=Minuit' $BASE/vhtt/125
#limit.py --max-likelihood --rMax 5 --userOpt '--rMin -5 --robustFit=1 --minimizerStrategy=2 --minimizerAlgo=Minuit' $BASE/vbf/125
#limit.py --max-likelihood --rMax 5 --userOpt '--rMin -5 --robustFit=1 --minimizerStrategy=2 --minimizerAlgo=Minuit' $BASE/fermionic/125
#limit.py --max-likelihood --rMax 5 --userOpt '--rMin -5 --robustFit=1 --minimizerStrategy=2 --minimizerAlgo=Minuit' $BASE/boost/125

function fit {
  BASE=$1
  echo "Fitting $BASE"
  method=--multi-dim-fit
  #method=--max-likelihood
  limit.py $method --norepeat --rMin -5 --rMax 5 --stable  $BASE/vhtt/125 &> /dev/null
  limit.py $method --norepeat --rMin -5 --rMax 5 --stable  $BASE/vbf/125 
  limit.py $method --norepeat --rMin -5 --rMax 5 --stable  $BASE/fermionic/125 
  #limit.py $method --norepeat --rMin -5 --rMax 5 --stable  $BASE/boost/125 &> /dev/null
  #limit.py $method --norepeat --rMin -5 --rMax 5 --stable  $BASE/cmb/125 &> /dev/null
}


fit NO_ET
fit ALL-LIMITS
fit STANDARD-LIMITS

#limit.py --max-likelihood --rMax 5 --userOpt '--rMin -5 --robustFit=1 --minimizerTolerance=0.012 --minimizerStrategy=2 --minimizerAlgo=Minuit' ALL-LIMITS/cmb/125
