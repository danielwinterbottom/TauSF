import ROOT
import math
from array import array
from argparse import ArgumentParser
ROOT.gROOT.SetBatch(1)

# HI
description = '''This script makes the graphs containing the split uncertainties.'''
parser = ArgumentParser(prog="makeSFGraphs",description=description,epilog="Success!")
parser.add_argument('--dm-bins', dest='dm_bins', default=False, action='store_true', help="if specified then the mu+tauh channel fits are also split by tau decay-mode")
parser.add_argument('--file_total', '-f1', help= 'File containing the output of MultiDimFit with all uncertainties floating')
parser.add_argument('--file_comb1', '-f2', help= 'File containing the output of MultiDimFit with by eras uncertainties fixed')
parser.add_argument('--file_comb2', '-f3', help= 'File containing the output of MultiDimFit with by eras and by pT-bins uncertainties fixed')
parser.add_argument('--file_comb3', '-f4', help= 'File containing the output of MultiDimFit with by eras, by pT-bins, and by DM-bins uncertainties fixed')
parser.add_argument('-e', '--eras', dest='eras', type=str, default='all', help="Eras to make plots of pT dependent SFs for")
args = parser.parse_args()

if args.eras == 'all': eras = ['2016_preVFP', '2016_postVFP', '2017', '2018']
else: eras=args.eras.split(',')

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

      # dm = stat+dmbins - stat
      up_dmbins = (up_no_era_ptbins**2 - up_stat**2)**.5
      down_dmbins = (down_no_era_ptbins**2 - down_stat**2)**.5

      up_era = (up_total**2-up_no_era**2)**.5
      down_era= (down_total**2-down_no_era**2)**.5


      # total                  = stat+dm+era+pt
      # no_era_ptbins_dmbins   = stat
      # no_era_ptbins          = stat+dm
      # no_era                 = stat+dm+pt


      print era, dm, i
      up_ptbins = max(up_no_era**2-up_no_era_ptbins**2,0.)**.5
      print 'sizes:', up_era, up_ptbins, up_dmbins, up_stat
      down_ptbins = max(down_no_era**2-down_no_era_ptbins**2,0.)**.5
      

      print up_total, (up_stat**2+up_dmbins**2+up_ptbins**2+up_era**2)**.5
      print down_total, (down_stat**2+down_dmbins**2+down_ptbins**2+down_era**2)**.5


    else: 

      up_stat = up_no_era_ptbins
      down_stat = down_no_era_ptbins

      up_ptbins = (up_no_era**2-up_stat**2)**.5
      down_ptbins = (down_no_era**2-down_stat**2)**.5

      up_era = (up_total**2-up_no_era**2)**.5
      down_era = (down_total**2-down_no_era**2)**.5

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

fout = ROOT.TFile(out_file,'RECREATE')

for era in eras:
  dms = ['inclusive']
  if args.dm_bins: 
    dms = [0,1,10,11]

  for dm in dms:
 
    graph_name = 'DM%(dm)s_%(era)s' % vars()
  
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
    gout1.Write() 
    gout2.Write() 
    gout3.Write() 
