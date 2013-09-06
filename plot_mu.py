import ROOT
import os
from HiggsAnalysis.HiggsToTauTau.scanMultiDimFit import extract_band

'''
************************************************
*    Row   * quantileE *     limit *  limitErr *
************************************************
*        0 *       0.5 * 0.1895817 *         0 *
*        1 * 0.1599999 * -1.005340 *         0 *
*        2 * 0.8399999 * 0.9528349 *         0 *
*        3 *        -1 * 0.1895817 * 1.2079619 *
************************************************
'''

def get_fit_results(filename):
    ''' Unpack the wacky format for MaxLikelihood results '''
    file = ROOT.TFile(filename)
    result_tree = file.Get("limit")
    value = None
    err_up = None
    err_down = None
    for row in result_tree:
        if abs(row.quantileExpected - 0.5) < 1e-4:
            value = row.limit
        elif abs(row.quantileExpected - 0.8399) < 1e-4:
            err_up = row.limit
        elif abs(row.quantileExpected - 0.1599) < 1e-4:
            err_down = row.limit

    return (value, err_up-value, value-err_down)

canvas = ROOT.TCanvas("adf", "asdf", 800, 600)
canvas.SetLeftMargin(0.26)
canvas.SetRightMargin(0.06)
canvas.SetTopMargin(0.06)
canvas.SetBottomMargin(0.15)
canvas.SetTickx(1)
canvas.SetTickx(0)
canvas.SetFrameBorderMode(0)
canvas.SetBorderMode(0)
canvas.SetBorderSize(2)

frame = ROOT.TH1F("frame", "frame", 6, -0.5, 5.5)
frame.Draw('hbar')
frame.SetMinimum(-6)
frame.SetMaximum(8)

frame.GetYaxis().SetTitle("Best fit of #sigma/#sigma_{SM}")

keep = []

labels = {
    'fermionic' : "H #rightarrow #tau#tau (0/1jet)",
    'boost' : "H #rightarrow #tau#tau (1jet)",
    'vbf' : "H #rightarrow #tau#tau (VBF)",
    'vhtt' : "H #rightarrow #tau#tau (VH)",
}

graphs = {}

for base_dir in ['NO_ET', 'STANDARD-LIMITS', 'ALL-LIMITS']:
    frame.Draw('hbar')

    unc_box = ROOT.TBox(0.85-0.23, -0.5, 0.85+.23, 5.5)
    unc_box.SetFillColor(ROOT.EColor.kGreen)
    unc_box.Draw()

    line = ROOT.TLine(0.85, -0.5, 0.85, 5.5)
    line.SetLineStyle(2)
    line.Draw()


    #for i, directory in enumerate(['fermionic', 'vbf', 'vhtt', 'boost']):
    for i, directory in enumerate(['vhtt', 'vbf', 'fermionic',]):
        #to_get = os.path.join(base_dir, directory, '125',
                              #'higgsCombineTest.MaxLikelihoodFit.mH125.root')
        to_get = os.path.join(base_dir, directory, '125',
                              'higgsCombineTest.MultiDimFit.mH125.root')
        if not os.path.exists(to_get):
            continue
        #result = get_fit_results(to_get)
        lower_bound, best_r, upper_bound, full_graph = extract_band(to_get)
        result = (best_r, upper_bound - best_r, best_r - lower_bound)

        graphs['_'.join([base_dir, directory]) + '.pdf'] = full_graph


        frame.GetXaxis().SetBinLabel(frame.GetXaxis().FindBin(i+1), labels[directory])
        print directory, result
        graph = ROOT.TGraphAsymmErrors(1)
        graph.SetPoint(0, result[0], i+1)
        graph.SetPointError(0, abs(result[2]), abs(result[1]), 0, 0 )
        graph.SetMarkerStyle(21)
        graph.SetMarkerSize(1.5)
        graph.SetLineWidth(2)
        graph.Draw('pe,same')
        keep.append(graph)


    box = ROOT.TBox(-6, -0.5, 8, 5.5)
    box.SetLineWidth(2)
    box.SetFillStyle(0)
    box.Draw()

    canvas.SaveAs("htt_mu_%s.pdf" % base_dir.lower().replace('-', '_'))
    canvas.SaveAs("htt_mu_%s.png" % base_dir.lower().replace('-', '_'))

frame = ROOT.TH1F("frame", "frame", 6, -4, 4)
frame.SetMinimum(0)
frame.SetMaximum(0.6)
frame.GetXaxis().SetTitle("#mu")
frame.GetYaxis().SetTitle("#Delta NLL")
for filename, graph in graphs.iteritems():
    frame.Draw()
    graph.Draw("l")
    frame.SetMaximum(0.6)
    canvas.SaveAs(filename)
    frame.SetMaximum(0.1)
    canvas.SaveAs(filename.replace('.pdf', '_zoom.pdf'))
