import json
from collections import OrderedDict
import ROOT

eras = ['2016_preVFP','2016_postVFP','2017','2018']

def maketiddata_pt(era,wps=['Loose','Medium','Tight']):
  """Construct tau ID data block."""
  # get bin edges - same binning is used for all WPs so just determine these once for the tight WP 
  ptbins=GetBinEdges('tight',era)
  # store SFs and uncertainty variations into a dictionary
  sfs={wp: GetPTdependentData(wp.lower(),era) for wp in wps}

  tiddata = OrderedDict( # category:genmatch -> category:wp -> binning:pt -> category:syst
    nodetype='category', # category:genmatch
    input="genmatch",
    content= [
      OrderedDict(key=0, value=1.0), # j  -> tau_h fake
      OrderedDict(key=1, value=1.0), # e  -> tau_h fake
      OrderedDict(key=2, value=1.0), # mu -> tau_h fake
      OrderedDict(key=3, value=1.0), # e  -> tau_h fake
      OrderedDict(key=4, value=1.0), # mu -> tau_h fake
      OrderedDict(key=5,  # real tau_h
        value=OrderedDict(
          nodetype='category',
          input='wp',
          content=[
            OrderedDict(
              key=wp,
              value=OrderedDict(
                nodetype='binning',
                input='pt',
                edges=ptbins,
                flow='clamp',
                content=[
                   OrderedDict(
                     nodetype="category", 
                     input="syst", 
                     ptbin=pt, # remove later 
                     content=[
                       OrderedDict(key="nom", value=sfs[wp][int(pt)][0]),
                       OrderedDict(key="up", value=sfs[wp][int(pt)][1][0]),
                       OrderedDict(key="down", value=sfs[wp][int(pt)][1][1]),
                     ]
                   )
                for pt in ptbins[:-1]]
              ),
            )
          for wp in wps],
        ), 
      ), 
      OrderedDict(key=6, value=1.0), # j  -> tau_h fake
    ]
  )
  return tiddata


for era in eras:

  name='tau_sf_pt-dm_DeepTau2017v2p1VSjet_%(era)s' % vars()
  id='DeepTau2017v2p1VSjet'
  description = "%(id)s SFs: By default, use the pT-dependent SFs with the 'pt' flag. For analyses that split events based on tau DM or using hadronic tau triggers, use the DM-dependent SFs with flag 'dm'." % vars()
  inputs = [
  OrderedDict(name="pt",       type="real",   description="Reconstructed tau pT"),
  OrderedDict(name="dm",       type="int",    description="0, 1, 2, 10, 11"),
  OrderedDict(name="genmatch", type="int",    description="genmatch: 0 or 6 = unmatched or jet, 1 or 3 = electron, 2 or 4 = muon, 5 = real tau"),
  OrderedDict(name="wp",       type="string", description="DeepTau2017v2p1VSjet working point: VVVLoose-VVTight"),
  OrderedDict(name="syst",     type="string", description="Systematic 'nom', 'up', 'down'"), # need to adjust this for the new systematics
  OrderedDict(name="flag",     type="string", description="Flag: 'pt' = pT-binned SFs, 'dm' = DM-binned SFs with fitted pT-dependence"),
  ]
  output = OrderedDict(
      name= "sf",
      type= "real",
      description= "%(id)s scale factor" % vars()
  )
  
  def GetBinEdges(wp,era):
    input_file='outputs/tauSF_Feb20_DMinclusive_%(wp)s/split_uncertainties.root' % vars()
    f=ROOT.TFile(input_file)
    hist_name='DMinclusive_%(era)s_hist' % vars()
    sf_hist=f.Get(hist_name)
    bin_edges=[]
    for i in range(1,sf_hist.GetNbinsX()+2):
      bin_edges.append(sf_hist.GetBinLowEdge(i))
    return bin_edges
  
  def GetPTdependentData(wp,era):
  
    input_file='outputs/tauSF_Feb20_DMinclusive_%(wp)s/split_uncertainties.root' % vars()
    f=ROOT.TFile(input_file)
    graph_name='DMinclusive_%(era)s' % vars()
    hist_name=graph_name+'_hist'
    sf_graph=f.Get(graph_name)
    sf_hist=f.Get(hist_name)
  
    sf_graph_stat_err=f.Get(graph_name+'_stat')
    sf_graph_syst_alleras_err=f.Get(graph_name+'_syst_alleras')
    sf_graph_syst_oneera_err=f.Get(graph_name+'_syst_%(era)s' % vars())
  
    sf_pt={}
  
    for i in range(0,sf_graph.GetN()):
  
      x=ROOT.Double()
      y=ROOT.Double()
  
      sf_graph.GetPoint(i,x,y)
      bini=sf_hist.FindBin(x)
      bin_low=sf_hist.GetBinLowEdge(bini)
      #bin_high=sf_hist.GetBinLowEdge(bini+1)
  
      err_total_d=y-sf_graph.GetErrorYhigh(i)
      err_total_u=y+sf_graph.GetErrorYlow(i)
  
      err_stat_d=y-sf_graph_stat_err.GetErrorYhigh(i) 
      err_stat_u=y+sf_graph_stat_err.GetErrorYlow(i) 
  
      err_syst_alleras_d=y-sf_graph_syst_alleras_err.GetErrorYhigh(i)
      err_syst_alleras_u=y+sf_graph_syst_alleras_err.GetErrorYlow(i)
     
      err_syst_oneeras_d=y-sf_graph_syst_oneera_err.GetErrorYhigh(i)
      err_syst_oneeras_u=y+sf_graph_syst_oneera_err.GetErrorYlow(i) 
  
      sf_pt[int(bin_low)] = (y, (err_total_u, err_total_d), (err_stat_u,err_stat_d), (err_syst_alleras_u, err_syst_alleras_d), (err_syst_oneeras_u, err_syst_oneeras_d))
  
    return sf_pt
  
  GetPTdependentData('tight',era)

  tiddata=maketiddata_pt(era)

  # Data to be written
  dictionary = OrderedDict()
  dictionary['name'] =  name
  dictionary['description'] = description 
  dictionary['version'] =  0
  dictionary['inputs'] = inputs
  dictionary['output'] = output
  dictionary['data'] = tiddata
  
  # Serializing json
  json_object = json.dumps(dictionary, indent=2, sort_keys=False)
   
  # Writing to sample.json
  with open("sample_%(era)s.json" % vars(), "w") as outfile:
      outfile.write(json_object)
