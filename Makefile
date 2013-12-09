# Makefile to generate limit cards for VH
#
# Targets:
#
# llt, ltt, zh: generate cards and put them in auxiliaries/datacards
# cards: generate all cards (from above)
#
# limitdir: generate limit computation project area
#
# pulls: compute the pulls.  Stored in pulls/125
#
# massplots: make the pre and postfit plots
#
# limits: compute all the limits
#
# plotlimits: make limit plots
#
# plots/vh_table.tex: generate tex table
#
# all: do everything!

# Working directory
BASE=$(CMSSW_BASE)/src
WD=$(BASE)/HIG-13-004

# Location of the CGS and uncertainty configuration files
SETUP=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup/vhtt
SETUP1=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup
SETUPBBB=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup_bbb
SETUPBBB2=$(BASE)/HiggsAnalysis/HiggsToTauTau/setup_bbb2
HTT_TEST=$(BASE)/HiggsAnalysis/HiggsToTauTau/test

# where the limit directory lives (in HIG-12-053) 
LIMITDIR=$(WD)/limits

# where the raw generated cards are generated.
CARDDIR=$(BASE)/auxiliaries/datacards
CARDS=$(BASE)/auxiliaries/datacards/sm/vhtt
COLLECT=$(BASE)/auxiliaries/shapes/VHTT


################################################################################
#####  Recipes for combining all shape files ###################################
################################################################################

# Combine all 8TeV shape files
$(SETUP)/vhtt.inputs-sm-8TeV.root: $(COLLECT)/vhtt_llt.inputs-sm-8TeV.root $(COLLECT)/vhtt_llLL.inputs-sm-8TeV.root $(COLLECT)/vhtt_ltt.inputs-sm-8TeV.root
	hadd -f $@ $^

# Combine all 7TeV shape files 
$(SETUP)/vhtt.inputs-sm-7TeV.root: $(COLLECT)/vhtt_llt.inputs-sm-7TeV.root $(COLLECT)/vhtt_llLL.inputs-sm-7TeV.root $(COLLECT)/vhtt_ltt.inputs-sm-7TeV.root
	hadd -f $@ $^

SHAPEFILE7=$(SETUP)/vhtt.inputs-sm-7TeV.root 
SHAPEFILE8=$(SETUP)/vhtt.inputs-sm-8TeV.root 


################################################################################
#####  Recipes for building EMT and MMT cards ##################################
################################################################################

LLT_CONFIGS7=$(wildcard $(SETUP)/*-sm-7TeV-00.* $(SETUP)/*-sm-7TeV-01.* $(SETUP)/*-sm-7TeV-02.*)
LLT_CONFIGS8=$(wildcard $(SETUP)/*-sm-8TeV-00.* $(SETUP)/*-sm-8TeV-01.* $(SETUP)/*-sm-8TeV-02.*)

# Recipe for building LLT cards
$(CARDS)/.llt7_timestamp: $(SHAPEFILE7) $(LLT_CONFIGS7)
	@echo "Recipes for building EET, EMT and MMT cards 7TeV"
	rm -f $(CARDS)/vhtt_0_7TeV*
	rm -f $(CARDS)/vhtt_1_7TeV*
	rm -f $(CARDS)/vhtt_2_7TeV*
	# $@ is the .timestamp file
	rm -f $@
	# change to base, run the setup command, and touch the .timestamp if 
	# successful
	cd $(BASE) && $(WD)/add_bbb_errors_VH.py -f 'vhtt:7TeV:00,01:fakes' -i $(SETUPBBB) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 7TeV --a sm 90-145:5 -c vhtt --sm-categories-vhtt "0 1" && touch $@

$(CARDS)/.llt8_timestamp: $(SHAPEFILE8) $(LLT_CONFIGS8)
	@echo "Recipes for building EET, EMT and MMT cards 8TeV"
	rm -f $(CARDS)/vhtt_0_8TeV*
	rm -f $(CARDS)/vhtt_1_8TeV*
	rm -f $(CARDS)/vhtt_2_8TeV*
	rm -f $@
	cd $(BASE) && $(WD)/add_bbb_errors_VH.py -f 'vhtt:8TeV:00:fakes' -i $(SETUPBBB) -o $(SETUPBBB) --threshold 0.10 --normalize && $(WD)/add_bbb_errors_VH.py -f 'vhtt:8TeV:01:charge_fakes>fakes' -i $(SETUPBBB) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 8TeV --a sm 90-145:5 -c vhtt --sm-categories-vhtt "0 1" && touch $@

llt: $(CARDS)/.llt7_timestamp $(CARDS)/.llt8_timestamp
#llt: $(CARDS)/.llt8_timestamp

################################################################################
#####  Recipes for building ZH cards ###########################################
################################################################################

ZH_CONFIGS7=$(wildcard $(SETUP)/*-sm-7TeV-03.* $(SETUP)/*-sm-7TeV-04.* $(SETUP)/*-sm-7TeV-05.* $(SETUP)/*-sm-7TeV-06.*)
ZH_CONFIGS8=$(wildcard $(SETUP)/*-sm-8TeV-03.* $(SETUP)/*-sm-8TeV-04.* $(SETUP)/*-sm-8TeV-05.* $(SETUP)/*-sm-8TeV-06.*)

# Recipe for building ZH cards
$(CARDS)/.zh7_timestamp: $(SHAPEFILE7) $(ZH_CONFIGS7)
	@echo "Recipes for building ZH cards 7TeV"
	rm -f $(CARDS)/vhtt_3_7TeV*
	rm -f $(CARDS)/vhtt_4_7TeV*
	rm -f $(CARDS)/vhtt_5_7TeV*
	rm -f $(CARDS)/vhtt_6_7TeV*
	rm -f $@
	cd $(BASE) && $(WD)/add_bbb_errors_VH.py -f 'vhtt:7TeV:03,04,05,06:Zjets' -i $(SETUPBBB) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 7TeV --a sm 90-145:5 -c vhtt --sm-categories-vhtt "3 4 5 6" && touch $@

$(CARDS)/.zh8_timestamp: $(SHAPEFILE8) $(ZH_CONFIGS8)
	@echo "Recipes for building ZH cards 8TeV"
	rm -f $(CARDS)/vhtt_3_8TeV*
	rm -f $(CARDS)/vhtt_4_8TeV*
	rm -f $(CARDS)/vhtt_5_8TeV*
	rm -f $(CARDS)/vhtt_6_8TeV*
	rm -f $@
	cd $(BASE)  && $(WD)/add_bbb_errors_VH.py -f 'vhtt:8TeV:03,04,05,06:Zjets' -i $(SETUPBBB) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 8TeV --a sm 90-145:5 -c vhtt --sm-categories-vhtt "3 4 5 6" && touch $@

zh: $(CARDS)/.zh7_timestamp $(CARDS)/.zh8_timestamp
#zh: $(CARDS)/.zh8_timestamp

################################################################################
#####  Recipes for building LTT cards ##########################################
################################################################################

LTT_CONFIGS7=$(wildcard $(SETUP)/*-sm-7TeV-07.* $(SETUP)/*-sm-7TeV-08.*)
LTT_CONFIGS8=$(wildcard $(SETUP)/*-sm-8TeV-07.* $(SETUP)/*-sm-8TeV-08.*)

# Recipe for building LTT cards
$(CARDS)/.ltt7_timestamp: $(SHAPEFILE7) $(LTT_CONFIGS7)
	@echo "Recipes for building LTT cards 7TeV"
	rm -f $(CARDS)/vhtt_7_7TeV*
	rm -f $(CARDS)/vhtt_8_7TeV*
	rm -f $@
	cd $(BASE) && $(WD)/add_bbb_errors_VH.py -f 'vhtt:7TeV:07,08:wz' -i $(SETUP1) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 7TeV --a sm 90-145:5 -c vhtt --sm-categories-vhtt "7 8" && touch $@

$(CARDS)/.ltt8_timestamp: $(SHAPEFILE8) $(LTT_CONFIGS8)
	@echo "Recipes for building LTT cards 8TeV"
	rm -f $(CARDS)/vhtt_7_8TeV*
	rm -f $(CARDS)/vhtt_8_8TeV*
	rm -f $@
	cp $(SETUP1)/vhtt/vhtt.inputs-sm-8TeV.root $(SETUPBBB)/vhtt/.
	cd $(BASE) && $(WD)/add_bbb_errors_VH.py  -f 'vhtt:8TeV:07,08:wz' -i $(SETUPBBB) -o $(SETUPBBB) --threshold 0.10 --normalize && setup-datacards.py -i $(SETUPBBB) -p 8TeV --a sm 90-145:5 -c vhtt --sm-categories-vhtt "7 8" && touch $@

ltt: $(CARDS)/.ltt7_timestamp $(CARDS)/.ltt8_timestamp
#ltt: $(CARDS)/.ltt8_timestamp

cards: zh ltt llt

################################################################################
#####  Recipes for generating the limit combo directory ########################
################################################################################

$(LIMITDIR)/.timestamp:  $(CARDS)/.ltt7_timestamp $(CARDS)/.ltt8_timestamp\
  $(CARDS)/.zh7_timestamp $(CARDS)/.zh8_timestamp\
  $(CARDS)/.llt7_timestamp $(CARDS)/.llt8_timestamp
	rm -rf $(LIMITDIR)
	cd $(BASE) && $(WD)/setup_htt_channels.py -o $(LIMITDIR) -c vhtt --sm-categories-vhtt "0 1 3 4 5 6 7 8" 90-145:5 && setup-htt.py -o $(LIMITDIR) -c vhtt --sm-categories-vhtt "0 1 3 4 5 6 7 8" 90-145:5 && touch $@

limitdir: $(LIMITDIR)/.timestamp

################################################################################
#####  The single card which has everything at 125 -used to make plots #########
################################################################################

megacard_125.txt: $(LIMITDIR)/.timestamp
	combineCards.py \
        ltt_7_7TeV=$(LIMITDIR)/cmb/125/vhtt_7_7TeV.txt \
        ltt_7_8TeV=$(LIMITDIR)/cmb/125/vhtt_7_8TeV.txt \
        ltt_8_7TeV=$(LIMITDIR)/cmb/125/vhtt_8_7TeV.txt \
        ltt_8_8TeV=$(LIMITDIR)/cmb/125/vhtt_8_8TeV.txt \
        zh_6_7TeV=$(LIMITDIR)/cmb/125/vhtt_6_7TeV.txt \
        zh_6_8TeV=$(LIMITDIR)/cmb/125/vhtt_6_8TeV.txt \
        zh_5_7TeV=$(LIMITDIR)/cmb/125/vhtt_5_7TeV.txt \
        zh_5_8TeV=$(LIMITDIR)/cmb/125/vhtt_5_8TeV.txt \
        zh_4_7TeV=$(LIMITDIR)/cmb/125/vhtt_4_7TeV.txt \
        zh_4_8TeV=$(LIMITDIR)/cmb/125/vhtt_4_8TeV.txt \
        zh_3_7TeV=$(LIMITDIR)/cmb/125/vhtt_3_7TeV.txt \
        zh_3_8TeV=$(LIMITDIR)/cmb/125/vhtt_3_8TeV.txt \
        llt_0_7TeV=$(LIMITDIR)/cmb/125/vhtt_0_7TeV.txt \
	llt_0_8TeV=$(LIMITDIR)/cmb/125/vhtt_0_8TeV.txt \
        llt_1_7TeV=$(LIMITDIR)/cmb/125/vhtt_1_7TeV.txt \
        llt_1_8TeV=$(LIMITDIR)/cmb/125/vhtt_1_8TeV.txt > $@
	
################################################################################
#####  Computing the pulls  ####################################################
################################################################################

pulls/.timestamp: $(LIMITDIR)/.timestamp do_pull.sh
	rm -rf pulls
	mkdir -p pulls
	cp -r $(LIMITDIR)/cmb/125 pulls/125
	cp -r $(LIMITDIR)/cmb/common pulls/common	
	./do_pull.sh && touch $@

pulls: pulls/.timestamp

################################################################################
#####  Computing the limits ####################################################
################################################################################

NPROCS=10

$(LIMITDIR)/.computed: $(LIMITDIR)/.timestamp
	echo "Computing combined limits"
	./compute_limits.sh cmb $(NPROCS)
	echo "Computing ZH combined limits"
	./compute_limits.sh vhtt_zh $(NPROCS)
	echo "Computing LTT limits"
	./compute_limits.sh vhtt_wh_had $(NPROCS)
	echo "Computing LLT limits"
	./compute_limits.sh vhtt_wh $(NPROCS)
	touch $@

$(LIMITDIR)/.chan_computed: $(LIMITDIR)/.timestamp
	echo "Computing ZH combined limits"
	./compute_limits.sh llem $(NPROCS)
	./compute_limits.sh llmt $(NPROCS)
	./compute_limits.sh llet $(NPROCS)
	./compute_limits.sh lltt $(NPROCS)
	echo "Computing LTT limits"
	./compute_limits.sh mtt $(NPROCS)
	./compute_limits.sh ett $(NPROCS)
	echo "Computing LLT limits"
	./compute_limits.sh mmt $(NPROCS)
	./compute_limits.sh emt $(NPROCS)
	touch $@

limits: $(LIMITDIR)/.computed $(LIMITDIR)/.chan_computed

################################################################################
#####  Computing the significances #############################################
################################################################################

$(LIMITDIR)/.computed_signif: $(LIMITDIR)/.timestamp
	echo "Computing combined significance"
	./compute_significance.sh cmb 
	touch $@

significance: $(LIMITDIR)/.computed_signif


################################################################################
#####  Plotting the limits #####################################################
################################################################################

# This dumb macro needs to be compiled.
$(BASE)/HiggsAnalysis/HiggsToTauTau/macros/compareLimits_C.so: $(BASE)/HiggsAnalysis/HiggsToTauTau/macros/compareLimits.C
	cd $(BASE) && source HiggsAnalysis/HiggsToTauTau/environment.sh

comparemacro: $(BASE)/HiggsAnalysis/HiggsToTauTau/macros/compareLimits_C.so

$(LIMITDIR)/.plot_timestamp: $(LIMITDIR)/.computed $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_*.py
	rm -f $@
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py cmb/ 
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py vhtt_zh/
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py vhtt_zh/
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py vhtt_wh/
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py vhtt_wh/
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py vhtt_wh_had/
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py vhtt_wh_had/
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py cmb/
	# Combine the output of all the individual limit results into a single file.
	rm -f $(LIMITDIR)/limits_limit.root 
	hadd $(LIMITDIR)/limits_limit.root $(LIMITDIR)/*h_limit.root $(LIMITDIR)/*b_limit.root $(LIMITDIR)/*d_limit.root
	cd $(LIMITDIR) && root -b -q '../../HiggsAnalysis/HiggsToTauTau/macros/compareLimits.C+("limits_limit.root", "cmb,vhtt_zh,vhtt_wh_had,vhtt_wh", true, false, "sm-xsex", 0, 25, false,"  Preliminary, VH#rightarrow#tau#tau, #sqrt{s} = 7-8 TeV, L=24.7 fb^{-1}")'
	touch $@

plots/.limits_timestamp: $(LIMITDIR)/.plot_timestamp
	mkdir -p plots
	cp $(LIMITDIR)/vhtt_zh_exp_limit.pdf plots/
	cp $(LIMITDIR)/vhtt_zh_exp_limit.tex plots/
	cp $(LIMITDIR)/vhtt_wh_exp_limit.pdf plots/
	cp $(LIMITDIR)/vhtt_wh_exp_limit.tex plots/
	cp $(LIMITDIR)/vhtt_wh_had_exp_limit.pdf plots/
	cp $(LIMITDIR)/vhtt_wh_had_exp_limit.tex plots/
	cp $(LIMITDIR)/cmb_exp_limit.pdf plots/
	cp $(LIMITDIR)/cmb_exp_limit.tex plots/
	cp $(LIMITDIR)/vhtt_zh_limit.pdf plots/
	cp $(LIMITDIR)/vhtt_zh_limit.tex plots/
	cp $(LIMITDIR)/vhtt_wh_limit.pdf plots/
	cp $(LIMITDIR)/vhtt_wh_limit.tex plots/
	cp $(LIMITDIR)/vhtt_wh_had_limit.pdf plots/
	cp $(LIMITDIR)/vhtt_wh_had_limit.tex plots/
	cp $(LIMITDIR)/cmb_limit.pdf plots/
	cp $(LIMITDIR)/cmb_limit.tex plots/
	cp $(LIMITDIR)/singleLimits_expected_sm.pdf plots/exp_limit_breakdown.pdf
	#cp $(LIMITDIR)/singleLimits_observed_sm.pdf plots/obs_limit_breakdown.pdf
	touch $@

$(LIMITDIR)/.chan_plot_timestamp: $(LIMITDIR)/.chan_computed $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_*.py
	rm -f $@
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py llem/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py llmt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py llet/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py lltt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py mmt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py emt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py mtt/ max=30.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py ett/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llem/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llmt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llet/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py lltt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py mmt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py emt/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py mtt/ max=30.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py ett/ max=40.0
	cd $(LIMITDIR) && plot --asymptotic $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_exp_layout.py cmb/
	rm -f $(LIMITDIR)/limits_limit.root 
	hadd $(LIMITDIR)/limits_limit.root $(LIMITDIR)/*h_limit.root $(LIMITDIR)/*t_limit.root $(LIMITDIR)/*m_limit.root $(LIMITDIR)/*b_limit.root $(LIMITDIR)/*d_limit.root
	root -b -q 'compareVHlimits.C+("limits/limits_limit.root", "vhtt_wh_had,vhtt_zh,vhtt_wh,cmb", true, false, "sm-xsex", 0, 20, false,"CMS, 4.9 fb^{-1} at 7TeV, 19.7 fb^{-1} at 8TeV",false,true)'
	mv singleLimits_expected_sm.pdf plots/compa_ZH_WH.pdf
	root -b -q 'compareVHlimits.C+("limits/limits_limit.root", "ett,mtt,vhtt_wh_had", true, false, "sm-xsex", 0, 30, false,"CMS, 4.9 fb^{-1} at 7TeV, 19.7 fb^{-1} at 8TeV",false,true)'
	mv singleLimits_expected_sm.pdf plots/compa_wh_had.pdf
	root -b -q 'compareVHlimits.C+("limits/limits_limit.root", "mmt,emt,vhtt_wh", true, false, "sm-xsex", 0, 30, false,"CMS, 4.9 fb^{-1} at 7TeV, 19.7 fb^{-1} at 8TeV",false,true)'
	mv singleLimits_expected_sm.pdf plots/compa_wh_lep.pdf
	root -b -q 'compareVHlimits.C+("limits/limits_limit.root", "llem,llet,lltt,llmt,vhtt_zh", true, false, "sm-xsex", 0, 30, false,"CMS, 4.9 fb^{-1} at 7TeV, 19.7 fb^{-1} at 8TeV",false,true)'
	mv singleLimits_expected_sm.pdf plots/compa_zh.pdf
	touch $@

plots/.chan_limits_timestamp: $(LIMITDIR)/.chan_plot_timestamp
	mkdir -p plots
	cp $(LIMITDIR)/*limit.pdf plots/
	cp $(LIMITDIR)/*limit.tex plots/
	touch $@

plotlimits: plots/.limits_timestamp plots/.chan_limits_timestamp

################################################################################
#####  Plotting the significances ##############################################
################################################################################

$(LIMITDIR)/.plot_signif_timestamp: $(LIMITDIR)/.computed_signif $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_*.py
	rm -f $@
	cd $(LIMITDIR) && plot --significance-frequentist $(BASE)/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_significance_layout.py cmb/ 
	touch $@

plots/.significances_timestamp: $(LIMITDIR)/.plot_signif_timestamp
	cp $(LIMITDIR)/cmb_significance.tex plots/
	cp $(LIMITDIR)/cmb_significance.pdf plots/
	touch $@

plotsignificances: plots/.significances_timestamp


################################################################################
#####  Making the post fit shape files for the nice plots ######################
################################################################################

# ML fit and copy the 125 combined mass point into the postfit zone
$(HTT_TEST)/.fit_timestamp: $(LIMITDIR)/.timestamp
	cd $(HTT_TEST) && ./mlfit_and_copy.py $(LIMITDIR)/cmb/125 && touch $@
	cp $(HTT_TEST)/fitresults/mlfit_sm.txt mlfit_vh.txt
	prune-uncerts-htt.py --fit-results='$(WD)/limits/cmb/125/out/mlfit.txt' --threshold=0.10 --whitelist='_bin_' limits/cmb/125 --shielding 125:0.3 && sh pruning.sh

# Make .root files with the applied pulls
$(HTT_TEST)/root_postfit/.timestamp: $(HTT_TEST)/.fit_timestamp
	# make a copy of the directory so we can mess with them.
	rm -fr $(HTT_TEST)/root_postfit
	cp -r $(HTT_TEST)/root $(HTT_TEST)/root_postfit
	# apply all the pulls to the shapes
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_3_8TeV.txt \
	  --bins eeem_zh mmme_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_4_8TeV.txt \
	  --bins eemt_zh mmmt_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_5_8TeV.txt \
	  --bins eeet_zh mmet_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_6_8TeV.txt \
	  --bins eett_zh mmtt_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_3_7TeV.txt \
          --bins eeem_zh mmme_zh \
          --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_4_7TeV.txt \
          --bins eemt_zh mmmt_zh \
          --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_5_7TeV.txt \
          --bins eeet_zh mmet_zh \
          --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_6_7TeV.txt \
          --bins eett_zh mmtt_zh \
          --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_7_8TeV.txt \
	  --bins mtt --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_8_8TeV.txt \
	  --bins ett --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_7_7TeV.txt \
	  --bins mtt --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_8_7TeV.txt \
	  --bins ett --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_0_8TeV.txt \
          --bins mmtCatHigh mmtCatLow \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_1_8TeV.txt \
          --bins emtCatHigh emtCatLow \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_0_7TeV.txt \
	--bins mmt \
	--verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_1_7TeV.txt \
	  --bins emt \
--verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	# all done
	touch $@

plots/.mass_timestamp: $(HTT_TEST)/root_postfit/.timestamp pas_plots.py
	rm -rf plots
	mkdir -p plots
	python VH_massplots.py --prefit --period 7TeV --MLfit all
	python VH_massplots.py --prefit --period 8TeV --MLfit all
	python VH_massplots.py --period 7TeV --MLfit all
	python VH_massplots.py --period 8TeV --MLfit all
	touch $@

postfit: $(HTT_TEST)/root_postfit/.timestamp

massplots: plots/.mass_timestamp

#################################################################################################################
#####  Making the post fit shape files for the nice plots  (different fit for each category #####################
#################################################################################################################

# Make .root files with the applied pulls
$(HTT_TEST)/root_postfit_zh/.cat_timestamp: $(LIMITDIR)/.timestamp
	# make a copy of the directory so we can mess with them.
	rm -fr $(HTT_TEST)/root_postfit_zh
	cd $(HTT_TEST) && ./mlfit_and_copy.py $(LIMITDIR)/vhtt_zh/125 --rMin -7.0
	cp -r $(HTT_TEST)/root $(HTT_TEST)/root_postfit_zh
	cp $(HTT_TEST)/fitresults/mlfit_sm.txt mlfit_zh.txt
	# apply all the pulls to the shapes
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_8TeV.root datacards/vhtt_3_8TeV.txt \
	  --bins eeem_zh mmme_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_8TeV.root datacards/vhtt_4_8TeV.txt \
	  --bins eemt_zh mmmt_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_8TeV.root datacards/vhtt_5_8TeV.txt \
	  --bins eeet_zh mmet_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_8TeV.root datacards/vhtt_6_8TeV.txt \
	  --bins eett_zh mmtt_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_7TeV.root datacards/vhtt_3_7TeV.txt \
	  --bins eeem_zh mmme_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_7TeV.root datacards/vhtt_4_7TeV.txt \
	  --bins eemt_zh mmmt_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_7TeV.root datacards/vhtt_5_7TeV.txt \
	  --bins eeet_zh mmet_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_zh/vhtt.input_7TeV.root datacards/vhtt_6_7TeV.txt \
	  --bins eett_zh mmtt_zh \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	rm -fr $(HTT_TEST)/root_postfit_wh_had
	cd $(HTT_TEST) && ./mlfit_and_copy.py $(LIMITDIR)/vhtt_wh_had/125 --rMin -7.0
	cp -r $(HTT_TEST)/root $(HTT_TEST)/root_postfit_wh_had
	cp $(HTT_TEST)/fitresults/mlfit_sm.txt mlfit_wh_had.txt
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh_had/vhtt.input_8TeV.root datacards/vhtt_7_8TeV.txt \
	  --bins mtt --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh_had/vhtt.input_8TeV.root datacards/vhtt_8_8TeV.txt \
	  --bins ett --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh_had/vhtt.input_7TeV.root datacards/vhtt_7_7TeV.txt \
	  --bins mtt --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh_had/vhtt.input_7TeV.root datacards/vhtt_8_7TeV.txt \
	  --bins ett --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	rm -fr $(HTT_TEST)/root_postfit_wh
	cd $(HTT_TEST) && ./mlfit_and_copy.py $(LIMITDIR)/vhtt_wh/125 --rMin -7.0
	cp -r $(HTT_TEST)/root $(HTT_TEST)/root_postfit_wh
	cp $(HTT_TEST)/fitresults/mlfit_sm.txt mlfit_wh.txt
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh/vhtt.input_8TeV.root datacards/vhtt_0_8TeV.txt \
	  --bins mmtCatHigh mmtCatLow \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh/vhtt.input_8TeV.root datacards/vhtt_1_8TeV.txt \
	  --bins emtCatHigh emtCatLow \
	  --verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh/vhtt.input_7TeV.root datacards/vhtt_0_7TeV.txt \
	--bins mmt \
	--verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	cd $(HTT_TEST) && ./postfit.py root_postfit_wh/vhtt.input_7TeV.root datacards/vhtt_1_7TeV.txt \
	  --bins emt \
	--verbose --fitresults "mlfit_cmb_131203/out/mlfit.txt"
	# all done
	touch $@

plots/.mass_cat_timestamp: $(HTT_TEST)/root_postfit_zh/.cat_timestamp pas_plots.py
	rm -rf plots
	mkdir -p plots
	python VH_massplots.py --prefit --period 7TeV --MLfit channel
	python VH_massplots.py --prefit --period 8TeV --MLfit channel
	python VH_massplots.py --period 7TeV --MLfit channel
	python VH_massplots.py --period 8TeV --MLfit channel 
	touch $@

massplots_cat: plots/.mass_cat_timestamp


################################################################################
#####  Making the yield table files for the nice plots ######################
################################################################################

vh_table.tex: megacard_125.txt make_yields_table.py
	python make_yields_table.py

plots/vh_table.tex: vh_table.tex
	cp vh_table.tex plots/vh_table.tex

all: massplots plots/vh_table.tex plotlimits

clean:
	rm -f vh_table.tex
	rm -rf plots/
	rm -rf pulls
	rm -rf $(LIMITDIR)
	rm -rf $(SETUP)/*.root

.PHONY: cards zh ltt llt limitdir pulls postfit massplots massplots_cat limits significance comparemacro plotlimits plotsignificances clean
