import os
import sys
import ROOT
import argparse

parser = argparse.ArgumentParser(description="Submit jobs for VVV analysis")
parser.add_argument('-I' , '--InputROOTFile'    , dest='InputROOTFile'  , help='Input ROOTFile'     , type=str,                default=None                         )
parser.add_argument('-O' , '--OutputROOTFile'    , dest='OutputROOTFile'  , help='Output ROOTFile'     , type=str,                default=None                         )
parser.add_argument('-d' , '--Data'      , dest='Data'    , help='data'                ,  default=False , action='store_true')
parser.add_argument('-m' , '--MC'      , dest='MC'    , help='MC'                ,  default=False , action='store_true')
args = parser.parse_args()


class Transfer_Tree:
    def __init__(self):
        self.Data = args.Data
        self.MC = args.MC

        if ( not (self.Data | self.MC) ) | (self.Data & self.MC) :
            sys.exit("data or mc is not defined or mc,data both defined")

        self.InputROOTFile = args.InputROOTFile
        self.OutputROOTFile = args.OutputROOTFile

        self.cut = " ( abs(Lep1fatJet2_LeptonPDGID) == 13 && Lep1fatJet2_HLT_IsoMu24 == 1 ) && Lep1fatJet2_LeptonPt > 30 && Lep1fatJet2_FatJet_pt > 200 && Lep1fatJet2_FatJet_pt_2 > 200 && Lep1fatJet2_FatJet_msoftdrop > 40 && Lep1fatJet2_FatJet_msoftdrop_2 > 40 && nb_m_deep_in == 0 "

        self.TreeInName = "t"
        self.TreeOutName = "t"
        
        self.Intime_py_list = [
            "weight.py",
            "Events_Level.py",
            "AK8.py",
            "leptonic_W.py",
            "bJet.py",
            "Genparticle_matching.py",
        ]
        self.Intime_py_list = ["config/Intime/"+i for i in self.Intime_py_list]

        if self.Data : 
            self.Intime_Add_Variables = []
            self.OutColumn = {

            }
        if self.MC : 
            self.Intime_Add_Variables = [
                "weight",
                "ST", "MJJlv", "HT",
                "Lep1fatJet2_FatJet_particleNetMD_WvsQCD", "Lep1fatJet2_FatJet_tau21","Lep1fatJet2_FatJet_particleNetMD_WvsQCD_2","Lep1fatJet2_FatJet_tau21_2",
                "Lep1fatJet2_LeptonicWPt_2",
                "nb_l_deep_ex","nb_m_deep_ex","nb_t_deep_ex","nb_l_deep_in","nb_m_deep_in","nb_t_deep_in",
                "matching",
            ]
            self.OutColumn = []
            with open("Tool/Transfer_Tree/OutColumn.py","r") as f:
                exec(f.read())
            self.OutColumn = set(self.OutColumn)


    def PrintInfo(self):
        if self.Data:
            print "Data"
        if self.MC:
            print "MC"
        print self.cut
        print self.InputROOTFile
        print self.OutputROOTFile
        print "Intime_Add_Variables:\n",self.Intime_Add_Variables
        print "OutColumn:\n",self.OutColumn

    def Add_New_Column(self):

        for Intime_py in self.Intime_py_list:
            with open(Intime_py,"r") as f:
                exec(f.read())
        
        df = ROOT.RDataFrame( self.TreeInName, self.InputROOTFile )

        if self.Intime_Add_Variables:
            for iselection in self.Intime_Add_Variables:
                df = df.Define(   iselection ,eval(iselection) )

        df = df.Filter( self.cut )

        df.Snapshot(self.TreeOutName, self.OutputROOTFile, self.OutColumn )

Instance_Transfer_Tree = Transfer_Tree( )
Instance_Transfer_Tree.PrintInfo()
Instance_Transfer_Tree.Add_New_Column()

