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

```bash
combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs rate_tauSF_DMinclusive_pT20to25_2018 --saveFitResult -d outputs/tauSF_output/cmb/ws.root --there -n ".ztt.bestfit"  --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --robustFit
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
