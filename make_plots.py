'''

Build plots for HIG-12-032 results.

'''

from rootpy.plotting import views, Legend
import math
import rootpy.io as io
import ROOT
ROOT.gROOT.SetBatch(True)
from poisson import convert

def get_real_maximum(histo):
    max = 0
    for bin in range(histo.GetNbinsX()):
        content = histo.GetBinContent(bin) 
        upper = content + math.sqrt(content)
        #print bin, upper, max
        if upper > max:
            max = upper
    return max

def add_cms_blurb(sqrts, intlumi, preliminary=True, blurb=''):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(31)
    latex.SetTextAlign(11)
    label_text = "CMS"
    if preliminary:
        label_text += " Preliminary"
    label_text += " %s TeV" % sqrts
    label_text += " L=%sfb^{-1}" % (intlumi)
    label_text += " " + blurb
    return latex.DrawLatex(0.18, 0.97, label_text)

vh_7TeV = io.open('VHTT/cmb/common/vhtt.input_7TeV.root')
vh_8TeV = io.open('VHTT/cmb/common/vhtt.input_8TeV.root')

vh_7TeV_pf = io.open('../HiggsAnalysis/HiggsToTauTau/test/root_postfit/vhtt.input_7TeV.root')
vh_8TeV_pf = io.open('../HiggsAnalysis/HiggsToTauTau/test/root_postfit/vhtt.input_8TeV.root')

# We only care about 7 + 8 TeV
for pf_suffix, (vh7file, vh8file) in [('', (vh_7TeV, vh_8TeV)), ('_postfit', (vh_7TeV_pf, vh_8TeV_pf))]:
    vh_7and8 = views.SumView(vh7file, vh8file)
    for period, vh_combined in [('7+8', vh_7and8), ('7', vh7file), ('8', vh8file)]:

        # Now combine sub-channels
        llt_combined = views.SumView(*[
            views.SubdirectoryView(vh_combined, x) for x in ['emt', 'mmt', ]])

        zh_combined = views.SumView(*[
            views.SubdirectoryView(vh_combined, x) for x in [
                'eeem_zh', 'eeet_zh', 'eemt_zh', 'eett_zh',
                'mmme_zh', 'mmet_zh', 'mmmt_zh', 'mmtt_zh',
            ]])


        # Make views of individual backgrounds
        channels = {
            'llt' : {},
            'ltt' : {},
            'zh' : {},
            # tau_h tau_h
            'boost' : {},
            'vbf' : {},
        }

        # Define styles.  Normally this is done in FSA, but lets keep it static here.
        main_irreducible = {
            'legendstyle' : 'f',
            'format' : 'hist',
            # Same as Z+jets
            'fillstyle' : 1001,
            'fillcolor' : '#FFCC66',
            'linecolor' : '#000000',
            'linewidth' : 3,
        }
        next_irreducible = {
            'legendstyle' : 'f',
            'format' : 'hist',
            # Same as W+jets
            'fillstyle' : 1001,
            'fillcolor' : '#990000',
            'linecolor' : '#000000',
            'linewidth' : 3,
        }
        third_irreducible = {
            'legendstyle' : 'f',
            'format' : 'hist',
            # Same as ttbar
            'fillstyle' : 1001,
            'fillcolor' : '#9999CC',
            'linecolor' : '#000000',
            'linewidth' : 3,
        }
        fakes = {
            'legendstyle' : 'f',
            'format' : 'hist',
            # Same as QCD
            'fillcolor' : '#FFCCFF',
            'linecolor' : '#000000',
            'fillstyle' : 1001,
            'linewidth' : 3,
        }
        signal = {
            'legendstyle' : 'f',
            'format' : 'hist',
            'fillcolor' : 0,
            'fillstyle' : 0,
            'linestyle' : 2,
            'linewidth' : 5,
            'linecolor' : '#1C1C76',
            'name' : "VH",
        }
        data =  {
            'markerstyle' : 20,
            'markersize' : 2,
            'linewidth' : 2,
            'markercolor' : '#000000',
            'legendstyle' : 'pe',
            'format' : 'pe',
            'name' : "Observed",
        }


        Style = views.StyleView
        Subdir = views.SubdirectoryView
        Sum = views.SumView
        Title = views.TitleView
        ScaleView = views.ScaleView
        sigscale = 1

        def set_line_width(x):
            x.SetLineWidth(3)
            #print "Setting line width"
            return x

        # stupid hack to get always get a given histogram no matter what the Get(x) is
        def Getter(view, histoname, title=None):
            def doot(x):
                #print "doot", histoname
                return histoname

            if title is not None:
                return views.FunctorView(views.TitleView(views.PathModifierView(view, doot), title), set_line_width)
            else:
                return views.FunctorView(views.PathModifierView(view, doot), set_line_width)

        signal_label = 'm_{H}=125 GeV'

        channels['llt']['wz'] = Style(Getter(llt_combined, 'wz', 'WZ'), **main_irreducible)
        channels['llt']['zz'] = Style(Getter(llt_combined, 'zz', 'ZZ'), **next_irreducible)
        channels['llt']['fakes'] = Style(Getter(llt_combined, 'fakes', 'Non-prompt'), **fakes)
        channels['llt']['signal'] = Title(ScaleView(Style(
            Sum(
                Getter(llt_combined, 'WH125'),
                Getter(llt_combined, 'WH_hww125'),
            ), **signal), sigscale),
            signal_label)
        channels['llt']['obs'] = Style(Getter(llt_combined, 'data_obs', "Observed"), **data)

        #channels['ltt']['wz'] = Style(Getter(ltt_combined, 'WZ', 'WZ'), **main_irreducible)
        #channels['ltt']['zz'] = Style(Getter(ltt_combined, 'ZZ', 'ZZ'), **next_irreducible)
        #channels['ltt']['fakes'] = Style(Getter(ltt_combined, 'FakeRate', 'Non-prompt'), **fakes)
        #channels['ltt']['signal'] = Title(ScaleView(
            #Style(Sum(Getter(ltt_combined, 'WH125')), **signal), sigscale),
            #signal_label)

        channels['zh']['zz'] = Style(Getter(zh_combined, 'ZZ', 'ZZ'), **next_irreducible)
        channels['zh']['fakes'] = Style(Getter(zh_combined, 'Zjets', 'Non-prompt'), **fakes)
        channels['zh']['signal'] = Title(ScaleView(Style(
            Sum(
                Getter(zh_combined, 'ZH_htt125'),
                Getter(zh_combined, 'ZH_hww125'),
            ), **signal), sigscale),
            signal_label)
        channels['zh']['obs'] = Style(Getter(zh_combined, 'data_obs', "Observed"), **data)

        #print "ZH overflow check"
        zh_fakes = channels['zh']['fakes'].Get(None)
        #print zh_fakes.GetBinContent(zh_fakes.GetNbinsX())
        #print zh_fakes.GetBinContent(0)
        #print zh_fakes.Integral()

        llt_stack = views.StackView(
            *[channels['llt'][x] for x in ['zz', 'wz', 'fakes', 'signal']])

        #ltt_stack = views.StackView(
            #*[channels['ltt'][x] for x in ['zz', 'wz', 'fakes', 'signal']])

        zh_stack = views.StackView(
            *[channels['zh'][x] for x in ['zz', 'fakes', 'signal']])

        canvas = ROOT.TCanvas("asdf", "asdf", 800, 800)


        def make_a_legend(entries=5):
            vh_legend = Legend(
                entries, rightmargin=0.26, topmargin=0.05, leftmargin=0.375)
            vh_legend.SetEntrySeparation(0.0)
            vh_legend.SetMargin(0.35)
            vh_legend.SetBorderSize(0)
            return vh_legend

        lumi_maps = {
            '7+8' : '17',
            '8' : '12',
            '7' : '5',
        }

        # Draw LLT
        vh_legend = make_a_legend()
        llt = llt_stack.Get(None)
        llt.Draw()
        llt.GetHistogram().GetXaxis().SetRangeUser(0, 200)
        llt.GetHistogram().GetXaxis().SetTitle("m_{vis} [GeV]")
        llt.GetHistogram().GetXaxis().SetLabelSize(0.037)
        llt.GetHistogram().GetYaxis().SetTitle("Events")
        llt_data = channels['llt']['obs'].Get(None)
        llt.GetHistogram().GetYaxis().SetTitle("Events/%i GeV" % llt_data.GetBinWidth(1))
        #llt_data.Draw('same, pe')
        llt_data_pois = convert(llt_data, set_zero_bins=-10)
        llt_data_pois.Draw('pe')
        llt.SetMaximum(1.5*get_real_maximum(llt_data))
        blurb = add_cms_blurb(period, lumi_maps[period], blurb=' ll#tau_{h}')
        vh_legend.AddEntry(llt_data)
        vh_legend.AddEntry(llt)
        vh_legend.Draw()
        canvas.Update()
        canvas.SaveAs('llt' + period + pf_suffix + '.pdf')
        canvas.SaveAs('llt' + period + pf_suffix + '.png')

        ## Draw LTT
        #vh_legend = make_a_legend()
        #ltt = ltt_stack.Get(None)
        #ltt.Draw()
        #ltt.Draw()
        #ltt.GetHistogram().GetXaxis().SetRangeUser(0, 200)
        #ltt.GetHistogram().GetXaxis().SetTitle("m_{vis} [GeV]")
        #ltt.GetHistogram().GetYaxis().SetTitle("Events")
        #blurb = add_cms_blurb('7+8', '10.0')
        #vh_legend.AddEntry(ltt)
        #vh_legend.Draw()
        #canvas.Update()
        #canvas.SaveAs('ltt.pdf')

        vh_legend = make_a_legend(4)
        zh = zh_stack.Get(None)
        zh.Draw()
        zh.GetHistogram().GetXaxis().SetRangeUser(0, 200)
        zh.GetHistogram().GetXaxis().SetTitle("m_{vis} [GeV]")
        zh.GetHistogram().GetXaxis().SetLabelSize(0.037)
        zh.GetHistogram().GetYaxis().SetTitle("Events")
        blurb = add_cms_blurb(period, lumi_maps[period], blurb='llLL')
        zh_data = channels['zh']['obs'].Get(None)
        #zh_data.Draw('same, pe')
        zh_data_pois = convert(zh_data, set_zero_bins=-10)
        zh_data_pois.Draw('pe')
        zh.SetMaximum(1.5*get_real_maximum(zh_data))
        zh.GetHistogram().GetYaxis().SetTitle("Events/%i GeV" % zh_data.GetBinWidth(1))
        vh_legend.AddEntry(zh_data)
        vh_legend.AddEntry(zh)
        vh_legend.Draw()
        canvas.Update()
        canvas.SaveAs('zh' + period + pf_suffix + '.pdf')
        canvas.SaveAs('zh' + period + pf_suffix + '.png')

        print period, pf_suffix
        zh_fakes = channels['zh']['fakes'].Get(None)
        print "fakes", zh_fakes.Integral()
        zh_zz = channels['zh']['zz'].Get(None)
        print "zz", zh_zz.Integral()
        zh_obs = channels['zh']['obs'].Get(None)
        print "bkg", zh_zz.Integral() + zh_fakes.Integral()
        print "obs", zh_obs.Integral()

