output_dir=$1
working_pointVsJets=$2
working_pointVsEle=$3

pois="rate_tauSF_DM0_pT20to25_2016_preVFP,rate_tauSF_DM0_pT25to30_2016_preVFP,rate_tauSF_DM0_pT30to35_2016_preVFP,rate_tauSF_DM0_pT35to40_2016_preVFP,rate_tauSF_DM0_pT40to50_2016_preVFP,rate_tauSF_DM0_pT50to60_2016_preVFP,rate_tauSF_DM0_pT60to80_2016_preVFP,rate_tauSF_DM0_pT80to100_2016_preVFP,rate_tauSF_DM0_pT100to200_2016_preVFP,rate_tauSF_DM1_pT20to25_2016_preVFP,rate_tauSF_DM1_pT25to30_2016_preVFP,rate_tauSF_DM1_pT30to35_2016_preVFP,rate_tauSF_DM1_pT35to40_2016_preVFP,rate_tauSF_DM1_pT40to50_2016_preVFP,rate_tauSF_DM1_pT50to60_2016_preVFP,rate_tauSF_DM1_pT60to80_2016_preVFP,rate_tauSF_DM1_pT80to100_2016_preVFP,rate_tauSF_DM1_pT100to200_2016_preVFP,rate_tauSF_DM10_pT20to25_2016_preVFP,rate_tauSF_DM10_pT25to30_2016_preVFP,rate_tauSF_DM10_pT30to35_2016_preVFP,rate_tauSF_DM10_pT35to40_2016_preVFP,rate_tauSF_DM10_pT40to50_2016_preVFP,rate_tauSF_DM10_pT50to60_2016_preVFP,rate_tauSF_DM10_pT60to80_2016_preVFP,rate_tauSF_DM10_pT80to100_2016_preVFP,rate_tauSF_DM10_pT100to200_2016_preVFP,rate_tauSF_DM11_pT20to25_2016_preVFP,rate_tauSF_DM11_pT25to30_2016_preVFP,rate_tauSF_DM11_pT30to35_2016_preVFP,rate_tauSF_DM11_pT35to40_2016_preVFP,rate_tauSF_DM11_pT40to50_2016_preVFP,rate_tauSF_DM11_pT50to60_2016_preVFP,rate_tauSF_DM11_pT60to80_2016_preVFP,rate_tauSF_DM11_pT80to100_2016_preVFP,rate_tauSF_DM11_pT100to200_2016_preVFP,rate_tauSF_DM0_pT20to25_2016_postVFP,rate_tauSF_DM0_pT25to30_2016_postVFP,rate_tauSF_DM0_pT30to35_2016_postVFP,rate_tauSF_DM0_pT35to40_2016_postVFP,rate_tauSF_DM0_pT40to50_2016_postVFP,rate_tauSF_DM0_pT50to60_2016_postVFP,rate_tauSF_DM0_pT60to80_2016_postVFP,rate_tauSF_DM0_pT80to100_2016_postVFP,rate_tauSF_DM0_pT100to200_2016_postVFP,rate_tauSF_DM1_pT20to25_2016_postVFP,rate_tauSF_DM1_pT25to30_2016_postVFP,rate_tauSF_DM1_pT30to35_2016_postVFP,rate_tauSF_DM1_pT35to40_2016_postVFP,rate_tauSF_DM1_pT40to50_2016_postVFP,rate_tauSF_DM1_pT50to60_2016_postVFP,rate_tauSF_DM1_pT60to80_2016_postVFP,rate_tauSF_DM1_pT80to100_2016_postVFP,rate_tauSF_DM1_pT100to200_2016_postVFP,rate_tauSF_DM10_pT20to25_2016_postVFP,rate_tauSF_DM10_pT25to30_2016_postVFP,rate_tauSF_DM10_pT30to35_2016_postVFP,rate_tauSF_DM10_pT35to40_2016_postVFP,rate_tauSF_DM10_pT40to50_2016_postVFP,rate_tauSF_DM10_pT50to60_2016_postVFP,rate_tauSF_DM10_pT60to80_2016_postVFP,rate_tauSF_DM10_pT80to100_2016_postVFP,rate_tauSF_DM10_pT100to200_2016_postVFP,rate_tauSF_DM11_pT20to25_2016_postVFP,rate_tauSF_DM11_pT25to30_2016_postVFP,rate_tauSF_DM11_pT30to35_2016_postVFP,rate_tauSF_DM11_pT35to40_2016_postVFP,rate_tauSF_DM11_pT40to50_2016_postVFP,rate_tauSF_DM11_pT50to60_2016_postVFP,rate_tauSF_DM11_pT60to80_2016_postVFP,rate_tauSF_DM11_pT80to100_2016_postVFP,rate_tauSF_DM11_pT100to200_2016_postVFP,rate_tauSF_DM0_pT20to25_2017,rate_tauSF_DM0_pT25to30_2017,rate_tauSF_DM0_pT30to35_2017,rate_tauSF_DM0_pT35to40_2017,rate_tauSF_DM0_pT40to50_2017,rate_tauSF_DM0_pT50to60_2017,rate_tauSF_DM0_pT60to80_2017,rate_tauSF_DM0_pT80to100_2017,rate_tauSF_DM0_pT100to200_2017,rate_tauSF_DM1_pT20to25_2017,rate_tauSF_DM1_pT25to30_2017,rate_tauSF_DM1_pT30to35_2017,rate_tauSF_DM1_pT35to40_2017,rate_tauSF_DM1_pT40to50_2017,rate_tauSF_DM1_pT50to60_2017,rate_tauSF_DM1_pT60to80_2017,rate_tauSF_DM1_pT80to100_2017,rate_tauSF_DM1_pT100to200_2017,rate_tauSF_DM10_pT20to25_2017,rate_tauSF_DM10_pT25to30_2017,rate_tauSF_DM10_pT30to35_2017,rate_tauSF_DM10_pT35to40_2017,rate_tauSF_DM10_pT40to50_2017,rate_tauSF_DM10_pT50to60_2017,rate_tauSF_DM10_pT60to80_2017,rate_tauSF_DM10_pT80to100_2017,rate_tauSF_DM10_pT100to200_2017,rate_tauSF_DM11_pT20to25_2017,rate_tauSF_DM11_pT25to30_2017,rate_tauSF_DM11_pT30to35_2017,rate_tauSF_DM11_pT35to40_2017,rate_tauSF_DM11_pT40to50_2017,rate_tauSF_DM11_pT50to60_2017,rate_tauSF_DM11_pT60to80_2017,rate_tauSF_DM11_pT80to100_2017,rate_tauSF_DM11_pT100to200_2017,rate_tauSF_DM0_pT20to25_2018,rate_tauSF_DM0_pT25to30_2018,rate_tauSF_DM0_pT30to35_2018,rate_tauSF_DM0_pT35to40_2018,rate_tauSF_DM0_pT40to50_2018,rate_tauSF_DM0_pT50to60_2018,rate_tauSF_DM0_pT60to80_2018,rate_tauSF_DM0_pT80to100_2018,rate_tauSF_DM0_pT100to200_2018,rate_tauSF_DM1_pT20to25_2018,rate_tauSF_DM1_pT25to30_2018,rate_tauSF_DM1_pT30to35_2018,rate_tauSF_DM1_pT35to40_2018,rate_tauSF_DM1_pT40to50_2018,rate_tauSF_DM1_pT50to60_2018,rate_tauSF_DM1_pT60to80_2018,rate_tauSF_DM1_pT80to100_2018,rate_tauSF_DM1_pT100to200_2018,rate_tauSF_DM10_pT20to25_2018,rate_tauSF_DM10_pT25to30_2018,rate_tauSF_DM10_pT30to35_2018,rate_tauSF_DM10_pT35to40_2018,rate_tauSF_DM10_pT40to50_2018,rate_tauSF_DM10_pT50to60_2018,rate_tauSF_DM10_pT60to80_2018,rate_tauSF_DM10_pT80to100_2018,rate_tauSF_DM10_pT100to200_2018,rate_tauSF_DM11_pT20to25_2018,rate_tauSF_DM11_pT25to30_2018,rate_tauSF_DM11_pT30to35_2018,rate_tauSF_DM11_pT35to40_2018,rate_tauSF_DM11_pT40to50_2018,rate_tauSF_DM11_pT50to60_2018,rate_tauSF_DM11_pT60to80_2018,rate_tauSF_DM11_pT80to100_2018,rate_tauSF_DM11_pT100to200_2018"

if [ "${working_pointVsEle}" == True ]; then
  python scripts/harvestDatacards_newQCD_uncerts.py --dm-bins -o "outputs/${output_dir}" --wp "${working_pointVsJets}" --tightVsEle --useCRs

else
  python scripts/harvestDatacards_newQCD_uncerts.py --dm-bins -o "outputs/${output_dir}" --wp "${working_pointVsJets}"  --useCRs
fi

#fix combine memory issues
ulimit -s unlimited

combineTool.py -M T2W -i outputs/${output_dir}/cmb/ -o ws.root --X-allow-no-signal

echo "Running first fit"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -n ".ztt.bestfit.singles" -d outputs/${output_dir}/cmb/ws.root

echo "Running snapshot fit"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit" --snapshotName MultiDimFit

echo "Running snapshot fit with byErasAndBins frozen"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins" --snapshotName MultiDimFit  --freezeNuisanceGroups byErasAndBins

echo "Running snapshot fit with byErasAndBins and byBins frozen"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins" --snapshotName MultiDimFit  --freezeNuisanceGroups byErasAndBins,byBins

echo "Running snapshot fit with byErasAndBins, byBins, and byDM frozen"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveWorkspace --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo singles --cl=0.68 --there -d outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.MultiDimFit.mH125.root -n ".ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins_byDM" --snapshotName MultiDimFit   --freezeNuisanceGroups byErasAndBins,byBins,byDM0,byDM1,byDM10,byDM11


echo "Making graphs with SFs"

if [ "${working_pointVsEle}" == True ]; then
   for x in "" .freeze_byErasAndBins .freeze_byErasAndBins_byBins .freeze_byErasAndBins_byBins_byDM; do python scripts/makeSFGraphs.py  -f outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.postfit${x}.MultiDimFit.mH125.root --dm-bins --saveJson --wp="${working_pointVsJets}vsjet_tightvsele" ; done
else
   for x in "" .freeze_byErasAndBins .freeze_byErasAndBins_byBins .freeze_byErasAndBins_byBins_byDM; do python scripts/makeSFGraphs.py  -f outputs/${output_dir}/cmb/higgsCombine.ztt.bestfit.singles.postfit${x}.MultiDimFit.mH125.root --dm-bins --saveJson --wp="${working_pointVsJets}vsjet_vvloosevsele" ; done
fi

echo "Making graphs with decomposed uncertainties"

dir=outputs/${output_dir}/cmb/

python scripts/decoupleUncerts.py -f1 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.MultiDimFit.mH125.TGraphAsymmErrors.root -f2 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins.MultiDimFit.mH125.TGraphAsymmErrors.root -f3 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins.MultiDimFit.mH125.TGraphAsymmErrors.root  -f4 ${dir}/higgsCombine.ztt.bestfit.singles.postfit.freeze_byErasAndBins_byBins_byDM.MultiDimFit.mH125.TGraphAsymmErrors.root --dm-bins -o "outputs/${output_dir}/cmb/"
