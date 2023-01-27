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

 
