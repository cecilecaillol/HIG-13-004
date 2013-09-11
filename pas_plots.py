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
		   #print path,histogram
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
                        if path=="ett" or directories=="mtt":
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

    # LLT
    histograms['llt'] = {}
    llt_channels = ['emtCatHigh','emtCatLow', 'mmtCatHigh','mmtCatLow','eetCatHigh','eetCatLow']
    llt_channels_flip = ['eetCatLow','eetCatHigh']

    histograms['llt']['wz'] = get_combined_histogram(
        'wz', llt_channels, files_to_use_wh, title='WZ',
        style='wz'
    )
    histograms['llt']['zz'] = get_combined_histogram(
        'zz', llt_channels, files_to_use_wh, title='ZZ',
        style='zz'
    )
    histograms['llt']['fakes'] = get_combined_histogram(
        'fakes', llt_channels, files_to_use_wh, title='Reducible bkg.', style='fakes'
    )
    histograms['llt']['charge_fakes'] = get_combined_histogram(
        'charge_fakes', llt_channels_flip, files_to_use_wh, title='Reducible bkg. charge flip', style='charge_fakes'
    )
    histograms['llt']['signal'] = get_combined_histogram(
        'WH125', llt_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='signal',
    )
    histograms['llt']['hww'] = get_combined_histogram(
        'WH_hww125', llt_channels, files_to_use_wh,
        title='m_{H}=125 GeV', style='hww',
    )
    histograms['llt']['data'] = get_combined_histogram(
        'data_obs', llt_channels, files_to_use_wh,
        title='data', style='data'
    )
    def make_legend():
        output = ROOT.TLegend(0.55, 0.65, 0.90, 0.90, "", "brNDC")
        output.SetLineWidth(0)
        output.SetLineStyle(0)
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        return output
    histograms['llt']['stack'] = ROOT.THStack("llt_stack", "llt_stack")
    histograms['llt']['stack'].Add(histograms['llt']['charge_fakes'], 'hist')
    histograms['llt']['stack'].Add(histograms['llt']['fakes'], 'hist')
    histograms['llt']['stack'].Add(histograms['llt']['zz'], 'hist')
    histograms['llt']['stack'].Add(histograms['llt']['wz'], 'hist')
    histograms['llt']['stack'].Add(histograms['llt']['hww'], 'hist')

    errorLLT=histograms['llt']['zz'].Clone()
    errorLLT.SetFillStyle(3013)
    errorLLT.Add(histograms['llt']['fakes'])
    errorLLT.Add(histograms['llt']['charge_fakes'])
    errorLLT.Add(histograms['llt']['wz'])
    errorLLT.Add(histograms['llt']['hww'])
    errorLLT.SetMarkerSize(0)
    errorLLT.SetFillColor(1)
    errorLLT.SetLineWidth(1)

    histograms['llt']['stack'].Add(histograms['llt']['signal'], 'hist')

    histograms['llt']['legend'] = make_legend()
    histograms['llt']['legend'].AddEntry(histograms['llt']['signal'],
                                         "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
    histograms['llt']['legend'].AddEntry(histograms['llt']['data'],
                                         "#bf{observed}", "lp")
    histograms['llt']['legend'].AddEntry(histograms['llt']['hww'], "#bf{VH(125 GeV)#rightarrow VWW}", "f")
    histograms['llt']['legend'].AddEntry(histograms['llt']['wz'], "#bf{WZ}", "f")
    histograms['llt']['legend'].AddEntry(histograms['llt']['zz'], "#bf{ZZ}", "f")
    histograms['llt']['legend'].AddEntry(histograms['llt']['fakes'],
                                         "#bf{reducible bkg.}", "f")
    if args.prefit==False:
       histograms['llt']['legend'].AddEntry(errorLLT, "#bf{bkg. uncertainty}", "f")

    # ZH
    histograms['zh'] = {}
    zh_channels = [
        'eeem_zh', 'eeet_zh', 'eemt_zh', 'eett_zh',
        'mmme_zh', 'mmet_zh', 'mmmt_zh', 'mmtt_zh',
    ]

    histograms['zh']['zz'] = get_combined_histogram(
        ['ZZ', 'GGToZZ2L2L', 'TTZ'], zh_channels, files_to_use_zh, title='ZZ',
        style='zz'
    )

    histograms['zh']['fakes'] = get_combined_histogram(
        'Zjets', zh_channels, files_to_use_zh, title='Reducible bkg.',
        style='fakes'
    )

    histograms['zh']['hww'] = get_combined_histogram(
        'ZH_hww125', zh_channels, files_to_use_zh,
        title='m_{H}=125 GeV', style='hww',
    )

    histograms['zh']['signal'] = get_combined_histogram(
        'ZH_htt125', zh_channels, files_to_use_zh,
        title='m_{H}=125 GeV', style='signal',
    )

    histograms['zh']['data'] = get_combined_histogram(
        'data_obs', zh_channels, files_to_use_zh,
        title='data', style='data',
    )

    histograms['zh']['stack'] = ROOT.THStack("zh_stack", "zh_stack")
    histograms['zh']['stack'].Add(histograms['zh']['fakes'], 'hist')
    histograms['zh']['stack'].Add(histograms['zh']['zz'], 'hist')
    histograms['zh']['stack'].Add(histograms['zh']['hww'], 'hist')
    histograms['zh']['stack'].Add(histograms['zh']['signal'], 'hist')
    
    errorZH=histograms['zh']['zz'].Clone()
    errorZH.SetFillStyle(3013)
    errorZH.Add(histograms['zh']['fakes'])
    errorZH.Add(histograms['zh']['hww'])
    errorZH.SetMarkerSize(0) 
    errorZH.SetFillColor(1)
    errorZH.SetLineWidth(1)
    
    histograms['zh']['legend'] = make_legend()
    histograms['zh']['legend'].AddEntry(histograms['zh']['signal'],
                                        "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
    histograms['zh']['legend'].AddEntry(histograms['llt']['data'],
                                        "#bf{observed}", "lp")
    histograms['zh']['legend'].AddEntry(histograms['zh']['hww'],
                                        "#bf{VH(125 GeV)#rightarrow VWW}", "f")
    histograms['zh']['legend'].AddEntry(histograms['zh']['zz'], "#bf{ZZ}", "f")
    histograms['zh']['legend'].AddEntry(histograms['zh']['fakes'],
                                        "#bf{reducible bkg.}", "f")
    if args.prefit==False:
       histograms['zh']['legend'].AddEntry(errorZH, "#bf{bkg. uncertainty}", "F")

    # LTT
    histograms['ltt'] = {}
    ltt_channels = ['ett', 'mtt']

    histograms['ltt']['wz'] = get_combined_histogram(
        'wz', ltt_channels, files_to_use_wh_had, title='WZ',
        style='wz',
    )

    histograms['ltt']['zz'] = get_combined_histogram(
        'zz', ltt_channels, files_to_use_wh_had, title='ZZ',
        style='zz',)

    histograms['ltt']['fakes'] = get_combined_histogram(
        'fakes', ltt_channels, files_to_use_wh_had, title='Reducible bkg.',
        style='fakes',
    )

    histograms['ltt']['signal'] = get_combined_histogram(
        ['WH_htt125'], ltt_channels, files_to_use_wh_had,
        title='m_{H}=125 GeV', style='signal')

    histograms['ltt']['data'] = get_combined_histogram(
        'data_obs', ltt_channels, files_to_use_wh_had,
        title='data', style='data')

    histograms['ltt']['stack'] = ROOT.THStack("ltt_stack", "ltt_stack")
    histograms['ltt']['stack'].Add(histograms['ltt']['fakes'], "hist")
    histograms['ltt']['stack'].Add(histograms['ltt']['zz'], "hist")
    histograms['ltt']['stack'].Add(histograms['ltt']['wz'], "hist")
    histograms['ltt']['stack'].Add(histograms['ltt']['signal'], "hist")


    errorLTT=histograms['ltt']['zz'].Clone()
    errorLTT.SetFillStyle(3013)
    errorLTT.Add(histograms['ltt']['fakes'])
    errorLTT.Add(histograms['ltt']['wz'])
    errorLTT.SetMarkerSize(0) 
    errorLTT.SetFillColor(1)
    errorLTT.SetLineWidth(1)

    histograms['ltt']['legend'] = make_legend()
    histograms['ltt']['legend'].AddEntry(histograms['ltt']['signal'],
                                         "#bf{VH(125 GeV)#rightarrow V#tau#tau}", "l")
    histograms['ltt']['legend'].AddEntry(histograms['ltt']['data'],
                                         "#bf{observed}", "lp")
    histograms['ltt']['legend'].AddEntry(histograms['ltt']['wz'], "#bf{WZ}", "f")
    histograms['ltt']['legend'].AddEntry(histograms['ltt']['zz'], "#bf{ZZ}", "f")
    histograms['ltt']['legend'].AddEntry(histograms['ltt']['fakes'],
                                         "#bf{reducible bkg.}", "f")
    if args.prefit==False:
       histograms['ltt']['legend'].AddEntry(errorLTT,"#bf{bkg. uncertainty}","F")

    # Apply some styles to all the histograms
    for channel in ['llt', 'zh', 'ltt']:
    #for channel in ['zh']:
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
	if channel=='zh':
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

    # Figure out what goes in the CMS preliminary line
    blurb_map = {
        '7TeV': ('5.0', '7'),
        '8TeV': ('19.7', '8'),
        'all': ('24.7', '7+8'),
    }
    int_lumi, sqrts = blurb_map[args.period]

    canvas=MakeCanvas("asdf","asdf",800,800)

    histograms['llt']['stack'].Draw()
    if args.prefit==False:
       errorLLT.Draw("e2same");
    #histograms['llt']['poisson'].Draw('pe same')
    catllt.Draw("same")
    histograms['llt']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    canvas.SaveAs('plots/llt' + plot_suffix)

    histograms['zh']['stack'].Draw()
    if args.prefit==False:
       errorZH.Draw("e2same")
    histograms['zh']['poisson'].SetMarkerStyle(20)
    histograms['zh']['poisson'].SetMarkerColor(ROOT.EColor.kBlack)
    histograms['zh']['poisson'].SetLineColor(ROOT.EColor.kBlack)
    histograms['zh']['poisson'].SetLineWidth(2)
    histograms['zh']['poisson'].SetMarkerSize(2)
    histograms['zh']['poisson'].Draw('pe same')
    catZH.Draw("same")
    histograms['zh']['legend'].Draw()
    lumiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    canvas.SaveAs('plots/zh' + plot_suffix)

    histograms['ltt']['stack'].Draw()
    if args.prefit==False:
       errorLTT.Draw("e2same")
    histograms['ltt']['poisson'].Draw('pe same')
    catltt.Draw("same")
    histograms['ltt']['legend'].Draw()
    limiBlurb=add_cms_blurb(sqrts, int_lumi)
    lumiBlurb.Draw("same")
    canvas.SaveAs('plots/ltt' + plot_suffix)
