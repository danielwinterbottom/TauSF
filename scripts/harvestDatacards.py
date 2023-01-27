import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
import CombineHarvester.CombineTools.ch as ch
from CombineHarvester.CombineTools.ch import CombineHarvester, CardWriter, SetStandardBinNames
from argparse import ArgumentParser
import yaml
#import os

# specify with eras to fit or combine all eras together by specifying "all"
valid_eras = ['2016preVFP', '2016postVFP', '2017', '2018', 'all']

# HI
description = '''This script makes datacards with CombineHarvester for performing tau ID SF measurments.'''
parser = ArgumentParser(prog="harvesterDatacards",description=description,epilog="Success!")
parser.add_argument('-c', '--config', dest='config', type=str, default='config/harvestDatacards.yml', action='store', help="set config file")
args = parser.parse_args()

with open(args.config, 'r') as file:
   setup = yaml.safe_load(file)

output_folder = setup["output_folder"]
era_tag = setup["eras"]


if era_tag == 'all': eras = ['2017', '2018'] # add other eras later
else: eras = era_tag.split(',')

for e in eras: 
  if e not in valid_eras: raise Exception("ERROR: one or more of the eras you specified is not supported, available options are: %s" % ",".join(valid_eras)) 

def green(string,**kwargs):
    return kwargs.get('pre',"")+"\x1b[0;32;40m%s\033[0m"%string

def NegativeBins(p):
  '''Replaces negative bins in hists with 0'''
  hist = p.shape()
  has_negative = False
  for i in range(1,hist.GetNbinsX()+1):
    if hist.GetBinContent(i) < 0:
       has_negative = True
       print("Process: ",p.process()," has negative bins.")
  if (has_negative):
    for i in range(1,hist.GetNbinsX()+1):
       if hist.GetBinContent(i) < 0:
          hist.SetBinContent(i,0)
  p.set_shape(hist,False)

channels = ['zmm'] # add mt later!
bkg_procs = {}
# procs for the dimuon channel
bkg_procs['zmm'] = ['ZL', 'ZJ', 'ZTT', 'W', 'VVL', 'VVJ', 'TTL', 'TTJ']
# procs for the mu+tauh channel
bkg_procs['mt'] = ['ZL', 'ZJ', 'W', 'VVJ', 'TTJ', 'QCD']

# signal processes are defined as any with genuine hadronic taus in the mt channel
sig_procs = ['ZTT','VVL','TTL']

cats = {}
cats['zmm'] = [(1, 'zmm_inclusive')]

# Create an empty CombineHarvester instance
cb = CombineHarvester()

# Add processes and observations
for chn in channels:
  for era in eras:
    # Adding Data,Signal Processes and Background processes to the harvester instance
    cb.AddObservations(['*'], ['ztt'], [era], [chn], cats[chn])
    cb.AddProcesses(['*'], ['ztt'], [era], [chn], bkg_procs[chn], cats[chn], False)
    if chn == 'mt': cb.AddProcesses(['*'], ['ztt'], [era], [chn], sig_procs, cats[chn], True)


# Add systematics

# muon selection efficiency for second muon in di-muon dataset
cb.cp().channel(['zmm']).process(['W'],False).AddSyst(cb, "CMS_eff_m", "lnN", ch.SystMap()(1.02))

# for Wjets in dimuon data the second muon is a fake so add a seperate uncertainty for this - as this uncertainty is so large we don't need to add another uncertainty for the cross section
cb.cp().channel(['zmm']).process(['W']).AddSyst(cb, "CMS_j_fake_m", "lnN", ch.SystMap()(1.3))

# uncertainty on VV cross-section - set to 10% to cover missing higher order terms which are typically this large
cb.cp().process(['TTT','VVJ']).AddSyst(cb, "CMS_htt_vvXsec", "lnN", ch.SystMap()(1.1))

# uncertainty on ttbar cross-section - set to 10% to cover missing higher order terms which are typically this large
cb.cp().process(['TTL','TTJ']).AddSyst(cb, "CMS_htt_tjXsec", "lnN", ch.SystMap()(1.06))

# DY shape uncertainty from re-weighting pT-mass to data (100% variation taked as the uncertainty)
cb.cp().process(['ZTT','ZL','ZJ']).AddSyst(cb, "CMS_htt_dyShape", "shape", ch.SystMap()(1.0))
# ttbar shape uncertainty from re-weighting pT-mass to data (100% variation taked as the uncertainty)
cb.cp().process(['TTL','TTJ']).AddSyst(cb, "CMS_htt_ttbarShape", "shape", ch.SystMap()(1.0))

# TES uncertainties
cb.cp().channel(['mt']).process(['ZTT','TTL','VVL']).AddSyst(cb, "CMS_scale_t_1prong_$ERA","shape", ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(['ZTT','TTL','VVL']).AddSyst(cb, "CMS_scale_t_1prong1pizero_$ERA","shape", ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(['ZTT','TTL','VVL']).AddSyst(cb, "CMS_scale_t_3prong_$ERA", "shape", ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(['ZTT','TTL','VVL']).AddSyst(cb, "CMS_scale_t_3prong1pizero_$ERA", "shape", ch.SystMap()(1.0))

# mu->tauh energy scale split by decay mode (might want to eventually make sure these don't get added for dm 10 and 11)
cb.cp().channel(['mt']).process(['ZL']).AddSyst(cb, "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", ch.SystMap()(1.00))

cb.cp().channel(['mt']).process(['ZL']).AddSyst(cb, "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))

# now add unconstrained rate parameters

# a common rate parameter that scales all MC processes in the di-muon channel and the the ZTT, TTL, and VVL in the mu+tauh channel
# this doesn't need to scale ZL TTJ, VVJ, and W in the mu+tauh channel as there are seperate rate parameters for these processes 

cb.cp().channel(['zmm']).AddSyst(cb, "rate_DY_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTL", "VVL"]).AddSyst(cb, "rate_DY_$ERA","rateParam",ch.SystMap()(1.0))

# rate parameters to scale jet->tauh fake processes in the mu+tauh channel (W, TTJ, VVJ) - one per bin

# rate parameters to scale QCD in the mu+tauh channel  - one per bin

# rate parameters to scale ZL in the mu+tauh channel  - one per bin

# rate parameter to scale the ZTT, TTL, and VVL which in the mu+tauh categories - one per bin

# set sensible ranges for all rate params
for era in eras:
  cb.GetParameter("rate_DY_%s" % era).set_range(0.5,1.5)

# Populating Observation, Process and Systematic entries in the harvester instance
for chn in channels:
  for era in eras:
    if chn == 'zmm': filename = 'shapes/ztt.datacard.m_vis.zmm.%s.root' % era
    #else: filename = .... add mt ones later 
    print ">>>   file %s" % (filename)
    print('%s, %s' % (chn, era))
    cb.cp().channel([chn]).process(bkg_procs[chn]).era([era]).ExtractShapes(filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")
    if chn == 'mt': cb.cp().channel([chn]).process(sig_procs).era([era]).ExtractShapes(filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")

# Merge to one bin for Z->mumu CRs
for b in cb.cp().channel(['zmm']).bin_set():
  print("Rebinning Z->mumu CRs into 1-bin categories")
  cb.cp().bin([b]).VariableRebin([50.,150,]);

# Rebin histograms for mt channel using Auto Rebinning
# ...

# Convert any shapes in Z->mumu CRs to lnN
cb.cp().channel(['zmm']).syst_type(["shape"]).ForEachSyst(lambda sys: sys.set_type('lnN'))

# Zero negetive bins
print(green("Zeroing NegativeBins"))
cb.ForEachProc(NegativeBins)

SetStandardBinNames(cb)
# Add bbb uncerts using autoMC stats
cb.SetAutoMCStats(cb, 0., 1, 1)

# Write datacards
print green(">>> writing datacards...")
datacardtxt  = "%s/cmb/$BIN.txt"%(output_folder)
datacardroot = "%s/cmb/common/$BIN_input.root"%(output_folder)
writer = CardWriter(datacardtxt,datacardroot)
writer.SetVerbosity(1)
writer.SetWildcardMasses([ ])
writer.WriteCards("cmb", cb)
