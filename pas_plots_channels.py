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

def text_channel(texte):
   """ Writes channel name """
   chan     = ROOT.TPaveText(0.20, 0.76+0.061, 0.32, 0.76+0.161, "NDC")
   chan.SetBorderSize(   0 )
   chan.SetFillStyle(    0 )
   chan.SetTextAlign(   12 )
   chan.SetTextSize ( 0.05 )
   chan.SetTextColor(    1 )
   chan.SetTextFont (   62 )
   chan.AddText(str(texte))
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
    label_text +=", VH#rightarrow V#tau#tau,"
    label_text += " L = %sfb^{-1}" % (intlumi)
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
		   #if os.path.isfile(path + '/' + histogram):
                   th1 = file.Get(path + '/' + histogram)
                   if output is None:
                       output = th1.Clone()
                   else:
                       output.Add(th1)
                   if histogram=="data_obs":
                        if path=="eeem_zh" or path=="mmme_zh" or path=="mmet_zh" or path=="eeet_zh" or path=="mmmt_zh" or path=="eemt_zh" or path=="mmtt_zh" or path=="eett_zh":
                            for i in range(6,9):#partial blinding
                                 output.SetBinContent(i,-100)
                   #     if path=="eetCatLow" or path=="mmtCatLow" or path=="emtCatLow" or path=="eetCatHigh" or path=="mmtCatHigh" or path=="emtCatHigh":
                   #         for i in range(4,7):
                   #              output.SetBinContent(i,-100)
                        if path=="ett" or path=="mtt":
                            for i in range(4,7):
                                 output.SetBinContent(i,-100)
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
    files_to_use_zh =prefit_7TeV_file
    files_to_use_wh =prefit_7TeV_file
    files_to_use_wh_had =prefit_7TeV_file

    if args.MLfit=="channel":
       postfit_7TeV_file_wh_had = ROOT.TFile.Open(postfit_src_wh_had + "/vhtt.input_7TeV.root")
       postfit_8TeV_file_wh_had = ROOT.TFile.Open(postfit_src_wh_had + "/vhtt.input_8TeV.root")
       postfit_7TeV_file_wh = ROOT.TFile.Open(postfit_src_wh + "/vhtt.input_7TeV.root")
       postfit_8TeV_file_wh = ROOT.TFile.Open(postfit_src_wh + "/vhtt.input_8TeV.root")
       postfit_7TeV_file_zh = ROOT.TFile.Open(postfit_src_zh + "/vhtt.input_7TeV.root")
       postfit_8TeV_file_zh = ROOT.TFile.Open(postfit_src_zh + "/vhtt.input_8TeV.root")

       #files_to_use_map = {
       #    (True, '7TeV'): [prefit_7TeV_file],
       #    (True, '8TeV'): [prefit_8TeV_file],
       #    (True, 'all'): [prefit_8TeV_file, prefit_7TeV_file],
       #    (False, '7TeV'): [postfit_7TeV_file],
       #    (False, '8TeV'): [postfit_8TeV_file],
       #    (False, 'all'): [postfit_8TeV_file, postfit_7TeV_file],
       #}

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

    # MMT
    histograms['mmt'] = {}
    mmt_channels = ['mmtCatHigh','mmtCatLow']

    histograms['mmt']['wz'] = get_combined_histogram(
        'wz', mmt_channels, files_to_use_wh, title='WZ',
        style='wz'
    )

    histograms['mmt']['zz'] = get_combined_histogram(
        'zz', mmt_channels, files_to_use_wh, title='ZZ',
        style='zz'
    )

    histograms['mmt']['fakes'] = get_combined_histogram(
        'fakes', mmt_channels, files_to_use_wh, title='Reducible bkg.', style='fakes'
    )

    histograms['mmt']['signal'] = get_combined_histogram(
        'WH125', mmt_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['mmt']['hww'] = get_combined_histogram(
        'WH_hww125', mmt_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='hww',
    )

    histograms['mmt']['data'] = get_combined_histogram(
        'data_obs', mmt_channels, files_to_use_wh,
        title='data', style='data'
    )

    def make_legend():
        output = ROOT.TLegend(0.55, 0.65, 0.90, 0.90, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        return output

    histograms['mmt']['stack'] = ROOT.THStack("mmt_stack", "mmt_stack")
    histograms['mmt']['stack'].Add(histograms['mmt']['fakes'], 'hist')
    histograms['mmt']['stack'].Add(histograms['mmt']['zz'], 'hist')
    histograms['mmt']['stack'].Add(histograms['mmt']['wz'], 'hist')
    histograms['mmt']['stack'].Add(histograms['mmt']['hww'], 'hist')

    errorMMT=histograms['mmt']['zz'].Clone()
    errorMMT.SetFillStyle(3013)
    errorMMT.Add(histograms['mmt']['fakes'])
    errorMMT.Add(histograms['mmt']['hww'])
    errorMMT.Add(histograms['mmt']['wz'])
    errorMMT.SetMarkerSize(0)
    errorMMT.SetFillColor(1)
    errorMMT.SetLineWidth(1)

    histograms['mmt']['stack'].Add(histograms['mmt']['signal'], 'hist')

    histograms['mmt']['legend'] = make_legend()
    histograms['mmt']['legend'].AddEntry(histograms['mmt']['signal'],
                                         "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
    histograms['mmt']['legend'].AddEntry(histograms['mmt']['data'],
                                         "#bf{observed}", "lp")
    histograms['mmt']['legend'].AddEntry(histograms['mmt']['hww'], "#bf{VH(125 GeV)#rightarrow VWW}", "f")
    histograms['mmt']['legend'].AddEntry(histograms['mmt']['wz'], "#bf{WZ}", "f")
    histograms['mmt']['legend'].AddEntry(histograms['mmt']['zz'], "#bf{ZZ}", "f")
    histograms['mmt']['legend'].AddEntry(histograms['mmt']['fakes'],
                                         "#bf{reducible bkg.}", "f")
    if args.prefit==False:
       histograms['mmt']['legend'].AddEntry(errorMMT, "#bf{bkg. uncertainty}", "f")

    # EMT
    histograms['emt'] = {}
    emt_channels = ['emtCatHigh','emtCatLow']

    histograms['emt']['wz'] = get_combined_histogram(
        'wz', emt_channels, files_to_use_wh, title='WZ',
        style='wz'
    )

    histograms['emt']['zz'] = get_combined_histogram(
        'zz', emt_channels, files_to_use_wh, title='ZZ',
        style='zz'
    )

    histograms['emt']['fakes'] = get_combined_histogram(
        'fakes', emt_channels, files_to_use_wh, title='Reducible bkg.', style='fakes'
    )

    histograms['emt']['signal'] = get_combined_histogram(
        'WH125', emt_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['emt']['hww'] = get_combined_histogram(
        'WH_hww125', emt_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='hww',
    )

    histograms['emt']['data'] = get_combined_histogram(
        'data_obs', emt_channels, files_to_use_wh,
        title='data', style='data'
    )

    histograms['emt']['stack'] = ROOT.THStack("emt_stack", "emt_stack")
    histograms['emt']['stack'].Add(histograms['emt']['fakes'], 'hist')
    histograms['emt']['stack'].Add(histograms['emt']['zz'], 'hist')
    histograms['emt']['stack'].Add(histograms['emt']['wz'], 'hist')
    histograms['emt']['stack'].Add(histograms['emt']['hww'], 'hist')

    errorEMT=histograms['emt']['zz'].Clone()
    errorEMT.SetFillStyle(3013)
    errorEMT.Add(histograms['emt']['fakes'])
    errorEMT.Add(histograms['emt']['wz'])
    errorEMT.Add(histograms['emt']['hww'])
    errorEMT.SetMarkerSize(0)
    errorEMT.SetFillColor(1)
    errorEMT.SetLineWidth(1)

    histograms['emt']['stack'].Add(histograms['emt']['signal'], 'hist')


    # EET
    histograms['eet'] = {}
    eet_channels = ['eetCatHigh','eetCatLow']
    eet_channels_flip = ['eetCatLow','eetCatHigh']

    histograms['eet']['wz'] = get_combined_histogram(
        'wz', eet_channels, files_to_use_wh, title='WZ',
        style='wz'
    )

    histograms['eet']['zz'] = get_combined_histogram(
        'zz', eet_channels, files_to_use_wh, title='ZZ',
        style='zz'
    )

    histograms['eet']['fakes'] = get_combined_histogram(
        'fakes', eet_channels, files_to_use_wh, title='Reducible bkg.', style='fakes'
    )

    histograms['eet']['charge_fakes'] = get_combined_histogram(
        'charge_fakes', eet_channels_flip, files_to_use_wh, title='Reducible bkg. charge flip', style='charge_fakes'
    )

    histograms['eet']['signal'] = get_combined_histogram(
        'WH125', eet_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['eet']['hww'] = get_combined_histogram(
        'WH_hww125', eet_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='hww',
    )

    histograms['eet']['data'] = get_combined_histogram(
        'data_obs', eet_channels, files_to_use_wh,
        title='data', style='data'
    )

    histograms['eet']['stack'] = ROOT.THStack("eet_stack", "eet_stack")
    histograms['eet']['stack'].Add(histograms['eet']['charge_fakes'], 'hist')
    histograms['eet']['stack'].Add(histograms['eet']['fakes'], 'hist')
    histograms['eet']['stack'].Add(histograms['eet']['zz'], 'hist')
    histograms['eet']['stack'].Add(histograms['eet']['wz'], 'hist')
    histograms['eet']['stack'].Add(histograms['eet']['hww'], 'hist')

    errorEET=histograms['eet']['zz'].Clone()
    errorEET.SetFillStyle(3013)
    errorEET.Add(histograms['eet']['fakes'])
    errorEET.Add(histograms['eet']['charge_fakes'])
    errorEET.Add(histograms['eet']['wz'])
    errorEET.Add(histograms['eet']['hww'])
    errorEET.SetMarkerSize(0)
    errorEET.SetFillColor(1)
    errorEET.SetLineWidth(1)

    histograms['eet']['stack'].Add(histograms['eet']['signal'], 'hist')

    # LLEM
    histograms['llem'] = {}
    llem_channels = ['eeem_zh', 'mmme_zh']

    histograms['llem']['zz'] = get_combined_histogram(
        ['ZZ', 'GGToZZ2L2L', 'TTZ'], llem_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['llem']['hww'] = get_combined_histogram(
        'ZH_hww125', llem_channels, files_to_use_zh, title='HWW',
        style='hww'
    )

    histograms['llem']['fakes'] = get_combined_histogram(
        'Zjets', llem_channels, files_to_use_zh, title='Reducible bkg.',
        style='fakes'
    )

    histograms['llem']['signal'] = get_combined_histogram(
        'ZH_htt125', llem_channels, files_to_use_zh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['llem']['data'] = get_combined_histogram(
        'data_obs', llem_channels, files_to_use_zh,
        title='data', style='data',
    )

    histograms['llem']['stack'] = ROOT.THStack("llem_stack", "llem_stack")
    histograms['llem']['stack'].Add(histograms['llem']['fakes'], 'hist')
    histograms['llem']['stack'].Add(histograms['llem']['zz'], 'hist')
    histograms['llem']['stack'].Add(histograms['llem']['hww'], 'hist')
    histograms['llem']['stack'].Add(histograms['llem']['signal'], 'hist')

    errorLLEM=histograms['llem']['zz'].Clone()
    errorLLEM.SetFillStyle(3013)
    errorLLEM.Add(histograms['llem']['fakes'])
    errorLLEM.Add(histograms['llem']['hww'])
    errorLLEM.SetMarkerSize(0) 
    errorLLEM.SetFillColor(1)
    errorLLEM.SetLineWidth(1)

    histograms['llem']['data'].SetMarkerStyle(20)
    histograms['llem']['data'].SetMarkerColor(ROOT.EColor.kBlack)
    histograms['llem']['data'].SetLineColor(ROOT.EColor.kBlack)
    histograms['llem']['data'].SetLineWidth(2)
    histograms['llem']['data'].SetMarkerSize(2)

    histograms['llem']['legend'] = make_legend()
    histograms['llem']['legend'].AddEntry(histograms['llem']['signal'],
                                        "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
    histograms['llem']['legend'].AddEntry(histograms['llem']['data'],
                                        "#bf{observed}", "lp")
    histograms['llem']['legend'].AddEntry(histograms['llem']['hww'], "#bf{VH(125 GeV)#rightarrow VWW}", "f")
    histograms['llem']['legend'].AddEntry(histograms['llem']['zz'], "#bf{ZZ}", "f")
    histograms['llem']['legend'].AddEntry(histograms['llem']['fakes'],
                                        "#bf{reducible bkg.}", "f")
    if args.prefit==False:
       histograms['llem']['legend'].AddEntry(errorLLEM, "#bf{bkg. uncertainty}", "F")

    # LLMT
    histograms['llmt'] = {}
    llmt_channels = ['eemt_zh', 'mmmt_zh']

    histograms['llmt']['zz'] = get_combined_histogram(
        'ZZ', llmt_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['llmt']['zz'] = get_combined_histogram(
        ['ZZ', 'GGToZZ2L2L', 'TTZ'], llmt_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['llmt']['hww'] = get_combined_histogram(
        'ZH_hww125', llmt_channels, files_to_use_zh, title='HWW',
        style='hww'
    )

    histograms['llmt']['fakes'] = get_combined_histogram(
        'Zjets', llmt_channels, files_to_use_zh, title='Reducible bkg.',
        style='fakes'
    )

    histograms['llmt']['signal'] = get_combined_histogram(
        'ZH_htt125', llmt_channels, files_to_use_zh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['llmt']['data'] = get_combined_histogram(
        'data_obs', llmt_channels, files_to_use_zh,
        title='data', style='data',
    )

    histograms['llmt']['stack'] = ROOT.THStack("llmt_stack", "llmt_stack")
    histograms['llmt']['stack'].Add(histograms['llmt']['fakes'], 'hist')
    histograms['llmt']['stack'].Add(histograms['llmt']['zz'], 'hist')
    histograms['llmt']['stack'].Add(histograms['llmt']['hww'], 'hist')
    histograms['llmt']['stack'].Add(histograms['llmt']['signal'], 'hist')

    errorLLMT=histograms['llmt']['zz'].Clone()
    errorLLMT.SetFillStyle(3013)
    errorLLMT.Add(histograms['llmt']['fakes'])
    errorLLMT.Add(histograms['llmt']['hww'])
    errorLLMT.SetMarkerSize(0)
    errorLLMT.SetFillColor(1)
    errorLLMT.SetLineWidth(1)

    # LLET
    histograms['llet'] = {}
    llet_channels = ['eeet_zh','mmet_zh']

    histograms['llet']['zz'] = get_combined_histogram(
        'ZZ', llet_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['llet']['zz'] = get_combined_histogram(
        ['ZZ', 'GGToZZ2L2L', 'TTZ'], llet_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['llet']['hww'] = get_combined_histogram(
        'ZH_hww125', llet_channels, files_to_use_zh, title='HWW',
        style='hww'
    )

    histograms['llet']['fakes'] = get_combined_histogram(
        'Zjets', llet_channels, files_to_use_zh, title='Reducible bkg.',
        style='fakes'
    )

    histograms['llet']['signal'] = get_combined_histogram(
        'ZH_htt125', llet_channels, files_to_use_zh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['llet']['data'] = get_combined_histogram(
        'data_obs', llet_channels, files_to_use_zh,
        title='data', style='data',
    )

    histograms['llet']['stack'] = ROOT.THStack("llet_stack", "llet_stack")
    histograms['llet']['stack'].Add(histograms['llet']['fakes'], 'hist')
    histograms['llet']['stack'].Add(histograms['llet']['zz'], 'hist')
    histograms['llet']['stack'].Add(histograms['llet']['hww'], 'hist')
    histograms['llet']['stack'].Add(histograms['llet']['signal'], 'hist')

    errorLLET=histograms['llet']['zz'].Clone()
    errorLLET.SetFillStyle(3013)
    errorLLET.Add(histograms['llet']['fakes'])
    errorLLET.Add(histograms['llet']['hww'])
    errorLLET.SetMarkerSize(0)
    errorLLET.SetFillColor(1)
    errorLLET.SetLineWidth(1)

    # LLTT
    histograms['lltt'] = {}
    lltt_channels = ['eett_zh','mmtt_zh']

    histograms['lltt']['zz'] = get_combined_histogram(
        'ZZ', lltt_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['lltt']['zz'] = get_combined_histogram(
        ['ZZ', 'GGToZZ2L2L', 'TTZ'], lltt_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['lltt']['hww'] = get_combined_histogram(
        'ZH_hww125', lltt_channels, files_to_use_zh, title='HWW',
        style='hww'
    )

    histograms['lltt']['fakes'] = get_combined_histogram(
        'Zjets', lltt_channels, files_to_use_zh, title='Reducible bkg.',
        style='fakes'
    )

    histograms['lltt']['signal'] = get_combined_histogram(
        'ZH_htt125', lltt_channels, files_to_use_zh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['lltt']['data'] = get_combined_histogram(
        'data_obs', lltt_channels, files_to_use_zh,
        title='data', style='data',
    )

    histograms['lltt']['stack'] = ROOT.THStack("lltt_stack", "lltt_stack")
    histograms['lltt']['stack'].Add(histograms['lltt']['fakes'], 'hist')
    histograms['lltt']['stack'].Add(histograms['lltt']['zz'], 'hist')
    histograms['lltt']['stack'].Add(histograms['lltt']['hww'], 'hist')
    histograms['lltt']['stack'].Add(histograms['lltt']['signal'], 'hist')

    errorLLTT=histograms['lltt']['zz'].Clone()
    errorLLTT.SetFillStyle(3013)
    errorLLTT.Add(histograms['lltt']['fakes'])
    errorLLTT.Add(histograms['lltt']['hww'])
    errorLLTT.SetMarkerSize(0)
    errorLLTT.SetFillColor(1)
    errorLLTT.SetLineWidth(1)

    # LTT
    histograms['mtt'] = {}
    mtt_channels = ['mtt']

    histograms['mtt']['wz'] = get_combined_histogram(
        'wz', mtt_channels, files_to_use_wh_had, title='WZ',
        style='wz',
    )

    histograms['mtt']['zz'] = get_combined_histogram(
        'zz', mtt_channels, files_to_use_wh_had, title='ZZ',
        style='zz',)

    histograms['mtt']['fakes'] = get_combined_histogram(
        'fakes', mtt_channels, files_to_use_wh_had, title='Reducible bkg.',
        style='fakes',
    )

    histograms['mtt']['signal'] = get_combined_histogram(
        ['WH_htt125'], mtt_channels, files_to_use_wh_had,
        title='m_{H}=125 GeV', style='signal')

    histograms['mtt']['data'] = get_combined_histogram(
        'data_obs', mtt_channels, files_to_use_wh_had,
        title='data', style='data')

    histograms['mtt']['stack'] = ROOT.THStack("mtt_stack", "mtt_stack")
    histograms['mtt']['stack'].Add(histograms['mtt']['fakes'], "hist")
    histograms['mtt']['stack'].Add(histograms['mtt']['zz'], "hist")
    histograms['mtt']['stack'].Add(histograms['mtt']['wz'], "hist")
    histograms['mtt']['stack'].Add(histograms['mtt']['signal'], "hist")

    errorMTT=histograms['mtt']['zz'].Clone()
    errorMTT.SetFillStyle(3013)
    errorMTT.Add(histograms['mtt']['fakes'])
    errorMTT.Add(histograms['mtt']['wz'])
    errorMTT.SetMarkerSize(0) 
    errorMTT.SetFillColor(1)
    errorMTT.SetLineWidth(1)

    histograms['mtt']['legend'] = make_legend()
    histograms['mtt']['legend'].AddEntry(histograms['mtt']['signal'],
                                         "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
    histograms['mtt']['legend'].AddEntry(histograms['mtt']['data'],
                                         "#bf{observed}", "lp")
    histograms['mtt']['legend'].AddEntry(histograms['mtt']['wz'], "#bf{WZ}", "f")
    histograms['mtt']['legend'].AddEntry(histograms['mtt']['zz'], "#bf{ZZ}", "f")
    histograms['mtt']['legend'].AddEntry(histograms['mtt']['fakes'],
                                         "#bf{reducible bkg.}", "f")
    if args.prefit==False:
       histograms['mtt']['legend'].AddEntry(errorMTT,"#bf{bkg. uncertainty}","F")


    # ETT
    histograms['ett'] = {}
    ett_channels = ['ett']

    histograms['ett']['wz'] = get_combined_histogram(
        'wz', ett_channels, files_to_use_wh_had, title='WZ',
        style='wz',
    )

    histograms['ett']['zz'] = get_combined_histogram(
        'zz', ett_channels, files_to_use_wh_had, title='ZZ',
        style='zz',)

    histograms['ett']['fakes'] = get_combined_histogram(
        'fakes', ett_channels, files_to_use_wh_had, title='Reducible bkg.',
        style='fakes',
    )

    histograms['ett']['signal'] = get_combined_histogram(
        ['WH_htt125'], ett_channels, files_to_use_wh_had,
        title='m_{H}=125 GeV', style='signal')

    histograms['ett']['data'] = get_combined_histogram(
        'data_obs', ett_channels, files_to_use_wh_had,
        title='data', style='data')

    histograms['ett']['stack'] = ROOT.THStack("ett_stack", "ett_stack")
    histograms['ett']['stack'].Add(histograms['ett']['fakes'], "hist")
    histograms['ett']['stack'].Add(histograms['ett']['zz'], "hist")
    histograms['ett']['stack'].Add(histograms['ett']['wz'], "hist")
    histograms['ett']['stack'].Add(histograms['ett']['signal'], "hist")

    errorETT=histograms['ett']['zz'].Clone()
    errorETT.SetFillStyle(3013)
    errorETT.Add(histograms['ett']['fakes'])
    errorETT.Add(histograms['ett']['wz'])
    errorETT.SetMarkerSize(0)
    errorETT.SetFillColor(1)
    errorETT.SetLineWidth(1)

    # Apply some styles to all the histograms
    for channel in ['emt', 'mmt', 'eet', 'llem', 'llet', 'llmt', 'lltt', 'ett', 'mtt']:
        # Use Poissonian error bars. The set_zero_bins makes it so bins w/o
        # any data are blank.
        histograms[channel]['poisson'] = convert(histograms[channel]['data'],
                                                 set_zero_bins=-10)
        # Make sure all data points are visible
        fix_maximum(histograms[channel])
        # We have to draw it so things like the axes are initialized.
        histograms[channel]['stack'].Draw()
        histograms[channel]['stack'].GetYaxis().SetTitle(
            "#bf{Events/%i GeV}" % histograms[channel]['data'].GetBinWidth(1))
	if channel=='lltt' or channel=="llet" or channel=="llmt" or channel=="llem":
           histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{#tau#tau} [GeV]}")
	else:
           histograms[channel]['stack'].GetXaxis().SetTitle("#bf{m_{vis} [GeV]}")


    plot_suffix = "_%s_%s_%s.pdf" % (
        'prefit' if args.prefit else 'postfit',
        args.period,
	'FitByChannel' if args.MLfit=="channel" else 'FitAllChannels'
    )

    catllt      = ROOT.TPaveText(0.20, 0.71+0.061, 0.32, 0.71+0.161, "NDC");
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

    chan_ett=text_channel("e#tau#tau")
    chan_mtt=text_channel("#mu#tau#tau")
    chan_em=text_channel("e#mu")
    chan_mt=text_channel("#mu#tau")
    chan_emt=text_channel("e#mu#tau")
    chan_mmt=text_channel("#mu#mu#tau")
    chan_eet=text_channel("ee#tau")
    chan_tt=text_channel("#tau#tau")
    chan_et=text_channel("e#tau")

    # Figure out what goes in the CMS preliminary line
    blurb_map = {
        '7TeV': ('5.0', '7'),
        '8TeV': ('19.7', '8'),
        'all': ('24.7', '7+8'),
    }
    int_lumi, sqrts = blurb_map[args.period]

    canvas=MakeCanvas("asdf","asdf",800,800)

    histograms['mmt']['stack'].Draw()
    if args.prefit==False:
       errorMMT.Draw("e2same");
    #histograms['mmt']['poisson'].Draw('pe same')
    catllt.Draw("same")
    histograms['mmt']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_mmt.Draw("same")
    canvas.SaveAs('plots/mmt' + plot_suffix)

    histograms['emt']['stack'].Draw()
    if args.prefit==False:
       errorEMT.Draw("e2same");
    #histograms['emt']['poisson'].Draw('pe same')
    catllt.Draw("same")
    histograms['mmt']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_emt.Draw("same")
    canvas.SaveAs('plots/emt' + plot_suffix)

    histograms['eet']['stack'].Draw()
    if args.prefit==False:
       errorEET.Draw("e2same");
    #histograms['eet']['poisson'].Draw('pe same')
    catllt.Draw("same")
    histograms['mmt']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_eet.Draw("same")
    canvas.SaveAs('plots/eet' + plot_suffix)

    histograms['llem']['stack'].Draw()
    if args.prefit==False:
       errorLLEM.Draw("e2same")
    histograms['llem']['poisson'].SetMarkerStyle(20)
    histograms['llem']['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
    histograms['llem']['poisson'].SetLineColor(ROOT.EColor.kBlack)
    histograms['llem']['poisson'].SetLineWidth(2)
    histograms['llem']['poisson'].SetMarkerSize(2)
    histograms['llem']['poisson'].Draw('pe same')
    catZH.Draw("same")
    histograms['llem']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_em.Draw("same")
    canvas.SaveAs('plots/llem' + plot_suffix)

    histograms['llmt']['stack'].Draw()
    if args.prefit==False:
       errorLLMT.Draw("e2same")
    histograms['llmt']['poisson'].SetMarkerStyle(20)
    histograms['llmt']['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
    histograms['llmt']['poisson'].SetLineColor(ROOT.EColor.kBlack)
    histograms['llmt']['poisson'].SetLineWidth(2)
    histograms['llmt']['poisson'].SetMarkerSize(2)
    histograms['llmt']['poisson'].Draw('pe same')
    catZH.Draw("same")
    histograms['llem']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_mt.Draw("same")
    canvas.SaveAs('plots/llmt' + plot_suffix)

    histograms['llet']['stack'].Draw()
    if args.prefit==False:
       errorLLET.Draw("e2same")
    histograms['llet']['poisson'].SetMarkerStyle(20)
    histograms['llet']['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
    histograms['llet']['poisson'].SetLineColor(ROOT.EColor.kBlack)
    histograms['llet']['poisson'].SetLineWidth(2)
    histograms['llet']['poisson'].SetMarkerSize(2)
    histograms['llet']['poisson'].Draw('pe same')
    catZH.Draw("same")
    histograms['llem']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_et.Draw("same")
    canvas.SaveAs('plots/llet' + plot_suffix)

    histograms['lltt']['stack'].Draw()
    if args.prefit==False:
       errorLLTT.Draw("e2same")
    histograms['lltt']['poisson'].SetMarkerStyle(20)
    histograms['lltt']['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
    histograms['lltt']['poisson'].SetLineColor(ROOT.EColor.kBlack)
    histograms['lltt']['poisson'].SetLineWidth(2)
    histograms['lltt']['poisson'].SetMarkerSize(2)
    histograms['lltt']['poisson'].Draw('pe same')
    catZH.Draw("same")
    histograms['llem']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_tt.Draw("same")
    canvas.SaveAs('plots/lltt' + plot_suffix)

    histograms['mtt']['stack'].Draw()
    if args.prefit==False:
       errorMTT.Draw("e2same")
    histograms['mtt']['poisson'].Draw('pe same')
    catltt.Draw("same")
    histograms['mtt']['legend'].Draw()
    limiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_mtt.Draw("same")
    canvas.SaveAs('plots/mtt' + plot_suffix)

    histograms['ett']['stack'].Draw()
    if args.prefit==False:
       errorETT.Draw("e2same")
    histograms['ett']['poisson'].Draw('pe same')
    catltt.Draw("same")
    histograms['mtt']['legend'].Draw()
    limiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    chan_ett.Draw("same")
    canvas.SaveAs('plots/ett' + plot_suffix)
