AN-13-187
=========

AN-13-187 plotting and limit macros

Installation
------------

Install the HiggsToTauTau limit package,


```shell
cmsrel CMSSW_5_3_7
cd CMSSW_5_3_7/src/
cmsenv
cvs co -r V02-02-08 HiggsAnalysis/CombinedLimit
cvs co -r V00-03-10 HiggsAnalysis/HiggsToTauTau
python HiggsAnalysis/HiggsToTauTau/scripts/init.py --tag V00-01-00-noModels
# Remove any leftover shape files
rm HiggsAnalysis/HiggsToTauTau/setup/vhtt/*root
scram b -j 4; rehash
```

then check out this package:

```shell
git clone https://github.com/mverzett/AN-13-187.git
```

and get the latest VH datacards:

```shell
cd auxiliaries/datacards/collected/
cvs up -A -d vhtt
```

Producing Results
-----------------

All the tricks to build the results are contained in the Makefile.  The
important commands are:

```shell
cd AN-13-187

# Run the post fit and make all the final mass distribution plots
make massplots
# Compute all the limits
make limits
# Plot the limits (they show up in limits/*pdf)
make plotlimits
# Make vh_table.tex for the PAS
make plots/vh_table.tex
```

or you can just run "make all", which runs everything.

Signal Injection
----------------

Do the following to make the signal injected plots.  
```shell
# Run a bunch of jobs with different pseudoexperiments
./inject_step1.sh
# Wait for those jobs to all finish, then collect all the results
./inject_step2.sh
# Plot the results 
./inject_step3.sh
```

This example is for the UW cluster.  Omit the --condor option in the scripts to
run on LXBatch.  

