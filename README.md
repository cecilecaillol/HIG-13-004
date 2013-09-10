HIG-13-004
==========

VH combination plots for HIG-13-004 

Installation
------------

Install the HiggsToTauTau limit package,


```shell
export SCRAM_ARCH=slc5_amd64_gcc472
cmsrel CMSSW_6_1_1
cd CMSSW_6_1_1/src/
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git HiggsAnalysis/HiggsToTauTau
git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries
scram b -j 4; rehash
```

then check out this package:

```shell
git clone https://github.com/cecilecaillol/HIG-13-004.git
```

and get the latest VH datacards:


Producing Results
-----------------

All the tricks to build the results are contained in the Makefile.  The
important commands are:

```shell
cd HIG-13-004

# Run the post fit and make all the final mass distribution plots
make massplots
# Compute all the limits
make limits
# Plot the limits (they show up in limits/*pdf)
make plotlimits

# Compute all the significances
make significance
# Plot the significances (they show up in limits/*pdf)
make plotsignificance

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

