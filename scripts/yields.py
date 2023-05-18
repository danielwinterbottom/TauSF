import ROOT
import json
from builtins import min
from builtins import max
# Open the first ROOT file and get a histogram from a directory
bin_boundaries = [20.,25.,30.,35.,40.,50.,60.,80.,100.,200.]
pt_vals = [23., 28., 32., 37., 44., 54., 68., 89., 125.]
wps = ["loose", "medium", "tight", "vtight", "vvtight"]#, "vvtight"]
wpsvsele = ["vvloose", "tight"]
eras = ["2016_preVFP", "2016_postVFP", "2017", "2018"]
dm_no = [1,2,3,4]
dms = [0, 1, 10, 11]
for wp in wps:
   for wpvsele in wpsvsele:
      #print (r"%(wp)s VsJets                                                                                                     %(wpvsele)s VsEle") %vars()
      #data = json.loads("jsons/tau_SF_strings_dm_binned_%(wp)svsjet_%(wpvsele)svsele_v2p5.json" %vars())
      with open("jsons/tau_SF_strings_dm_binned_%(wp)svsjet_%(wpvsele)svsele_v2p5.json" %vars()) as f:
         data = json.load(f)
      for k in eras:
         era = k
         value = data["%(wp)svsjet_%(wpvsele)svsele" %vars()]["%(era)s" %vars()]
         for j in dm_no:
            dm = j
            dm_id = dms[j-1]
            #result = eval(value, {'__builtins__': None}, {'gen_match_2': 5, 'tau_decay_mode_2': dm_id, 'pt_2': pt_vals[i], 'min': min, 'max': max})
            #print result
            print(r"\begin{frame}")
            print(r"\frametitle{Prefit and Postfit Closure - Yields}")
            print(r"\begin{table}[h]")
            print(r"\centering")
            print(r"\tiny")
            print(r"\begin{tabularx}{6.365cm}{ |p{0.4cm}||p{0.65cm}|p{0.65cm}|p{0.65cm}|p{0.65cm}|p{0.65cm}| }")
            print(r"\hline")
            print(r"\multicolumn{6}{|c|}{%(era)s DM%(dm_id)s %(wp)svsjet\_%(wpvsele)svsele} \\")%vars()
            print(r"\hline")
            print(r" $p_T$      &SF      &ZTT    &QCD   &W &QCD+W\\")
            print(r"\hline")
            for i in range(len(pt_vals)):
               index = i+1
               result = eval(value, {'__builtins__': None}, {'gen_match_2': 5, 'tau_decay_mode_2': dm_id, 'pt_2': pt_vals[i], 'min': min, 'max': max})
               #print result
               if wpvsele == "tight": file1 = ROOT.TFile.Open("outputs/tauSF_output_v2p5_%(wp)s_tightVsEle_dm_all_years_new/final_shapes_prefit.root" %vars())
               elif wpvsele == "vvloose": file1 = ROOT.TFile.Open("outputs/tauSF_output_v2p5_%(wp)s_dm_all_years_new/final_shapes_prefit.root" %vars())
               ztt1 = file1.Get("ztt_mt_%i0%i_%s/ZTT" %(dm, index, era))
               qcd1 = file1.Get("ztt_mt_%i0%i_%s/QCD" %(dm, index, era))
               w1 = file1.Get("ztt_mt_%i0%i_%s/W" %(dm, index, era))

               # Open the second ROOT file and get a histogram from a directory
               if wpvsele == "tight": file2 = ROOT.TFile.Open("outputs/tauSF_output_v2p5_%(wp)s_tightVsEle_dm_all_years_new/final_shapes_postfit.root" %vars())
               elif wpvsele == "vvloose": file2 = ROOT.TFile.Open("outputs/tauSF_output_v2p5_%(wp)s_dm_all_years_new/final_shapes_postfit.root" %vars())
               ztt2 = file2.Get("ztt_mt_%i0%i_%s/ZTT" %(dm, index, era))
               qcd2 = file2.Get("ztt_mt_%i0%i_%s/QCD" %(dm, index, era))
               w2 = file2.Get("ztt_mt_%i0%i_%s/W" %(dm, index, era))

               z_ratio = ztt2.Integral()/ztt1.Integral() #need sum!!!!!
               w_ratio = w2.Integral()/w1.Integral()
               if qcd1 == None or qcd2 == None: 
                  qcd_ratio = 0
                  q_and_w = w_ratio
               else: 
                  qcd_ratio = qcd2.Integral()/qcd1.Integral()
                  q_and_w = (qcd2.Integral()+w2.Integral())/(qcd1.Integral()+w1.Integral())
               pt_0 = pt_vals[i]
               pt = result
               DM =dms[j-1]
               #print "%(era)s		 DM%(DM)s		scale_factor=%(pt)f			ZTT Yield Ratio: %(z_ratio)f			QCD Yield Ratio: %(qcd_ratio)f			W Yield Ratio: %(w_ratio)f" %vars()
               print(r"%(pt_0)i	&%(pt)f		&%(z_ratio)f	&%(qcd_ratio)f	&%(w_ratio)f &%(q_and_w)f\\")%vars()

               # Close the ROOT files
               file1.Close()
               file2.Close()
            print(r"\hline")
            print(r"\end{tabularx}")
            print(r"\end{table}")
            print(r"\end{frame}")
