output_dir=$1
options=$2

pois="rate_tauSF_DMinclusive_pT20to25_2016_preVFP,rate_tauSF_DMinclusive_pT25to30_2016_preVFP,rate_tauSF_DMinclusive_pT30to35_2016_preVFP,rate_tauSF_DMinclusive_pT35to40_2016_preVFP,rate_tauSF_DMinclusive_pT40to50_2016_preVFP,rate_tauSF_DMinclusive_pT50to60_2016_preVFP,rate_tauSF_DMinclusive_pT60to80_2016_preVFP,rate_tauSF_DMinclusive_pT80to100_2016_preVFP,rate_tauSF_DMinclusive_pT100to200_2016_preVFP,rate_tauSF_DMinclusive_pT20to25_2016_postVFP,rate_tauSF_DMinclusive_pT25to30_2016_postVFP,rate_tauSF_DMinclusive_pT30to35_2016_postVFP,rate_tauSF_DMinclusive_pT35to40_2016_postVFP,rate_tauSF_DMinclusive_pT40to50_2016_postVFP,rate_tauSF_DMinclusive_pT50to60_2016_postVFP,rate_tauSF_DMinclusive_pT60to80_2016_postVFP,rate_tauSF_DMinclusive_pT80to100_2016_postVFP,rate_tauSF_DMinclusive_pT100to200_2016_postVFP,rate_tauSF_DMinclusive_pT20to25_2017,rate_tauSF_DMinclusive_pT25to30_2017,rate_tauSF_DMinclusive_pT30to35_2017,rate_tauSF_DMinclusive_pT35to40_2017,rate_tauSF_DMinclusive_pT40to50_2017,rate_tauSF_DMinclusive_pT50to60_2017,rate_tauSF_DMinclusive_pT60to80_2017,rate_tauSF_DMinclusive_pT80to100_2017,rate_tauSF_DMinclusive_pT100to200_2017,rate_tauSF_DMinclusive_pT20to25_2018,rate_tauSF_DMinclusive_pT25to30_2018,rate_tauSF_DMinclusive_pT30to35_2018,rate_tauSF_DMinclusive_pT35to40_2018,rate_tauSF_DMinclusive_pT40to50_2018,rate_tauSF_DMinclusive_pT50to60_2018,rate_tauSF_DMinclusive_pT60to80_2018,rate_tauSF_DMinclusive_pT80to100_2018,rate_tauSF_DMinclusive_pT100to200_2018"

python scripts/harvestDatacards.py -o "outputs/${output_dir}" ${options}

combineTool.py -M T2W -i outputs/${output_dir}/cmb/ -o ws.root --X-allow-no-signal

echo "Running first fit"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -n ".ztt.bestfit.singles" -d outputs/${output_dir}/cmb/ws.root

echo "Running snapshot fit"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit" --snapshotName MultiDimFit

echo "Running snapshot fit with byErasAndBins frozen"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins" --snapshotName MultiDimFit   --freezeNuisanceGroups byErasAndBins

echo "Running snapshot fit with byErasAndBins and byBins frozen"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins" --snapshotName MultiDimFit   --freezeNuisanceGroups byErasAndBins,byBins

echo "Making graphs with SFs"

for x in "" .freeze_byErasAndBins .freeze_byErasAndBins_byBins ; do python scripts/makeSFGraphs.py  -f outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.postfit${x}.MultiDimFit.mH125.root -e 2018; done

echo "Making graphs with decomposed uncertainties"

dir=outputs/${output_dir}/cmb/

python scripts/decoupleUncerts.py -f1 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.MultiDimFit.mH125.TGraphAsymmErrors.root -f2 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins.MultiDimFit.mH125.TGraphAsymmErrors.root -f3 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins.MultiDimFit.mH125.TGraphAsymmErrors.root -e 2018 -o outputs/${output_dir} 
