import ROOT
import sys
import array
import pathfinder

ROOT.gSystem.Load(pathfinder.libPyOrcaROOT)
ROOT.gSystem.Load(pathfinder.libWaveWaveBase)

class WFConvert(ROOT.ORPyTreeWriter):
    def __init__(self, dec, treeName):
        ROOT.ORPyTreeWriter.__init__(self, dec, treeName)
        self.fEventTime = array.array('d', [0.]) 
        self.fCrate = array.array('h', [0])
        self.fCard = array.array('h', [0]) 
        self.fChannel = array.array('h', [0])
        self.fEnergy = array.array('L', [0])
        self.fFlags = array.array('L', [0])
        self.Clear()
        self.fTheWaveform = ROOT.TUShortWaveform()
        self.DoNotAutoFillTree()

    def Clear(self):
        self.fEventTime[0] = 0
        self.fCrate[0] = 0
        self.fCard[0] = 0
        self.fChannel[0] = 0
        self.fEnergy[0] = 0 
        self.fFlags[0] = 0 
   
    def InitializeBranches(self):
        t = self.GetTree()
        t.Branch("eventTime", self.fEventTime, "eventTime/D")
        t.Branch("crate", self.fCrate, "crate/s")
        t.Branch("card", self.fCard, "card/s")
        t.Branch("channel", self.fChannel, "channel/s")
        t.Branch("energy", self.fEnergy, "energy/i")
        t.Branch("flags", self.fFlags, "flags/i")
        t.Branch("wf", self.fTheWaveform)
        return self.kSuccess

    def ProcessMyDataRecord(self, record):
        ed = self.GetDecoder()
        if ed is None:
            print "No decoder defined!"
            return self.kFailure
        if not ed.SetDataRecord(record): return self.kFailure
        self.fCrate[0] = ed.CrateOf()
        self.fCard[0] = ed.CardOf()
        for i in range(ed.GetNumberOfEvents()):
            self.fEventTime[0] = ed.GetEventTime(i)
            self.fChannel[0] = ed.GetEventChannel(i)
            self.fEnergy[0] = ed.GetEventEnergy(i)
            self.fFlags[0] = ed.GetEventFlags(i)
            self.fTheWaveform.SetLength(ed.GetEventWaveformLength(i))
            self.fTheWaveform.SetSamplingFreq(ed.GetSamplingFrequency()/ROOT.TMath.Power(2, ed.GetAveragingForChannel(self.fChannel[0])))
            ed.CopyWaveformData(self.fTheWaveform.GetData(), self.fTheWaveform.GetLength())
            self.GetTree().Fill()
        return self.kSuccess

def main(inputs):
    reader = ROOT.ORFileReader()
    for afile in inputs[1:]: reader.AddFileToProcess(afile)

    mgr = ROOT.ORDataProcManager(reader)
    fw = ROOT.ORFileWriter("adcTest")
    run_notes = ROOT.ORRunNotesProcessor()
    xycom = ROOT.ORXYCom564Decoder()
    rdTree = ROOT.ORBasicRDTreeWriter(xycom, "xyCom")

    sisGen = ROOT.ORSIS3302GenericDecoder()
    wf = WFConvert(sisGen, "sisDec") 
    mgr.AddProcessor(fw)
    mgr.AddProcessor(run_notes)
    mgr.AddProcessor(wf)

    mgr.ProcessDataStream()

if __name__ == "__main__":
    main(sys.argv)
