import ROOT; ROOT.PyConfig.IgnoreCommandLineOptions = True
import CombineHarvester.CombineTools.ch as ch
from CombineHarvester.CombineTools.ch import CombineHarvester, CardWriter, SetStandardBinNames, AutoRebin
from argparse import ArgumentParser
import yaml
#import os

# specify with eras to fit or combine all eras together by specifying "all"
valid_eras = ['2016_preVFP', '2016_postVFP', '2017', '2018', 'all']

# HI
description = '''This script makes datacards with CombineHarvester for performing tau ID SF measurments.'''
parser = ArgumentParser(prog="harvesterDatacards",description=description,epilog="Success!")
parser.add_argument('-c', '--config', dest='config', type=str, default='config/harvestDatacards.yml', action='store', help="set config file")
parser.add_argument('--dm-bins', dest='dm_bins', default=False, action='store_true', help="if specified then the mu+tauh channel fits are also split by tau decay-mode")
args = parser.parse_args()
dm_bins=args.dm_bins

with open(args.config, 'r') as file:
   setup = yaml.safe_load(file)

output_folder = setup["output_folder"]
era_tag = setup["eras"]


if era_tag == 'all': eras = ['2016_preVFP', '2016_postVFP', '2017', '2018'] # add other eras later
else: eras = era_tag.split(',')

for e in eras: 
  if e not in valid_eras: raise Exception("ERROR: one or more of the eras you specified is not supported, available options are: %s" % ",".join(valid_eras)) 

def green(string,**kwargs):
    '''Displays text in green text inside a black background'''
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

channels = ['zmm','mt']
bkg_procs = {}
# procs for the dimuon channel
bkg_procs['zmm'] = ['ZL', 'ZJ', 'ZTT', 'W', 'VVL', 'VVJ', 'TTL', 'TTJ']
# procs for the mu+tauh channel
bkg_procs['mt'] = ['ZL', 'ZJ', 'W', 'VVJ', 'TTJ', 'QCD']

# signal processes are defined as any with genuine hadronic taus in the mt channel
sig_procs = ['ZTT','VVT','TTT']

cats = {}
cats['zmm'] = [(0, 'zmm_inclusive')]

if dm_bins:
  cats['mt'] = []
  for i, dm in enumerate([0,1,10,11]):
    cats['mt'] += [
     ((i+1)*100+1,  'mt_dm%i_mTLt30_pT_20_to_25' % dm),
     ((i+1)*100+2,  'mt_dm%i_mTLt30_pT_25_to_30' % dm),
     ((i+1)*100+3,  'mt_dm%i_mTLt30_pT_30_to_35' % dm),
     ((i+1)*100+4,  'mt_dm%i_mTLt30_pT_35_to_40' % dm),
     ((i+1)*100+5,  'mt_dm%i_mTLt30_pT_40_to_50' % dm),
     ((i+1)*100+6, 'mt_dm%i_mTLt30_pT_50_to_60' % dm),
     ((i+1)*100+7, 'mt_dm%i_mTLt30_pT_60_to_80' % dm),
     ((i+1)*100+8, 'mt_dm%i_mTLt30_pT_80_to_100' % dm),
     ((i+1)*100+9, 'mt_dm%i_mTLt30_pT_100_to_200' % dm),
    ]
else:

  cats['mt'] = [
               (1, 'mt_inclusive_mTLt30_pT_20_to_25'),
               (2, 'mt_inclusive_mTLt30_pT_25_to_30'),
               (3, 'mt_inclusive_mTLt30_pT_30_to_35'),
               (4, 'mt_inclusive_mTLt30_pT_35_to_40'),
               (5, 'mt_inclusive_mTLt30_pT_40_to_50'),
               (6, 'mt_inclusive_mTLt30_pT_50_to_60'),
               (7, 'mt_inclusive_mTLt30_pT_60_to_80'),
               (8, 'mt_inclusive_mTLt30_pT_80_to_100'),
               (9, 'mt_inclusive_mTLt30_pT_100_to_200'), 
  ]

# Create an empty CombineHarvester instance
cb = CombineHarvester()

# Add processes and observations
for chn in channels:
  for era in eras:
    # Adding Data,Signal Processes and Background processes to the harvester instance
    cb.AddObservations(['*'], ['ztt'], [era], [chn], cats[chn])
    cb.AddProcesses(['*'], ['ztt'], [era], [chn], bkg_procs[chn], cats[chn], False)
    if chn == 'mt': cb.AddProcesses(['*'], ['ztt'], [era], [chn], sig_procs, cats[chn], False)


# Add systematics

inclusive_bins = [1,2,3,4,5,6,7,8,9]
dm0_bins = [101,102,103,104,105,106,107,108,109]
dm1_bins = [201,202,203,204,205,206,207,208,209]
dm10_bins = [301,302,303,304,305,306,307,308,309]
dm11_bins = [401,402,403,404,405,406,407,408,409]

# muon selection efficiency for second muon in di-muon dataset
#cb.cp().channel(['zmm']).process(['W'],False).AddSyst(cb, "CMS_eff_m", "lnN", ch.SystMap()(1.02))
# better to shift the muon efficiency to the mt channel processes (will effectivly shift these in the opposite direction)
cb.cp().channel(['mt']).process(['ZTT','TTT','VVT','TTJ','VVJ','ZL','ZJ']).AddSyst(cb, "CMS_eff_m", "lnN", ch.SystMap()(0.98))

# for Wjets in dimuon data the second muon is a fake so add a seperate uncertainty for this - as this uncertainty is so large we don't need to add another uncertainty for the cross section
cb.cp().channel(['zmm']).process(['W']).AddSyst(cb, "CMS_j_fake_m", "lnN", ch.SystMap()(1.3))

# uncertainty on VV cross-section - set to 10% to cover missing higher order terms which are typically this large
cb.cp().process(['VVL','VVJ','VVT']).AddSyst(cb, "CMS_htt_vvXsec", "lnN", ch.SystMap()(1.1))

# uncertainty on ttbar cross-section - set to 10% to cover missing higher order terms which are typically this large
cb.cp().process(['TTL','TTJ','TTT']).AddSyst(cb, "CMS_htt_tjXsec", "lnN", ch.SystMap()(1.06))

# DY shape uncertainty from re-weighting pT-mass to data (100% variation taked as the uncertainty)
cb.cp().process(['ZTT','ZL','ZJ']).AddSyst(cb, "CMS_htt_dyShape", "shape", ch.SystMap()(1.0))
# ttbar shape uncertainty from re-weighting pT-mass to data (100% variation taked as the uncertainty)
cb.cp().process(['TTL','TTJ','TTT']).AddSyst(cb, "CMS_htt_ttbarShape", "shape", ch.SystMap()(1.0))

# TES uncertainties
cb.cp().channel(['mt']).process(['ZTT','TTT','VVT']).bin_id(dm0_bins+inclusive_bins).AddSyst(cb, "CMS_scale_t_1prong_$ERA","shape", ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(['ZTT','TTT','VVT']).bin_id(dm1_bins+inclusive_bins).AddSyst(cb, "CMS_scale_t_1prong1pizero_$ERA","shape", ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(['ZTT','TTT','VVT']).bin_id(dm10_bins+inclusive_bins).AddSyst(cb, "CMS_scale_t_3prong_$ERA", "shape", ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(['ZTT','TTT','VVT']).bin_id(dm11_bins+inclusive_bins).AddSyst(cb, "CMS_scale_t_3prong1pizero_$ERA", "shape", ch.SystMap()(1.0))

# mu->tauh energy scale split by decay mode (might want to eventually make sure these don't get added for dm 10 and 11)
cb.cp().channel(['mt']).process(['ZL']).bin_id(dm0_bins+inclusive_bins).AddSyst(cb, "CMS_ZLShape_$CHANNEL_1prong_$ERA", "shape", ch.SystMap()(1.00))

cb.cp().channel(['mt']).process(['ZL']).bin_id(dm1_bins+inclusive_bins).AddSyst(cb, "CMS_ZLShape_$CHANNEL_1prong1pizero_$ERA", "shape", ch.SystMap()(1.00))

#MET related uncertainties
cb.cp().channel(['mt']).process(['QCD'],False).AddSyst(cb, "CMS_scale_j_$ERA", "shape", ch.SystMap()(1.00))
cb.cp().channel(['mt']).process(['QCD'],False).AddSyst(cb, "CMS_res_j_$ERA", "shape", ch.SystMap()(1.00))
cb.cp().channel(['mt']).process(['QCD'],False).AddSyst(cb, "CMS_scale_met_unclustered_$ERA", "shape", ch.SystMap()(1.00))

# jet-tau fake-rate in MC - not for W as this will float in the fit
cb.cp().channel(['mt']).process(['TTJ','VVJ','ZJ']).bin_id(inclusive_bins).AddSyst(cb, "CMS_j_fake_t", "lnN", ch.SystMap()(1.2))
cb.cp().channel(['mt']).process(['TTJ','VVJ','ZJ']).bin_id(dm0_bins).AddSyst(cb, "CMS_j_fake_t_DM0", "lnN", ch.SystMap()(1.2))
cb.cp().channel(['mt']).process(['TTJ','VVJ','ZJ']).bin_id(dm1_bins).AddSyst(cb, "CMS_j_fake_t_DM1", "lnN", ch.SystMap()(1.2))
cb.cp().channel(['mt']).process(['TTJ','VVJ','ZJ']).bin_id(dm10_bins).AddSyst(cb, "CMS_j_fake_t_DM10", "lnN", ch.SystMap()(1.2))
cb.cp().channel(['mt']).process(['TTJ','VVJ','ZJ']).bin_id(dm11_bins).AddSyst(cb, "CMS_j_fake_t_DM11", "lnN", ch.SystMap()(1.2))
# add a part decoupled by pT bin
cb.cp().channel(['mt']).process(['TTJ','VVJ','ZJ']).AddSyst(cb, "CMS_j_fake_t_$BIN_$ERA", "lnN", ch.SystMap()(1.2))


# to do - split this by DM for the dm-binned fits!! - might want to split by pT as well 
cb.cp().channel(['mt']).process(['ZL']).bin_id(inclusive_bins).AddSyst(cb, "CMS_l_fake_t", "lnN", ch.SystMap()(1.3))
cb.cp().channel(['mt']).process(['ZL']).bin_id(dm0_bins).AddSyst(cb, "CMS_l_fake_t_DM0", "lnN", ch.SystMap()(1.3))
cb.cp().channel(['mt']).process(['ZL']).bin_id(dm0_bins).AddSyst(cb, "CMS_l_fake_t_DM1", "lnN", ch.SystMap()(1.3))
cb.cp().channel(['mt']).process(['ZL']).bin_id(dm10_bins).AddSyst(cb, "CMS_l_fake_t_DM10", "lnN", ch.SystMap()(1.3))
cb.cp().channel(['mt']).process(['ZL']).bin_id(dm11_bins).AddSyst(cb, "CMS_l_fake_t_DM11", "lnN", ch.SystMap()(1.3))
# add a part decoupled by pT bin
cb.cp().channel(['mt']).process(['ZL']).AddSyst(cb, "CMS_l_fake_t_$BIN_$ERA", "lnN", ch.SystMap()(1.3))

# now add unconstrained rate parameters

# a common rate parameter that scales all MC processes in the di-muon channel and the the ZTT, TTT, and VVT in the mu+tauh channel
# this doesn't need to scale the W in the mu+tauh channel as there is a seperate rate parameters for this processes 
cb.cp().channel(['zmm']).AddSyst(cb, "rate_DY_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT","TTT","VVT","ZL","TTJ","VVJ"]).AddSyst(cb, "rate_DY_$ERA","rateParam",ch.SystMap()(1.0))

cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([1]).AddSyst(cb, "rate_tauSF_DMinclusive_pT20to25_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([2]).AddSyst(cb, "rate_tauSF_DMinclusive_pT25to30_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([3]).AddSyst(cb, "rate_tauSF_DMinclusive_pT30to35_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([4]).AddSyst(cb, "rate_tauSF_DMinclusive_pT35to40_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([5]).AddSyst(cb, "rate_tauSF_DMinclusive_pT40to50_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([6]).AddSyst(cb, "rate_tauSF_DMinclusive_pT50to60_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([7]).AddSyst(cb, "rate_tauSF_DMinclusive_pT60to80_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([8]).AddSyst(cb, "rate_tauSF_DMinclusive_pT80to100_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([9]).AddSyst(cb, "rate_tauSF_DMinclusive_pT100to200_$ERA","rateParam",ch.SystMap()(1.0))

for i, dm in enumerate([0,1,10,11]):
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+1]).AddSyst(cb, "rate_tauSF_DM%i_pT20to25_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+2]).AddSyst(cb, "rate_tauSF_DM%i_pT25to30_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+3]).AddSyst(cb, "rate_tauSF_DM%i_pT30to35_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+4]).AddSyst(cb, "rate_tauSF_DM%i_pT35to40_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+5]).AddSyst(cb, "rate_tauSF_DM%i_pT40to50_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+6]).AddSyst(cb, "rate_tauSF_DM%i_pT50to60_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+7]).AddSyst(cb, "rate_tauSF_DM%i_pT60to80_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+8]).AddSyst(cb, "rate_tauSF_DM%i_pT80to100_$ERA" % dm,"rateParam",ch.SystMap()(1.0))
  cb.cp().channel(['mt']).process(["ZTT", "TTT", "VVT"]).bin_id([(i+1)*100+9]).AddSyst(cb, "rate_tauSF_DM%i_pT100to200_$ERA" % dm,"rateParam",ch.SystMap()(1.0))

#single rate parameters for QCD and W+jets
cb.cp().channel(['mt']).process(["QCD"]).bin_id(inclusive_bins).AddSyst(cb, "rate_QCD_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["W"]).bin_id(inclusive_bins).AddSyst(cb, "rate_W_$ERA","rateParam",ch.SystMap()(1.0))

cb.cp().channel(['mt']).process(["QCD"]).bin_id(dm0_bins).AddSyst(cb, "rate_QCD_DM0_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["W"]).bin_id(dm0_bins).AddSyst(cb, "rate_W_DM0_$ERA","rateParam",ch.SystMap()(1.0))

cb.cp().channel(['mt']).process(["QCD"]).bin_id(dm1_bins).AddSyst(cb, "rate_QCD_DM1_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["W"]).bin_id(dm1_bins).AddSyst(cb, "rate_W_DM1_$ERA","rateParam",ch.SystMap()(1.0))

cb.cp().channel(['mt']).process(["QCD"]).bin_id(dm10_bins).AddSyst(cb, "rate_QCD_DM10_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["W"]).bin_id(dm10_bins).AddSyst(cb, "rate_W_DM10_$ERA","rateParam",ch.SystMap()(1.0))

cb.cp().channel(['mt']).process(["QCD"]).bin_id(dm11_bins).AddSyst(cb, "rate_QCD_DM11_$ERA","rateParam",ch.SystMap()(1.0))
cb.cp().channel(['mt']).process(["W"]).bin_id(dm11_bins).AddSyst(cb, "rate_W_DM11_$ERA","rateParam",ch.SystMap()(1.0))

# additional uncorrelated rate uncertainties to account for different extrapolations per pT bin
cb.cp().channel(['mt']).process(['W']).AddSyst(cb, "CMS_W_extrap_$BIN_$ERA", "lnN", ch.SystMap()(1.1))
cb.cp().channel(['mt']).process(['QCD']).AddSyst(cb, "CMS_QCD_extrap_$BIN_$ERA", "lnN", ch.SystMap()(1.1))

# set sensible ranges for all rate params
for era in eras:
  cb.GetParameter("rate_DY_%s" % era).set_range(0.5,1.5)

# Populating Observation, Process and Systematic entries in the harvester instance
for chn in channels:
  for era in eras:
    filename = 'shapes/ztt.datacard.m_vis.%s.%s.root' % (chn,era)
    print ">>>   file %s" % (filename)
    print('%s, %s' % (chn, era))
    cb.cp().channel([chn]).process(bkg_procs[chn]).era([era]).ExtractShapes(filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")
    if chn == 'mt': cb.cp().channel([chn]).process(sig_procs).era([era]).ExtractShapes(filename, "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC")

# Merge to one bin for Z->mumu CRs
for b in cb.cp().channel(['zmm']).bin_set():
  print("Rebinning Z->mumu CRs into 1-bin categories")
  cb.cp().bin([b]).VariableRebin([50.,150,]);

# Rebin histograms for mt channel using Auto Rebinning

rebin = AutoRebin()
rebin.SetBinThreshold(100)
rebin.SetBinUncertFraction(0.2)
rebin.SetRebinMode(1)
rebin.SetPerformRebin(True)
rebin.SetVerbosity(1) 
rebin.Rebin(cb,cb)

# Convert any shapes in Z->mumu CRs to lnN
cb.cp().channel(['zmm']).syst_type(["shape"]).ForEachSyst(lambda sys: sys.set_type('lnN'))
for era in eras:
  cb.cp().channel(['mt']).syst_name(['CMS_scale_j_%s' % era,'CMS_res_j_%s' % era, 'CMS_scale_met_unclustered_%s' % era]).syst_type(["shape"]).ForEachSyst(lambda sys: sys.set_type('lnN'))

def SetSystToOne(syst):
  if syst.value_u()<=0.: syst.set_value_u(1.)
  if syst.asymm() and syst.value_d() <=0: syst.set_value_d(1.)

cb.cp().syst_type(["lnN"]).ForEachSyst(SetSystToOne)

# Zero negetive bins
print(green("Zeroing NegativeBins"))
cb.ForEachProc(NegativeBins)

SetStandardBinNames(cb)
# Add bbb uncerts using autoMC stats
cb.SetAutoMCStats(cb, 0., 1, 1)

# define groups - this will help determine correlated uncertainties later on

#cb.AddDatacardLineAtEnd("byYearsandBins group = CMS_eff_m")
#cb.AddDatacardLineAtEnd("byBins group = rate_DY_2016_postVFP rate_DY_2016_preVFP")

# Write datacards
print green(">>> writing datacards...")
datacardtxt  = "%s/cmb/$BIN.txt"%(output_folder)
datacardroot = "%s/cmb/common/$BIN_input.root"%(output_folder)
writer = CardWriter(datacardtxt,datacardroot)
writer.SetVerbosity(1)
writer.SetWildcardMasses([ ])
writer.WriteCards("cmb", cb)
