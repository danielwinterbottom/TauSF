# this script takes the fit result and converts it into a set of TGraphAsymmErrors objects

import ROOT
from array import array
from argparse import ArgumentParser

# HI
description = '''This script makes TGraphAsymmErrors objects from tau ID SF measurments.'''
parser = ArgumentParser(prog="makeSFGraphs",description=description,epilog="Success!")
parser.add_argument('--dm-bins', dest='dm_bins', default=False, action='store_true', help="if specified then the mu+tauh channel fits are also split by tau decay-mode")
parser.add_argument('--file', '-f', help= 'File containing the output of MultiDimFit')
args = parser.parse_args()
dm_bins=args.dm_bins

f = ROOT.TFile(args.file)

fout_name = args.file.replace('.root','.TGraphAsymmErrors.root')

l = f.Get('limit')

vals = {}
if dm_bins:
  pois = ['rate_tauSF_DM0_pT20to25_2016_preVFP','rate_tauSF_DM0_pT25to30_2016_preVFP','rate_tauSF_DM0_pT30to35_2016_preVFP','rate_tauSF_DM0_pT35to40_2016_preVFP','rate_tauSF_DM0_pT40to50_2016_preVFP','rate_tauSF_DM0_pT50to60_2016_preVFP','rate_tauSF_DM0_pT60to80_2016_preVFP','rate_tauSF_DM0_pT80to100_2016_preVFP','rate_tauSF_DM0_pT100to200_2016_preVFP','rate_tauSF_DM1_pT20to25_2016_preVFP','rate_tauSF_DM1_pT25to30_2016_preVFP','rate_tauSF_DM1_pT30to35_2016_preVFP','rate_tauSF_DM1_pT35to40_2016_preVFP','rate_tauSF_DM1_pT40to50_2016_preVFP','rate_tauSF_DM1_pT50to60_2016_preVFP','rate_tauSF_DM1_pT60to80_2016_preVFP','rate_tauSF_DM1_pT80to100_2016_preVFP','rate_tauSF_DM1_pT100to200_2016_preVFP','rate_tauSF_DM10_pT20to25_2016_preVFP','rate_tauSF_DM10_pT25to30_2016_preVFP','rate_tauSF_DM10_pT30to35_2016_preVFP','rate_tauSF_DM10_pT35to40_2016_preVFP','rate_tauSF_DM10_pT40to50_2016_preVFP','rate_tauSF_DM10_pT50to60_2016_preVFP','rate_tauSF_DM10_pT60to80_2016_preVFP','rate_tauSF_DM10_pT80to100_2016_preVFP','rate_tauSF_DM10_pT100to200_2016_preVFP','rate_tauSF_DM11_pT20to25_2016_preVFP','rate_tauSF_DM11_pT25to30_2016_preVFP','rate_tauSF_DM11_pT30to35_2016_preVFP','rate_tauSF_DM11_pT35to40_2016_preVFP','rate_tauSF_DM11_pT40to50_2016_preVFP','rate_tauSF_DM11_pT50to60_2016_preVFP','rate_tauSF_DM11_pT60to80_2016_preVFP','rate_tauSF_DM11_pT80to100_2016_preVFP','rate_tauSF_DM11_pT100to200_2016_preVFP','rate_tauSF_DM0_pT20to25_2016_postVFP','rate_tauSF_DM0_pT25to30_2016_postVFP','rate_tauSF_DM0_pT30to35_2016_postVFP','rate_tauSF_DM0_pT35to40_2016_postVFP','rate_tauSF_DM0_pT40to50_2016_postVFP','rate_tauSF_DM0_pT50to60_2016_postVFP','rate_tauSF_DM0_pT60to80_2016_postVFP','rate_tauSF_DM0_pT80to100_2016_postVFP','rate_tauSF_DM0_pT100to200_2016_postVFP','rate_tauSF_DM1_pT20to25_2016_postVFP','rate_tauSF_DM1_pT25to30_2016_postVFP','rate_tauSF_DM1_pT30to35_2016_postVFP','rate_tauSF_DM1_pT35to40_2016_postVFP','rate_tauSF_DM1_pT40to50_2016_postVFP','rate_tauSF_DM1_pT50to60_2016_postVFP','rate_tauSF_DM1_pT60to80_2016_postVFP','rate_tauSF_DM1_pT80to100_2016_postVFP','rate_tauSF_DM1_pT100to200_2016_postVFP','rate_tauSF_DM10_pT20to25_2016_postVFP','rate_tauSF_DM10_pT25to30_2016_postVFP','rate_tauSF_DM10_pT30to35_2016_postVFP','rate_tauSF_DM10_pT35to40_2016_postVFP','rate_tauSF_DM10_pT40to50_2016_postVFP','rate_tauSF_DM10_pT50to60_2016_postVFP','rate_tauSF_DM10_pT60to80_2016_postVFP','rate_tauSF_DM10_pT80to100_2016_postVFP','rate_tauSF_DM10_pT100to200_2016_postVFP','rate_tauSF_DM11_pT20to25_2016_postVFP','rate_tauSF_DM11_pT25to30_2016_postVFP','rate_tauSF_DM11_pT30to35_2016_postVFP','rate_tauSF_DM11_pT35to40_2016_postVFP','rate_tauSF_DM11_pT40to50_2016_postVFP','rate_tauSF_DM11_pT50to60_2016_postVFP','rate_tauSF_DM11_pT60to80_2016_postVFP','rate_tauSF_DM11_pT80to100_2016_postVFP','rate_tauSF_DM11_pT100to200_2016_postVFP','rate_tauSF_DM0_pT20to25_2017','rate_tauSF_DM0_pT25to30_2017','rate_tauSF_DM0_pT30to35_2017','rate_tauSF_DM0_pT35to40_2017','rate_tauSF_DM0_pT40to50_2017',
  'rate_tauSF_DM0_pT50to60_2017','rate_tauSF_DM0_pT60to80_2017','rate_tauSF_DM0_pT80to100_2017','rate_tauSF_DM0_pT100to200_2017','rate_tauSF_DM1_pT20to25_2017','rate_tauSF_DM1_pT25to30_2017','rate_tauSF_DM1_pT30to35_2017','rate_tauSF_DM1_pT35to40_2017','rate_tauSF_DM1_pT40to50_2017','rate_tauSF_DM1_pT50to60_2017','rate_tauSF_DM1_pT60to80_2017','rate_tauSF_DM1_pT80to100_2017','rate_tauSF_DM1_pT100to200_2017','rate_tauSF_DM10_pT20to25_2017','rate_tauSF_DM10_pT25to30_2017','rate_tauSF_DM10_pT30to35_2017','rate_tauSF_DM10_pT35to40_2017','rate_tauSF_DM10_pT40to50_2017','rate_tauSF_DM10_pT50to60_2017','rate_tauSF_DM10_pT60to80_2017','rate_tauSF_DM10_pT80to100_2017','rate_tauSF_DM10_pT100to200_2017','rate_tauSF_DM11_pT20to25_2017','rate_tauSF_DM11_pT25to30_2017','rate_tauSF_DM11_pT30to35_2017','rate_tauSF_DM11_pT35to40_2017','rate_tauSF_DM11_pT40to50_2017','rate_tauSF_DM11_pT50to60_2017','rate_tauSF_DM11_pT60to80_2017','rate_tauSF_DM11_pT80to100_2017','rate_tauSF_DM11_pT100to200_2017','rate_tauSF_DM0_pT20to25_2018','rate_tauSF_DM0_pT25to30_2018','rate_tauSF_DM0_pT30to35_2018','rate_tauSF_DM0_pT35to40_2018','rate_tauSF_DM0_pT40to50_2018','rate_tauSF_DM0_pT50to60_2018','rate_tauSF_DM0_pT60to80_2018','rate_tauSF_DM0_pT80to100_2018','rate_tauSF_DM0_pT100to200_2018','rate_tauSF_DM1_pT20to25_2018','rate_tauSF_DM1_pT25to30_2018','rate_tauSF_DM1_pT30to35_2018','rate_tauSF_DM1_pT35to40_2018','rate_tauSF_DM1_pT40to50_2018','rate_tauSF_DM1_pT50to60_2018','rate_tauSF_DM1_pT60to80_2018','rate_tauSF_DM1_pT80to100_2018','rate_tauSF_DM1_pT100to200_2018','rate_tauSF_DM10_pT20to25_2018','rate_tauSF_DM10_pT25to30_2018','rate_tauSF_DM10_pT30to35_2018','rate_tauSF_DM10_pT35to40_2018','rate_tauSF_DM10_pT40to50_2018','rate_tauSF_DM10_pT50to60_2018','rate_tauSF_DM10_pT60to80_2018','rate_tauSF_DM10_pT80to100_2018','rate_tauSF_DM10_pT100to200_2018','rate_tauSF_DM11_pT20to25_2018','rate_tauSF_DM11_pT25to30_2018','rate_tauSF_DM11_pT30to35_2018','rate_tauSF_DM11_pT35to40_2018','rate_tauSF_DM11_pT40to50_2018','rate_tauSF_DM11_pT50to60_2018','rate_tauSF_DM11_pT60to80_2018','rate_tauSF_DM11_pT80to100_2018','rate_tauSF_DM11_pT100to200_2018']
else:
  pois = ['rate_tauSF_DMinclusive_pT20to25_2016_preVFP','rate_tauSF_DMinclusive_pT25to30_2016_preVFP','rate_tauSF_DMinclusive_pT30to35_2016_preVFP','rate_tauSF_DMinclusive_pT35to40_2016_preVFP','rate_tauSF_DMinclusive_pT40to50_2016_preVFP','rate_tauSF_DMinclusive_pT50to60_2016_preVFP','rate_tauSF_DMinclusive_pT60to80_2016_preVFP','rate_tauSF_DMinclusive_pT80to100_2016_preVFP','rate_tauSF_DMinclusive_pT100to200_2016_preVFP','rate_tauSF_DMinclusive_pT20to25_2016_postVFP','rate_tauSF_DMinclusive_pT25to30_2016_postVFP','rate_tauSF_DMinclusive_pT30to35_2016_postVFP','rate_tauSF_DMinclusive_pT35to40_2016_postVFP','rate_tauSF_DMinclusive_pT40to50_2016_postVFP','rate_tauSF_DMinclusive_pT50to60_2016_postVFP','rate_tauSF_DMinclusive_pT60to80_2016_postVFP','rate_tauSF_DMinclusive_pT80to100_2016_postVFP','rate_tauSF_DMinclusive_pT100to200_2016_postVFP','rate_tauSF_DMinclusive_pT20to25_2017','rate_tauSF_DMinclusive_pT25to30_2017','rate_tauSF_DMinclusive_pT30to35_2017','rate_tauSF_DMinclusive_pT35to40_2017','rate_tauSF_DMinclusive_pT40to50_2017','rate_tauSF_DMinclusive_pT50to60_2017','rate_tauSF_DMinclusive_pT60to80_2017','rate_tauSF_DMinclusive_pT80to100_2017','rate_tauSF_DMinclusive_pT100to200_2017','rate_tauSF_DMinclusive_pT20to25_2018','rate_tauSF_DMinclusive_pT25to30_2018','rate_tauSF_DMinclusive_pT30to35_2018','rate_tauSF_DMinclusive_pT35to40_2018','rate_tauSF_DMinclusive_pT40to50_2018','rate_tauSF_DMinclusive_pT50to60_2018','rate_tauSF_DMinclusive_pT60to80_2018','rate_tauSF_DMinclusive_pT80to100_2018','rate_tauSF_DMinclusive_pT100to200_2018']


# get values and +/- 1 sigma shifts from tree
for poi in pois:
#  if 'postVFP' in poi: continue
  vals[poi] = set()

  for i in range(0, l.GetEntries()):
    l.GetEntry(i)
    x=getattr(l, poi)
    vals[poi].add(x)

# group x, y values and errors by DM
graph_values = {}

eras = ['2016_preVFP', '2016_postVFP', '2017', '2018']

for e in eras:
  if dm_bins:
    for dm in [0,1,10,11]: graph_values['%i_%s' % (dm,e)] = []
  else: graph_values['inclusive_%s' % e] = []  

bin_boundaries = [20.,25.,30.,35.,40.,50.,60.,80.,100.,200.]

# taking pt bins from average values instead
pt_vals = [23., 28., 32., 37., 44., 54., 68., 89., 125.] 


for v in vals: 
  x = list(vals[v])
  # list contains nominal value and +/- 1 sigma shited value
  # sort list and subtract nominal value to obtain up and down errors
  x.sort()
  val = x[1]
  e_up = x[2]-val
  e_down = val-x[0]
  dm_bin = v.split('_')[2][2:]
  pt_bin = v.split('_')[3][2:]
  era='_'.join(v.split('_')[4:])
  pt_lo=float(pt_bin.split('to')[0])
  pt_hi=float(pt_bin.split('to')[1])
  ave_pt = (pt_lo+pt_hi)/2 # can use average pT to define bin centres 
  # but if option is specific then will take the average pT values within each bin instead
  x_val = ave_pt
  graph_values['%s_%s' % (dm_bin,era)].append((x_val, val, e_down, e_up))



for i, b in enumerate(bin_boundaries[:-1]]: 
  print '(pt_2>=%i&&pt_2<%i)*(%.2f)' %(b, bin_boundaries[i+1], graph_values[i]) 


print ('Writing to file: %s' % fout_name)
fout = ROOT.TFile(fout_name,'RECREATE')

for g_val in graph_values:

  gr = ROOT.TGraphAsymmErrors()
  gr.SetName('DM%s' % g_val)
  for x in graph_values[g_val]:
    n=gr.GetN()
    gr.SetPoint(n,x[0], x[1])
    gr.SetPointError (n, 0., 0., x[2], x[3])
  fout.cd()
  gr.Write()
