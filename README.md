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

then copy the fit results from HTT+VHTT fit, and the corrected postfit.py:
```shell
cp -r HIG-13-004/mlfit_cmb_131203 HiggsAnalysis/HiggsToTauTau/test/.
cp HIG-13-004/postfit_right_errors.py HiggsAnalysis/HiggsToTauTau/test/postfit.py
```


Producing Results
-----------------

All the tricks to build the results are contained in the Makefile.  The
important commands are:

```shell
cd HIG-13-004

# Run the post fit and make all the final mass distribution plots (1 ML fit for all channels together)
make massplots
# Or run the post fit and make all the final mass distribution plots (1 ML fit for each channel -> 3 ML fits)
make massplots_cat

# Compute all the limits (ZH, LLT, LTT, cmb + each sub-channel/category)
make limits
# Plot the limits (they show up in limits/*pdf)
make plotlimits

# Compute the combined significance
make significance
# Plot the significance (it shows up in limits/*pdf)
make plotsignificances

# Make vh_table.tex for the PAS (Moriond style)
make plots/vh_table.tex
```

or you can just run "make all", which runs everything.

Run sh organize_plot_directory.sh if you want to sort all the plots in the "plots" directory.

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

