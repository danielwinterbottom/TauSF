import ROOT
ROOT.gROOT.SetBatch(1)

colourlist=[ROOT.kBlue,ROOT.kRed,ROOT.kGreen+3,ROOT.kBlack,ROOT.kYellow+2,ROOT.kOrange,ROOT.kCyan+3,ROOT.kMagenta+2,ROOT.kViolet-5,ROOT.kGray]

eras=['2016_preVFP','2016_postVFP','2017','2018']

wps=['loose','medium','tight','vtight']

def PlotGraphs(graphs, leg_titles, plot_name):

  mg = ROOT.TMultiGraph("mg","")
  graph_count=0
  legend_graphs=[]
  hs = ROOT.THStack("hs","")
  for graph_count, graph in enumerate(graphs):
      g = graph.Clone()
      g.SetFillColor(0)
      g.SetLineWidth(3)
      g.SetLineColor(colourlist[graph_count])
      g.SetMarkerSize(0)
      mg.Add(g)
      hs.Add(g.GetHistogram())
      legend_graphs.append(g.Clone())

  c1 = ROOT.TCanvas()
  c1.cd()

  mg.Draw('ape')
  mg.GetYaxis().SetTitle('SF')
  mg.GetXaxis().SetTitle('p_{T} (GeV)')

  leg = ROOT.TLegend(0.15,0.92,0.9,0.96)
  leg.SetNColumns(4)
  leg.SetBorderSize(0)
  for i in range(len(graphs)): leg.AddEntry(legend_graphs[i],leg_titles[i],'pe')
  leg.Draw()

  c1.Print(plot_name+'.pdf')



for era in eras:

  graph_name = 'DMinclusive_%(era)s' % vars()
  graphs = []
  leg_titles = []

  for wp in wps:

    f1 = ROOT.TFile('outputs/tauSF_Mar02_PFMet_DMinclusive_%(wp)s/split_uncertainties.root' % vars())
    graphs.append(f1.Get(graph_name).Clone())
    leg_titles.append(wp)

  PlotGraphs(graphs, leg_titles, 'compare_WPs_DMinclusive_%(era)s' % vars())


  # now make dm-binned version  
