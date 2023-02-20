import json
from collections import OrderedDict
import ROOT

era=2018
name='tau_sf_pt-dm_DeepTau2017v2p1VSjet_%(era)s' % vars()
id='DeepTau2017v2p1VSjet'
description = "%(id)s SFs: By default, use the pT-dependent SFs with the 'pt' flag. For analyses that split events based on tau DM or using hadronic tau triggers, use the DM-dependent SFs with flag 'dm'." % vars()
inputs = [
{'name': "pt",       'type': "real",   'description': "Reconstructed tau pT"},
{'name': "dm",       'type': "int",    'description': "0, 1, 2, 10, 11"},
{'name': "genmatch", 'type': "int",    'description': "genmatch: 0 or 6 = unmatched or jet, 1 or 3 = electron, 2 or 4 = muon, 5 = real tau"},
{'name': "wp",       'type': "string", 'description': "DeepTau2017v2p1VSjet working point: VVVLoose-VVTight"},
{'name': "syst",     'type': "string", 'description': "Systematic 'nom', 'up', 'down'"}, # need to adjust this for the new systematics
{'name': "flag",     'type': "string", 'description': "Flag: 'pt' = pT-binned SFs, 'dm' = DM-binned SFs with fitted pT-dependence"},
]
output = {
    "name": "sf",
    "type": "real",
    "description": "%(id)s scale factor" % vars()
}

def GetBinEdges(wp,era):
  input_file='outputs/tauSF_Feb20_DMinclusive_%(wp)s/split_uncertainties.root' % vars()
  f=ROOT.TFile(input_file)
  hist_name='DMinclusive_%(era)s_hist' % vars()
  sf_hist=f.Get(hist_name)
  bin_edges=[]
  for i in range(1,sf_hist.GetNbinsX()+2):
    bin_edges.append(sf_hist.GetBinLowEdge(i))
  #bin_edges.append(20000.)
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

    err_stat_d=y-sf_graph_stat_err.GetErrorYhigh(i) 
    err_stat_u=y+sf_graph_stat_err.GetErrorYlow(i) 

    err_syst_alleras_d=y-sf_graph_syst_alleras_err.GetErrorYhigh(i)
    err_syst_alleras_u=y+sf_graph_syst_alleras_err.GetErrorYlow(i)
   
    err_syst_oneeras_d=y-sf_graph_syst_oneera_err.GetErrorYhigh(i)
    err_syst_oneeras_u=y+sf_graph_syst_oneera_err.GetErrorYlow(i) 

    #sf_pt.append((bin_low, y, (err_stat_u,err_stat_d), (err_syst_alleras_u, err_syst_alleras_d), (err_syst_oneeras_u, err_syst_oneeras_d)))
    sf_pt[int(bin_low)] = (y, (err_stat_u,err_stat_d), (err_syst_alleras_u, err_syst_alleras_d), (err_syst_oneeras_u, err_syst_oneeras_d))

  #sf_pt = sorted(sf_pt)

  #for x in sf_pt: print x, sf_pt[x]
  return sf_pt

GetPTdependentData('tight',era)

def maketiddata_pt(era,wps=['Tight']):
  """Construct tau ID data block."""
  #x=GetPTdependentData('tight','2018')
  # get bin edges - same binning is used for all WPs so just determine these once for the tight WP 
  ptbins=GetBinEdges('tight',era)
  # store SFs and uncertainty variations into a dictionary
  sfs={wp: GetPTdependentData(wp.lower(),era) for wp in wps}
#  tiddata=OrderedDict()
#  tiddata['nodetype'] = 'category' # category:genmatch
#  tiddata['input'] = 'genmatch' # category:genmatch
#  tiddata['content'] = []

  tiddata = OrderedDict([ # category:genmatch -> category:wp -> binning:pt -> category:syst
    ('nodetype', 'category'), # category:genmatch
    ('input', "genmatch"),
    #'default': 1.0, # no default: throw error if unrecognized genmatch
    ('content', [
      { 'key': 0, 'value': 1.0 }, # j  -> tau_h fake
      { 'key': 1, 'value': 1.0 }, # e  -> tau_h fake
      { 'key': 2, 'value': 1.0 }, # mu -> tau_h fake
      { 'key': 3, 'value': 1.0 }, # e  -> tau_h fake
      { 'key': 4, 'value': 1.0 }, # mu -> tau_h fake
      {'key': 5,  # real tau_h
        'value': OrderedDict([
          ('nodetype','binning'),
          ('input','pt'),
          ('edges', ptbins),
          ('flow', 'clamp'),
          ('content',[
             OrderedDict([])
           for pt in ptbins]
          ), 
        ]),
      }, 
      ###  OrderedDict([('value',[ 
     #     'nodetype': 'category', # category:wp
     #     'input': "wp",
     #     #'default': 1.0, # no default: throw error if unrecognized WP
     #     'content': [ # key:wp
     #       { 'key': wp,
     #         'value': {
     #           'nodetype': 'binning', # binning:pt
     #           'input': "pt",
     #           'edges': ptbins,
     #           'flow': "clamp",
     #           'content': [ # bin:pt
     #             { 'nodetype': 'category', # syst
     #               'input': "syst",
     #               'content': [
     #                 { 'key': 'nom',  'value': sfs[wp][pt][0]  },
     #                 #{ 'key': 'nom',  'value': maketid(sf,pt,'nom')  },
     #                 #{ 'key': 'up',   'value': maketid(sf,pt,'up')   },
     #                 #{ 'key': 'down', 'value': maketid(sf,pt,'down') },
     #               ]
     #             } for pt in ptbins[:-1] # loop over pT bins
     #           ] # bin:pt
     #         } # binning:pt
     #       } for wp in wps
     #     ] # key:wp
     #   } # category:wp
      ###  ])])
      #},
      { 'key': 6, 'value': 1.0 }, # j  -> tau_h fake
    ])
  ])
  return tiddata

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
json_object = json.dumps(dictionary, indent=2)

 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
