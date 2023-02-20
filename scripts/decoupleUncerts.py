import ROOT
import math
from array import array
from argparse import ArgumentParser
from CombineHarvester.TauSF.fit_tools import DecomposeUncerts, FitSF, PlotSF
ROOT.gROOT.SetBatch(1)

# HI
description = '''This script makes the graphs containing the split uncertainties.'''
parser = ArgumentParser(prog="decoupleUncerts",description=description,epilog="Success!")
parser.add_argument('--dm-bins', dest='dm_bins', default=False, action='store_true', help="if specified then the mu+tauh channel fits are also split by tau decay-mode")
parser.add_argument('--file_total', '-f1', help= 'File containing the output of MultiDimFit with all uncertainties floating')
parser.add_argument('--file_comb1', '-f2', help= 'File containing the output of MultiDimFit with by eras uncertainties fixed')
parser.add_argument('--file_comb2', '-f3', help= 'File containing the output of MultiDimFit with by eras and by pT-bins uncertainties fixed')
parser.add_argument('--file_comb3', '-f4', help= 'File containing the output of MultiDimFit with by eras, by pT-bins, and by DM-bins uncertainties fixed')
parser.add_argument('-e', '--eras', dest='eras', type=str, default='all', help="Eras to make plots of pT dependent SFs for")
parser.add_argument('-o', '--output_folder', dest='output_folder', type=str, default='./', help="Name of the output folder to save the root files and plots")
args = parser.parse_args()

if args.eras == 'all': eras = ['2016_preVFP', '2016_postVFP', '2017', '2018']
else: eras=args.eras.split(',')

output_folder=args.output_folder

def SplitUncerts(g1,g2,g3,era,dm=None,g4=None):

  gout1=g1.Clone()
  gout2=g1.Clone()
  gout3=g1.Clone()
  name = g1.GetName()
  gout1.SetName(name+'_stat') 
  gout2.SetName(name+'_syst_alleras') 
  gout3.SetName(name+'_syst_%(era)s' % vars()) 
  if dm is not None: 
    gout4=g1.Clone()
    gout4.SetName(name+'_syst_dm%(dm)i_%(era)s' % vars())  

  for i in range(0,g1.GetN()):
    up_total=g1.GetErrorYhigh(i)
    down_total=g1.GetErrorYlow(i)
  
    up_no_era=g2.GetErrorYhigh(i)
    down_no_era=g2.GetErrorYlow(i)
  
    up_no_era_ptbins=g3.GetErrorYhigh(i)
    down_no_era_ptbins=g3.GetErrorYlow(i)

    up_no_era_ptbins_dmbins=0.
    down_no_era_ptbins_dmbins=0.


    if dm is not None:

      up_no_era_ptbins_dmbins=g4.GetErrorYhigh(i)
      down_no_era_ptbins_dmbins=g4.GetErrorYlow(i)

      up_stat = up_no_era_ptbins_dmbins
      down_stat = down_no_era_ptbins_dmbins

      up_dmbins = max(up_no_era_ptbins**2-up_stat**2,0.)**.5
      down_dmbins = max(down_no_era_ptbins**2-down_stat**2,0.)**.5

      up_era = max(up_total**2-up_no_era**2,0.)**.5
      down_era= max(down_total**2-down_no_era**2,0.)**.5

      up_ptbins = max(up_no_era**2-up_no_era_ptbins**2,0.)**.5
      down_ptbins = max(down_no_era**2-down_no_era_ptbins**2,0.)**.5

    else: 

      up_stat = up_no_era_ptbins
      down_stat = down_no_era_ptbins

      up_ptbins = max(up_no_era**2-up_stat**2,0.)**.5
      down_ptbins = max(down_no_era**2-down_stat**2,0.)**.5

      up_era = max(up_total**2-up_no_era**2,0.)**.5
      down_era = max(down_total**2-down_no_era**2,0.)**.5

    gout1.SetPointEYhigh(i,up_stat)
    gout1.SetPointEYlow(i,down_stat)
    gout2.SetPointEYhigh(i,up_era) 
    gout2.SetPointEYlow(i,down_era)
    gout3.SetPointEYhigh(i,up_ptbins)  
    gout3.SetPointEYlow(i,down_ptbins)   

    #for uncertainty variations we just store the errors and set the nominal values to 0 
    x=ROOT.Double()
    y=ROOT.Double()

    g1.GetPoint(i,x,y)
 
    gout1.SetPoint(i,x,0.)
    gout2.SetPoint(i,x,0.)
    gout3.SetPoint(i,x,0.)
    if dm is not None:
      gout4.SetPointEYhigh(i,up_dmbins)
      gout4.SetPointEYlow(i,down_dmbins) 
      gout4.SetPoint(i,x,0.)
 
  if dm is not None:
    return(gout1,gout2,gout3,gout4)
  else:
    return(gout1,gout2,gout3)


f1 = ROOT.TFile(args.file_total)
f2 = ROOT.TFile(args.file_comb1)
f3 = ROOT.TFile(args.file_comb2)

if args.dm_bins:
  f4 = ROOT.TFile(args.file_comb3)

if args.dm_bins: out_file='split_uncertainties_dmbins.root'
else: out_file='split_uncertainties.root'

fout = ROOT.TFile(output_folder+'/'+out_file,'RECREATE')

for era in eras:
  dms = ['inclusive']
  if args.dm_bins: 
    dms = [0,1,10,11]

  for dm in dms:
 
    graph_name = 'DM%(dm)s_%(era)s' % vars()
    
    h1 = f1.Get(graph_name+'_hist') 
    g1 = f1.Get(graph_name)
    g2 = f2.Get(graph_name)
    g3 = f3.Get(graph_name)
    g4=None
    
    if args.dm_bins:
      g4 = f4.Get(graph_name)
      gout1,gout2,gout3,gout4 = SplitUncerts(g1,g2,g3,era,dm,g4)
      fout.cd()
      gout4.Write() 
    else:
      gout1,gout2,gout3 = SplitUncerts(g1,g2,g3,era)
  
    fout.cd()
    g1.Write() 
    h1.Write() 
    gout1.Write() 
    gout2.Write() 
    gout3.Write()

# for dm-binned SF we now want to construct up and down shifted templates for the systematic variations
# then we fit these with the same functions we use for the nominal SFs
# the fitted distributions then correspond to our uncertainty variations


def MakeUpAndDownVariations(g,guncert):

  x = ROOT.Double()
  y = ROOT.Double()

  x_uncert = ROOT.Double()
  y_uncert = ROOT.Double()

  gout_up = g.Clone()
  gout_down = g.Clone()

  for i in range(0,g.GetN()):
    g.GetPoint(i,x,y) 
    guncert.GetPoint(i,x_uncert,y_uncert)
  
    if x_uncert != x: 
      print 'ERRRO: x bins values don\'t match!'
      exit() 

    up=y+guncert.GetErrorYhigh(i)
    down=y-guncert.GetErrorYlow(i)
   
    gout_up.SetPoint(i,x,up) 
    gout_down.SetPoint(i,x,down) 

    gout_up.SetName(guncert.GetName()+'_up')
    gout_down.SetName(guncert.GetName()+'_down')

  return (gout_up,gout_down)

def PlotpTBinned(nom, systs,output_name):

  colors = [2,3]

  c1=ROOT.TCanvas()

  nom.GetXaxis().SetTitle('p_{T} (GeV)')
  nom.GetYaxis().SetTitle('correction')
  nom.SetTitle('')
  nom.SetMarkerStyle(20)
  nom.Draw('ape')
  leg = ROOT.TLegend(0.15,0.92,0.9,0.96)
  leg.SetNColumns(4)
  leg.SetBorderSize(0)
  leg.AddEntry(nom,'total uncert.' ,'ep')
  for i, syst in enumerate(systs):
    syst.SetLineColor(colors[i]) 
    leg.AddEntry(syst,'_'.join(str(syst.GetName()).split('_')[2:]),'e')
    for j in range(0,nom.GetN()):
      x=ROOT.Double()
      y=ROOT.Double()
      nom.GetPoint(j,x,y)
      syst.SetPoint(j,x,y)
    syst.Draw('pep') 
  leg.Draw() 
 
  c1.Print(output_name+'.pdf')


def CompareSystsPlot(nom, systs,output_name):

  colors = [1,2,4,6,3,7,9,8]

  c1=ROOT.TCanvas()

  to_draw = []
 
  for i, syst in enumerate(systs):
    up=syst[0]
    down=syst[1]
    up_r=ROOT.TF1('%s_ratio' % up.GetName(),'(%s)/(%s)' % (up.GetExpFormula('p'), nom.GetExpFormula('p')),20,140)
    down_r=ROOT.TF1('%s_ratio' % down.GetName(),'(%s)/(%s)' % (down.GetExpFormula('p'), nom.GetExpFormula('p')),20,140)

    up_r.SetLineColor(colors[i]) 
    down_r.SetLineColor(colors[i]) 
    down_r.SetLineStyle(2)

    to_draw.append(up_r)
    to_draw.append(down_r)
 
    up_r.Draw('same')
    down_r.Draw('same')

  nom_r=ROOT.TF1('nom_ratio','0',20,140)
  nom_r.GetXaxis().SetTitle('p_{T} (GeV)')
  nom_r.GetYaxis().SetTitle('relative uncertainty')
  nom_r.SetTitle('')
  nom_r.SetMaximum(1.1)
  nom_r.SetMinimum(0.9)
  nom_r.Draw() 
  leg = ROOT.TLegend(0.15,0.92,0.9,0.96)
  leg.SetNColumns(4)
  leg.SetBorderSize(0)
  for p in to_draw: 
    p.Draw('same')
    leg.AddEntry(p,'_'.join(str(p.GetName()).split('_')[2:-1]),'l')
  leg.Draw()
  c1.Print(output_name+'.pdf')

if args.dm_bins:

  for era in eras:
    for dm in [0,1,10,11]:

      fit_func='pol1'
      if dm==1 and era != '2016_preVFP': fit_func='erf'
      graph_name = 'DM%(dm)s_%(era)s' % vars()

      g=fout.Get(graph_name)
      systs = ['_syst_alleras', '_syst_%(era)s' % vars(),  '_syst_dm%(dm)s_%(era)s' % vars()]
      systs_to_plot = []

      for syst in systs:
        guncert=fout.Get(graph_name+syst)

        gr_up,gr_down=MakeUpAndDownVariations(g,guncert)

        fout.cd()
        gr_up.Write() 
        gr_down.Write() 
  
        fit_up, h_uncert_up, h_up, uncerts_up = FitSF(gr_up,func=fit_func) 
        fit_down, h_uncert_down, h_down, uncerts_down = FitSF(gr_down,func=fit_func)

        fit_up.Write()
        fit_down.Write()
        systs_to_plot.append((fit_up.Clone(), fit_down.Clone()))

      # we also fit the nominal SFs again, just to make sure everything is consistent with the uncertainties
      fit_nom, h_uncert_nom, h_nom, uncerts_nom = FitSF(g,func=fit_func)

      g.Write(g.GetName()+'_fitted')
      fit_nom.Write()
      h_uncert_nom.Write()

      # we also fit the nominal SFs with a pol0 function for pT>40 to match the old prescription
      g_pol0 = g.Clone()
      g_pol0.SetName(g.GetName()+'_pol0_gt40')
      fit_pol0, h_uncert_pol0, h_pol0, uncerts_pol0 = FitSF(g_pol0,func='pol0_gt40')
      fit_pol0.Write()
      h_uncert_pol0.Write()

      name = fit_nom.GetName()
 

      stats_to_plot = []
      for x in uncerts_nom:
        x[1].SetName(name+'_%s_up' %x[0])
        x[2].SetName(name+'_%s_down' %x[0])
        stats_to_plot.append((x[1].Clone(), x[2].Clone()))
        x[1].Write()
        x[2].Write()

      # make some plots of SFs and uncertainties
      PlotSF(g, h_uncert_nom, 'tau_sf_DM%(dm)s_%(era)s' % vars(), title='DM%(dm)s, %(era)s' % vars(), output_folder=output_folder)
      CompareSystsPlot(fit_nom,systs_to_plot,output_folder+'/'+'uncerts_systs_tau_sf_DM%(dm)s_%(era)s' % vars())
      CompareSystsPlot(fit_nom,stats_to_plot,output_folder+'/'+'uncerts_stats_tau_sf_DM%(dm)s_%(era)s' % vars())

# make plots of pT-dependent SFs
if not args.dm_bins:
  for era in eras:
    systs=[fout.Get('DMinclusive_%(era)s_syst_alleras' % vars()).Clone(), fout.Get('DMinclusive_%(era)s_syst_%(era)s' % vars()).Clone()]
    PlotpTBinned(fout.Get('DMinclusive_%(era)s' % vars()),systs,output_folder+'/'+'tau_sf_DMinclusive_%(era)s' % vars())
