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

for chn in channels:
  for era in eras:
    # Adding Data,Signal Processes and Background processes to the harvester instance
    cb.AddObservations(['*'], ['ztt'], [era], [chn], cats[chn])
    cb.AddProcesses(['*'], ['ztt'], [era], [chn], bkg_procs[chn], cats[chn], False)
    if chn == 'mt': cb.AddProcesses(['*'], ['ztt'], [era], [chn], sig_procs, cats[chn], True)


# Add systematics
#...

# Populating Observation, Process and Systematic entries in the harvester instance
for chn in channels:
  for era in eras:
    if chn == 'zmm': filename = 'shapes/ztt.datacard.m_vis.zmm.%s.root' % era
    #else: filename = .... add mt ones later 
    print ">>>   file %s"%(filename)
    print(chn, era)
    cb.cp().channel([chn]).process(bkg_procs[chn]).era([era]).ExtractShapes(filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")
    if chn == 'mt': cb.cp().channel([chn]).process(sig_procs).era([era]).ExtractShapes(filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")




# Convert any shapes in Z->mumu CRs to lnN
cb.cp().channel(['zmm']).syst_type(["shape"]).ForEachSyst(lambda sys: sys.set_type('lnN')) 
 


## Merge to one bin for Z->mumu CRs
#cb.cp().channel(['zmm']).ForEachProc(To1Bin<ch::Process>);
#cb.cp().channel(['zmm']).ForEachObs(To1Bin<ch::Observation>);

# rebin histograms for mt channel
# ...
# zero any negative bins
# ...
# delete processes with 0 yield
# ...

# add bbb uncerts using autoMC stats

# Write datacards
SetStandardBinNames(cb)
print green(">>> writing datacards...")
datacardtxt  = "%s/cmb/$BIN.txt"%(output_folder)
datacardroot = "%s/cmb/common/$BIN_input.root"%(output_folder)
writer = CardWriter(datacardtxt,datacardroot)
writer.SetVerbosity(1)
writer.SetWildcardMasses([ ])
writer.WriteCards("cmb", cb)
