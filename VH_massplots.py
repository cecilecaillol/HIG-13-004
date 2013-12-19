'''

Make plots for the HIG-12-053 PAS

'''

from RecoLuminosity.LumiDB import argparse
import math
import os
from poisson import convert
from poisson import poisson_errors
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
from HiggsAnalysis.HiggsToTauTau.sigfigs import sigfigs
from sobWeightedCombine import SOBPlotter
from sobWeightedCombine import *
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine('.x tdrStyle.C')
postfit_src = os.path.join(os.environ['CMSSW_BASE'],
                           'src/HiggsAnalysis/HiggsToTauTau/test/',
                           'root_postfit')
postfit_src_wh_had = os.path.join(os.environ['CMSSW_BASE'],
                           'src/HiggsAnalysis/HiggsToTauTau/test/',
                           'root_postfit_wh_had')
postfit_src_wh = os.path.join(os.environ['CMSSW_BASE'],
                           'src/HiggsAnalysis/HiggsToTauTau/test/',
                           'root_postfit_wh')
postfit_src_zh = os.path.join(os.environ['CMSSW_BASE'],
                           'src/HiggsAnalysis/HiggsToTauTau/test/',
                           'root_postfit_zh')

is_blind=True

def getSOverSplusB_WH(signal1, wz1, zz1, fakes1, hww1):
    sumBG=zz1.Clone()
    sumBG.Add(wz1)
    sumBG.Add(fakes1)
    sumBG.Add(hww1)
    signal=sumBG.Clone()
    signal.Add(signal1)
    bb=range(10)
    x=SOBPlotter()
    x.getSoB(signal, sumBG,bb)
    return bb[0]

def getSOverSplusB_ZH(signal1, zz1, fakes1, hww1):
    sumBG=zz1.Clone()
    sumBG.Add(fakes1)
    sumBG.Add(hww1)
    signal=sumBG.Clone()
    signal.Add(signal1)
    a=range(10)
    x=SOBPlotter()
    x.getSoB(signal, sumBG,a)
    return a[0]

def rebin_dN(hist):
    output=hist.Clone()
    for bin in range(output.GetNbinsX()+1):
        output.SetBinContent(bin,output.GetBinContent(bin)/output.GetBinWidth(bin))
        output.SetBinError(bin,output.GetBinError(bin)/output.GetBinWidth(bin))
    return output

def rebin_data_dN(graph,hist):
    output=graph.Clone()
    ref=hist.Clone()
    for bin in range(output.GetN()):
        output.SetPoint(bin, output.GetX()[bin], output.GetY()[bin]/ref.GetBinWidth(bin))
        output.SetPointEYhigh(bin, output.GetErrorYhigh(bin)/ref.GetBinWidth(bin))
        output.SetPointEYlow(bin, output.GetErrorYlow(bin)/ref.GetBinWidth(bin))
    return output

def text_channel(canal):   
   """ Writes channel name """
   subchannels_left=['zh','llem','llet','llmt','lltt','eeem','eeet','eemt','eett','mmem','mmet','mmmt','mmtt']
   if args.period=="7TeV":
       subchannels_left=['zh','llem','llet','llmt','lltt','eeem','eeet','eemt','eett','mmem','mmet','mmmt','mmtt','mmt']
   if canal in subchannels_left:
      chan     = ROOT.TPaveText(0.22, 0.76+0.013, 0.44, 0.76+0.155, "NDC")
   else:
      chan     = ROOT.TPaveText(0.53, 0.48+0.013, 0.75, 0.48+0.155, "NDC")
   chan.SetBorderSize(   0 )
   chan.SetFillStyle(    0 )
   chan.SetTextAlign(   12 )
   chan.SetTextSize ( 0.05 )
   chan.SetTextColor(    1 )
   chan.SetTextFont (   62 )
   texte=' '
   if canal=='emt_high':
	 texte="#splitline{e + #mu#tau#lower[0.8]{#scale[0.7]{h}}}{#mu + e#tau#lower[0.8]{#scale[0.7]{h}}}   high #it{L}#lower[0.8]{#scale[0.7]{T}}"
   if canal=='emt_low':
	 texte='#splitline{e + #mu#tau#lower[0.8]{#scale[0.7]{h}}}{#mu + e#tau#lower[0.8]{#scale[0.7]{h}}}   low #it{L}#lower[0.8]{#scale[0.7]{T}}'
   if canal=='mmt_high':
	 texte='#mu + #mu#tau#lower[0.8]{#scale[0.7]{h}} high #it{L}#lower[0.8]{#scale[0.7]{T}}'
   if canal=='mmt_low':
	 texte='#mu + #mu#tau#lower[0.8]{#scale[0.7]{h}} low #it{L}#lower[0.8]{#scale[0.7]{T}}'
   if canal=='emt':
	 texte='#splitline{e + #mu#tau#lower[0.8]{#scale[0.7]{h}}}{#mu + e#tau#lower[0.8]{#scale[0.7]{h}}}'
   if canal=='mmt':
	 texte='#mu + #mu#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='ett':
	 texte='e + #tau#lower[0.8]{#scale[0.7]{h}}#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='mtt':
	 texte='#mu + #tau#lower[0.8]{#scale[0.7]{h}}#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='llem':
	 texte='#it{l}#it{l} + e#mu'
   if canal=='llet':
	 texte='#it{l}#it{l} + e#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='llmt':
	 texte='#it{l}#it{l} + #mu#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='lltt':
	 texte='#it{l}#it{l} + #tau#lower[0.8]{#scale[0.7]{h}}#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='mmem':
         texte='#mu#mu + e#mu'
   if canal=='mmet':
         texte='#mu#mu + e#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='mmmt':
         texte='#mu#mu + #mu#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='mmtt':
         texte='#mu#mu + #tau#lower[0.8]{#scale[0.7]{h}}#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='eeem':
         texte='ee + e#mu'
   if canal=='eeet':
         texte='ee + e#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='eemt':
         texte='ee + #mu#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='eett':
         texte='ee + #tau#lower[0.8]{#scale[0.7]{h}}#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='zh':
	 texte='#it{l}#it{l} + #it{L}#it{L}\''
   if canal=='llt':
	 texte='#it{l} + #it{l}\'#tau#lower[0.8]{#scale[0.7]{h}}'
   if canal=='llt_high':
         texte='#it{l} + #it{l}\'#tau#lower[0.8]{#scale[0.7]{h}} high #it{L}#lower[0.8]{#scale[0.7]{T}}'
   if canal=='llt_low':
         texte='#it{l} + #it{l}\'#tau#lower[0.8]{#scale[0.7]{h}} low #it{L}#lower[0.8]{#scale[0.7]{T}}'
   if canal=='ltt':
	 texte='#it{l} + #tau#lower[0.8]{#scale[0.7]{h}}#tau#lower[0.8]{#scale[0.7]{h}}' 

   chan.AddText(texte)
   return chan


def fix_maximum(channel_dict, type):
    """ Make sure everything is visible """
    max = channel_dict['stack'].GetMaximum()
    histo = channel_dict['data']
    cushion=1.5
    for bin in range(histo.GetNbinsX()):
        content = histo.GetBinContent(bin)
	L,U=poisson_errors(content)
        #if content>0:
        #   upper = content + math.sqrt(content)
        #else:
        #   upper = content
        #print bin, upper, max
        if  U > max:
            max = U
    if type=="ZH":
        channel_dict['stack'].SetMaximum(cushion * max/20)
    if type=="LLT":
        channel_dict['stack'].SetMaximum(cushion * max/15)
    if type=="LLT7":
        channel_dict['stack'].SetMaximum(cushion * max/40)
    if type=="LTT":
        channel_dict['stack'].SetMaximum(cushion * max/28)


def add_cms_blurb(sqrts, intlumi, preliminary=False, blurb=''):
    """ Add a CMS blurb to a plot """
    # Same style as Htt
    label_text = "CMS"
    if preliminary:
        label_text += " Preliminary"
    label_text +=","
    label_text += " %s fb^{-1}" % (intlumi)
    label_text += " at %s TeV" % sqrts
    label_text += " " + blurb
    lowX=0.16
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextSize ( 0.04 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont (   62 )
    lumi.AddText(label_text)
    return lumi

_styles = {
    "wz": {
        # Same as Z+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.TColor.GetColor(248,206,104),
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "zz": {
        # Same as W+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.TColor.GetColor(222,90,106),
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "fakes": {
        # Same as QCD
        'fillcolor': ROOT.TColor.GetColor(250,202,255),
        'linecolor': ROOT.EColor.kBlack,
        'fillstyle': 1001,
        'linewidth': 3,
    },
    "charge_fakes": {
        # Same as QCD
        'fillcolor': ROOT.TColor.GetColor(250,202,255),
        'linecolor': ROOT.TColor.GetColor(250,202,255),
        'fillstyle': 1001,
        'linewidth': 0,
    },
    "GGToZZ2L2L": {
        # Same as QCD
        'fillcolor': ROOT.TColor.GetColor(222,90,106),
        'linecolor': ROOT.TColor.GetColor(222,90,106),
        'fillstyle': 1001,
        'linewidth': 1,
    },
    "hww": {
        'fillstyle': 1001,
        'fillcolor': ROOT.EColor.kGreen + 2,
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "signal": {
        'fillcolor': 0,
        'fillstyle': 0,
        'linestyle': 11,
        'linewidth': 3,
        'linecolor': ROOT.EColor.kBlue,
        'name': "VH",
    },
    "data": {
        'markerstyle': 20,
        'markersize': 2,
        'linewidth': 3,
        'markercolor': ROOT.EColor.kBlack,
        'legendstyle': 'pe',
        'format': 'pe',
        'name': "Observed",
    }
}


def apply_style(histogram, style_type):
    style = _styles[style_type]
    if 'fillstyle' in style:
        histogram.SetFillStyle(style['fillstyle'])
    if 'fillcolor' in style:
        histogram.SetFillColor(style['fillcolor'])
    if 'linecolor' in style:
        histogram.SetLineColor(style['linecolor'])
    if 'linestyle' in style:
        histogram.SetLineStyle(style['linestyle'])
    if 'linewidth' in style:
        histogram.SetLineWidth(style['linewidth'])
    if 'markersize' in style:
        histogram.SetMarkerSize(style['markersize'])
    if 'markercolor' in style:
        histogram.SetMarkerColor(style['markercolor'])


def get_combined_histogram(histograms, directories, files, title=None,
                           scale=None, style=None):
    """ Get a histogram that is the combination of all paths/files"""
    if isinstance(histograms, basestring):
        histograms = [histograms]
    output = None
    for file in files:
        for path in directories:
            for histogram in histograms:
                   #print path,histogram
                   #if os.path.isfile(path + '/' + histogram):
                   th1 = file.Get(path + '/' + histogram)
                   if output is None:
                       output = th1.Clone()
                   else :
                       output.Add(th1)
                   #if histogram=="data_obs":
                   #     if path=="eeem_zh" or path=="mmme_zh" or path=="mmet_zh" or path=="eeet_zh" or path=="mmmt_zh" or path=="eemt_zh" or path=="mmtt_zh" or path=="eett_zh":
                   #         for i in range(6,9):#partial blinding
                   #              output.SetBinContent(i,-100)
                   #     if path=="eetCatLow" or path=="mmtCatLow" or path=="emtCatLow" or path=="eetCatHigh" or path=="mmtCatHigh" or path=="emtCatHigh":
                   #         for i in range(4,7):
                   #              output.SetBinContent(i,-100)
                   #     if path=="ett" or path=="mtt":
                   #         for i in range(4,7):
                   #              output.SetBinContent(i,-100)
    if scale is not None:
        output.Scale(scale)
    if title is not None:
        output.SetTitle(title)
    if style:
        apply_style(output, style)
    return output


if __name__ == "__main__":
    # The input files

    style1=GetStyleHtt()
    style1.cd()


    parser = argparse.ArgumentParser()

    parser.add_argument('--prefit', action='store_true',
                        help="Don't use postfit")

    parser.add_argument('--period', default="all",
                        choices=['7TeV', '8TeV', 'all'],
                        help="Which data taking period")

    parser.add_argument('--MLfit', default="all",
                        choices=['channel', 'all'],
                        help="Which fit")

    args = parser.parse_args()

    prefit_7TeV_file = ROOT.TFile.Open(
        "limits/cmb/common/vhtt.input_7TeV.root")
    prefit_8TeV_file = ROOT.TFile.Open(
        "limits/cmb/common/vhtt.input_8TeV.root")

    #postfit_7TeV_file = ROOT.TFile.Open(postfit_src + "/vhtt.input_7TeV.root")
    #postfit_8TeV_file = ROOT.TFile.Open(postfit_src + "/vhtt.input_8TeV.root")
    files_to_use_zh=prefit_7TeV_file
    files_to_use_wh_had=prefit_7TeV_file
    files_to_use_wh=prefit_7TeV_file

    if args.MLfit=="channel":
       postfit_7TeV_file_wh_had = ROOT.TFile.Open(postfit_src_wh_had + "/vhtt.input_7TeV.root")
       postfit_8TeV_file_wh_had = ROOT.TFile.Open(postfit_src_wh_had + "/vhtt.input_8TeV.root")
       postfit_7TeV_file_wh = ROOT.TFile.Open(postfit_src_wh + "/vhtt.input_7TeV.root")
       postfit_8TeV_file_wh = ROOT.TFile.Open(postfit_src_wh + "/vhtt.input_8TeV.root")
       postfit_7TeV_file_zh = ROOT.TFile.Open(postfit_src_zh + "/vhtt.input_7TeV.root")
       postfit_8TeV_file_zh = ROOT.TFile.Open(postfit_src_zh + "/vhtt.input_8TeV.root")

       files_to_use_map_zh = {
           (True, '7TeV'): [prefit_7TeV_file],
           (True, '8TeV'): [prefit_8TeV_file],
           (True, 'all'): [prefit_8TeV_file, prefit_7TeV_file],
           (False, '7TeV'): [postfit_7TeV_file_zh],
           (False, '8TeV'): [postfit_8TeV_file_zh],
           (False, 'all'): [postfit_8TeV_file_zh, postfit_7TeV_file_zh],
       }

       files_to_use_map_wh = {
           (True, '7TeV'): [prefit_7TeV_file],
           (True, '8TeV'): [prefit_8TeV_file],
           (True, 'all'): [prefit_8TeV_file, prefit_7TeV_file],
           (False, '7TeV'): [postfit_7TeV_file_wh],
           (False, '8TeV'): [postfit_8TeV_file_wh],
           (False, 'all'): [postfit_8TeV_file_wh, postfit_7TeV_file_wh],
       }

       files_to_use_map_wh_had = {
           (True, '7TeV'): [prefit_7TeV_file],
           (True, '8TeV'): [prefit_8TeV_file],
           (True, 'all'): [prefit_8TeV_file, prefit_7TeV_file],
           (False, '7TeV'): [postfit_7TeV_file_wh_had],
           (False, '8TeV'): [postfit_8TeV_file_wh_had],
           (False, 'all'): [postfit_8TeV_file_wh_had, postfit_7TeV_file_wh_had],
       }

       files_to_use_zh = files_to_use_map_zh[(args.prefit, args.period)]
       files_to_use_wh_had = files_to_use_map_wh_had[(args.prefit, args.period)]
       files_to_use_wh = files_to_use_map_wh[(args.prefit, args.period)]

    if args.MLfit=="all":
        postfit_7TeV_file = ROOT.TFile.Open(postfit_src + "/vhtt.input_7TeV.root")
        postfit_8TeV_file = ROOT.TFile.Open(postfit_src + "/vhtt.input_8TeV.root")
        files_to_use_map = {
            (True, '7TeV'): [prefit_7TeV_file],
            (True, '8TeV'): [prefit_8TeV_file],
            (True, 'all'): [prefit_8TeV_file, prefit_7TeV_file],
            (False, '7TeV'): [postfit_7TeV_file],
            (False, '8TeV'): [postfit_8TeV_file],
            (False, 'all'): [postfit_8TeV_file, postfit_7TeV_file],
        }
        files_to_use_zh = files_to_use_map[(args.prefit, args.period)]
        files_to_use_wh_had = files_to_use_map[(args.prefit, args.period)]
        files_to_use_wh = files_to_use_map[(args.prefit, args.period)]

    # Get all our histograms
    histograms = {}
    yield_errors = {}
    yields = {}

    # Map LLT subplots to different category combinations
    all_llt_channels = ['emtCatLow', 'mmtCatLow',
                        'emtCatHigh', 'mmtCatHigh']
    llt_subplots = {
        'llt': all_llt_channels,
        'llt_low': [x for x in all_llt_channels if 'Low' in x],
        'llt_high': [x for x in all_llt_channels if 'High' in x],
        'mmt': [x for x in all_llt_channels if 'mmt' in x],
        'emt': [x for x in all_llt_channels if 'emt' in x],
        'mmt_low': ['mmtCatLow'],
        'mmt_high': ['mmtCatHigh'],
        'emt_low': ['emtCatLow'],
        'emt_high': ['emtCatHigh'],
    }
    if args.period=="7TeV":
	llt_subplots = {
           'llt': ['emt','mmt'],
           'mmt': ['mmt'],
           'emt': ['emt'],
       }
    ltt_subplots = {
        'ltt': ['ett','mtt'],
	'ett': ['ett'],
	'mtt': ['mtt'],
    }
    zh_subplots = {
        'zh': ['eeem_zh','mmme_zh','eeet_zh','mmet_zh','eemt_zh','mmmt_zh','eett_zh','mmtt_zh'],
        'llem': ['eeem_zh','mmme_zh'],
        'llet': ['eeet_zh','mmet_zh'],
        'llmt': ['eemt_zh','mmmt_zh'],
        'lltt': ['eett_zh','mmtt_zh'],
        'eeem': ['eeem_zh'],
        'eeet': ['eeet_zh'],
        'eemt': ['eemt_zh'],
        'eett': ['eett_zh'],
        'mmem': ['mmme_zh'],
        'mmet': ['mmet_zh'],
        'mmmt': ['mmmt_zh'],
        'mmtt': ['mmtt_zh'],
    }

    num_bins_llt=9
    if args.period=="7TeV":
	num_bins_llt=3
    num_bins_zh=15
    num_bins_ltt=20

    # LLT
    for lltsubset, channel_subset in llt_subplots.iteritems():
        llt_plots = {}
	llt_erreurs={}
	llt_integrales={}
	yield_errors[lltsubset] = llt_erreurs
	yields[lltsubset] = llt_integrales
        histograms[lltsubset] = llt_plots
        # only EMT has charge flip background
        channel_subset_flip = [x for x in channel_subset
                               if 'emt' in x]

        llt_plots['wz'] = get_combined_histogram(
            'wz', channel_subset, files_to_use_wh, title='WZ',
            style='wz'
        )
	erreur=ROOT.Double(0)
	integrale=llt_plots['wz'].IntegralAndError(1,num_bins_llt,erreur)
	llt_integrales['wz']=float(integrale)
	llt_erreurs['wz']=float(erreur)
	#print integrale, erreur
        llt_plots['zz'] = get_combined_histogram(
            'zz', channel_subset, files_to_use_wh, title='ZZ',
            style='zz'
        )
        integrale=llt_plots['zz'].IntegralAndError(1,num_bins_llt,erreur)
        llt_integrales['zz']=float(integrale)
        llt_erreurs['zz']=float(erreur)
        llt_plots['fakes'] = get_combined_histogram(
            'fakes', channel_subset, files_to_use_wh, title='Reducible bkg.',
            style='fakes'
        )
        integrale=llt_plots['fakes'].IntegralAndError(1,num_bins_llt,erreur)
        llt_integrales['fakes']=float(integrale)
        llt_erreurs['fakes']=float(erreur)
        if channel_subset_flip:
            llt_plots['charge_fakes'] = get_combined_histogram(
                'charge_fakes', channel_subset_flip, files_to_use_wh,
                title='Reducible bkg. charge flip', style='charge_fakes'
            )
            integrale=llt_plots['charge_fakes'].IntegralAndError(1,num_bins_llt,erreur)
            llt_integrales['fakes']+=float(integrale)
        llt_plots['signal'] = get_combined_histogram(
            'WH125', channel_subset, files_to_use_wh,
            title='m_{H}=125 GeV', style='signal',
        )
        integrale=llt_plots['signal'].IntegralAndError(1,num_bins_llt,erreur)
        llt_integrales['signal']=float(integrale)
        llt_erreurs['signal']=float(erreur)
	print integrale, erreur
        llt_plots['hww'] = get_combined_histogram(
            'WH_hww125', channel_subset, files_to_use_wh,
            title='m_{H}=125 GeV', style='hww',
        )
        integrale=llt_plots['hww'].IntegralAndError(1,num_bins_llt,erreur)
        llt_integrales['hww']=float(integrale)
        llt_erreurs['hww']=float(erreur)
        llt_plots['data'] = get_combined_histogram(
            'data_obs', channel_subset, files_to_use_wh,
            title='data', style='data'
        )
        integrale=llt_plots['data'].IntegralAndError(1,num_bins_llt,erreur)
        llt_integrales['data']=float(integrale)
        llt_erreurs['data']=float(erreur)
        def make_legend():
            output = ROOT.TLegend(0.53, 0.65, 0.95, 0.90, "", "brNDC")
            output.SetLineWidth(0)
            output.SetLineStyle(0)
            output.SetFillStyle(0)
            output.SetBorderSize(0)
	    output.SetTextFont(62)
            return output
        llt_plots['stack'] = ROOT.THStack("llt_stack", "llt_stack")
        if channel_subset_flip:
            llt_plots['stack'].Add(rebin_dN(llt_plots['charge_fakes']), 'hist')
        llt_plots['stack'].Add(rebin_dN(llt_plots['fakes']), 'hist')
        llt_plots['stack'].Add(rebin_dN(llt_plots['zz']), 'hist')
        llt_plots['stack'].Add(rebin_dN(llt_plots['wz']), 'hist')
        llt_plots['stack'].Add(rebin_dN(llt_plots['hww']), 'hist')

        errorLLT = llt_plots['zz'].Clone()
        errorLLT.SetFillStyle(3013)
        errorLLT.Add(llt_plots['fakes'])
        if channel_subset_flip:
            errorLLT.Add(llt_plots['charge_fakes'])
        errorLLT.Add(llt_plots['wz'])
        errorLLT.Add(llt_plots['hww'])
        errorLLT.SetMarkerSize(0)
        errorLLT.SetFillColor(13)
        errorLLT.SetLineWidth(1)
	errorLLT_rebin=rebin_dN(errorLLT)
        llt_plots['error'] = errorLLT_rebin
        llt_plots['data'].SetMarkerStyle(20)
        llt_plots['data'].SetMarkerColor(ROOT.EColor.kBlack)
        llt_plots['data'].SetLineColor(ROOT.EColor.kBlack)
        llt_plots['data'].SetLineWidth(2)
        llt_plots['data'].SetMarkerSize(2)
	#llt_plots['wz_rebin']=rebin_dN(llt_plots['wz']).Clone()

        llt_plots['stack'].Add(rebin_dN(llt_plots['signal']), 'hist')

        llt_plots['legend'] = make_legend()
        llt_plots['legend'].AddEntry(
            llt_plots['signal'],
            "SM H(125 GeV)#rightarrow #tau#tau", "l")
        llt_plots['legend'].AddEntry(
            llt_plots['data'],
            "Observed", "lp")
        llt_plots['legend'].AddEntry(llt_plots['hww'],
                                     "SM H(125 GeV)#rightarrow WW", "f")
        llt_plots['legend'].AddEntry(llt_plots['wz'], "WZ", "f")
        llt_plots['legend'].AddEntry(llt_plots['zz'], "ZZ", "f")
        llt_plots['legend'].AddEntry(llt_plots['fakes'],
                                     "Reducible bkg.", "f")
        if not args.prefit:
            llt_plots['legend'].AddEntry(
                errorLLT, "Bkg. uncertainty", "f")

    # ZH
    histograms['zh'] = {}
    yields['zh']={}
    yield_errors['zh'] = {}
    zh_channels = [
        'eeem_zh', 'eeet_zh', 'eemt_zh', 'eett_zh',
        'mmme_zh', 'mmet_zh', 'mmmt_zh', 'mmtt_zh',
    ]
    for zhsubset, channel_subset in zh_subplots.iteritems():
        zh_plots = {}
        zh_erreurs = {}
	zh_integrales = {}
        histograms[zhsubset] = zh_plots
	yields[zhsubset] = zh_integrales
        yield_errors[zhsubset] = zh_erreurs

        zh_plots['zz'] = get_combined_histogram(
            ['ZZ', 'GGToZZ2L2L', 'TTZ'], channel_subset, files_to_use_zh, title='ZZ',
            style='zz'
        )
        erreur=ROOT.Double(0)
        integrale=zh_plots['zz'].IntegralAndError(1,num_bins_zh,erreur)
        zh_integrales['zz']=float(integrale)
        zh_erreurs['zz']=float(erreur)

        zh_plots['fakes'] = get_combined_histogram(
            'Zjets', channel_subset, files_to_use_zh, title='Reducible bkg.',
            style='fakes'
        )
        integrale=zh_plots['fakes'].IntegralAndError(1,num_bins_zh,erreur)
        zh_integrales['fakes']=float(integrale)
        zh_erreurs['fakes']=float(erreur)
        zh_plots['hww'] = get_combined_histogram(
            'ZH_hww125', channel_subset, files_to_use_zh,
            title='m_{H}=125 GeV', style='hww',
        )
        integrale=zh_plots['hww'].IntegralAndError(1,num_bins_zh,erreur)
        zh_integrales['hww']=float(integrale)
        zh_erreurs['hww']=float(erreur)
        zh_plots['signal'] = get_combined_histogram(
            'ZH_htt125', channel_subset, files_to_use_zh,
            title='m_{H}=125 GeV', style='signal',
        )
        integrale=zh_plots['signal'].IntegralAndError(1,num_bins_zh,erreur)
        zh_integrales['signal']=float(integrale)
        zh_erreurs['signal']=float(erreur)
        zh_plots['data'] = get_combined_histogram(
            'data_obs', channel_subset, files_to_use_zh,
            title='data', style='data',
        )
        integrale=zh_plots['data'].IntegralAndError(1,num_bins_zh,erreur)
        zh_integrales['data']=float(integrale)
        zh_erreurs['data']=float(erreur)
        zh_plots['stack'] = ROOT.THStack("zh_stack", "zh_stack")
        zh_plots['stack'].Add(rebin_dN(zh_plots['fakes']), 'hist')
        zh_plots['stack'].Add(rebin_dN(zh_plots['zz']), 'hist')
        zh_plots['stack'].Add(rebin_dN(zh_plots['hww']), 'hist')
        zh_plots['stack'].Add(rebin_dN(zh_plots['signal']), 'hist')

        errorZH=zh_plots['zz'].Clone()
        errorZH.SetFillStyle(3013)
        errorZH.Add(zh_plots['fakes'])
        errorZH.Add(zh_plots['hww'])
        errorZH.SetMarkerSize(0)
        errorZH.SetFillColor(13)
        errorZH.SetLineWidth(1)
        errorZH_rebin=rebin_dN(errorZH)

	zh_plots['error'] = errorZH_rebin
	zh_plots['data'].SetMarkerStyle(20)
        zh_plots['data'].SetMarkerColor(ROOT.EColor.kBlack)
        zh_plots['data'].SetLineColor(ROOT.EColor.kBlack)
        zh_plots['data'].SetLineWidth(2)
        zh_plots['data'].SetMarkerSize(2)
	#zh_plots['data_rebin']=rebin_dN(zh_plots['data'])

        zh_plots['legend'] = make_legend()
        zh_plots['legend'].AddEntry(zh_plots['signal'],
                                        "SM H(125 GeV)#rightarrow #tau#tau", "l")
        zh_plots['legend'].AddEntry(zh_plots['data'],
                                        "Observed", "lp")
        zh_plots['legend'].AddEntry(zh_plots['hww'],
                                        "SM H(125 GeV)#rightarrow WW", "f")
        zh_plots['legend'].AddEntry(zh_plots['zz'], "ZZ", "f")
        zh_plots['legend'].AddEntry(zh_plots['fakes'],
                                        "Reducible bkg.", "f")
        if args.prefit==False:
           zh_plots['legend'].AddEntry(errorZH, "Bkg. uncertainty", "F")

    # LTT

    for lttsubset, channel_subset in ltt_subplots.iteritems():
        ltt_plots = {}
	ltt_integrales = {}
	ltt_erreurs = {}
	yields[lttsubset]=ltt_integrales
	yield_errors[lttsubset]=ltt_erreurs
        histograms[lttsubset] = ltt_plots

        ltt_plots['wz'] = get_combined_histogram(
            'wz', channel_subset, files_to_use_wh_had, title='WZ',
            style='wz',
        )
	erreur=ROOT.Double(0)
        integrale=ltt_plots['wz'].IntegralAndError(1,num_bins_ltt,erreur)
        ltt_integrales['wz']=float(integrale)
        ltt_erreurs['wz']=float(erreur)
        ltt_plots['zz'] = get_combined_histogram(
            'zz', channel_subset, files_to_use_wh_had, title='ZZ',
            style='zz',)
        integrale=ltt_plots['zz'].IntegralAndError(1,num_bins_ltt,erreur)
        ltt_integrales['zz']=float(integrale)
        ltt_erreurs['zz']=float(erreur)
        ltt_plots['fakes'] = get_combined_histogram(
            'fakes', channel_subset, files_to_use_wh_had, title='Reducible bkg.',
            style='fakes',
        )
        integrale=ltt_plots['fakes'].IntegralAndError(1,num_bins_ltt,erreur)
        ltt_integrales['fakes']=float(integrale)
        ltt_erreurs['fakes']=float(erreur)
        ltt_plots['signal'] = get_combined_histogram(
            ['WH_htt125'], channel_subset, files_to_use_wh_had,
            title='m_{H}=125 GeV', style='signal')
        integrale=ltt_plots['signal'].IntegralAndError(1,num_bins_ltt,erreur)
        ltt_integrales['signal']=float(integrale)
        ltt_erreurs['signal']=float(erreur)
	print integrale, erreur
        ltt_plots['data'] = get_combined_histogram(
            'data_obs', channel_subset, files_to_use_wh_had,
            title='data', style='data')
	ltt_plots['data_rebin']=rebin_dN(ltt_plots['data'])
        integrale=ltt_plots['data'].IntegralAndError(1,num_bins_ltt,erreur)
        ltt_integrales['data']=float(integrale)
        ltt_erreurs['data']=float(erreur)
        ltt_plots['stack'] = ROOT.THStack("ltt_stack", "ltt_stack")
        ltt_plots['stack'].Add(rebin_dN(ltt_plots['fakes']), "hist")
        ltt_plots['stack'].Add(rebin_dN(ltt_plots['zz']), "hist")
        ltt_plots['stack'].Add(rebin_dN(ltt_plots['wz']), "hist")
        ltt_plots['stack'].Add(rebin_dN(ltt_plots['signal']), "hist")

        errorLTT=ltt_plots['zz'].Clone()
        errorLTT.SetFillStyle(3013)
        errorLTT.Add(ltt_plots['fakes'])
        errorLTT.Add(ltt_plots['wz'])
        errorLTT.SetMarkerSize(0)
        errorLTT.SetFillColor(13)
        errorLTT.SetLineWidth(1)
	errorLTT_rebin=rebin_dN(errorLTT)

	ltt_plots['error'] = errorLTT_rebin

        ltt_plots['legend'] = make_legend()
        ltt_plots['legend'].AddEntry(ltt_plots['signal'],
                                         "SM H(125 GeV)#rightarrow #tau#tau", "L")
        ltt_plots['legend'].AddEntry(ltt_plots['data'],
                                         "Observed", "LP")
        ltt_plots['legend'].AddEntry(ltt_plots['wz'], "WZ", "F")
        ltt_plots['legend'].AddEntry(ltt_plots['zz'], "ZZ", "F")
        ltt_plots['legend'].AddEntry(ltt_plots['fakes'],
                                             "Reducible bkg.", "F")
        if args.prefit==False:
           ltt_plots['legend'].AddEntry(errorLTT,"Bkg. uncertainty","F")

    # Apply some styles to all the histograms
    for channel in histograms.keys():
    #for channel in ['zh']:
        # Use Poissonian error bars. The set_zero_bins makes it so bins w/o
        # any data are blank.
        histograms[channel]['poisson'] = convert(histograms[channel]['data'],
                                                 set_zero_bins=-10)
        # Make sure all data points are visible
	if channel in llt_subplots:
	    if args.period=="7TeV":
                fix_maximum(histograms[channel],'LLT7')
	    else:
                fix_maximum(histograms[channel],'LLT')
        if channel in zh_subplots:
            fix_maximum(histograms[channel],'ZH')
        if channel in ltt_subplots:
            fix_maximum(histograms[channel],'LTT')
        # We have to draw it so things like the axes are initialized.
        histograms[channel]['stack'].Draw()
        #histograms[channel]['stack'].GetYaxis().SetTitle(
        #    "#bf{Events/%i GeV}" % histograms[channel]['data'].GetBinWidth(1))
	if channel in zh_subplots:
           histograms[channel]['stack'].GetYaxis().SetTitle(
            "#bf{dN/dm_{#tau#tau} [1/GeV]}" )
	else:
           histograms[channel]['stack'].GetYaxis().SetTitle(
            "#bf{dN/dm_{vis} [1/GeV]}" )
        if channel in zh_subplots:
           histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{#tau#tau} [GeV]}")
        else:
           histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{vis} [GeV]}")
	if channel in ltt_subplots:
	   histograms[channel]['stack'].GetXaxis().SetRangeUser(0,300)


    plot_suffix = "_%s_%s_%s.pdf" % (
        'prefit' if args.prefit else 'postfit',
        args.period,
        'FitByChannel' if args.MLfit=="channel" else 'FitAllChannels'
    )
    plot_suffix_png = "_%s_%s_%s.png" % (
        'prefit' if args.prefit else 'postfit',
        args.period,
        'FitByChannel' if args.MLfit=="channel" else 'FitAllChannels'
    )

    catllt = ROOT.TPaveText(0.20, 0.71+0.061, 0.32, 0.71+0.161, "NDC");
    catllt.SetBorderSize(   0 );
    catllt.SetFillStyle(    0 );
    catllt.SetTextAlign(   12 );
    catllt.SetTextSize ( 0.05 );
    catllt.SetTextColor(    1 );
    catllt.SetTextFont (   62 );
    catllt.AddText("WH semi-lep");

    catZH      = ROOT.TPaveText(0.20, 0.71+0.061, 0.32, 0.71+0.161, "NDC");
    catZH.SetBorderSize(   0 );
    catZH.SetFillStyle(    0 );
    catZH.SetTextAlign(   12 );
    catZH.SetTextSize ( 0.05 );
    catZH.SetTextColor(    1 );
    catZH.SetTextFont (   62 );
    catZH.AddText("ZH");

    catltt      = ROOT.TPaveText(0.20, 0.71+0.061, 0.32, 0.71+0.161, "NDC");
    catltt.SetBorderSize(   0 );
    catltt.SetFillStyle(    0 );
    catltt.SetTextAlign(   12 );
    catltt.SetTextSize ( 0.05 );
    catltt.SetTextColor(    1 );
    catltt.SetTextFont (   62 );
    catltt.AddText("WH fully-had");

    # Figure out what goes in the CMS preliminary line
    blurb_map = {
        '7TeV': ('4.9', '7'),
        '8TeV': ('19.7', '8'),
        'all': ('24.7', '7+8'),
    }
    int_lumi, sqrts = blurb_map[args.period]

    canvas = MakeCanvas("asdf","asdf",800,800)

    for llt_key in llt_subplots:
        #print "Plotting: ", llt_key
        histograms[llt_key]['stack'].Draw()
        if not args.prefit:
            histograms[llt_key]['error'].Draw("e2same")
        histograms[llt_key]['poisson'].SetMarkerStyle(20)
        histograms[llt_key]['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
        histograms[llt_key]['poisson'].SetLineColor(ROOT.EColor.kBlack)
        histograms[llt_key]['poisson'].SetLineWidth(2)
        histograms[llt_key]['poisson'].SetMarkerSize(2)
        histograms[llt_key]['poisson_rebin']=rebin_data_dN(histograms[llt_key]['poisson'],histograms[llt_key]['wz'])
        histograms[llt_key]['poisson_rebin'].Draw('pe same')
        #catllt.Draw("same")
	histograms[llt_key]['legend'].SetTextFont(62)
        histograms[llt_key]['legend'].Draw()
        lumiBlurb = add_cms_blurb(sqrts, int_lumi)
        lumiBlurb.Draw("same")
	channel_text=text_channel(llt_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + llt_key + plot_suffix)
	canvas.SaveAs('plots/' + llt_key + plot_suffix_png)

    for zh_key in zh_subplots:
        histograms[zh_key]['stack'].Draw()
        if args.prefit==False:
           histograms[zh_key]['error'].Draw("e2same")
        histograms[zh_key]['poisson'].SetMarkerStyle(20)
        histograms[zh_key]['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
        histograms[zh_key]['poisson'].SetLineColor(ROOT.EColor.kBlack)
        histograms[zh_key]['poisson'].SetLineWidth(2)
        histograms[zh_key]['poisson'].SetMarkerSize(2)
	histograms[zh_key]['poisson_rebin']=rebin_data_dN(histograms[zh_key]['poisson'],histograms[zh_key]['zz'])
        histograms[zh_key]['poisson_rebin'].Draw('pe same')
        #catZH.Draw("same")
	histograms[zh_key]['legend'].SetTextFont(62)
        histograms[zh_key]['legend'].Draw()
        lumiBlurb=add_cms_blurb(sqrts, int_lumi)
        lumiBlurb.Draw("same")
        channel_text=text_channel(zh_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + zh_key + plot_suffix)
        canvas.SaveAs('plots/' + zh_key + plot_suffix_png)

    for ltt_key in ltt_subplots:
	#histograms[ltt_key]['stack'].GetXaxis().SetRange(0,300)
        histograms[ltt_key]['stack'].Draw()
        if args.prefit==False:
           histograms[ltt_key]['error'].Draw("e2same")
	histograms[ltt_key]['poisson_rebin']=rebin_data_dN(histograms[ltt_key]['poisson'],histograms[ltt_key]['wz'])
        histograms[ltt_key]['poisson_rebin'].Draw('pe same')
        #catltt.Draw("same")
	histograms[ltt_key]['legend'].SetTextFont(62)
        histograms[ltt_key]['legend'].Draw()
        limiBlurb=add_cms_blurb(sqrts, int_lumi)
        lumiBlurb.Draw("same")
        channel_text=text_channel(ltt_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + ltt_key + plot_suffix)
        canvas.SaveAs('plots/' + ltt_key + plot_suffix_png)

    a=getSOverSplusB_ZH(histograms['eeem']['signal'],histograms['eeem']['fakes'],histograms['eeem']['zz'],histograms['eeem']['hww'])

    postfit="postfit"
    if args.prefit:
	postfit="prefit"
    text_file=open("vh_table_yields_"+postfit+args.period+"_"+args.MLfit+".txt","w")
    text_file.write('\\begin{tabular}{l | c | c | c} \n')
    text_file.write('Process &$\\ell \\ell \\tau_h$& $\\ell\\tau_h\\tau_h$ & $\\ell\\ell LL$ \\\\ \n')
    text_file.write('Fakes & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & \multirow{2}{*}{%.2f $\\pm$ %.2f} \\\\ \n'%(yields['llt']['fakes'],yield_errors['llt']['fakes'],yields['ltt']['fakes'],yield_errors['ltt']['fakes'],yields['zh']['fakes'],yield_errors['zh']['fakes']))
    text_file.write('WZ & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & \\\\ \n'%(yields['llt']['wz'],yield_errors['llt']['wz'],yields['ltt']['wz'],yield_errors['ltt']['wz']))
    text_file.write('\hline \n')
    text_file.write('ZZ & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f \\\\ \n'%(yields['llt']['zz'],yield_errors['llt']['zz'],yields['ltt']['zz'],yield_errors['ltt']['zz'],yields['zh']['zz'],yield_errors['zh']['zz']))
    text_file.write('\hline  \n')
    text_file.write('\hline  \n')
    text_file.write('Total bkg. & %.2f $\\pm$ %.2f & %.2f $\\pm$ %.2f  & %.2f $\\pm$ %.2f  \\\\ \n '%((yields['llt']['zz']+yields['llt']['fakes']+yields['llt']['wz']),(yield_errors['llt']['zz']**2+yield_errors['llt']['wz']**2+yield_errors['llt']['fakes']**2)**0.5,(yields['ltt']['zz']+yields['ltt']['fakes']+yields['ltt']['wz']),((yield_errors['ltt']['fakes']**2+yield_errors['ltt']['zz']**2+yield_errors['ltt']['wz']**2)**0.5),(yields['zh']['zz']+yields['zh']['fakes']),((yield_errors['zh']['zz']**2+yield_errors['zh']['fakes']**2)**0.5)))
    text_file.write('\hline  \n')
    text_file.write('VH$\\to$V$\\tau\\tau (m_H=125\\GeV)$ & & %.2f & %.2f  & %.2f \\\\ \n'%(yields['llt']['signal'],yields['ltt']['signal'],yields['zh']['signal']))
    text_file.write('VH$\\to$VWW $(m_H=125\\GeV)$ &  %.2f $\\pm$ %.2f & & %.2f $\\pm$ %.2f  \\\\ \n'%(yields['llt']['hww'],yield_errors['llt']['hww'],yields['zh']['hww'],yield_errors['zh']['hww']))
    text_file.write('\hline \n')
    text_file.write('Observed & %.0f $\\pm$ %.0f & %.0f $\\pm$ %.0f & %.0f $\\pm$ %.0f \\\\ \n'%(yields['llt']['data'],yield_errors['llt']['data'],yields['ltt']['data'],yield_errors['ltt']['data'],yields['zh']['data'],yield_errors['zh']['data']))
    text_file.write('\end{tabular} \n')

    periode="7\\,\\TeV"
    if args.period=="8TeV":
       periode="8\\,\\TeV"
    postfit="postfit"
    if args.prefit:
        postfit="prefit"
    text_file2=open("vh_table_paper_"+postfit+args.period+"_"+args.MLfit+".txt","w")
    text_file2.write('\\begin{tabular}{l | c | c | c | c} \n')
    text_file2.write('Process & Signal & Background & Data & $\\frac{S}{S+B}$ \\\\ \n')
    text_file2.write('\hline \n\hline \n')
    text_file2.write('$\\ell\\ell +LL$ & & & & \\\\ \n')
    text_file2.write('$\\Pe\\Pe + \\Pe\\Pgm$ %s & %.3f $\\pm %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['eeem']['signal'],yield_errors['eeem']['signal'],yields['eeem']['fakes']+yields['eeem']['zz'],(yield_errors['eeem']['zz']**2+yield_errors['eeem']['fakes']**2)**0.5,yields['eeem']['data'],getSOverSplusB_ZH(histograms['eeem']['signal'],histograms['eeem']['fakes'],histograms['eeem']['zz'],histograms['eeem']['hww'])))
    text_file2.write('$\\Pgm\\Pgm + \\Pe\\Pgm$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['mmem']['signal'],yield_errors['mmem']['signal'],yields['mmem']['fakes']+yields['mmem']['zz'],(yield_errors['mmem']['zz']**2+yield_errors['mmem']['fakes']**2)**0.5,yields['mmem']['data'],getSOverSplusB_ZH(histograms['mmem']['signal'],histograms['mmem']['fakes'],histograms['mmem']['zz'],histograms['mmem']['hww'])))
    text_file2.write('$\\Pe\\Pe + \\Pgth\\Pgth$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['eett']['signal'],yield_errors['eett']['signal'],yields['eett']['fakes']+yields['eett']['zz'],(yield_errors['eett']['zz']**2+yield_errors['eett']['fakes']**2)**0.5,yields['eett']['data'],getSOverSplusB_ZH(histograms['eett']['signal'],histograms['eett']['fakes'],histograms['eett']['zz'],histograms['eett']['hww'])))
    text_file2.write('$\\Pgm\\Pgm + \\Pgth\\Pgth$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['mmtt']['signal'],yield_errors['mmtt']['signal'],yields['mmtt']['fakes']+yields['mmtt']['zz'],(yield_errors['mmtt']['zz']**2+yield_errors['mmtt']['fakes']**2)**0.5,yields['mmtt']['data'],getSOverSplusB_ZH(histograms['mmtt']['signal'],histograms['mmtt']['fakes'],histograms['mmtt']['zz'],histograms['mmtt']['hww'])))
    text_file2.write('$\\Pe\\Pe + \\Pe\\Pgth$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['eeet']['signal'],yield_errors['eeet']['signal'],yields['eeet']['fakes']+yields['eeet']['zz'],(yield_errors['eeet']['zz']**2+yield_errors['eeet']['fakes']**2)**0.5,yields['eeet']['data'],getSOverSplusB_ZH(histograms['eeet']['signal'],histograms['eeet']['fakes'],histograms['eeet']['zz'],histograms['eeet']['hww'])))
    text_file2.write('$\\Pgm\\Pgm + \\Pe\\Pgth$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['mmet']['signal'],yield_errors['mmet']['signal'],yields['mmet']['fakes']+yields['mmet']['zz'],(yield_errors['mmet']['zz']**2+yield_errors['mmet']['fakes']**2)**0.5,yields['mmet']['data'],getSOverSplusB_ZH(histograms['mmet']['signal'],histograms['mmet']['fakes'],histograms['mmet']['zz'],histograms['mmet']['hww'])))
    text_file2.write('$\\Pe\\Pe + \\Pgm\\Pgth$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['eemt']['signal'],yield_errors['eemt']['signal'],yields['eemt']['fakes']+yields['eemt']['zz'],(yield_errors['eemt']['zz']**2+yield_errors['eemt']['fakes']**2)**0.5,yields['eemt']['data'],getSOverSplusB_ZH(histograms['eemt']['signal'],histograms['eemt']['fakes'],histograms['eemt']['zz'],histograms['eemt']['hww'])))
    text_file2.write('$\\Pgm\\Pgm + \\Pgm\\Pgth$ %s & %.3f $\\pm$ %.3f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['mmmt']['signal'],yield_errors['mmmt']['signal'],yields['mmmt']['fakes']+yields['mmmt']['zz'],(yield_errors['mmmt']['zz']**2+yield_errors['mmmt']['fakes']**2)**0.5,yields['mmmt']['data'],getSOverSplusB_ZH(histograms['mmmt']['signal'],histograms['mmmt']['fakes'],histograms['mmmt']['zz'],histograms['mmmt']['hww'])))
    text_file2.write('\\hline \n')
#print getSOverSplusB_WH(histograms['ett']['signal'],histograms['ett']['signal'],histograms['ett']['signal'],histograms['ett']['signal'],histograms['ett']['signal'])
    text_file2.write('$\\ell +\\ell\\Pgth$ & & & & \\\\ \n')
    if args.period=="8TeV":
       text_file2.write('$\\Pgm + \\Pgm\\Pgth$ low \\LT %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['mmt_low']['signal'],yield_errors['mmt_low']['signal'],yields['mmt_low']['fakes']+yields['mmt_low']['wz']+yields['mmt_low']['zz'],(yield_errors['mmt_low']['wz']**2+yield_errors['mmt_low']['zz']**2+yield_errors['mmt_low']['fakes']**2)**0.5,yields['mmt_low']['data'],getSOverSplusB_WH(histograms['mmt_low']['signal'],histograms['mmt_low']['fakes'],histograms['mmt_low']['zz'],histograms['mmt_low']['hww'],histograms['mmt_low']['wz'])))
       text_file2.write('$\\Pgm + \\Pgm\\Pgth$ high \\LT %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['mmt_high']['signal'],yield_errors['mmt_high']['signal'],yields['mmt_high']['fakes']+yields['mmt_high']['wz']+yields['mmt_high']['zz'],(yield_errors['mmt_high']['wz']**2+yield_errors['mmt_high']['zz']**2+yield_errors['mmt_high']['fakes']**2)**0.5,yields['mmt_high']['data'],getSOverSplusB_WH(histograms['mmt_high']['signal'],histograms['mmt_high']['fakes'],histograms['mmt_high']['zz'],histograms['mmt_high']['hww'],histograms['mmt_high']['wz'])))
       text_file2.write('$\\Pe + \\Pgm\\Pgth$ $\\Pgm + \\Pe\\Pgth$ low \\LT %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['emt_low']['signal'],yield_errors['emt_low']['signal'],yields['emt_low']['fakes']+yields['emt_low']['wz']+yields['emt_low']['zz'],(yield_errors['emt_low']['wz']**2+yield_errors['emt_low']['zz']**2+yield_errors['emt_low']['fakes']**2)**0.5,yields['emt_low']['data'],getSOverSplusB_WH(histograms['emt_low']['signal'],histograms['emt_low']['fakes'],histograms['emt_low']['zz'],histograms['emt_low']['hww'],histograms['emt_low']['wz'])))
       text_file2.write('$\\Pe + \\Pgm\\Pgth$ $\\Pgm + \\Pe\\Pgth$ high \\LT %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f\\\\ \n' %(periode,yields['emt_high']['signal'],yield_errors['emt_high']['signal'],yields['emt_high']['fakes']+yields['emt_high']['wz']+yields['emt_high']['zz'],(yield_errors['emt_high']['wz']**2+yield_errors['emt_high']['zz']**2+yield_errors['emt_high']['fakes']**2)**0.5,yields['emt_high']['data'],getSOverSplusB_WH(histograms['emt_high']['signal'],histograms['emt_high']['fakes'],histograms['emt_high']['zz'],histograms['emt_high']['hww'],histograms['emt_high']['wz'])))
    if args.period=="7TeV":
       text_file2.write('$\\Pgm + \\Pgm\\Pgth$ %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['mmt']['signal'],yield_errors['mmt']['signal'],yields['mmt']['fakes']+yields['mmt']['wz']+yields['mmt']['zz'],(yield_errors['mmt']['wz']**2+yield_errors['mmt']['zz']**2+yield_errors['mmt']['fakes']**2)**0.5,yields['mmt']['data'],getSOverSplusB_WH(histograms['mmt']['signal'],histograms['mmt']['fakes'],histograms['mmt']['zz'],histograms['mmt']['hww'],histograms['mmt']['wz'])))
       text_file2.write('$\\Pe + \\Pgm\\Pgth$ $\\Pgm + \\Pe\\Pgth$ %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['emt']['signal'],yield_errors['emt']['signal'],yields['emt']['fakes']+yields['emt']['wz']+yields['emt']['zz'],(yield_errors['emt']['wz']**2+yield_errors['emt']['zz']**2+yield_errors['emt']['fakes']**2)**0.5,yields['emt']['data'],getSOverSplusB_WH(histograms['emt']['signal'],histograms['emt']['fakes'],histograms['emt']['zz'],histograms['emt']['hww'],histograms['emt']['wz'])))
    text_file2.write('\\hline \n')
    text_file2.write('$\\ell + \\Pgth\\Pghth & & & \\\\ \n')
    text_file2.write('$\\Pe + \\Pgth\\Pgth$ %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['ett']['signal'],yield_errors['ett']['signal'],yields['ett']['fakes']+yields['ett']['wz']+yields['ett']['zz'],(yield_errors['ett']['wz']**2+yield_errors['ett']['zz']**2+yield_errors['ett']['fakes']**2)**0.5,yields['ett']['data'],getSOverSplusB_ZH(histograms['ett']['signal'],histograms['ett']['fakes'],histograms['ett']['zz'],histograms['ett']['wz'])))
    text_file2.write('$\\Pgm + \\Pgth\\Pgth$ %s & %.2f $\\pm$ %.2f & %.1f $\\pm$ %.1f & %.0f & %.3f \\\\ \n' %(periode,yields['mtt']['signal'],yield_errors['mtt']['signal'],yields['mtt']['fakes']+yields['mtt']['wz']+yields['mtt']['zz'],(yield_errors['mtt']['wz']**2+yield_errors['mtt']['zz']**2+yield_errors['mtt']['fakes']**2)**0.5,yields['mtt']['data'],getSOverSplusB_ZH(histograms['mtt']['signal'],histograms['mtt']['fakes'],histograms['mtt']['zz'],histograms['mtt']['wz'])))
    text_file2.write('\\end{tabular} \n')

