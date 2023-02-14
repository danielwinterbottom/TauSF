# TauSF
a repository for fitting the tau ID SFs using ZTT events

## Setup

setup CMSSW:

```bash
 cmsrel CMSSW_10_2_13
 cd CMSSW_10_2_13/src
 cmsenv
``` 
Clone combine and combine harvester:

```bash
 git clone -b 102x git@github.com:cms-analysis/CombineHarvester.git CombineHarvester
 git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
 cd HiggsAnalysis/CombinedLimit
 git fetch origin
 git checkout v8.2.0
 cd -
```

Clone tauSF repository:

```bash
git clone git@github.com:danielwinterbottom/TauSF.git TauSF
```

compile:

```bash
scram b clean
scram b -j8
``` 

## Copy datacards to shapes directory

Add instructions to retrieve these from a repository

....

## Converting datacards

If you are starting from 2D histograms in bins of pT vs m_vis these must first be split into
1D histograms in bins of m_vis
Run this script to split the datacards:

```bash
python scripts/convertDatacards.py -f shapes/ztt.datacard.pt_2_vs_m_vis.mt.2017.root
```

## Produce txt datacards

The various options are set in the config/harvestDatacards.yml config file 

Run the following script to produce the txt datacards
```bash
python scripts/harvestDatacards.py
```

## Create workspace

```bash
combineTool.py -M T2W -i outputs/tauSF_output/cmb/ -o ws.root --X-allow-no-signal
```

## Run fits 

Run fits to determine proper values and errors of all POIs

When using DM-binned fits define POIs with:

```bash
pois="rate_tauSF_DM0_pT20to25_2016_preVFP,rate_tauSF_DM0_pT25to30_2016_preVFP,rate_tauSF_DM0_pT30to35_2016_preVFP,rate_tauSF_DM0_pT35to40_2016_preVFP,rate_tauSF_DM0_pT40to50_2016_preVFP,rate_tauSF_DM0_pT50to60_2016_preVFP,rate_tauSF_DM0_pT60to80_2016_preVFP,rate_tauSF_DM0_pT80to100_2016_preVFP,rate_tauSF_DM0_pT100to200_2016_preVFP,rate_tauSF_DM1_pT20to25_2016_preVFP,rate_tauSF_DM1_pT25to30_2016_preVFP,rate_tauSF_DM1_pT30to35_2016_preVFP,rate_tauSF_DM1_pT35to40_2016_preVFP,rate_tauSF_DM1_pT40to50_2016_preVFP,rate_tauSF_DM1_pT50to60_2016_preVFP,rate_tauSF_DM1_pT60to80_2016_preVFP,rate_tauSF_DM1_pT80to100_2016_preVFP,rate_tauSF_DM1_pT100to200_2016_preVFP,rate_tauSF_DM10_pT20to25_2016_preVFP,rate_tauSF_DM10_pT25to30_2016_preVFP,rate_tauSF_DM10_pT30to35_2016_preVFP,rate_tauSF_DM10_pT35to40_2016_preVFP,rate_tauSF_DM10_pT40to50_2016_preVFP,rate_tauSF_DM10_pT50to60_2016_preVFP,rate_tauSF_DM10_pT60to80_2016_preVFP,rate_tauSF_DM10_pT80to100_2016_preVFP,rate_tauSF_DM10_pT100to200_2016_preVFP,rate_tauSF_DM11_pT20to25_2016_preVFP,rate_tauSF_DM11_pT25to30_2016_preVFP,rate_tauSF_DM11_pT30to35_2016_preVFP,rate_tauSF_DM11_pT35to40_2016_preVFP,rate_tauSF_DM11_pT40to50_2016_preVFP,rate_tauSF_DM11_pT50to60_2016_preVFP,rate_tauSF_DM11_pT60to80_2016_preVFP,rate_tauSF_DM11_pT80to100_2016_preVFP,rate_tauSF_DM11_pT100to200_2016_preVFP,rate_tauSF_DM0_pT20to25_2016_postVFP,rate_tauSF_DM0_pT25to30_2016_postVFP,rate_tauSF_DM0_pT30to35_2016_postVFP,rate_tauSF_DM0_pT35to40_2016_postVFP,rate_tauSF_DM0_pT40to50_2016_postVFP,rate_tauSF_DM0_pT50to60_2016_postVFP,rate_tauSF_DM0_pT60to80_2016_postVFP,rate_tauSF_DM0_pT80to100_2016_postVFP,rate_tauSF_DM0_pT100to200_2016_postVFP,rate_tauSF_DM1_pT20to25_2016_postVFP,rate_tauSF_DM1_pT25to30_2016_postVFP,rate_tauSF_DM1_pT30to35_2016_postVFP,rate_tauSF_DM1_pT35to40_2016_postVFP,rate_tauSF_DM1_pT40to50_2016_postVFP,rate_tauSF_DM1_pT50to60_2016_postVFP,rate_tauSF_DM1_pT60to80_2016_postVFP,rate_tauSF_DM1_pT80to100_2016_postVFP,rate_tauSF_DM1_pT100to200_2016_postVFP,rate_tauSF_DM10_pT20to25_2016_postVFP,rate_tauSF_DM10_pT25to30_2016_postVFP,rate_tauSF_DM10_pT30to35_2016_postVFP,rate_tauSF_DM10_pT35to40_2016_postVFP,rate_tauSF_DM10_pT40to50_2016_postVFP,rate_tauSF_DM10_pT50to60_2016_postVFP,rate_tauSF_DM10_pT60to80_2016_postVFP,rate_tauSF_DM10_pT80to100_2016_postVFP,rate_tauSF_DM10_pT100to200_2016_postVFP,rate_tauSF_DM11_pT20to25_2016_postVFP,rate_tauSF_DM11_pT25to30_2016_postVFP,rate_tauSF_DM11_pT30to35_2016_postVFP,rate_tauSF_DM11_pT35to40_2016_postVFP,rate_tauSF_DM11_pT40to50_2016_postVFP,rate_tauSF_DM11_pT50to60_2016_postVFP,rate_tauSF_DM11_pT60to80_2016_postVFP,rate_tauSF_DM11_pT80to100_2016_postVFP,rate_tauSF_DM11_pT100to200_2016_postVFP,rate_tauSF_DM0_pT20to25_2017,rate_tauSF_DM0_pT25to30_2017,rate_tauSF_DM0_pT30to35_2017,rate_tauSF_DM0_pT35to40_2017,rate_tauSF_DM0_pT40to50_2017,rate_tauSF_DM0_pT50to60_2017,rate_tauSF_DM0_pT60to80_2017,rate_tauSF_DM0_pT80to100_2017,rate_tauSF_DM0_pT100to200_2017,rate_tauSF_DM1_pT20to25_2017,rate_tauSF_DM1_pT25to30_2017,rate_tauSF_DM1_pT30to35_2017,rate_tauSF_DM1_pT35to40_2017,rate_tauSF_DM1_pT40to50_2017,rate_tauSF_DM1_pT50to60_2017,rate_tauSF_DM1_pT60to80_2017,rate_tauSF_DM1_pT80to100_2017,rate_tauSF_DM1_pT100to200_2017,rate_tauSF_DM10_pT20to25_2017,rate_tauSF_DM10_pT25to30_2017,rate_tauSF_DM10_pT30to35_2017,rate_tauSF_DM10_pT35to40_2017,rate_tauSF_DM10_pT40to50_2017,rate_tauSF_DM10_pT50to60_2017,rate_tauSF_DM10_pT60to80_2017,rate_tauSF_DM10_pT80to100_2017,rate_tauSF_DM10_pT100to200_2017,rate_tauSF_DM11_pT20to25_2017,rate_tauSF_DM11_pT25to30_2017,rate_tauSF_DM11_pT30to35_2017,rate_tauSF_DM11_pT35to40_2017,rate_tauSF_DM11_pT40to50_2017,rate_tauSF_DM11_pT50to60_2017,rate_tauSF_DM11_pT60to80_2017,rate_tauSF_DM11_pT80to100_2017,rate_tauSF_DM11_pT100to200_2017,rate_tauSF_DM0_pT20to25_2018,rate_tauSF_DM0_pT25to30_2018,rate_tauSF_DM0_pT30to35_2018,rate_tauSF_DM0_pT35to40_2018,rate_tauSF_DM0_pT40to50_2018,rate_tauSF_DM0_pT50to60_2018,rate_tauSF_DM0_pT60to80_2018,rate_tauSF_DM0_pT80to100_2018,rate_tauSF_DM0_pT100to200_2018,rate_tauSF_DM1_pT20to25_2018,rate_tauSF_DM1_pT25to30_2018,rate_tauSF_DM1_pT30to35_2018,rate_tauSF_DM1_pT35to40_2018,rate_tauSF_DM1_pT40to50_2018,rate_tauSF_DM1_pT50to60_2018,rate_tauSF_DM1_pT60to80_2018,rate_tauSF_DM1_pT80to100_2018,rate_tauSF_DM1_pT100to200_2018,rate_tauSF_DM10_pT20to25_2018,rate_tauSF_DM10_pT25to30_2018,rate_tauSF_DM10_pT30to35_2018,rate_tauSF_DM10_pT35to40_2018,rate_tauSF_DM10_pT40to50_2018,rate_tauSF_DM10_pT50to60_2018,rate_tauSF_DM10_pT60to80_2018,rate_tauSF_DM10_pT80to100_2018,rate_tauSF_DM10_pT100to200_2018,rate_tauSF_DM11_pT20to25_2018,rate_tauSF_DM11_pT25to30_2018,rate_tauSF_DM11_pT30to35_2018,rate_tauSF_DM11_pT35to40_2018,rate_tauSF_DM11_pT40to50_2018,rate_tauSF_DM11_pT50to60_2018,rate_tauSF_DM11_pT60to80_2018,rate_tauSF_DM11_pT80to100_2018,rate_tauSF_DM11_pT100to200_2018"
```


For for DM-inclusive fits define POIs with:

```bash
pois="rate_tauSF_DMinclusive_pT20to25_2016_preVFP,rate_tauSF_DMinclusive_pT25to30_2016_preVFP,rate_tauSF_DMinclusive_pT30to35_2016_preVFP,rate_tauSF_DMinclusive_pT35to40_2016_preVFP,rate_tauSF_DMinclusive_pT40to50_2016_preVFP,rate_tauSF_DMinclusive_pT50to60_2016_preVFP,rate_tauSF_DMinclusive_pT60to80_2016_preVFP,rate_tauSF_DMinclusive_pT80to100_2016_preVFP,rate_tauSF_DMinclusive_pT100to200_2016_preVFP,rate_tauSF_DMinclusive_pT20to25_2016_postVFP,rate_tauSF_DMinclusive_pT25to30_2016_postVFP,rate_tauSF_DMinclusive_pT30to35_2016_postVFP,rate_tauSF_DMinclusive_pT35to40_2016_postVFP,rate_tauSF_DMinclusive_pT40to50_2016_postVFP,rate_tauSF_DMinclusive_pT50to60_2016_postVFP,rate_tauSF_DMinclusive_pT60to80_2016_postVFP,rate_tauSF_DMinclusive_pT80to100_2016_postVFP,rate_tauSF_DMinclusive_pT100to200_2016_postVFP,rate_tauSF_DMinclusive_pT20to25_2017,rate_tauSF_DMinclusive_pT25to30_2017,rate_tauSF_DMinclusive_pT30to35_2017,rate_tauSF_DMinclusive_pT35to40_2017,rate_tauSF_DMinclusive_pT40to50_2017,rate_tauSF_DMinclusive_pT50to60_2017,rate_tauSF_DMinclusive_pT60to80_2017,rate_tauSF_DMinclusive_pT80to100_2017,rate_tauSF_DMinclusive_pT100to200_2017,rate_tauSF_DMinclusive_pT20to25_2018,rate_tauSF_DMinclusive_pT25to30_2018,rate_tauSF_DMinclusive_pT30to35_2018,rate_tauSF_DMinclusive_pT35to40_2018,rate_tauSF_DMinclusive_pT40to50_2018,rate_tauSF_DMinclusive_pT50to60_2018,rate_tauSF_DMinclusive_pT60to80_2018,rate_tauSF_DMinclusive_pT80to100_2018,rate_tauSF_DMinclusive_pT100to200_2018"
```

Run the fit with all systematics floating using:

```bash
combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -n ".ztt.bestfit.singles" -d outputs/tauSF_output_DMinclusive_mTLt60_newsysts_v4/cmb/ws.root
```

For decomposition of the uncertainties into groups that allow uncertainties to be correlated by era and by bins we need to run the following additional fits:

.... add these to the instructions ...

Once the fits are run it is also possible to make a summary plot of the uncertainty magnitudes using:

```bash
scripts/compareSFUncerts.py 
```

Note the names of the graphs are currently hardcoded in this script

## Run postfit plots

First need to run a fit and store the fit result. We use the robustHesse option to make sure the covariance matrix is accurate 

```bash
combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveFitResult --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo none --there -n ".ztt.bestfit.singles.robustHesse" -d outputs/tauSF_Feb08_DMinclusive_mTLt30/cmb/ws.root --robustHesse=1
``` 

Make the histograms containing the postfit shapes.
Note this script only computes the uncertainties for the TotalBkg histogram not for the individual processes to save time (note ZTT is included as background in the current setup)

```bash
python python/PostFitShapesCombEras.py -f outputs/tauSF_Feb08_DMinclusive_mTLt30/cmb/multidimfit.ztt.bestfit.singles.robustHesse.root:fit_mdf -w outputs/tauSF_Feb08_DMinclusive_mTLt30/cmb/ws.root -d outputs/tauSF_Feb08_DMinclusive_mTLt30/cmb/combined.txt.cmb --output shapes_postfit.root
```
You can optionally use the option "-b" to only specify one bin at a time allowing the shapes to be run parallel e.g "-b ztt_mt_1_2018"

Make the plots by running the script "scripts/postFitPlots.py"

e.g to make the plots for all eras and pT-dependent bins:

```bash
for b in 1 2 3 4 5 6 7 8 9; do for era in 2016_preVFP 2016_postVFP 2017 2018; do python scripts/postFitPlots.py --file shapes_postfit.root --file_dir ztt_mt_${b}_${era} --ratio --ratio_range 0.8,1.2; done; done
```

## Run impacts (approximate)

Do fits:
```bash
combineTool.py -M Impacts  --doFits --robustFit=1 --approx robust --redefineSignalPOIs rate_tauSF_DM1_pT40to50_2018 -d outputs/tauSF_output_DMbinned/cmb/ws.root  -n ".ztt.impacts"  --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 -m 125
```
Collect results:

```bash
combineTool.py -M Impacts --approx robust --redefineSignalPOIs rate_tauSF_DM1_pT40to50_2018 -d outputs/tauSF_output_DMbinned/cmb/ws.root  -n ".ztt.impacts" -o impacts.json -m 125
```

Make plot:
```bash
plotImpacts.py -i impacts.json -o impacts
```

## Make TGraphAsymmErrors for fitted results. For dm-binned SF use option --dm-bins - this will also perform fits of the SFs vs pT 

Produce the graphs:

```bash
python scripts/makeSFGraphs.py -f outputs/tauSF_Feb08_DMinclusive_tightVsE_mTLt30/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root
```

for pT-dependent SF you can also make a plot of the graphs after running the previous script using:

```bash
python scripts/plotInclusiveSF.py -f outputs/tauSF_Feb08_DMinclusive_tightVsE_mTLt30/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.TGraphAsymmErrors.root
```
