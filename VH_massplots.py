'''

Make plots for the HIG-12-053 PAS

'''

from RecoLuminosity.LumiDB import argparse
import math
import os
from poisson import convert
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
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

def text_channel(canal):   
   """ Writes channel name """
   chan     = ROOT.TPaveText(0.20, 0.76+0.061, 0.32, 0.76+0.161, "NDC")
   chan.SetBorderSize(   0 )
   chan.SetFillStyle(    0 )
   chan.SetTextAlign(   12 )
   chan.SetTextSize ( 0.05 )
   chan.SetTextColor(    1 )
   chan.SetTextFont (   62 )
   texte=' '
   if canal=='emt_high':
	 texte="e#mu#tau_{h} high"
   if canal=='emt_low':
	 texte='e#mu#tau_{h} low'
   if canal=='mmt_high':
	 texte='#mu#mu#tau_{h} high'
   if canal=='mmt_low':
	 texte='#mu#mu#tau_{h} low'
   if canal=='emt':
	 texte='e#mu#tau_{h}'
   if canal=='mmt':
	 texte='#mu#mu#tau_{h}'
   if canal=='ett':
	 texte='e#tau_{h}#tau_{h}'
   if canal=='mtt':
	 texte='#mu#tau_{h}#tau_{h}'
   if canal=='llem':
	 texte='lle#mu'
   if canal=='llet':
	 texte='lle#tau_{h}'
   if canal=='llmt':
	 texte='ll#mu#tau_{h}'
   if canal=='lltt':
	 texte='ll#tau_{h}#tau_{h}'

   chan.AddText(texte)
   return chan


def fix_maximum(channel_dict, cushion=1.3):
    """ Make sure everything is visible """
    max = channel_dict['stack'].GetMaximum()
    histo = channel_dict['data']
    for bin in range(histo.GetNbinsX()):
        content = histo.GetBinContent(bin)
        if content>0:
           upper = content + math.sqrt(content)
        else:
           upper = content
        #print bin, upper, max
        if upper > max:
            max = upper
    channel_dict['stack'].SetMaximum(cushion * max)


def add_cms_blurb(sqrts, intlumi, preliminary=True, blurb=''):
    """ Add a CMS blurb to a plot """
    # Same style as Htt
    label_text = "CMS"
    if preliminary:
        label_text += " Preliminary"
    label_text +=", "
    label_text += " %sfb^{-1}" % (intlumi)
    label_text += " at %s TeV" % sqrts
    label_text += " " + blurb
    lowX=0.16
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextSize ( 0.03 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont (   62 )
    lumi.AddText(label_text)
    return lumi

_styles = {
    "wz": {
        # Same as Z+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.EColor.kOrange - 4,
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "zz": {
        # Same as W+jets
        'fillstyle': 1001,
        'fillcolor': ROOT.EColor.kRed + 2,
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "fakes": {
        # Same as QCD
        'fillcolor': ROOT.EColor.kMagenta - 10,
        'linecolor': ROOT.EColor.kBlack,
        'fillstyle': 1001,
        'linewidth': 3,
    },
    "charge_fakes": {
        # Same as QCD
        'fillcolor': ROOT.EColor.kMagenta - 10,
        'linecolor': ROOT.EColor.kMagenta - 10,
        'fillstyle': 1001,
        'linewidth': 0,
    },
    "GGToZZ2L2L": {
        # Same as QCD
        'fillcolor': ROOT.EColor.kRed + 2,
        'linecolor': ROOT.EColor.kRed + 2,
        'fillstyle': 1001,
        'linewidth': 3,
    },
    "hww": {
        'fillstyle': 1001,
        'fillcolor': ROOT.EColor.kGreen + 3,
        'linecolor': ROOT.EColor.kBlack,
        'linewidth': 3,
    },
    "signal": {
        'fillcolor': 0,
        'fillstyle': 0,
        'linestyle': 2,
        'linewidth': 5,
        'linecolor': ROOT.EColor.kBlue,
        'name': "VH",
    },
    "data": {
        'markerstyle': 20,
        'markersize': 2,
        'linewidth': 2,
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
                   else:
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
        'llt_high': [x for x in all_llt_channels if 'Low' in x],
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
            output = ROOT.TLegend(0.55, 0.65, 0.90, 0.90, "", "brNDC")
            output.SetLineWidth(0)
            output.SetLineStyle(0)
            output.SetFillStyle(0)
            output.SetBorderSize(0)
            return output
        llt_plots['stack'] = ROOT.THStack("llt_stack", "llt_stack")
        if channel_subset_flip:
            llt_plots['stack'].Add(llt_plots['charge_fakes'], 'hist')
        llt_plots['stack'].Add(llt_plots['fakes'], 'hist')
        llt_plots['stack'].Add(llt_plots['zz'], 'hist')
        llt_plots['stack'].Add(llt_plots['wz'], 'hist')
        llt_plots['stack'].Add(llt_plots['hww'], 'hist')

        errorLLT = llt_plots['zz'].Clone()
        errorLLT.SetFillStyle(3013)
        errorLLT.Add(llt_plots['fakes'])
        if channel_subset_flip:
            errorLLT.Add(llt_plots['charge_fakes'])
        errorLLT.Add(llt_plots['wz'])
        errorLLT.Add(llt_plots['hww'])
        errorLLT.SetMarkerSize(0)
        errorLLT.SetFillColor(1)
        errorLLT.SetLineWidth(1)
        llt_plots['error'] = errorLLT

        llt_plots['stack'].Add(llt_plots['signal'], 'hist')

        llt_plots['legend'] = make_legend()
        llt_plots['legend'].AddEntry(
            llt_plots['signal'],
            "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
        llt_plots['legend'].AddEntry(
            llt_plots['data'],
            "#bf{observed}", "lp")
        llt_plots['legend'].AddEntry(llt_plots['hww'],
                                     "#bf{VH(125 GeV)#rightarrow VWW}", "f")
        llt_plots['legend'].AddEntry(llt_plots['wz'], "#bf{WZ}", "f")
        llt_plots['legend'].AddEntry(llt_plots['zz'], "#bf{ZZ}", "f")
        llt_plots['legend'].AddEntry(llt_plots['fakes'],
                                     "#bf{reducible bkg.}", "f")
        if not args.prefit:
            llt_plots['legend'].AddEntry(
                errorLLT, "#bf{bkg. uncertainty}", "f")

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
        zh_plots['stack'].Add(zh_plots['fakes'], 'hist')
        zh_plots['stack'].Add(zh_plots['zz'], 'hist')
        zh_plots['stack'].Add(zh_plots['hww'], 'hist')
        zh_plots['stack'].Add(zh_plots['signal'], 'hist')

        errorZH=zh_plots['zz'].Clone()
        errorZH.SetFillStyle(3013)
        errorZH.Add(zh_plots['fakes'])
        errorZH.Add(zh_plots['hww'])
        errorZH.SetMarkerSize(0)
        errorZH.SetFillColor(1)
        errorZH.SetLineWidth(1)

	zh_plots['error'] = errorZH

        zh_plots['legend'] = make_legend()
        zh_plots['legend'].AddEntry(zh_plots['signal'],
                                        "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
        zh_plots['legend'].AddEntry(zh_plots['data'],
                                        "#bf{observed}", "lp")
        zh_plots['legend'].AddEntry(zh_plots['hww'],
                                        "#bf{VH(125 GeV)#rightarrow VWW}", "f")
        zh_plots['legend'].AddEntry(zh_plots['zz'], "#bf{ZZ}", "f")
        zh_plots['legend'].AddEntry(zh_plots['fakes'],
                                        "#bf{reducible bkg.}", "f")
        if args.prefit==False:
           zh_plots['legend'].AddEntry(errorZH, "#bf{bkg. uncertainty}", "F")

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
        integrale=ltt_plots['data'].IntegralAndError(1,num_bins_ltt,erreur)
        ltt_integrales['data']=float(integrale)
        ltt_erreurs['data']=float(erreur)
        ltt_plots['stack'] = ROOT.THStack("ltt_stack", "ltt_stack")
        ltt_plots['stack'].Add(ltt_plots['fakes'], "hist")
        ltt_plots['stack'].Add(ltt_plots['zz'], "hist")
        ltt_plots['stack'].Add(ltt_plots['wz'], "hist")
        ltt_plots['stack'].Add(ltt_plots['signal'], "hist")

        errorLTT=ltt_plots['zz'].Clone()
        errorLTT.SetFillStyle(3013)
        errorLTT.Add(ltt_plots['fakes'])
        errorLTT.Add(ltt_plots['wz'])
        errorLTT.SetMarkerSize(0)
        errorLTT.SetFillColor(1)
        errorLTT.SetLineWidth(1)

	ltt_plots['error'] = errorLTT

        ltt_plots['legend'] = make_legend()
        ltt_plots['legend'].AddEntry(ltt_plots['signal'],
                                         "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
        ltt_plots['legend'].AddEntry(ltt_plots['data'],
                                         "#bf{observed}", "lp")
        ltt_plots['legend'].AddEntry(ltt_plots['wz'], "#bf{WZ}", "f")
        ltt_plots['legend'].AddEntry(ltt_plots['zz'], "#bf{ZZ}", "f")
        ltt_plots['legend'].AddEntry(ltt_plots['fakes'],
                                             "#bf{reducible bkg.}", "f")
        if args.prefit==False:
           ltt_plots['legend'].AddEntry(errorLTT,"#bf{bkg. uncertainty}","F")

    # Apply some styles to all the histograms
    for channel in histograms.keys():
    #for channel in ['zh']:
        # Use Poissonian error bars. The set_zero_bins makes it so bins w/o
        # any data are blank.
        histograms[channel]['poisson'] = convert(histograms[channel]['data'],
                                                 set_zero_bins=-10)
        # Make sure all data points are visible
        fix_maximum(histograms[channel])
        # We have to draw it so things like the axes are initialized.
        histograms[channel]['stack'].Draw()
        #histograms[channel]['stack'].GetYaxis().SetTitle(
        #    "#bf{Events/%i GeV}" % histograms[channel]['data'].GetBinWidth(1))
        histograms[channel]['stack'].GetYaxis().SetTitle(
            "#bf{Events}" )
        if channel=='zh':
           histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{#tau#tau} [GeV]}")
        else:
           histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{vis} [GeV]}")


    plot_suffix = "_%s_%s_%s.pdf" % (
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
        histograms[llt_key]['poisson'].Draw('pe same')
        catllt.Draw("same")
        histograms[llt_key]['legend'].Draw()
        lumiBlurb = add_cms_blurb(sqrts, int_lumi)
        lumiBlurb.Draw("same")
	channel_text=text_channel(llt_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + llt_key + plot_suffix)

    for zh_key in zh_subplots:
        histograms[zh_key]['stack'].Draw()
        if args.prefit==False:
           histograms[zh_key]['error'].Draw("e2same")
        histograms[zh_key]['poisson'].SetMarkerStyle(20)
        histograms[zh_key]['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
        histograms[zh_key]['poisson'].SetLineColor(ROOT.EColor.kBlack)
        histograms[zh_key]['poisson'].SetLineWidth(2)
        histograms[zh_key]['poisson'].SetMarkerSize(2)
        histograms[zh_key]['poisson'].Draw('pe same')
        catZH.Draw("same")
        histograms[zh_key]['legend'].Draw()
        lumiBlurb=add_cms_blurb(sqrts, int_lumi)
        lumiBlurb.Draw("same")
        channel_text=text_channel(zh_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + zh_key + plot_suffix)

    for ltt_key in ltt_subplots:
        histograms[ltt_key]['stack'].Draw()
        if args.prefit==False:
           histograms[ltt_key]['error'].Draw("e2same")
        histograms[ltt_key]['poisson'].Draw('pe same')
        catltt.Draw("same")
        histograms[ltt_key]['legend'].Draw()
        limiBlurb=add_cms_blurb(sqrts, int_lumi)
        lumiBlurb.Draw("same")
        channel_text=text_channel(ltt_key)
        channel_text.Draw('same')
        canvas.SaveAs('plots/' + ltt_key + plot_suffix)

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


