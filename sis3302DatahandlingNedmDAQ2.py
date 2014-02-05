8# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 10:35:34 2012

@author: bernd
"""
import ROOT
import os
import sys
import array
sys.path.append('/Users/nedmdaq/software/Sis3302DatahandlingNedmDAQ2')
from convert_sis3302_filesNedmDAQ2 import WFConvert

#os.chdir('/Users/nedmdaq/Desktop/Data/Rootified')

ROOT.gSystem.Load(" ~/software/OrcaROOT/Bindings/libPyOrcaROOT")
ROOT.gSystem.Load("~/software/TWaveform/lib/libWaveWaveBase")

class orcadatamanipulation(object):
    def __init__(self, orcafile, rootfile, channelnum, numtriggers):
        """
        functions to transform Orca files to root or ascii(averaged) files  
        """
        self.orcafile=orcafile
        self.channelnum=channelnum
        self.rootfile=rootfile
        self.numtriggers=numtriggers
        ROOT.gSystem.Load("~/root/TWaveform/lib/libWaveWaveBase")
        self.rootfilefolder="/Users/nedmdaq/Desktop/Data/Rootified/"
        self.index=self.orcafile.rfind("/",0,len(self.orcafile))
        #self.txtfilepath=self.orcafile[0:self.index+1]
	self.txtfilepath="/Users/nedmdaq/Desktop/Data/Txtified/"
    def rootify(self):
	""" obsolete , use rooter """
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
    def rooter(self):
	reader = ROOT.ORFileReader()
        #for afile in self.orcafile: reader.AddFileToProcess(afile)
	reader.AddFileToProcess(self.orcafile)
	print self.orcafile
        mgr = ROOT.ORDataProcManager(reader)
        fw = ROOT.ORFileWriter('/Users/nedmdaq/Desktop/Data/Rootified/pref')
        run_notes = ROOT.ORRunNotesProcessor()
        xycom = ROOT.ORXYCom564Decoder()
        rdTree = ROOT.ORBasicRDTreeWriter(xycom, "xyCom")

        sisGen = ROOT.ORSIS3302GenericDecoder()
        wf = WFConvert(sisGen, "sisDec")
        mgr.AddProcessor(fw)
        mgr.AddProcessor(run_notes)
        mgr.AddProcessor(wf)

        mgr.ProcessDataStream()
        index=self.orcafile.rfind("/",0,len(self.orcafile))
        runnumber=self.orcafile[index+1:len(self.orcafile)].lower()
        runnumber.lower()
        self.rootfile=self.rootfilefolder+'pref_'+runnumber+".root"
        print self.rootfile


    def draw_all_counts(self, event=None):
        self.feil=ROOT.TFile(self.rootfile)
	self.feil.Get('sisDec')
        if event:
            self.feil.sisDec.GetEntry(event)
            self.feil.sisDec.wf.GimmeHist().Draw()
            raw_input("jump ma die leider weider")
        else:    
            for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
                self.feil.sisDec.GetEntry(n)
                self.feil.sisDec.wf.GimmeHist().Draw()
                raw_input("jump ma die leider weider")
    def txtify(self, event=None):
        """
        save each count to a .txt file 
        """
        feil=ROOT.TFile(self.rootfile)
	feil.Get('sisDec')
        run=self.orcafile[self.index+1:len(self.orcafile)]
        if event:
	        feil.sisDec.GetEntry(event)
	        FILE=open(self.txtfilepath+run+"count"+str(event)+".txt","w")
	        data=feil.sisDec.wf.GetData()
	        for i in range(0,feil.sisDec.wf.GetLength(),10):
			avg=0
			for j in range (10):
				avg=avg+data.__getitem__(i+j)
		        FILE.write(str(avg/10)+"\n")
	        FILE.close()
        else:            

            for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
	            feil.sisDec.GetEntry(n)
	            FILE=open(self.txtfilepath+run+"count"+str(n)+".txt","w")
	            data=feil.sisDec.wf.GetData()
	            for i in range(0,feil.sisDec.wf.GetLength(),10):
                        avg=0
                        for j in range (10):
                                avg=avg+data.__getitem__(i+j)
                        FILE.write(str(avg/10)+"\n")
	            FILE.close()
