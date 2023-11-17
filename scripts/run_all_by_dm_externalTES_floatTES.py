import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from argparse import ArgumentParser
import os

pois=["rate_tauSF_DM0_pT20to25_$YEAR","rate_tauSF_DM0_pT25to30_$YEAR","rate_tauSF_DM0_pT30to35_$YEAR","rate_tauSF_DM0_pT35to40_$YEAR","rate_tauSF_DM0_pT40to50_$YEAR","rate_tauSF_DM0_pT50to60_$YEAR","rate_tauSF_DM0_pT60to80_$YEAR","rate_tauSF_DM0_pT80to100_$YEAR","rate_tauSF_DM0_pT100to200_$YEAR","rate_tauSF_DM1_pT20to25_$YEAR","rate_tauSF_DM1_pT25to30_$YEAR","rate_tauSF_DM1_pT30to35_$YEAR","rate_tauSF_DM1_pT35to40_$YEAR","rate_tauSF_DM1_pT40to50_$YEAR","rate_tauSF_DM1_pT50to60_$YEAR","rate_tauSF_DM1_pT60to80_$YEAR","rate_tauSF_DM1_pT80to100_$YEAR","rate_tauSF_DM1_pT100to200_$YEAR","rate_tauSF_DM10_pT20to25_$YEAR","rate_tauSF_DM10_pT25to30_$YEAR","rate_tauSF_DM10_pT30to35_$YEAR","rate_tauSF_DM10_pT35to40_$YEAR","rate_tauSF_DM10_pT40to50_$YEAR","rate_tauSF_DM10_pT50to60_$YEAR","rate_tauSF_DM10_pT60to80_$YEAR","rate_tauSF_DM10_pT80to100_$YEAR","rate_tauSF_DM10_pT100to200_$YEAR","rate_tauSF_DM11_pT20to25_$YEAR","rate_tauSF_DM11_pT25to30_$YEAR","rate_tauSF_DM11_pT30to35_$YEAR","rate_tauSF_DM11_pT35to40_$YEAR","rate_tauSF_DM11_pT40to50_$YEAR","rate_tauSF_DM11_pT50to60_$YEAR","rate_tauSF_DM11_pT60to80_$YEAR","rate_tauSF_DM11_pT80to100_$YEAR","rate_tauSF_DM11_pT100to200_$YEAR"]

tes=["CMS_scale_t_1prong_$YEAR", "CMS_scale_t_1prong1pizero_$YEAR", "CMS_scale_t_3prong_$YEAR", "CMS_scale_t_3prong1pizero_$YEAR"]

parser = ArgumentParser()
parser.add_argument('-o', '--output_folder', dest='output_folder', type=str, default='', help="set output folder name")
parser.add_argument('-e', '--eras', dest='eras', type=str, default='all', help="set eras to be processed; can be either UL or 2022")
parser.add_argument('--wp', dest='wp', default='medium', help="The vs jet WP to measure SFs for")
parser.add_argument('--tightVsEle', dest='tightVsEle', default=False, action='store_true', help="if specified then use the tight WP of the vs electron ID, otherwise the vvloose WP is used")
args = parser.parse_args()

if args.eras == 'UL': eras = ['2016_preVFP', '2016_postVFP', '2017', '2018'] # add other eras later
if args.eras == '2022': eras = ['2022_preEE', '2022_postEE']
else: eras=args.eras.split(',')

fix_tes=False

output_dir = args.output_folder

os.system('ulimit -s unlimited') #everytime you do os, it opens a new shell so this won't work - need to run it before the script

# make text datacards
os.system('python scripts/harvestDatacards_newQCD_uncerts.py --dm-bins -o \"outputs/%s\" --wp %s --useCRs -e %s' % (output_dir, args.wp, args.eras) + (' --tightVsEle' if args.tightVsEle else ''))

# make workspaces
os.system('combineTool.py -M T2W -i outputs/%s/cmb/ -o ws.root --X-allow-no-signal' % output_dir)


# run first fit floating TES between +/- 2sigma
tes_ranges_str='--setParameterRanges '
tes_pois_str=''
for p in tes:
  for year in eras: 
    # we have to make sure the range is sufficient to allow for a nominal value !=0
    # allowing ranges between -2 and 2 sigma should guarentee this - if pulls are larger then 2 sigma then the fit result might not be physical anyway so should be carefully checked
    if p == "CMS_scale_t_1prong_$YEAR":
       tes_ranges_str+='%s=-4,4:' % (p.replace('$YEAR',year))
       tes_pois_str+='%s,' % (p.replace('$YEAR',year))
    else:
       tes_ranges_str+='%s=-2,2:' % (p.replace('$YEAR',year))
       tes_pois_str+='%s,' % (p.replace('$YEAR',year))

pois_str=''
for p in pois:
  for year in eras:
    pois_str+='%s,' % (p.replace('$YEAR',year)) 

if tes_ranges_str[-1] ==':': tes_ranges_str=tes_ranges_str[:-1]
if tes_pois_str[-1] ==',': tes_pois_str=tes_pois_str[:-1]
if pois_str[-1] ==',': pois_str=pois_str[:-1]

# run first fit with TES floating

print("Running initital fit with all POIs floating")
os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s,%(tes_pois_str)s\" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -n ".ztt.bestfit.singles" -d outputs/%(output_dir)s/cmb/ws.root --saveFitResult %(tes_ranges_str)s --floatParameters \"%(tes_pois_str)s\"' % vars())


# after running fit we get the postfitvalues of the TES parameters:

# get values and +/- 1 sigma shifts from tree
f = ROOT.TFile('outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root' % vars())
l = f.Get('limit')
vals = {}
tes_actual_vals={}
tes_up_str=''
tes_down_str=''
tes_nom_str=''
for poi in tes:
  skip = True
  for year in eras:
    poi_=poi.replace('$YEAR',year)
    vals[poi_] = set()
    for i in range(0, l.GetEntries()):
      l.GetEntry(i)
      x=getattr(l, poi_)
      vals[poi_].add(x)
      # the factors must be set equal to the sie of the 1-sigma uncertainties for the TES parameters
      # 2% for DM=11, or 1.5% for the other DMs 
    if '3prong1pizero' in poi_: factor=0.02
    else: factor=0.015
    tes_actual_vals[poi_]= format(1.+sorted(list(vals[poi_]))[1]*factor, ".3f")
    tes_nom_str+='%s=%.4f,' % (poi_,sorted(list(vals[poi_]))[1])
    tes_down_str+='%s=%.4f,' % (poi_,sorted(list(vals[poi_]))[1]-1.)
    tes_up_str+='%s=%.4f,' % (poi_,sorted(list(vals[poi_]))[1]+1.)

    #if any up (down) TES uncertainties are larger than +2 (smaller than -2) sigma we need to adjust the range for the parameters as well otherwise they will get clipped at the boundary
    if sorted(list(vals[poi_]))[1]-1. < -2 or sorted(list(vals[poi_]))[1]+1. > 2:
      new_max = max(sorted(list(vals[poi_]))[1]+1.,2.)
      new_min = min(sorted(list(vals[poi_]))[1]-1.,-2.)
      tes_ranges_str=tes_ranges_str.replace('%s=-2,2' % poi_, '%s=%.4f,%.4f' % (poi_,new_min-0.1,new_max+0.1)) 

if tes_nom_str[-1] ==',': tes_nom_str=tes_nom_str[:-1]
if tes_up_str[-1] ==',': tes_up_str=tes_up_str[:-1]
if tes_down_str[-1] ==',': tes_down_str=tes_down_str[:-1]

# we store the TES values and uncertainties in histograms with uncertainties fixed to 2% for DM=11 and 1.5% for other DMs

for year in eras:
  fout=ROOT.TFile('outputs/%s/cmb/TauES_dm_DeepTau2018v2p5VSjet_UL%s_VSjet%s_VSele%s_Jul18.root' % (output_dir,year,args.wp.capitalize(), 'Tight' if args.tightVsEle else 'VVLoose'),'RECREATE')
  print( fout)
  h = ROOT.TH1D('tes','tes',12,0,12)
  h.GetXaxis().SetTitle("#tau_{h} decay modes")
  h.GetYaxis().SetTitle("SF")
  for dm in range(0,12):
    bin_i=h.FindBin(dm)
    if dm not in [0,1,10,11]: h.SetBinContent(bin_i,1.)
    else:
      if dm==0: key='CMS_scale_t_1prong_%s' % year
      if dm==1: key='CMS_scale_t_1prong1pizero_%s' % year
      if dm==10: key='CMS_scale_t_3prong_%s' % year
      if dm==11: key='CMS_scale_t_3prong1pizero_%s' % year
      h.SetBinContent(bin_i,float(tes_actual_vals[key]))
      h.SetBinError(bin_i, 0.015 if dm!=11 else 0.02)
  h.Write()
  fout.Close()

#now run fit with TES values fixed for nominal SFs

print("Running nominal fit")

os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s\" --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit" --snapshotName MultiDimFit --freezeNuisanceGroups TES %(tes_ranges_str)s --setParameters %(tes_nom_str)s' % vars())
   
# now run fits with TES values fixed to +/- 1 sigma for uncertainty variations

print("Running TES up fit")

os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s\" --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.TESUp" --snapshotName MultiDimFit --freezeNuisanceGroups TES --setParameters %(tes_up_str)s %(tes_ranges_str)s' % vars())


print("Running TES down fit")

os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s\" --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.TESDown" --snapshotName MultiDimFit --freezeNuisanceGroups TES --setParameters %(tes_down_str)s %(tes_ranges_str)s' % vars())

print("Running snapshot fit with byErasAndBins frozen")

os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s\" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins" --snapshotName MultiDimFit  --freezeNuisanceGroups TES,byErasAndBins %(tes_ranges_str)s' % vars())

print("Running snapshot fit with byErasAndBins and byBins frozen")

os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s\" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins" --snapshotName MultiDimFit  --freezeNuisanceGroups TES,byErasAndBins,byBins %(tes_ranges_str)s' % vars())

print("Running snapshot fit with byErasAndBins, byBins, and byDM frozen")

os.system('combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs \"%(pois_str)s\" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/%(output_dir)s/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins_byDM" --snapshotName MultiDimFit   --freezeNuisanceGroups TES,byErasAndBins,byBins,byDM0,byDM1,byDM10,byDM11 %(tes_ranges_str)s' % vars())

# produce graphs containing fitted SF for all uncertainty variations
print("Making graphs with decomposed uncertainties")

variations = [
  '.freeze_byErasAndBins',
  '.freeze_byErasAndBins_byBins',
  '.freeze_byErasAndBins_byBins_byDM',
  '.TESUp',
  '.TESDown',
  '',
]

if args.eras!='all':
  eras_str='-e \"%s\"' % args.eras
else: eras_str=''

# finally make final fits and obtain uncertainty variations
if args.tightVsEle:
  json_out="--saveJson --wp=%svsjet_tightvsele" % args.wp
else:
  json_out="--saveJson --wp=%svsjet_vvloosevsele" % args.wp

for v in variations:
  os.system('python scripts/makeSFGraphs.py  -f outputs/%s/cmb/higgsCombine.ztt.bestfit.singles.postfit%s.MultiDimFit.mH125.root --dm-bins %s %s' %(output_dir, v, json_out, eras_str))


dir_name='outputs/%(output_dir)s/cmb/' % vars()
for extra in ['','--split-fit']: 

  os.system('python scripts/decoupleUncerts.py -f1 %(dir_name)s/higgsCombine.ztt.bestfit.singles.postfit.MultiDimFit.mH125.TGraphAsymmErrors.root -f2 %(dir_name)s/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins.MultiDimFit.mH125.TGraphAsymmErrors.root -f3 %(dir_name)s/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins.MultiDimFit.mH125.TGraphAsymmErrors.root  -f4 %(dir_name)s/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins_byDM.MultiDimFit.mH125.TGraphAsymmErrors.root -f5 %(dir_name)s/higgsCombine.ztt.bestfit.singles.postfit.TESUp.MultiDimFit.mH125.TGraphAsymmErrors.root -f6 %(dir_name)s/higgsCombine.ztt.bestfit.singles.postfit.TESDown.MultiDimFit.mH125.TGraphAsymmErrors.root --dm-bins -o \"outputs/%(output_dir)s/cmb/\" %(json_out)s %(eras_str)s %(extra)s' % vars())

