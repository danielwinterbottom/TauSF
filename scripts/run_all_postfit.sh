output_dir=$1
bin=$2
year=$3
#pt_bin=$4
era=$4

if [ "${era}" == "UL" ]; then
 echo ${era}
 pois="rate_tauSF_DM0_pT20to25_2016_preVFP,rate_tauSF_DM0_pT25to30_2016_preVFP,rate_tauSF_DM0_pT30to35_2016_preVFP,rate_tauSF_DM0_pT35to40_2016_preVFP,rate_tauSF_DM0_pT40to50_2016_preVFP,rate_tauSF_DM0_pT50to60_2016_preVFP,rate_tauSF_DM0_pT60to80_2016_preVFP,rate_tauSF_DM0_pT80to100_2016_preVFP,rate_tauSF_DM0_pT100to200_2016_preVFP,rate_tauSF_DM1_pT20to25_2016_preVFP,rate_tauSF_DM1_pT25to30_2016_preVFP,rate_tauSF_DM1_pT30to35_2016_preVFP,rate_tauSF_DM1_pT35to40_2016_preVFP,rate_tauSF_DM1_pT40to50_2016_preVFP,rate_tauSF_DM1_pT50to60_2016_preVFP,rate_tauSF_DM1_pT60to80_2016_preVFP,rate_tauSF_DM1_pT80to100_2016_preVFP,rate_tauSF_DM1_pT100to200_2016_preVFP,rate_tauSF_DM10_pT20to25_2016_preVFP,rate_tauSF_DM10_pT25to30_2016_preVFP,rate_tauSF_DM10_pT30to35_2016_preVFP,rate_tauSF_DM10_pT35to40_2016_preVFP,rate_tauSF_DM10_pT40to50_2016_preVFP,rate_tauSF_DM10_pT50to60_2016_preVFP,rate_tauSF_DM10_pT60to80_2016_preVFP,rate_tauSF_DM10_pT80to100_2016_preVFP,rate_tauSF_DM10_pT100to200_2016_preVFP,rate_tauSF_DM11_pT20to25_2016_preVFP,rate_tauSF_DM11_pT25to30_2016_preVFP,rate_tauSF_DM11_pT30to35_2016_preVFP,rate_tauSF_DM11_pT35to40_2016_preVFP,rate_tauSF_DM11_pT40to50_2016_preVFP,rate_tauSF_DM11_pT50to60_2016_preVFP,rate_tauSF_DM11_pT60to80_2016_preVFP,rate_tauSF_DM11_pT80to100_2016_preVFP,rate_tauSF_DM11_pT100to200_2016_preVFP,rate_tauSF_DM0_pT20to25_2016_postVFP,rate_tauSF_DM0_pT25to30_2016_postVFP,rate_tauSF_DM0_pT30to35_2016_postVFP,rate_tauSF_DM0_pT35to40_2016_postVFP,rate_tauSF_DM0_pT40to50_2016_postVFP,rate_tauSF_DM0_pT50to60_2016_postVFP,rate_tauSF_DM0_pT60to80_2016_postVFP,rate_tauSF_DM0_pT80to100_2016_postVFP,rate_tauSF_DM0_pT100to200_2016_postVFP,rate_tauSF_DM1_pT20to25_2016_postVFP,rate_tauSF_DM1_pT25to30_2016_postVFP,rate_tauSF_DM1_pT30to35_2016_postVFP,rate_tauSF_DM1_pT35to40_2016_postVFP,rate_tauSF_DM1_pT40to50_2016_postVFP,rate_tauSF_DM1_pT50to60_2016_postVFP,rate_tauSF_DM1_pT60to80_2016_postVFP,rate_tauSF_DM1_pT80to100_2016_postVFP,rate_tauSF_DM1_pT100to200_2016_postVFP,rate_tauSF_DM10_pT20to25_2016_postVFP,rate_tauSF_DM10_pT25to30_2016_postVFP,rate_tauSF_DM10_pT30to35_2016_postVFP,rate_tauSF_DM10_pT35to40_2016_postVFP,rate_tauSF_DM10_pT40to50_2016_postVFP,rate_tauSF_DM10_pT50to60_2016_postVFP,rate_tauSF_DM10_pT60to80_2016_postVFP,rate_tauSF_DM10_pT80to100_2016_postVFP,rate_tauSF_DM10_pT100to200_2016_postVFP,rate_tauSF_DM11_pT20to25_2016_postVFP,rate_tauSF_DM11_pT25to30_2016_postVFP,rate_tauSF_DM11_pT30to35_2016_postVFP,rate_tauSF_DM11_pT35to40_2016_postVFP,rate_tauSF_DM11_pT40to50_2016_postVFP,rate_tauSF_DM11_pT50to60_2016_postVFP,rate_tauSF_DM11_pT60to80_2016_postVFP,rate_tauSF_DM11_pT80to100_2016_postVFP,rate_tauSF_DM11_pT100to200_2016_postVFP,rate_tauSF_DM0_pT20to25_2017,rate_tauSF_DM0_pT25to30_2017,rate_tauSF_DM0_pT30to35_2017,rate_tauSF_DM0_pT35to40_2017,rate_tauSF_DM0_pT40to50_2017,rate_tauSF_DM0_pT50to60_2017,rate_tauSF_DM0_pT60to80_2017,rate_tauSF_DM0_pT80to100_2017,rate_tauSF_DM0_pT100to200_2017,rate_tauSF_DM1_pT20to25_2017,rate_tauSF_DM1_pT25to30_2017,rate_tauSF_DM1_pT30to35_2017,rate_tauSF_DM1_pT35to40_2017,rate_tauSF_DM1_pT40to50_2017,rate_tauSF_DM1_pT50to60_2017,rate_tauSF_DM1_pT60to80_2017,rate_tauSF_DM1_pT80to100_2017,rate_tauSF_DM1_pT100to200_2017,rate_tauSF_DM10_pT20to25_2017,rate_tauSF_DM10_pT25to30_2017,rate_tauSF_DM10_pT30to35_2017,rate_tauSF_DM10_pT35to40_2017,rate_tauSF_DM10_pT40to50_2017,rate_tauSF_DM10_pT50to60_2017,rate_tauSF_DM10_pT60to80_2017,rate_tauSF_DM10_pT80to100_2017,rate_tauSF_DM10_pT100to200_2017,rate_tauSF_DM11_pT20to25_2017,rate_tauSF_DM11_pT25to30_2017,rate_tauSF_DM11_pT30to35_2017,rate_tauSF_DM11_pT35to40_2017,rate_tauSF_DM11_pT40to50_2017,rate_tauSF_DM11_pT50to60_2017,rate_tauSF_DM11_pT60to80_2017,rate_tauSF_DM11_pT80to100_2017,rate_tauSF_DM11_pT100to200_2017,rate_tauSF_DM0_pT20to25_2018,rate_tauSF_DM0_pT25to30_2018,rate_tauSF_DM0_pT30to35_2018,rate_tauSF_DM0_pT35to40_2018,rate_tauSF_DM0_pT40to50_2018,rate_tauSF_DM0_pT50to60_2018,rate_tauSF_DM0_pT60to80_2018,rate_tauSF_DM0_pT80to100_2018,rate_tauSF_DM0_pT100to200_2018,rate_tauSF_DM1_pT20to25_2018,rate_tauSF_DM1_pT25to30_2018,rate_tauSF_DM1_pT30to35_2018,rate_tauSF_DM1_pT35to40_2018,rate_tauSF_DM1_pT40to50_2018,rate_tauSF_DM1_pT50to60_2018,rate_tauSF_DM1_pT60to80_2018,rate_tauSF_DM1_pT80to100_2018,rate_tauSF_DM1_pT100to200_2018,rate_tauSF_DM10_pT20to25_2018,rate_tauSF_DM10_pT25to30_2018,rate_tauSF_DM10_pT30to35_2018,rate_tauSF_DM10_pT35to40_2018,rate_tauSF_DM10_pT40to50_2018,rate_tauSF_DM10_pT50to60_2018,rate_tauSF_DM10_pT60to80_2018,rate_tauSF_DM10_pT80to100_2018,rate_tauSF_DM10_pT100to200_2018,rate_tauSF_DM11_pT20to25_2018,rate_tauSF_DM11_pT25to30_2018,rate_tauSF_DM11_pT30to35_2018,rate_tauSF_DM11_pT35to40_2018,rate_tauSF_DM11_pT40to50_2018,rate_tauSF_DM11_pT50to60_2018,rate_tauSF_DM11_pT60to80_2018,rate_tauSF_DM11_pT80to100_2018,rate_tauSF_DM11_pT100to200_2018"
fi

if [ "${era}" == "2022" ]; then
 echo ${era}
 pois="rate_tauSF_DM0_pT20to25_2022_preEE,rate_tauSF_DM0_pT25to30_2022_preEE,rate_tauSF_DM0_pT30to35_2022_preEE,rate_tauSF_DM0_pT35to40_2022_preEE,rate_tauSF_DM0_pT40to50_2022_preEE,rate_tauSF_DM0_pT50to60_2022_preEE,rate_tauSF_DM0_pT60to80_2022_preEE,rate_tauSF_DM0_pT80to100_2022_preEE,rate_tauSF_DM0_pT100to200_2022_preEE,rate_tauSF_DM1_pT20to25_2022_preEE,rate_tauSF_DM1_pT25to30_2022_preEE,rate_tauSF_DM1_pT30to35_2022_preEE,rate_tauSF_DM1_pT35to40_2022_preEE,rate_tauSF_DM1_pT40to50_2022_preEE,rate_tauSF_DM1_pT50to60_2022_preEE,rate_tauSF_DM1_pT60to80_2022_preEE,rate_tauSF_DM1_pT80to100_2022_preEE,rate_tauSF_DM1_pT100to200_2022_preEE,rate_tauSF_DM10_pT20to25_2022_preEE,rate_tauSF_DM10_pT25to30_2022_preEE,rate_tauSF_DM10_pT30to35_2022_preEE,rate_tauSF_DM10_pT35to40_2022_preEE,rate_tauSF_DM10_pT40to50_2022_preEE,rate_tauSF_DM10_pT50to60_2022_preEE,rate_tauSF_DM10_pT60to80_2022_preEE,rate_tauSF_DM10_pT80to100_2022_preEE,rate_tauSF_DM10_pT100to200_2022_preEE,rate_tauSF_DM11_pT20to25_2022_preEE,rate_tauSF_DM11_pT25to30_2022_preEE,rate_tauSF_DM11_pT30to35_2022_preEE,rate_tauSF_DM11_pT35to40_2022_preEE,rate_tauSF_DM11_pT40to50_2022_preEE,rate_tauSF_DM11_pT50to60_2022_preEE,rate_tauSF_DM11_pT60to80_2022_preEE,rate_tauSF_DM11_pT80to100_2022_preEE,rate_tauSF_DM11_pT100to200_2022_preEE,rate_tauSF_DM0_pT20to25_2022_postEE,rate_tauSF_DM0_pT25to30_2022_postEE,rate_tauSF_DM0_pT30to35_2022_postEE,rate_tauSF_DM0_pT35to40_2022_postEE,rate_tauSF_DM0_pT40to50_2022_postEE,rate_tauSF_DM0_pT50to60_2022_postEE,rate_tauSF_DM0_pT60to80_2022_postEE,rate_tauSF_DM0_pT80to100_2022_postEE,rate_tauSF_DM0_pT100to200_2022_postEE,rate_tauSF_DM1_pT20to25_2022_postEE,rate_tauSF_DM1_pT25to30_2022_postEE,rate_tauSF_DM1_pT30to35_2022_postEE,rate_tauSF_DM1_pT35to40_2022_postEE,rate_tauSF_DM1_pT40to50_2022_postEE,rate_tauSF_DM1_pT50to60_2022_postEE,rate_tauSF_DM1_pT60to80_2022_postEE,rate_tauSF_DM1_pT80to100_2022_postEE,rate_tauSF_DM1_pT100to200_2022_postEE,rate_tauSF_DM10_pT20to25_2022_postEE,rate_tauSF_DM10_pT25to30_2022_postEE,rate_tauSF_DM10_pT30to35_2022_postEE,rate_tauSF_DM10_pT35to40_2022_postEE,rate_tauSF_DM10_pT40to50_2022_postEE,rate_tauSF_DM10_pT50to60_2022_postEE,rate_tauSF_DM10_pT60to80_2022_postEE,rate_tauSF_DM10_pT80to100_2022_postEE,rate_tauSF_DM10_pT100to200_2022_postEE,rate_tauSF_DM11_pT20to25_2022_postEE,rate_tauSF_DM11_pT25to30_2022_postEE,rate_tauSF_DM11_pT30to35_2022_postEE,rate_tauSF_DM11_pT35to40_2022_postEE,rate_tauSF_DM11_pT40to50_2022_postEE,rate_tauSF_DM11_pT50to60_2022_postEE,rate_tauSF_DM11_pT60to80_2022_postEE,rate_tauSF_DM11_pT80to100_2022_postEE,rate_tauSF_DM11_pT100to200_2022_postEE"
fi

ulimit -s unlimited
echo "Running postfit plots"

combineTool.py -m 125 -M MultiDimFit --redefineSignalPOIs "${pois}" --saveFitResult --X-rtd MINIMIZER_analytic --expectSignal 0 --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 0.1 --algo none --there -n ".ztt.bestfit.singles.robustHesse" -d outputs/${output_dir}/cmb/ws.root --robustHesse=1

echo "The current directory is: $(pwd)"
echo "Make histograms containing prefit shapes"
python python/PostFitShapesCombEras.py -f outputs/${output_dir}/cmb/multidimfit.ztt.bestfit.singles.robustHesse.root:fit_mdf -w outputs/${output_dir}/cmb/ws.root -d outputs/${output_dir}/cmb/combined.txt.cmb --output outputs/${output_dir}/cmb/new_shapes_prefit_${bin}_${year}.root --bin_match ztt_mt_${bin}_${year}

echo "Make histograms containing postfit shapes"

python python/PostFitShapesCombEras.py -f outputs/${output_dir}/cmb/multidimfit.ztt.bestfit.singles.robustHesse.root:fit_mdf -w outputs/${output_dir}/cmb/ws.root --postfit -d outputs/${output_dir}/cmb/combined.txt.cmb --output outputs/${output_dir}/cmb/new_shapes_postfit_${bin}_${year}.root --bin_match ztt_mt_${bin}_${year}

echo "Make prefit plots for all eras and pT-dependent bins"

python scripts/postFitPlots.py --file outputs/${output_dir}/cmb/final_shapes_prefit.root --file_dir ztt_mt_${bin}_${year} --mode prefit --ratio --ratio_range 0.5,1.5

#for a  in 100 200 300 400; do for b in 1 2 3 4 5 6 7 8 9; do for era in 2016_preVFP 2016_postVFP 2017 2018; do python scripts/postFitPlots.py --file outputs/${output_dir}/shapes_prefit.root --file_dir ztt_mt_$((a+b))_${era} --mode prefit --ratio --ratio_range 0.8,1.2; done; done; done

echo "Make postfit plots for all eras and pT-dependent bins"

python scripts/postFitPlots.py --file outputs/${output_dir}/cmb/final_shapes_postfit.root --file_dir ztt_mt_${bin}_${year} --mode postfit --ratio --ratio_range 0.5,1.5

#for a  in 100 200 300 400; do for b in 1 2 3 4 5 6 7 8 9; do for era in 2016_preVFP 2016_postVFP 2017 2018; do python scripts/postFitPlots.py --file outputs/${output_dir}/shapes_postfit.root --file_dir ztt_mt_$((a+b))_${era} --mode postfit --ratio --ratio_range 0.8,1.2; done; done; done
