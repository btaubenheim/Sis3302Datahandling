8# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 10:35:34 2012

@author: bernd
"""
import ROOT
import os

class orcadatamanipulation(object):
    def __init__(self, orcafile, rootfile, channelnum, numtriggers):
        """
        run source ~/.bash_profile first
        """
        self.orcafile=orcafile
        self.channelnum=channelnum
        self.rootfile=rootfile
        self.numtriggers=numtriggers
        ROOT.gSystem.Load("~/root/TWaveform/lib/libWaveWaveBase")
        self.rootfilefolder="/home/bernd/Dropbox/EXC_BerndShare/AnalyzeThis/greta_MarkIV_"#rootify doesnt yet save .root files
        self.index=self.orcafile.rfind("/",0,len(self.orcafile))
        self.txtfilepath=self.orcafile[0:self.index+1]
    def rootify(self):
       # os.system("export ROOTSYS=/home/bernd/Desktop/bernd/root/root")
        #os.system("export PYTHONPATH=${ROOTSYS}/lib")
        #os.system("export LD_LIBRARY_PATH=${ROOTSYS}/lib:${LD_LIBRARY_PATH}")
        #os.system("export LD_LIBRARY_PATH=/home/bernd/root/TWaveform/lib:${LD_LIBRARY_PATH}")
        #os.system("export LD_LIBRARY_PATH=/home/bernd/root/OrcaROOT/lib:${LD_LIBRARY_PATH}")
        #os.export("export PATH=${ROOTSYS}/bin:${PATH}")
        os.system("/home/bernd/Dropbox/EXC_BerndShare/AnalyzeThis/orcaroot_WF "+self.orcafile)
        index=self.orcafile.rfind("/",0,len(self.orcafile))
        runnumber=self.orcafile[index+1:len(self.orcafile)].lower()
        runnumber.lower()
        self.rootfile=self.rootfilefolder+runnumber+".root"
        print self.rootfile
    def draw_all_counts(self, event=None):
        file=ROOT.TFile(self.rootfile)
        if event:
            file.sisDec.GetEntry(event)
            file.sisDec.Waveform.GimmeHist().Draw()
            raw_input("jump ma die leider weider")
        else:    
            for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
                file.sisDec.GetEntry(n)
                file.sisDec.Waveform.GimmeHist().Draw()
                raw_input("jump ma die leider weider")
    def txtify(self, event=None):
        """
        save each count to a .txt file 
        """
        file=ROOT.TFile(self.rootfile)
        run=self.orcafile[self.index+1:len(self.orcafile)]
        if event:
	        file.sisDec.GetEntry(event)
	        FILE=open(self.txtfilepath+run+"count"+str(event)+".txt","w")
	        data=file.sisDec.Waveform.GetData()
	        for i in range(0,file.sisDec.Waveform.GetLength(),10):
		        FILE.write(str(data.__getitem__(i))+"\n")
	        FILE.close()
        else:            

            for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
	            file.sisDec.GetEntry(n)
	            FILE=open(self.txtfilepath+run+"count"+str(n)+".txt","w")
	            data=file.sisDec.Waveform.GetData()
	            for i in range(0,file.sisDec.Waveform.GetLength(),10):
		            FILE.write(str(data.__getitem__(i))+"\n")
	            FILE.close()
