# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 10:35:34 2012

@author: bernd
"""
import numpy
import ROOT
import os
import sys
import array
import pathfinder

from convert_sis3302_files import WFConvert





ROOT.gSystem.Load(pathfinder.libPyOrcaROOT)
ROOT.gSystem.Load(pathfinder.libWaveWaveBase)

class orcadatamanipulation(object):
    def __init__(self, orcafile='', rootfile='', channelnum=0, numtriggers=1):
        """
        functions to transform Orca files to root) or ascii(averaged) files  
        """
        self.orcafile=str(pathfinder.OrcaFileFolder)+'/'+orcafile
        self.channelnum=channelnum
        self.rootfile=pathfinder.ROOTFileFolder+rootfile
        self.numtriggers=numtriggers
        ROOT.gSystem.Load(pathfinder.libWaveWaveBase)
        self.rootfilefolder=pathfinder.ROOTFileFolder
	self.orcafilefolder=pathfinder.OrcaFileFolder
	self.npyfilefolder=pathfinder.NpyFileFolder
	self.index=self.orcafile.rfind("/",0,len(self.orcafile))
        #self.txtfilepath=self.orcafile[0:self.index+1]
	#self.txtfilepath="/Users/nedmdaq/Desktop/Data/Txtified/"
	self.txtfilefolder=pathfinder.TxtFileFolder
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
	if self.orcafile:
		print 'this file is used:'
		print self.orcafile
	else:
		print "no orcafile loaded"
		return
	reader.AddFileToProcess(str(self.orcafile))
        mgr = ROOT.ORDataProcManager(reader)
#        fw = ROOT.ORFileWriter('/Users/nedmdaq/Desktop/Data/Rootified/pref')
	fw = ROOT.ORFileWriter(self.rootfilefolder+"pref")
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
        self.rootfile=self.rootfilefolder+"pref_"+runnumber+".root"
        print self.rootfile


    def draw_all_counts(self, event=None):
	if self.channelnum and self.numtriggers:
		event=self.channelnum+8*self.numtriggers
	else:
		event=None
	if self.rootfile:
		print "this rootfile is used: "+self.rootfile
	else:
		if self.orcafile:
			self.rooter()
			print "orcafile used: "+self.orcafile
		else:
			print "no file loaded"
			return	
	self.feil=ROOT.TFile(self.rootfile)
	self.feil.Get('sisDec')
        if event:
            self.feil.sisDec.GetEntry(event)
            self.feil.sisDec.wf.GimmeHist().Draw()
            raw_input("jump ma die leider weider")
        else:    
            #for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
	    n=self.channelnum
	    while self.feil.sisDec.GetEntry(n):

                self.feil.sisDec.GetEntry(n)
                self.feil.sisDec.wf.GimmeHist().Draw()
                raw_input("jump ma die leider weider")
	        n=n+8
    def numpyfy(self, event=None):
	"""
	save counts as numpy arrays
	"""
	if self.rootfile:
		print "this rootfile is used: "+self.rootfile
	else:
		if self.orcafile:
			self.rooter()
			print "orcafile used: "+self.orcafile
		else:
			print "no file loaded"
			return	
	if self.channelnum and self.numtriggers!=None:
		event=self.channelnum+8*self.numtriggers
	else: 
		event=None
	feil=ROOT.TFile(self.rootfile)
	feil.Get('sisDec')
	index=self.rootfile.rfind("_",0,len(self.rootfile))
	run=self.rootfile[index+1:len(self.rootfile)].lower()[0:-5]
        run.lower()
	
	print "event:"
	print event

        if event != None:
	        feil.sisDec.GetEntry(event)
	        FILE=self.npyfilefolder+run+"count"+str(event)
		arr=numpy.array(feil.sisDec.wf,dtype="int16")
		numpy.save(FILE,arr)
	else:            
           # for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
	    n=self.channelnum
	    while feil.sisDec.GetEntry(n):
		feil.sisDec.GetEntry(n)
		FILE=self.npyfilefolder+run+"count"+str(n)
	  	arr=numpy.array(feil.sisDec.wf,dtype="int16")
		numpy.save(FILE,arr)
		n=n+8
		print arr.dtype
	print "done"
    def txtify(self, averages=10, event=None):
        """
        save each count to a .txt file 
        """
#	if orcafile:
#		run=self.orcafile[self.index+1:len(self.orcafile)]
	if self.rootfile:
		print "this rootfile is used: "+self.rootfile
	else:
		if self.orcafile:
			self.rooter()
			print "orcafile used: "+self.orcafile
		else:
			print "no file loaded"
			return	
	if self.channelnum and self.numtriggers:
		event=channelnum+8*numtriggers
	else: 
		event=None
	feil=ROOT.TFile(self.rootfile)
	feil.Get('sisDec')
	index=self.rootfile.rfind("_",0,len(self.rootfile))
	run=self.rootfile[index+1:len(self.rootfile)].lower()[0:-5]
        run.lower()

#        if event:
#	        feil.sisDec.GetEntry(event)
#	        feil.sisDec.GetEntry(event)
#        if event:
#	        feil.sisDec.GetEntry(event)
#	feil.Get('sisDec')

        if event:
	        feil.sisDec.GetEntry(event)
	        FILE=open(self.txtfilefolder+run+"count"+str(event)+".txt","w")
	        data=feil.sisDec.wf.GetData()
	        for i in range(0,feil.sisDec.wf.GetLength(),averages):
			avg=0
			for j in range (averages):
				avg=avg+data.__getitem__(i+j)
		        FILE.write(str(avg/averages)+"\n")
	        FILE.close()
        else:            
		
           # for n in range(self.channelnum, self.channelnum*8+self.numtriggers*8, 8):
	    n=self.channelnum
	    while feil.sisDec.GetEntry(n):
		    feil.sisDec.GetEntry(n)
	            FILE=open(self.txtfilefolder+run+"count"+str(n)+".txt","w")
    	            data=feil.sisDec.wf.GetData()
	            for i in range(0,feil.sisDec.wf.GetLength(),averages):
			avg=0
			for j in range (averages):
				avg=avg+data.__getitem__(i+j)
		        FILE.write(str(avg/averages)+"\n")
	            FILE.close()
		    n=n+8
