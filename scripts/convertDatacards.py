# this script take a datacard containing 2D histogram of vs pT vs mass and splits them into several 1D histograms of mass stored in seperate directories

import ROOT
import argparse
import os
import numpy as np
ROOT.TH1.AddDirectory(False)

bins=[20.,25.,30.,35.,40.,50.,60.,80.,100.,200.]

def WriteToTFile(obj, file, path):
    '''Writes an object to a root file in the given path. If the directory does not exist it is created.'''
    file.cd()
    as_vec = path.split('/')
    if len(as_vec) >= 1:
        for i in xrange(0, len(as_vec)-1):
            if not ROOT.gDirectory.GetDirectory(as_vec[i]):
                ROOT.gDirectory.mkdir(as_vec[i])
            ROOT.gDirectory.cd(as_vec[i])
    if not ROOT.gDirectory.FindKey(as_vec[-1]):
        obj.SetName(as_vec[-1])
        ROOT.gDirectory.WriteTObject(obj, as_vec[-1])
    ROOT.gDirectory.cd('/')

def splitHistogramsAndWriteToFile(infile,outfile,dirname):
    '''Split 2D histogram in bins of pT and m_vis into several 1D histograms in bins of m_vis'''
    directory = infile.Get(dirname)
    for key in directory.GetListOfKeys():
        name=key.GetName()
        histo = directory.Get(name)
        if isinstance(histo, ROOT.TH2):
            for i, b_lo in enumerate(bins[:-1]):
              b_hi = bins[i+1] 
              y1 = histo.GetYaxis().FindBin(b_lo)
              y2 = histo.GetYaxis().FindBin(b_hi)-1
              hnew = histo.ProjectionX(histo.GetName(),y1,y2)
              newdirname = '%s_pT_%i_to_%i' % (dirname, int(b_lo), int(b_hi))
              WriteToTFile(hnew, outfile, newdirname+"/"+name)

def findAvepT(infile,dirname):
    '''Find the average pT of the tau in each pT bin'''
    directory = infile.Get(dirname)
    name='ZTT'
    histo = directory.Get(name).Clone()
    histo.Add(directory.Get('TTT').Clone()) 
    histo.Add(directory.Get('VVT').Clone()) 
    if isinstance(histo, ROOT.TH2):
        bin_means = []
        for i, b_lo in enumerate(bins[:-1]):
          b_hi = bins[i+1]
          histo.GetYaxis().SetRangeUser(b_lo,b_hi)
          #print 'pT bin %i-%i, mean pT = %.1f' % (b_lo, b_hi, histo.GetMean(2))
          bin_means.append(round(histo.GetMean(2),1))
        print(bin_means)
parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', help= 'File from which subdirectories need to be dropped')
args = parser.parse_args()
filename = args.file

if 'pt_2_vs_m_vis' not in filename: raise Exception('ERROR: your input file does not appear to have the correct naming') 
newfilename=filename.replace('pt_2_vs_m_vis','m_vis')

original_file = ROOT.TFile(filename)
output_file   = ROOT.TFile(newfilename,"RECREATE")

for key in original_file.GetListOfKeys():
    if isinstance(original_file.Get(key.GetName()),ROOT.TDirectory):
        dirname=key.GetName()
        print('Converting histograms in directory: %s' % dirname)
        splitHistogramsAndWriteToFile(original_file,output_file,dirname)
        print('Finding mean pTs for directory: %s' % dirname)
        if 'Gt30' in dirname or 'method12' in dirname: continue
        findAvepT(original_file, dirname)
