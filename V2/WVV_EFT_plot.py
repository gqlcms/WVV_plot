#!usr/bin/env python
import os
import glob
import math
import datetime
import array
import ROOT
import ntpath
import sys
import subprocess
from subprocess import Popen
from optparse   import OptionParser
from time       import gmtime, strftime
from array import array
from ROOT import gROOT, TPaveLabel, TPie, gStyle, gSystem, TGaxis, TStyle, TLatex, TString, TF1,TFile,TLine, TLegend, TH1D,TH2D,THStack, TGraph, TGraphErrors,TChain, TCanvas, TMatrixDSym, TMath, TText, TPad, TVectorD, RooFit, RooArgSet, RooArgList, RooArgSet, RooAbsData, RooAbsPdf, RooAddPdf, RooWorkspace, RooExtendPdf,RooCBShape, RooLandau, RooFFTConvPdf, RooGaussian, RooBifurGauss, RooArgusBG,RooDataSet, RooExponential,RooBreitWigner, RooVoigtian, RooNovosibirsk, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooChebychev, RooSimultaneous, RooGenericPdf,RooConstVar, RooKeysPdf, RooHistPdf, RooEffProd, RooProdPdf, TIter, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite

parser = OptionParser()
parser.add_option('--channel',    action="store",type="string",dest="channel"    ,default="had")
parser.add_option('--MODE',       action="store",type="string",dest="MODE"       ,default="MC" )
parser.add_option('--REGION',     action="store",type="string",dest="REGION"     ,default="PS" )
parser.add_option('--SFs',        action="store",type="int"   ,dest="SFs"        ,default=0    )
parser.add_option('--piechart',   action="store",type="int"   ,dest="piechart"   ,default=0    )
parser.add_option('--tau',        action="store",type="float" ,dest="tau"        ,default=0.4  )
parser.add_option('--y',          action="store",type="string",dest="y"          ,default="16,17,18")
parser.add_option('--FBT',        action="store",type="int"   ,dest="FBT"        ,default=0    )
parser.add_option('--standalone',        action="store",type="string"   ,dest="standalone"        ,default=None    )
(options, args) = parser.parse_args()

# ====================== for Limit =====================
# ====================== for Limit =====================
# ====================== for Limit =====================
def Prepare_DataCards(**kwargs):
    templete_card = kwargs.get("templete_card", None)
    keywords = kwargs.get("keywords", None)
    output_datacard = kwargs.get("output_datacard", None)
    with open(templete_card, "r") as f:
        content = f.read().format(**keywords)
        with open( output_datacard, "w" ) as fout:
            fout.write( content )


def Commands(**kwargs):
    templete_card = kwargs.get("templete_commands", None)
    keywords = kwargs.get("keywords", None)
    output_datacard = kwargs.get("output_scripts", None)
    with open(templete_card, "r") as f:
        content = f.read().format(**keywords)
        with open( output_datacard, "w" ) as fout:
            fout.write( content )


def Store_ROOTFile( **kwargs ):
    output_ROOTFile = kwargs.get("output_ROOTFile", "LimitsInput_had.root" )
    REGION = kwargs.get("REGION", None )
    variable = kwargs.get("variable", None )
    s1 = kwargs.get("signal1", None )
    s2 = kwargs.get("signal2", None )
    Infile = kwargs.get("Infile", None )

    if not REGION : print "REGION is not defined" ; return None
    if not variable : print "variable is not defined" ; return None
    if not s1 : print "signal1 is not defined" ; return None
    if not s2 : print "signal2 is not defined" ; return None
    if not Infile : print "Infile is not defined" ; return None

    signal1 = s1.split(";")[0] ; scale1 = float(s1.split(";")[1]) ; 
    signal2 = s2.split(";")[0] ; scale2 = float(s2.split(";")[1]) ; 

    hList = ["data","QCD","TTbar","WJets","STop","Rest","VV","Signal1c","Signal2c"]
    inf =ROOT.TFile(Infile)
    for i in hList:
        exec('h_%s = inf.Get("h_%s")'%(i,i))

    h_data_obs   = h_data.Clone("had_SR%s_%s_data_obs"%(REGION,variable)) 
    h_qcd   = h_QCD.Clone("had_SR%s_%s_qcd"%(REGION,variable)) 
    h_ttbar = h_TTbar.Clone("had_SR%s_%s_ttbar"%(REGION,variable)) 
    h_rest  = h_Rest.Clone("had_SR%s_%s_rest"%(REGION,variable)) ; h_rest.Add(h_WJets) ; h_rest.Add(h_STop) 
    h_Sig1 = h_Signal1c.Clone("had_SR%s_%s_%s"%(REGION,variable,signal1)) ; h_Sig1.Scale(1./scale1) 
    h_Sig2 = h_Signal2c.Clone("had_SR%s_%s_%s"%(REGION,variable,signal2)) ; h_Sig2.Scale(1./scale2) 
    
    # outf = ROOT.TFile( output_ROOTFile, "update")
    outf = ROOT.TFile( output_ROOTFile, "recreate")
    try:
        outf.mkdir( "R%s/signal_region"%(REGION) )
    finally:
        print output_ROOTFile, "exists"
    outf.cd( "R%s/signal_region"%(REGION) )

    h_data_obs.Write()
    h_qcd.Write()
    h_ttbar.Write()
    h_rest.Write()
    h_Sig1.Write()
    h_Sig2.Write()

    outf.Close()
    inf.Close()


def Prepare_1Region(**kwargs):
    variable = kwargs.get("variable", "MJJ")
    REGION = kwargs.get("REGION", "1")
    signal1 = kwargs.get("signal1", "gKK_2500_250;1")
    signal2 = kwargs.get("signal2", "gKK_3000_1500;1")
    LIMIT_CODEPATH = kwargs.get("LIMIT_CODEPATH", None)
    inf = kwargs.get("inf", None)
    sig = kwargs.get("sig", None)

    if not LIMIT_CODEPATH : print "LIMIT_CODEPATH is not defined" ; return None
    if not inf : print "inf is not defined" ; return None
    if not sig : print "sig is not defined" ; return None

    outtag          = inf.split("/")[-1].replace(".root","")
    outf            = inf.replace(".root","_limit.root")
    output_datacard = inf.replace(".root","_limit.txt")
    output_scripts  = inf.replace(".root","_limit.sh")
    LOG             = inf.replace(".root","_LimitLog.log")

    keywords_Commands = {
        "card":output_datacard,
        "signal":sig,
        "region":1,
        "LOG":LOG,
        "LIMIT_CODEPATH":LIMIT_CODEPATH,
    }

    keywords = {
        "REGION" : REGION,
        "ROOTFile" : outf,
        "whichsig" : sig,
        "variable" : variable,
    }

    Prepare_DataCards( templete_card = "Tool/limit/templete/templete.txt", keywords = keywords, output_datacard = output_datacard )
    Commands( templete_commands = "Tool/limit/templete/commands.sh", keywords = keywords_Commands, output_scripts = output_scripts )
    Store_ROOTFile( output_ROOTFile = outf, Infile = inf, REGION = REGION, variable = variable, signal1 = signal1, signal2 = signal2)

    os.system("sh "+output_scripts)

    with open(LOG,"r") as f:
        upper_Limit = []
        Lines = f.readlines()
        for i,Line in enumerate(Lines):
            if "-- AsymptoticLimits ( CLs ) --" in Line:
                upper_Limit = [j.replace("Expected ","").replace("\n","") for j in Lines[i+2:i+7]]
                upper_Limit = [(j.split("r < ")[0]+str(round(float(j.split("r < ")[-1].replace(" ","").replace("\n","")),2))) for j in upper_Limit]

    return (outtag,output_scripts,LOG,upper_Limit)
# ====================== for Limit =====================
# ====================== for Limit =====================
# ====================== for Limit =====================


def UnderOverFlow1D(h):
    Bins=h.GetNbinsX();
    h.SetBinContent( 1,  h.GetBinContent(1)+h.GetBinContent(0) );  h.SetBinError(   1,  math.sqrt( h.GetBinError(1)*h.GetBinError(1) + h.GetBinError(0)*h.GetBinError(0)) );
    h.SetBinContent( Bins,  h.GetBinContent(Bins)+h.GetBinContent(Bins+1) );  h.SetBinError(   Bins,  math.sqrt( h.GetBinError(Bins)*h.GetBinError(Bins) + h.GetBinError(Bins+1)*h.GetBinError(Bins+1)) );
    return h;

def Integerization(h):
    Bins=h.GetNbinsX();
    for i in range(1,Bins+1):
        if (h.GetBinContent(i)-int(h.GetBinContent(i)))>0.5 : value=int(h.GetBinContent(i))+1;
        else : value=int(h.GetBinContent(i));
        h.SetBinContent( i, value          );
        h.SetBinError(   i, math.sqrt(value) );
    return h;

def FBT_(total, h):
    Bins = h.GetNbinsX(); I = total.Integral();
    for i in range(1, Bins + 1):
        valTotal = total.GetBinContent(i); ErrorTotal = total.GetBinError(i); 
        if valTotal==0: continue;
        value = h.GetBinContent(i); Error = h.GetBinError(i);
        h.SetBinContent( i, value*(I/Bins)/valTotal );  h.SetBinError(   i, Error*(I/Bins)/valTotal );
    return h;

def OptimalCut(B,S):
    Bins = B.GetNbinsX(); B0=B.Integral(); S0=S.Integral(); SigMax=0; CutLocation_L=0; 
    LeftCutBin = 0; RightCutBin = 0; 
    CutLocation_R=0; BKGRejection=0; Sig_Eff=0;
    for RightEnd in range(1,Bins+1):
        for LeftEnd in range(1,RightEnd+1):            #print LeftEnd,RightEnd;
            sig = S.Integral( LeftEnd , RightEnd )/((B.Integral( LeftEnd , RightEnd )+1)**0.5);
            if sig>SigMax: 
                SigMax=sig; LeftCutBin=LeftEnd; RightCutBin=RightEnd; 
                BKGrjc  = float(round(100*(1-B.Integral(LeftEnd,RightEnd)/(B0+0.0001)),1) );
                Sig_Eff = float(round(100*S.Integral(LeftEnd,RightEnd)/(S0+0.0001)    ,1) );
                SigMax  = float(round(SigMax,1));
    ResultList = [ LeftCutBin , RightCutBin , S.GetBinLowEdge(LeftCutBin) , S.GetBinLowEdge(RightCutBin+1), str(BKGrjc), str(Sig_Eff), str(SigMax) ];   #print ResultList;
    return ResultList;  

def RationUnc(h_data,h_TotalMC,h_Ratio,MaxY):
    for i in range(1,h_Ratio.GetNbinsX()+1,1):
        D  = h_data.GetBinContent(i);    eD = h_data.GetBinError(i);
        if D==0: eD=0.92;
        B  = h_TotalMC.GetBinContent(i); eB = h_TotalMC.GetBinError(i);
        if B<0.1 and eB>=B : eB=0.92; Err= 0.;
        if B!=0.        :Err=TMath.Sqrt( (eD*eD)/(B*B)  +(D*D*eB*eB)/(B*B*B*B)     ); h_Ratio.SetBinContent(i, D/B   );  h_Ratio.SetBinError(i, Err); #print i,")",h_Ratio.GetNbinsX()+1,")   data:",D," pm ",eD,"     Bkg:",B," pm ",eB,"   R:",D/B," pm ", Err
        if B==0.        :Err=TMath.Sqrt( (eD*eD)/(eB*eB)+(D*D*eB*eB)/(eB*eB*eB*eB) ); h_Ratio.SetBinContent(i, D/0.92);  h_Ratio.SetBinError(i, Err);
        if D==0 and B==0:                                                             h_Ratio.SetBinContent(i, -1);      h_Ratio.SetBinError(i, 0  );
        if h_Ratio.GetBinContent(i)>MaxY:h_Ratio.SetBinContent(i,MaxY); ### To visualise the points above axis... #h_Ratio.Fit("pol1");
    return h_Ratio;



class ANALYSIS:
    def __init__(self, channel , fit_model="ErfExp_v1", fit_model_alter="ErfPow_v1", input_workspace=None):
        
        self.setTDRStyle();
        
        self.channel    =channel;

        self.color_palet={'data':1, 'QCD':2,  'Rest':62,  'VV':62, 'STop':8, 'TTbar':80, 'ZJets':6, 'WJets':90, 'Signal':1, 'Uncertainty':1, }
        
        # ================== signal scale ================== 
        # ================== signal scale ================== 
        self.Scale_Signal_Auto = False
        self.Signal_Scale1 = 10000
        self.Signal_Scale2 = 10000
        if options.MODE == "DECO":
            self.Signal_Scale1 = 1
            self.Signal_Scale2 = 1
        # ================== signal scale ================== 
        # ================== signal scale ================== 
        
        self.Optimal = True

        # ================ for decomposite ==================
        # ================ for decomposite ==================
        self.DECO_OnlySignal = False
        self.Signal_To_Draw = None
        self.Intime_Add_Variables = None
        self.DECO_py = "config/DECO.py"
        self.signal1_File = "_out_Res1ToRes2GluToGluVV_M1-2500_R-250.root" ; self.signal1_DECO_Label = "(2500, 250) GeV"
        self.signal2_File = "_out_Res1ToRes2GluToGluVV_M1-3000_R-1500.root"
        self.BKG_to_Draw = None
        # self.DECO_Matching = "deep-Wa_flip"
        self.DECO_Matching = "deep-W_a"
        self.DECO_Matching = "deep-W_c"

        self.Unit_Norm = False
        # ================ for decomposite ==================
        # ================ for decomposite ==================
        
        # PlotPath
        self.PlotPath = "/eos/user/q/qiguo/www/gKK/plots/MET_Study/"

        # ================ for store histogram =================
        # ================ for store histogram =================
        self.Histogram_ToStore = ["h_data","h_QCD","h_WJets","h_TTbar","h_STop","h_WWW","h_WWZ","h_WZZ","h_TotalMC","h_VV"]
        # ================ for store histogram =================
        # ================ for store histogram =================


        # =============== for Intime Compile =================
        # =============== for Intime Compile =================
        self.Intime_Add_selection_Variables = None
        self.KeepColumn = {"Pt_tag3","Pt_tag1", "MET_et", "Nj8", "weight"}
        self.Plot2DFaster = False
        self.Intime_py_list = [
            "weight.py",
            "Events_Level.py",
            "AK8.py",
            "leptonic_W.py",
            "bJet.py",
            "Genparticle_matching.py",
        ]
        self.Intime_py_list = ["config/Intime/"+i for i in self.Intime_py_list]
        self.MutiThreads = False
        # =============== for Intime Compile =================
        # =============== for Intime Compile =================


        # =============== add Text for significance ================
        # =============== add Text for significance ================
        self.AddText_ToEachBin = False
        self.Textsize = 1.0
        if self.AddText_ToEachBin:
            self.Pad_Split = 0.5
        # =============== add Text for significance ================
        # =============== add Text for significance ================

        # special pad setting
        self.Pad_Split = None

        self.plotsize = None

        # ============== setting for Limit ================
        # ============== setting for Limit ================
        self.Run_limit = False
        self.Signal_limit = "gKK_2500_250"
        self.LIMIT_CODEPATH = "/eos/user/q/qiguo/gKK/limit/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limit/"
        self.TextColor_limit = 4
        # ============== setting for Limit ================
        # ============== setting for Limit ================

        self.Draw_Data_2D = False

        self.Plotname = None

        if options.MODE in ["MC","MCvsDATA","DECO"] :
            self.DrawData = True
        if options.MODE in ["MC", "DECO"] :
            self.DrawData = False

        # ============= DECO ==============
        self.MODE = "MC"
        self.DECO = ["unmatching","qg","W"]
        self.DECO_Cut = {
            "W" : "1",
            "qg" : "1",
            "unmatching" : "1",
        }
        self.Fill_Style = {
            "W" : 1,
            # "W" : 3001,
            "qg" : 3023,
            "unmatching" : 3010,
        }
        self.Only_Show_Component = True
        self.color_DECO = {
            "W" : 80,
            "qg" : 2,
            "unmatching" : 19,
        }
        self.DECO_Label = {
            "W" : "W",
            "qg" : "qg",
            "unmatching" : "un",
        }
        # ============= DECO ==============
        

    def View_Selection_With_Plots(self,Text_Name1,variable,selection,comment,View_Selection_Only = True):
        Swith_Char = {};Swith_Char["<"] = "&lt;"; Swith_Char[">"] = "&gt;"; Variable_Style = "<aaa>"; selection_Style = "<aa>"; comment_Style = "<aaaa>"; Switch_Line_Number_variable = 50; Switch_Line_Number_selection = 100; Switch_Line_Number_comment = 80; Text_Content = "";

        for i in Swith_Char:
            variable.replace(i,Swith_Char[i])
            selection.replace(i,Swith_Char[i])

        variable_list = list(variable)
        selection_list = list(selection)
        comment_list = list(comment)
        for i in range(1,int(float(len(variable_list)/Switch_Line_Number_variable))+1):
            variable_list.insert(i*Switch_Line_Number_variable,"<br>")
        for i in range(1,int(float(len(selection_list)/Switch_Line_Number_selection))+1):
            selection_list.insert(i*Switch_Line_Number_selection,"<br>")
        for i in range(1,int(float(len(comment)/Switch_Line_Number_comment))+1):
            selection_list.insert(i*Switch_Line_Number_comment,"<br>")
        variable = ''.join(variable_list)
        selection = ''.join(selection_list)
        comment = ''.join(comment_list)

        Text_Content += Variable_Style + variable + Variable_Style + "<br>"
        Text_Content += comment_Style + comment + comment_Style + "<br>"
        Text_Content += selection_Style + selection + selection_Style

        if View_Selection_Only:
            Text_Content = selection_Style + selection + selection_Style

        with open(Text_Name1,"w") as f:
            f.write(Text_Content)

    #================ SETTINGS FOR Canvas/pads/histos and more ==================
    def setTDRStyle(self):
        self.tdrStyle =TStyle("tdrStyle","Style for P-TDR");  self.tdrStyle.SetCanvasBorderMode(0);        self.tdrStyle.SetCanvasColor(kWhite);        self.tdrStyle.SetCanvasDefH(700);        self.tdrStyle.SetCanvasDefW(700);        self.tdrStyle.SetCanvasDefX(0);          self.tdrStyle.SetCanvasDefY(0);
        self.tdrStyle.SetPadBorderMode(0);             self.tdrStyle.SetPadColor(kWhite);        self.tdrStyle.SetPadGridX(False);        self.tdrStyle.SetPadGridY(False);        self.tdrStyle.SetGridColor(0);        self.tdrStyle.SetGridStyle(3);        self.tdrStyle.SetGridWidth(1);      
        self.tdrStyle.SetFrameBorderMode(0);        self.tdrStyle.SetFrameBorderSize(1);        self.tdrStyle.SetFrameFillColor(0);        self.tdrStyle.SetFrameFillStyle(0);        self.tdrStyle.SetFrameLineColor(1);        self.tdrStyle.SetFrameLineStyle(1);        self.tdrStyle.SetFrameLineWidth(1);
        self.tdrStyle.SetHistLineColor(1);        self.tdrStyle.SetHistLineStyle(0);        self.tdrStyle.SetHistLineWidth(1);        self.tdrStyle.SetEndErrorSize(2);              self.tdrStyle.SetMarkerStyle(20);      self.tdrStyle.SetErrorX(0.);
        self.tdrStyle.SetOptFit(1);        self.tdrStyle.SetFitFormat("5.4g");        self.tdrStyle.SetFuncColor(2);        self.tdrStyle.SetFuncStyle(1);        self.tdrStyle.SetFuncWidth(1);      self.tdrStyle.SetOptDate(0);      
        self.tdrStyle.SetOptFile(0); self.tdrStyle.SetOptStat(0); self.tdrStyle.SetStatColor(kWhite); self.tdrStyle.SetStatFont(42); self.tdrStyle.SetStatFontSize(0.025); self.tdrStyle.SetStatTextColor(1); self.tdrStyle.SetStatFormat("6.4g"); self.tdrStyle.SetStatBorderSize(1); self.tdrStyle.SetStatH(0.1); self.tdrStyle.SetStatW(0.15);
        self.tdrStyle.SetPadTopMargin(0.05);        self.tdrStyle.SetPadBottomMargin(0.13);        self.tdrStyle.SetPadLeftMargin(0.18);        self.tdrStyle.SetPadRightMargin(0.06);      
        self.tdrStyle.SetOptTitle(0);        self.tdrStyle.SetTitleFont(42);        self.tdrStyle.SetTitleColor(1);        self.tdrStyle.SetTitleTextColor(1);        self.tdrStyle.SetTitleFillColor(10);        self.tdrStyle.SetTitleFontSize(0.05);
        self.tdrStyle.SetTitleColor(1, "XYZ");        self.tdrStyle.SetTitleFont(42, "XYZ");        self.tdrStyle.SetTitleSize(0.06, "XYZ");  
        self.tdrStyle.SetTitleXOffset(0.8);        self.tdrStyle.SetTitleYOffset(0.8);      
        self.tdrStyle.SetLabelColor(1, "XYZ");        self.tdrStyle.SetLabelFont(42, "XYZ");        self.tdrStyle.SetLabelOffset(0.007, "XYZ");        self.tdrStyle.SetLabelSize(0.04, "XYZ");
        self.tdrStyle.SetAxisColor(1, "XYZ");        self.tdrStyle.SetStripDecimals(kTRUE);        self.tdrStyle.SetTickLength(0.03, "XYZ");        self.tdrStyle.SetNdivisions(510, "XYZ");        self.tdrStyle.SetPadTickX(1);       self.tdrStyle.SetPadTickY(1);      
        self.tdrStyle.SetOptLogx(0); self.tdrStyle.SetOptLogy(0); self.tdrStyle.SetOptLogz(0);
        self.tdrStyle.SetPaperSize(20.,20.); self.tdrStyle.cd();


    def DefineSelection_0lep(self):#==========[ 0lep REGIONS & SELECTION ]===========================================
        REGION=options.REGION; MODE=options.MODE;
        PS = "1"
        PS3 = "1"
        
        if self.MODE in ["MC","MCvsDATA","DECO"]: self.Make_Controlplots_for_0lep(eval(REGION),"","");

        # add by Qilong start
        if self.MODE == "2DPlot": 
            if options.standalone:
                with open(options.standalone,"r") as f:
                    exec(f.read())

    def Make_Controlplots_for_0lep(self,selection,selection2,tag,CR=0):
        REGION=options.REGION; Nj=234; MODE=options.MODE; logy=0; tag="";

        if self.MODE in ["MC","MCvsDATA","DECO"]: logy=0;
        if options.standalone:
            with open(options.standalone,"r") as f:
                exec(f.read())


    def construct_2Dplot(self, cut, variable,Xtitle,Ytitle,Xnbin,Xmin,Xmax,Ynbin,Ymin,Ymax, KeepColumn = None, Intime = False, tag = "", signal_sample ="mu_out_Res1ToRes2GluToGluVV_M1-2500_R-250.root", variable_bin = None ):

        for Intime_py in self.Intime_py_list:
            with open(Intime_py,"r") as f:
                exec(f.read())

        variable = list(variable) ; variablecopy = [variable[0],variable[1]];

        Xnbin_contour = 30; 
        Ynbin_contour = 30; 
        if not variable_bin:
                Bin = ("Plot2D",";%s;%s"%(Xtitle,Ytitle),Xnbin,Xmin,Xmax,Ynbin,Ymin,Ymax)
        if variable_bin:
            if variable_bin[0]:
                if not variable_bin[1]:
                    Xmin = variable_bin[0][0] ; Xmax = variable_bin[0][-1]; 
                    variable_bin[0] = array('d',variable_bin[0])
                    Bin = ("Plot2D",";%s;%s"%(Xtitle,Ytitle),(len(variable_bin[0])-1),variable_bin[0],Ynbin,Ymin,Ymax)
            if not variable_bin[0]:
                if variable_bin[1]:
                    Ymin = variable_bin[1][0] ; Ymax = variable_bin[1][-1]; 
                    variable_bin[1] = array('d',variable_bin[1])
                    Bin = ("Plot2D",";%s;%s"%(Xtitle,Ytitle),Xnbin,Xmin,Xmax,(len(variable_bin[1])-1),variable_bin[1])
            if variable_bin[0]:
                if variable_bin[1]:
                    Xmin = variable_bin[0][0] ; Xmax = variable_bin[0][-1]; 
                    Ymin = variable_bin[1][0] ; Ymax = variable_bin[1][-1]; 
                    variable_bin[0] = array('d',variable_bin[0])
                    variable_bin[1] = array('d',variable_bin[1])
                    Bin = ("Plot2D",";%s;%s"%(Xtitle,Ytitle),(len(variable_bin[0])-1),variable_bin[0],(len(variable_bin[1])-1),variable_bin[1])
        
        # first parameter of each element need to be increase
        ContourLevel = [(0.2,ROOT.kWhite),(0.5,ROOT.kOrange),(0.9,ROOT.kRed)]
        # sort the ContourLevel in case this is not increase
        ContourLevel.sort(key = lambda a: a[0], reverse=False)        

        REGION = options.REGION

        if options.y=="17"      :path="/eos/user/y/yusong/qilong/NTuple_Output/17/all/Tree_9_24/mu";  lumi= 35.9;

        # prepare Input File
        if self.Draw_Data_2D:
            df_data  = ROOT.RDataFrame("PKUTree", path+"_out_data.root"                                 ) 
        df_QCD      = ROOT.RDataFrame("PKUTree", path+"_PKUTree_Rest.root"                               ) 
        df_WJets    = ROOT.RDataFrame("PKUTree", path+"_PKUTree_Rest.root"                             ) 
        df_TTbar    = ROOT.RDataFrame("PKUTree", path+"_PKUTree_Rest.root"                                ) 
        df_STop     = ROOT.RDataFrame("PKUTree", path+"_PKUTree_Rest.root"                                ) 
        df_Rest     = ROOT.RDataFrame("PKUTree", path+"_PKUTree_Rest.root"                              ) 
        # df_QCD      = ROOT.RDataFrame("PKUTree", path+"_PKUTree_QCD.root"                               ) 
        # df_WJets    = ROOT.RDataFrame("PKUTree", path+"_out_WJetsToQQ.root"                             ) 
        # df_TTbar    = ROOT.RDataFrame("PKUTree", path+"_PKUTree_TT.root"                                ) 
        # df_STop     = ROOT.RDataFrame("PKUTree", path+"_PKUTree_ST.root"                                ) 
        # df_Rest     = ROOT.RDataFrame("PKUTree", path+"_PKUTree_Rest.root"                              ) 
        df_Signal1  = ROOT.RDataFrame("PKUTree", path + self.signal1_File ) 
        df_Signal2  = ROOT.RDataFrame("PKUTree", path + self.signal2_File ) 
            
        if self.Intime_Add_Variables:
            for iselection in self.Intime_Add_Variables:
                if not self.DECO_OnlySignal:
                    if self.Draw_Data_2D:
                        df_data    = df_data.Define( iselection ,eval(iselection) )
                    df_QCD      = df_QCD.Define(   iselection ,eval(iselection) )
                    df_WJets    = df_WJets.Define( iselection ,eval(iselection) )
                    df_TTbar    = df_TTbar.Define( iselection ,eval(iselection) )
                    df_STop     = df_STop.Define(  iselection ,eval(iselection) )
                    df_Rest     = df_Rest.Define(  iselection ,eval(iselection) )
                df_Signal1     = df_Signal1.Define(  iselection ,eval(iselection) )
                df_Signal2     = df_Signal2.Define(  iselection ,eval(iselection) )
                

        # apply selection
        print "selection ==>", cut

        if Intime:
            # define variable for plot
            if variable[0] not in [str(i) for i in df_Signal1.GetColumnNames()]:
                if not self.DECO_OnlySignal:
                    if self.Draw_Data_2D:
                        df_data    = df_data.Define("Var1",eval(variable[0])) 
                    df_QCD     = df_QCD.Define("Var1",eval(variable[0]))
                    df_WJets   = df_WJets.Define("Var1",eval(variable[0]))
                    df_TTbar   = df_TTbar.Define("Var1",eval(variable[0]))
                    df_STop    = df_STop.Define("Var1",eval(variable[0]))
                    df_Rest    = df_Rest.Define("Var1",eval(variable[0]))
                df_Signal1 = df_Signal1.Define("Var1",eval(variable[0]))
                df_Signal2 = df_Signal2.Define("Var1",eval(variable[0]))
                variable[0] = "Var1"
            if variable[1] not in [str(i) for i in df_Signal1.GetColumnNames()]:
                if not self.DECO_OnlySignal:
                    if self.Draw_Data_2D:
                        df_data    = df_data.Define("Var2",eval(variable[1])) # variable[1] = "PtInbalcance"
                    df_QCD     = df_QCD.Define("Var2",eval(variable[1]))
                    df_WJets   = df_WJets.Define("Var2",eval(variable[1]))
                    df_TTbar   = df_TTbar.Define("Var2",eval(variable[1]))
                    df_STop    = df_STop.Define("Var2",eval(variable[1]))
                    df_Rest    = df_Rest.Define("Var2",eval(variable[1]))
                df_Signal1 = df_Signal1.Define("Var2",eval(variable[1]))
                df_Signal2 = df_Signal2.Define("Var2",eval(variable[1]))
                variable[1] = "Var2"
        else:
            if variable[0] not in [str(i) for i in df_Signal1.GetColumnNames()]:
                if not self.DECO_OnlySignal:
                    if self.Draw_Data_2D:
                        df_data    = df_data.Define("Var1","return (%s);"%(variable[0])) # variable[0] = "PtInbalcance"
                    df_QCD     = df_QCD.Define("Var1","return (%s);"%(variable[0]))
                    df_WJets   = df_WJets.Define("Var1","return (%s);"%(variable[0]))
                    df_TTbar   = df_TTbar.Define("Var1","return (%s);"%(variable[0]))
                    df_STop    = df_STop.Define("Var1","return (%s);"%(variable[0]))
                    df_Rest    = df_Rest.Define("Var1","return (%s);"%(variable[0]))
                df_Signal1 = df_Signal1.Define("Var1","return (%s);"%(variable[0]))
                df_Signal2 = df_Signal2.Define("Var1","return (%s);"%(variable[0]))
                variable[0] = "Var1"
            if variable[1] not in [str(i) for i in df_Signal1.GetColumnNames()]:
                if not self.DECO_OnlySignal:
                    if self.Draw_Data_2D:
                        df_data    = df_data.Define("Var2","return (%s);"%(variable[1])) # variable[1] = "PtInbalcance"
                    df_QCD     = df_QCD.Define("Var2","return (%s);"%(variable[1]))
                    df_WJets   = df_WJets.Define("Var2","return (%s);"%(variable[1]))
                    df_TTbar   = df_TTbar.Define("Var2","return (%s);"%(variable[1]))
                    df_STop    = df_STop.Define("Var2","return (%s);"%(variable[1]))
                    df_Rest    = df_Rest.Define("Var2","return (%s);"%(variable[1]))
                df_Signal1 = df_Signal1.Define("Var2","return (%s);"%(variable[1]))
                df_Signal2 = df_Signal2.Define("Var2","return (%s);"%(variable[1]))
                variable[1] = "Var2"

        canvas = ROOT.TCanvas("Canvas","Canvas", 700,700);
       
        weight = "weight"
        if self.Draw_Data_2D:
            h_data = df_data.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_data"); 
        h_QCD = df_QCD.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_QCD"); 
        h_WJets = df_WJets.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_WJets"); 
        h_TTbar = df_TTbar.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_TTbar"); 
        h_STop = df_STop.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_STop"); 
        h_Rest = df_Rest.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_Rest"); 
        h_Signal1 = df_Signal1.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_Signal1"); 
        h_Signal2 = df_Signal2.Filter(  cut).Histo2D(   Bin, variable[0], variable[1], "weight").GetValue().Clone("h_Signal2"); 
        Bin_contour = ("Plot2D",";%s;%s"%(Xtitle,Ytitle),Xnbin_contour,Xmin,Xmax,Ynbin_contour,Ymin,Ymax)
        h_Signal1_contour = df_Signal1.Filter(  cut).Histo2D(   Bin_contour, variable[0], variable[1], "weight").GetValue(); 


        h_TotalMC = h_QCD.Clone("h_TotalMC")
        h_TotalMC.Add(h_WJets)
        h_TotalMC.Add(h_TTbar)
        h_TotalMC.Add(h_STop)
        h_TotalMC.Add(h_Rest)

        h_Signal1_contour.SetStats(0) ; h_TotalMC.SetStats(0)
        h_Signal1_contour.Smooth()
            
        h_Signal1_contour.SetContour(1);
        maxZ = h_Signal1_contour.GetMaximum()
        h_List = []
        for i,j in enumerate(ContourLevel):
            exec('hc_{i} = h_Signal1_contour.Clone("hc_{i}")'.format(i = i))
            exec('hc_{i}.SetContourLevel(0,maxZ*ContourLevel[i][0])'.format(i = i))
            exec('hc_{i}.SetLineColor(ContourLevel[i][1])'.format(i = i))
            exec('h_List.append(hc_{i})'.format(i = i))

        h_TotalMC.Draw("COLZ")
        for i in h_List:
            i.Draw("same CONT3")

        theLeg = TLegend(0.68, 0.65, 0.9, 0.92, "", "NDC");theLeg.SetName("theLegend"); theLeg.SetBorderSize(0); theLeg.SetLineColor(0); theLeg.SetFillColor(0);theLeg.SetFillStyle(0); theLeg.SetLineWidth(0); theLeg.SetLineStyle(0); theLeg.SetTextFont(42);theLeg.SetTextSize(.04);
        theLeg.SetFillColor(0);theLeg.SetBorderSize(0);theLeg.SetLineColor(0);theLeg.SetLineWidth(0);theLeg.SetLineStyle(0);theLeg.SetTextFont(42);theLeg.SetNColumns(len(ContourLevel));
        for i,j in enumerate(ContourLevel):
            if i == (len(ContourLevel)-1):
                exec('theLeg.AddEntry( "hc_{i}" ," signal" ,"L")'.format(i = i))
            else:
                exec('theLeg.AddEntry( "hc_{i}" ,"" ,"L")'.format(i = i))
        theLeg.Draw("Same")

        for c in [".","/","(",")","[","]","*","+",">","<"," ","=",",","deep","dnn","Decorr","jetAK8puppi","ass_tag","t_tag","_tag"]:
            variable1=variablecopy[0].replace(c,"_")
            variable2=variablecopy[1].replace(c,"_")
        for c in ["__","___","____","_____","______","_"]:
            variable1=variable1.replace(c,"");
            variable2=variable2.replace(c,"");
        Name=self.PlotPath+REGION+"_"+variable1+"__"+variable2+"_"+tag+".png"

        output_ROOTFile = Name.replace(".png",".root") ; outf = ROOT.TFile( output_ROOTFile, "recreate")
        for h in self.Histogram_ToStore:
            try:
                if h == "h_Signal1":
                    hist = eval(h).Clone("h_Signal1c")
                    hist.Write()
                if h == "h_Signal2":
                    hist = eval(h).Clone("h_Signal2c")
                    hist.Write()
                else:
                    eval(h).Write()
            except NameError:
                print h,"not exist"
            else:
                pass
        outf.Close()

        canvas.SaveAs(Name)
        print "\n --> generate %s &"%(Name);

    # add by Qilong end
    

    def construct_plot(self,Nj,variable,cut,cut1,tag,nbin,min,max,xtitle="",ytitle="",logy=1,CR=0, Intime = False, variable_bin = None):
        
        SFs=options.SFs; channel=options.channel; MODE=options.MODE;  REGION=options.REGION; 
        print " -->  MODE:",MODE," variable:",variable,"\n       { "+cut+" }\n"

        with open("config/Input/InputFile_2016.py","r") as f:
            exec(f.read())

        #----------------- paths to root files -------------------
        if options.y=="16"      :path=self.path16;  lumi=36.3;
        # if options.y=="17"      :path="";  lumi= 41.5;
        #if options.y=="18"      :path="/eos/cms/store/user/.........;  lumi=59.7;
        #if options.y=="16,17,18":path="/eos/cms/store/user/.........;  lumi=138;

        #====== DEFINE CANVAS ==========================
        if self.MODE in ["MC","MCvsDATA","COMP"]:
            if self.plotsize:
                canvas_controlplot = TCanvas(REGION+"_"+variable, REGION+"_"+variable, self.plotsize[0],self.plotsize[1]);
            else:
                canvas_controlplot = TCanvas(REGION+"_"+variable, REGION+"_"+variable, 700,700);
            fPads1 = TPad("pad1", "", 0.0, 0.29, 1.00, 1.00);
            fPads2 = TPad("pad2", ""    , 0.0, 0.00, 1.00, 0.29);
            if self.Pad_Split:
                fPads1 = TPad("pad1", "", 0.0, self.Pad_Split, 1.00, 1.00);
                fPads2 = TPad("pad2", ""    , 0.0, 0.00, 1.00, self.Pad_Split);
            fPads1.SetBottomMargin(0.007);fPads1.SetLeftMargin( 0.10);fPads1.SetRightMargin( 0.03);
            fPads2.SetLeftMargin(  0.10 );fPads2.SetRightMargin(0.03);fPads2.SetBottomMargin(0.25);
            fPads1.Draw(); fPads2.Draw(); fPads1.cd()

        if self.MODE in ["DECO"]:
            if self.plotsize:
                canvas_controlplot = TCanvas(REGION+"_"+variable, REGION+"_"+variable, self.plotsize[0],self.plotsize[1]);
            else:
                canvas_controlplot = TCanvas(REGION+"_"+variable, REGION+"_"+variable, 700,565);
            canvas_controlplot.SetLeftMargin(0.1); canvas_controlplot.SetRightMargin(0.03);  


        #====================== DEFINE TREES AND HISTOS ======================================

        ROOT.EnableImplicitMT() # allow to use mutiple core

        for Intime_py in self.Intime_py_list:
            with open(Intime_py,"r") as f:
                exec(f.read())
        
        print "plot ===== > ",
        try:
            print eval(variable)
        except NameError:
            print variable

        df_data  = ROOT.RDataFrame("t", path+"Mu_data.root"  )
        for BKG in self.BKG_List:
            exec('df_%s  = ROOT.RDataFrame("t", path + self.InputFile["%s"]) '%( BKG,BKG))
        for signal in self.signal_List:
            exec('df_%s  = ROOT.RDataFrame("t", path + self.InputFile["%s"]) '%( signal,signal))

        
        
        if self.Intime_Add_Variables:
            for iselection in self.Intime_Add_Variables:
                for BKG in self.BKG_List:
                    exec('df_%s      = df_%s.Define(   iselection ,eval(iselection) )'%(BKG,BKG))
                for signal in self.signal_List:
                    exec('df_%s      = df_%s.Define(   iselection ,eval(iselection) )'%(signal,signal))
                if self.DrawData:
                    df_data      = df_data.Define(   iselection ,eval(iselection) )

        hstack_TotalMC= THStack("hstack_TotalMC","hstack_TotalMC"+";%s;%s"%(xtitle,ytitle));                
        hstack_TotalMC_DECO= THStack("hstack_TotalMC_DECO","hstack_TotalMC_DECO"+";%s;%s"%(xtitle,ytitle));                

        #=================== SET WEIGHTS, SCALE TREES, DEFINE TOTAL AND STACK  =================================================
        weight="weight";
        weight_data="weight_data";

        if not variable_bin:
            Bin = ("Plot",";%s;%s"%(xtitle,ytitle),nbin,min,max)
        if variable_bin:
            Bin = ("Plot",";%s;%s"%(xtitle,ytitle),(len(histo_bin)-1),histo_bin)


        for signal in self.signal_List:
                df = eval("df_%s"%(signal))
                exec('h_%s     = df_%s.Filter(    cut).Histo1D(Bin, variable, weight).GetValue().Clone("h_%s"    )'%(signal,signal,signal))
        if self.MODE in ["MC","MCvsDATA"]:
            for BKG in self.BKG_List:
                df = eval("df_%s"%(BKG))
                exec('h_%s     = df_%s.Filter(    cut).Histo1D(Bin, variable, weight).GetValue().Clone("h_%s"    )'%(BKG,BKG,BKG))
        if self.MODE in ["MCvsDATA"]:
            h_data     = df_data.Filter(    cut).Histo1D(Bin, variable, weight_data).GetValue().Clone("h_data"    )

        if self.MODE == "DECO":
            for BKG in self.BKG_List:
                df = eval("df_%s"%(BKG))
                for DECO in self.DECO:
                    exec('h_{BKG}_{DECO}     = df_{BKG}.Filter( self.DECO_Cut[DECO] ).Histo1D(Bin, variable, weight).GetValue().Clone("h_{BKG}_{DECO}"    )'.format( BKG = BKG, DECO = DECO ) )
            for BKG in self.BKG_List:
                for DECO in self.DECO:
                    if DECO == self.DECO[0]:
                        exec('h_%s = h_%s_%s.Clone("h_%s")'%(BKG,BKG,DECO,BKG))
                    else:
                        exec('h_%s.Add(h_%s_%s)'%(BKG,BKG,DECO))


        # ============= scale =============
        for BKG in self.BKG_List:
            exec('h_%s.Scale(lumi*self.XS["%s"]/float(self.NEvents["%s"]))'%(BKG,BKG,BKG))
        for signal in self.signal_List:
            exec('h_%s.Scale(lumi*self.XS["%s"]/float(self.NEvents["%s"]))'%(signal,signal,signal))

        if self.MODE == "DECO":
            for BKG in self.BKG_List:
                for DECO in self.DECO:
                    exec('h_{BKG}_{DECO}.Scale(lumi*self.XS["{BKG}"]/float(self.NEvents["{BKG}"]))'.format(BKG = BKG, DECO = DECO))
        
        # ============= Merge =============
        for mBKG in self.Merge_BKG_Dic:
            for BKG in self.Merge_BKG_Dic[mBKG]:
                if BKG == self.Merge_BKG_Dic[mBKG][0]:
                    exec('h_%s = h_%s.Clone("h_%s")'%(mBKG,BKG,mBKG))
                else:
                    exec('h_%s.Add(h_%s)'%(mBKG,BKG))

        if self.MODE == "DECO":
            for mBKG in self.Merge_BKG_Dic:
                for BKG in self.Merge_BKG_Dic[mBKG]:
                    for DECO in self.DECO:
                        if BKG == self.Merge_BKG_Dic[mBKG][0]:
                            exec('h_%s_%s = h_%s_%s.Clone("h_%s_%s")'%(mBKG,DECO,BKG,DECO,mBKG,DECO))
                        else:
                            exec('h_%s_%s.Add(h_%s_%s)'%(mBKG,DECO,BKG,DECO))


        # ============= UnderOverflow =============
        for h in self.Merge_BKG_Dic:
            exec('h_%s = UnderOverFlow1D(h_%s)'%(mBKG,mBKG))
        for signal in self.signal_List:
            exec('h_%s = UnderOverFlow1D(h_%s)'%(signal,signal))
        if self.MODE == "DECO":
            for h in self.Merge_BKG_Dic:
                for DECO in self.DECO:
                    exec('h_%s_%s = UnderOverFlow1D(h_%s_%s)'%(mBKG,DECO,mBKG,DECO))
        if self.DrawData:
            for h in [h_data] : h = UnderOverFlow1D(h)
        if self.DrawData:
            h_data.SetBinErrorOption(TH1D.kPoisson);

        # ============= Stack =============
        First = True
        for mBKG in self.Merge_BKG_Dic_order:
            if mBKG not in self.Merge_BKG_Dic: continue
            hstack_TotalMC.Add(eval('h_%s'%(mBKG)))
            if First:
                h_TotalMC = eval('h_%s'%(mBKG)).Clone('h_%s'%(mBKG))
                First = False
            else:
                h_TotalMC.Add(eval('h_%s'%(mBKG)))

        if self.MODE == "DECO":
            if self.Only_Show_Component:
                for DECO in self.DECO:
                    First = True
                    for mBKG in self.Merge_BKG_Dic_order:
                        if mBKG not in self.Merge_BKG_Dic: continue
                        if First:
                            exec('h_%s = h_%s_%s.Clone("h_%s")'%(DECO,mBKG,DECO,DECO))
                            First = False
                        else:
                            exec('h_%s.Add(h_%s_%s)'%(DECO,mBKG,DECO))
                    hstack_TotalMC_DECO.Add(eval('h_%s'%(DECO)))
            else:
                for DECO in self.DECO:
                    for mBKG in self.Merge_BKG_Dic_order:
                        if mBKG not in self.Merge_BKG_Dic: continue
                        hstack_TotalMC_DECO.Add(eval('h_%s_%s'%(mBKG,DECO)))

        # ============= Norm =============
        if self.DrawData:
            print "data:",h_data.Integral()
        print "TotalMC:",h_TotalMC.Integral()
        
        

        for signal in self.signal_List:
            if self.Signal_Scale[signal] == -1:
                self.Signal_Scale[signal] = float("%.1g"%(h_TotalMC.GetMaximum()/eval('h_%s'%(signal)).GetMaximum()))
            exec('h_%s.Scale(self.Signal_Scale["%s"])'%(signal,signal))

        if self.DrawData:
            norm=h_data.Integral()/(h_TotalMC.Integral()+0.00001); 
            print "  norm=",norm;

        if self.MODE in ["MC","MCvsDATA"]: #---------- histogram cosmetics ---------------------
            if self.DrawData:
                h_data.SetLineColor(self.color_palet["data"]); h_data.SetFillColor(self.color_palet["data"]);
            for signal in self.signal_List:
                exec('h_%s.SetLineColor(self.color_palet["%s"])'%(signal,signal))
                exec('h_%s.SetLineWidth(4)'%(signal))
                # exec('h_%s.SetFillColor(self.color_palet["%s"])'%(signal,signal))
            for mBKG in self.Merge_BKG_Dic:
                exec('h_%s.SetLineColor(0)'%(mBKG))
                exec('h_%s.SetLineWidth(0)'%(mBKG))
                exec('h_%s.SetFillColor(self.color_palet["%s"])'%(mBKG,mBKG))
            h_TotalMC.SetLineStyle(3); h_TotalMC.SetMarkerStyle(0); h_TotalMC.SetLineWidth(5); h_TotalMC.SetLineColor(15);

        if self.MODE == "DECO":
            h_TotalMC.SetLineStyle(3); h_TotalMC.SetMarkerStyle(0); h_TotalMC.SetLineWidth(5); h_TotalMC.SetLineColor(15);
            for signal in self.signal_List:
                    exec('h_%s.SetLineColor(self.color_palet["%s"])'%(signal,signal))
                    exec('h_%s.SetLineWidth(4)'%(signal))
            if self.Only_Show_Component:
                for DECO in self.DECO:
                    exec('h_%s.SetLineColor(0)'%(DECO))
                    exec('h_%s.SetLineWidth(0)'%(DECO))
                    exec('h_%s.SetFillColor(self.color_DECO["%s"])'%(DECO,DECO))
            else:
                for mBKG in self.Merge_BKG_Dic:
                    for DECO in self.DECO:
                        exec('h_%s_%s.SetLineColor(0)'%(mBKG,DECO))
                        exec('h_%s_%s.SetLineWidth(0)'%(mBKG,DECO))
                        exec('h_%s_%s.SetFillColor(self.color_palet["%s"])'%(mBKG,DECO,mBKG))
                        exec('h_%s_%s.SetFillStyle(self.Fill_Style["%s"])'%(mBKG,DECO,DECO))
        
        #============ DRAW TOP PAD =====================
        if self.MODE in ["MC"]:
            print "5"; 
            h_TotalMC.Draw("e"); h_TotalMC.GetXaxis().SetNdivisions(509);
            hstack_TotalMC.Draw("same HIST"); # For unc-bars
            h_TotalMC.Draw("same e"   ); 
            for signal in self.signal_List:
                exec('h_%s.Draw("same HIST")'%(signal))

        if self.MODE in ["MCvsDATA"]:
            h_TotalMC.Draw("e"); h_TotalMC.GetXaxis().SetNdivisions(509);   
            h_data.Draw("e same"); h_data.GetXaxis().SetNdivisions(509);
            hstack_TotalMC.Draw("same HIST"); # For unc-bars
            h_data.Draw("same e");  #!needed 2nd time to draw data
            h_TotalMC.Draw("same e"   );
            for signal in self.signal_List:
                exec('h_%s.Draw("same HIST")'%(signal))
            canvas_controlplot.Update(); 

        if self.MODE == "DECO":
            h_TotalMC.Draw("e"); h_TotalMC.GetXaxis().SetNdivisions(509);
            hstack_TotalMC_DECO.Draw("same HIST"); # For unc-bars
            h_TotalMC.Draw("same e"   ); 
            for signal in self.signal_List:
                exec('h_%s.Draw("same HIST")'%(signal))


        #---------------- Add text in top pad -----------------------
        banner          = TLatex(0.96,0.96,str(lumi)+" fb^{-1} (13 TeV)");   banner.SetNDC();   banner.SetTextSize(0.034);     banner.SetTextFont(42);    banner.SetTextAlign(31);    banner.SetLineWidth(2);    banner.Draw();
        CMS             = TLatex(0.22,0.96,"CMS"                        );      CMS.SetNDC();      CMS.SetTextSize(0.042);        CMS.SetTextFont(42);       CMS.SetTextAlign(31);       CMS.SetLineWidth(2);       CMS.Draw();
        if self.MODE=="MCvsData":
            Extratext   = TLatex(0.24,0.96,"Preliminary"                );Extratext.SetNDC();Extratext.SetTextSize(0.034);  Extratext.SetTextFont(52); Extratext.SetTextAlign(11); Extratext.SetLineWidth(2); Extratext.Draw();
        if self.MODE=="DECO" or MODE=="MC":
            Extratext   = TLatex(0.24,0.96,"Simulation"                 );Extratext.SetNDC();Extratext.SetTextSize(0.034);  Extratext.SetTextFont(52); Extratext.SetTextAlign(11); Extratext.SetLineWidth(2); Extratext.Draw();
        RegionTxt       = TLatex(0.15,0.88,"%s"%(REGION)                );RegionTxt.SetNDC();RegionTxt.SetTextSize(0.042);  RegionTxt.SetTextFont(42);    RegionTxt.SetLineWidth(2); RegionTxt.Draw();
        if self.MODE in ["MCvsDATA"]:
            D_o_MC_txt  = TLatex(0.15,0.83,"Data / MC = %.2f"%(norm)    );D_o_MC_txt.SetNDC();D_o_MC_txt.SetTextSize(0.042);D_o_MC_txt.SetTextFont(42);   D_o_MC_txt.SetLineWidth(2);D_o_MC_txt.Draw();
        if SFs :
            SFsCorr     = TLatex(0.55, 0.96, "SFs corrected"            );   SFsCorr.SetNDC();   SFsCorr.SetTextSize(0.034);   SFsCorr.SetTextFont(52);   SFsCorr.SetTextAlign(11);   SFsCorr.SetLineWidth(2);   SFsCorr.Draw();
        #canvas_controlplot.Update(); 


        #========== DRAW BOTTOM PAD ============================================
        if self.MODE in ["MCvsDATA"]: #--------- Data / MC on 2nd pad ---------------------
            fPads2.cd(); 
            h_Ratio = h_data.Clone("h_Ratio"); h_Ratio.Divide( h_TotalMC ); MaxY=2; #TMath.Max( 2,  TMath.Min(3,h_Ratio.GetMaximum()*1.1) );
            h_Ratio.SetLineColor(1); h_Ratio.SetLineWidth(2); h_Ratio.SetMarkerStyle(8); h_Ratio.SetMarkerSize(0.7); h_Ratio.GetYaxis().SetRangeUser( 0 , MaxY );  h_Ratio.GetYaxis().SetNdivisions(504,0);
            h_Ratio.GetYaxis().SetTitle("Data / MC  ");  h_Ratio.GetYaxis().SetTitleOffset(0.35);  h_Ratio.GetYaxis().SetTitleSize(0.13);  h_Ratio.GetYaxis().SetTitleSize(0.13);  h_Ratio.GetYaxis().SetLabelSize(0.11); h_Ratio.GetXaxis().SetLabelSize(0.1); h_Ratio.GetXaxis().SetTitleOffset(0.7); h_Ratio.GetXaxis().SetTitleSize(0.14); 
            axis1=TGaxis( min,1,max,1, 0,0,0, "L"); axis1.SetLineColor(1); axis1.SetLineWidth(1);  #axis1->SetLabelColor(16); #fPads2.SetGridx(); #fPads2.SetGridy();
            h_Ratio=RationUnc(h_data,h_TotalMC,h_Ratio,MaxY);
            h_Ratio.Draw("e0"); axis1.Draw();
            fPads2.RedrawAxis(); fPads2.Update();
            fPads1.RedrawAxis(); fPads1.Update();

        if self.MODE in ["MC"]:  #--------- Significances on 2nd pad ---------------------
            fPads2.cd();  fPads2.SetLogy(); MaxY=7;
            axis2=TGaxis( min,2,max,2, 0,0,0, "L"); axis2.SetLineColor(2); axis2.SetLineWidth(1);
            axis3=TGaxis( min,5,max,5, 0,0,0, "L"); axis3.SetLineColor(3); axis3.SetLineWidth(1);
            #-------- build denominator of significance ------------
            MaxY = 0
            for signal in self.signal_List:
                exec('h_Signif_{signal} = self.Significance_Histogram(h_{signal}, h_TotalMC,"h_Signif_{signal}")'.format(signal = signal))
                eval('h_Signif_{signal}'.format(signal = signal)).GetYaxis().SetTitle("significance")
                eval('h_Signif_{signal}'.format(signal = signal)).GetYaxis().SetTitleOffset(0.38)
                eval('h_Signif_{signal}'.format(signal = signal)).GetYaxis().SetTitleSize(0.13)
                eval('h_Signif_{signal}'.format(signal = signal)).GetYaxis().SetLabelSize(0.11)
                eval('h_Signif_{signal}'.format(signal = signal)).GetYaxis().SetLabelSize(0.1)
                eval('h_Signif_{signal}'.format(signal = signal)).GetXaxis().SetTitleOffset(0.7)
                eval('h_Signif_{signal}'.format(signal = signal)).GetXaxis().SetTitleSize(0.14)
                MaxY = TMath.Max(MaxY, eval('h_Signif_{signal}'.format(signal = signal)).GetMaximum())
            MaxY=MaxY*1.5; MinY=0.01;
            for signal in self.signal_List:
                eval('h_Signif_{signal}'.format(signal = signal)).GetYaxis().SetRangeUser(MinY,MaxY);
            if self.AddText_ToEachBin:
                # ROOT.gStyle.SetPaintTextFormat("4.1f")
                for signal in self.signal_List:
                    eval('h_Signif_{signal}'.format(signal = signal)).SetMarkerSize(self.Textsize)
                    eval('h_Signif_{signal}'.format(signal = signal)).SetMarkerColor(self.color_palet[signal])
                    if signal == self.signal_List[0] : 
                        eval('h_Signif_{signal}'.format(signal = signal)).Draw("hist,text0")
                    else:
                        eval('h_Signif_{signal}'.format(signal = signal)).Draw("hist,text0,same")
            else:
                for signal in self.signal_List:
                    if signal == self.signal_List[0] : 
                        eval('h_Signif_{signal}'.format(signal = signal)).Draw("hist,text0")
                    else:
                        eval('h_Signif_{signal}'.format(signal = signal)).Draw("hist,text0,same")

            # axis2.Draw();axis3.Draw(); 
                
            fPads2.RedrawAxis(); fPads2.Update();
            fPads1.RedrawAxis(); fPads1.Update();


        #============= THE LEGEND SESSION =======================
        if self.MODE in ["MC","MCvsDATA"]:
            theLeg = TLegend(0.48, 0.55, 0.9, 0.9, "", "NDC");theLeg.SetName("theLegend"); theLeg.SetBorderSize(0); theLeg.SetLineColor(0); theLeg.SetFillColor(0);theLeg.SetFillStyle(0); theLeg.SetLineWidth(0); theLeg.SetLineStyle(0); theLeg.SetTextFont(42);theLeg.SetTextSize(.05);
            theLeg.SetFillColor(0);theLeg.SetBorderSize(0);theLeg.SetLineColor(0);theLeg.SetLineWidth(0);theLeg.SetLineStyle(0);theLeg.SetTextFont(42);#theLeg.SetNColumns(2);
            if self.MODE=="MCvsDATA":theLeg.AddEntry(h_data, "Data "+options.y,"ep");
            for mBKG in self.Merge_BKG_Dic:
                theLeg.AddEntry(eval('h_'+mBKG)    , self.Label[mBKG]             ,"F");
            for signal in self.signal_List:
                theLeg.AddEntry(eval('h_'+signal),  self.Label[signal] + "#times %s"%(self.Signal_Scale[signal]),"L");
            theLeg.SetY1NDC(0.9-0.08*6-0.005);
            theLeg.SetY1(theLeg.GetY1NDC()); fPads1.cd(); theLeg.Draw(); #theLeg.AddEntry(gr_MCStat, "Sys.","F");
            #============ SET MAX Y-AXIS FOR PLOTS ==================
            histsigmax = 0
            histsigmin = 999999999
            for signal in self.signal_List:
                histsigmax = TMath.Max( histsigmax, eval('h_'+signal).GetMaximum() )
                histsigmin = TMath.Max( histsigmin, eval('h_'+signal).GetMinimum() )
            if self.MODE in ["MCvsDATA"]:
                histsigmax = TMath.Max( histsigmax, h_data.GetMaximum() )  
                print histsigmax
            histsigmax = TMath.Max( histsigmax, h_TotalMC.GetMaximum() )         
            histsigmin = TMath.Min( histsigmin, h_TotalMC.GetMinimum() )
            for signal in self.signal_List:
                eval('h_'+signal).GetYaxis().SetRangeUser(0, histsigmax*1.3 )
                h_TotalMC.GetYaxis().SetRangeUser(0, histsigmax*1.3 )
            if self.DrawData:
                h_data.GetYaxis().SetRangeUser(   0, histsigmax*1.3 )
            if logy == 1:
                if histsigmin<=0: histsigmin=1;
                for signal in self.signal_List:
                    eval('h_'+signal).GetYaxis().SetRangeUser(0.5*histsigmin, histsigmax*100. )
                h_TotalMC.GetYaxis().SetRangeUser(0.5*histsigmin, histsigmax*100. )
                if self.DrawData:
                    h_data.GetYaxis().SetRangeUser(   0.5*histsigmin, histsigmax*100. )

        if self.MODE in ["DECO"]:
            theLeg = TLegend(0.48, 0.55, 0.9, 0.9, "", "NDC");theLeg.SetName("theLegend"); theLeg.SetBorderSize(0); theLeg.SetLineColor(0); theLeg.SetFillColor(0);theLeg.SetFillStyle(0); theLeg.SetLineWidth(0); theLeg.SetLineStyle(0); theLeg.SetTextFont(42);theLeg.SetTextSize(.05);
            theLeg.SetFillColor(0);theLeg.SetBorderSize(0);theLeg.SetLineColor(0);theLeg.SetLineWidth(0);theLeg.SetLineStyle(0);theLeg.SetTextFont(42);#theLeg.SetNColumns(2);
            if self.Only_Show_Component:
                for DECO in self.DECO:
                    fraction = str(round(100*(eval('h_%s'%(DECO)).Integral()/h_TotalMC.Integral()),1))+"%"
                    theLeg.AddEntry(eval('h_%s'%(DECO))    , self.DECO_Label[DECO]+" "+  fraction   ,"F");
            else:
                theLeg.SetNColumns(len(self.DECO));
                theLeg.SetTextSize(.02);
                for mBKG in self.Merge_BKG_Dic:
                    for DECO in self.DECO:
                        fraction = str(round(100*(eval('h_%s_%s'%(mBKG,DECO)).Integral()/eval('h_%s'%(mBKG)).Integral()),1))+"%"
                        theLeg.AddEntry(eval('h_%s_%s'%(mBKG,DECO))    , "%s,%s %s"%(self.Label[mBKG],self.DECO_Label[DECO],fraction)   ,"F");
            for signal in self.signal_List:
                theLeg.AddEntry(eval('h_'+signal),  self.Label[signal] + "#times %s"%(self.Signal_Scale[signal]),"L");
            theLeg.SetY1NDC(0.9-0.08*6-0.005);
            # theLeg.SetY1(theLeg.GetY1NDC()); fPads1.cd(); theLeg.Draw(); #theLeg.AddEntry(gr_MCStat, "Sys.","F");
            theLeg.Draw()
            #============ SET MAX Y-AXIS FOR PLOTS ==================
            histsigmax = 0
            histsigmin = 999999999
            for signal in self.signal_List:
                histsigmax = TMath.Max( histsigmax, eval('h_'+signal).GetMaximum() )
                histsigmin = TMath.Max( histsigmin, eval('h_'+signal).GetMinimum() )
            histsigmax = TMath.Max( histsigmax, hstack_TotalMC_DECO.GetMaximum() )         
            histsigmin = TMath.Min( histsigmin, hstack_TotalMC_DECO.GetMinimum() )
            for signal in self.signal_List:
                eval('h_'+signal).GetYaxis().SetRangeUser(0, histsigmax*1.3 )
            hstack_TotalMC_DECO.GetYaxis().SetRangeUser(0, histsigmax*1.3 )
            
        #============ SAVE PLOTS IN A DIRECTORY ============================
        extension   = "";
        if tag    !=  "": extension = extension + "_"+tag;
        if logy         : extension = extension + "_log";
        if options.FBT  : extension = extension + "_FBT";
        if SFs          : extension = extension + "_SFsCorr";
        #----------- Rename variables to a shorter name -----------------
        for c in [".","/","(",")","[","]","*","+",">","<"," ","=",",","deep","dnn","Decorr","jetAK8puppi","ass_tag","t_tag","_tag","|","&"]:variable=variable.replace(c,"_");
        for c in ["__","___","____","_____","______","_"]:variable=variable.replace(c,"");
        #for c in ["__","___","____","_____","______","_"]:variable=variable.replace(c,"_");
        #----------------- Save and open the plot -----------------------
        Name=REGION+"_"+variable+"_"+self.MODE+"_"+options.y+extension+".png"
        if self.Plotname:
            Name = self.Plotname+extension+".png"
        Name = self.PlotPath+Name
        file=TString(Name); 

        output_ROOTFile = Name.replace(".png",".root") ; outf = ROOT.TFile( output_ROOTFile, "recreate")
        for h in self.Histogram_ToStore:
            try:
                print h,":",eval(h).Integral()
                if h == "h_Signal1":
                    hist = eval(h).Clone("h_Signal1c")
                    hist.Scale(float(1./self.Signal_Scale1))
                    hist.Write()
                if h == "h_Signal2":
                    hist = eval(h).Clone("h_Signal2c")
                    hist.Scale(float(1./self.Signal_Scale2))
                    hist.Write()
                else:
                    eval(h).Write()
            except NameError:
                print h,"not exist"
            else:
                pass
        outf.Close()

        if self.Run_limit:
            Output = Prepare_1Region( LIMIT_CODEPATH = self.LIMIT_CODEPATH, sig = self.Signal_limit, inf = output_ROOTFile ) ; print Output;
            fPads1.cd()
            upper_limit = ROOT.TLatex( h_TotalMC.GetBinLowEdge(2), (h_TotalMC.GetMaximum())*0.7, "#splitline{#splitline{#splitline{%s}{%s}}{#splitline{%s}{%s}}}{%s}"%(Output[3][0],Output[3][1],Output[3][2],Output[3][3],Output[3][4]));  upper_limit.SetTextSize(0.03); 
            upper_limit.SetTextColor(self.TextColor_limit);
            upper_limit.Draw("same");

        self.comment = "No comment" ; Text_Name = Name.replace(".png",".txt") ; self.View_Selection_With_Plots(Text_Name,variable,cut,self.comment)

        canvas_controlplot.SaveAs( file.Data() )
        os.system("display %s &"%(Name) ); print "\n --> display %s &"%(Name);

        self.Plotname = None

        if options.piechart:#============== PIE CHARTS =================================
            num_events, colors = array('d'), array('i');   gStyle.SetOptStat(000000000);            
            piecanvas=TCanvas("PIES","PIES",400,400);  piecanvas.SetTickx(1); piecanvas.SetTicky(1); piecanvas.SetRightMargin(-0.5); piecanvas.SetTopMargin(-0.5); piecanvas.SetLeftMargin(-0.5); piecanvas.SetBottomMargin(-0.5);gStyle.SetOptStat(000000000);
            num_events.append(h_QCD.Integral());   num_events.append(h_WJets.Integral());  num_events.append(h_TTbar.Integral()); num_events.append(h_STop.Integral()); num_events.append(h_Rest.Integral());
            colors.append(self.color_palet["QCD"]);   colors.append(self.color_palet["WJets"]);  colors.append(self.color_palet["TTbar"]); colors.append(self.color_palet["STop"]); colors.append(self.color_palet["Rest"]);
            pieplot=TPie("PIE","",5,num_events,colors);
            pieplot.SetEntryLabel(0,"QCD");pieplot.SetEntryLabel(1,"W+jets"); pieplot.SetEntryLabel(2,"t#bar{t}");pieplot.SetEntryLabel(3,"single t");pieplot.SetEntryLabel(4,"Rest VV,Z+jets");
            pieplot.SetTextSize(.045); pieplot.SetAngularOffset(30); pieplot.SetLabelFormat("%val (%perc) %txt"); pieplot.SetRadius(.4); pieplot.SetLabelsOffset(-.33); piecanvas.cd(1);pieplot.Draw("nol <");RegionTxt.Draw();
            file2=TString("PIE_%s_%s.png"%(REGION,options.y)); piecanvas.SaveAs(file2.Data());
            os.system("display PIE_%s_%s.png &"%(REGION,options.y) );

def Significance_Histogram(self, h_signal, h_TotalMC,name):
    h = h_signal.Clone(name)
    for i in range(1,h_TotalMC.GetNbinsX()+1,1):
        s = h_signal.GetBinContent(i)
        b = h_TotalMC.GetBinContent(i)
        if b == 0:
            b = 1
        significance = (2*((s+b)*math.log((1+(s/b)),math.e)-s))**0.5
        h.SetBinContent(i,significance)
    return h

ANALYSIS.Significance_Histogram = Significance_Histogram

################# Main Code ################################
def Draw_Control_Plot( channel ) :
    if channel in ["had"]           : Instance_ANALYSIS = ANALYSIS( channel ); Instance_ANALYSIS.DefineSelection_0lep();
    #if channel in ["mu","el","lep"] : Instance_ANALYSIS = ANALYSIS( channel ); Instance_ANALYSIS.DefineSelection_1lep();

if __name__ == '__main__' : 
    Beginning = strftime("%H:%M:%S",gmtime())
    print '\n----RUN--------------channel:[',options.channel,']----------Region:[',options.REGION,']----------------[',Beginning,']--------'
    Draw_Control_Plot( options.channel );
    Finishing = strftime("%H:%M:%S",gmtime());
    #========== CALCULATE DURATION OF THE RUN ===========
    MIN=int(Finishing[3:5])-int(Beginning[3:5]); SEC=int(Finishing[6:8])-int(Beginning[6:8]); 
    if SEC<0 and MIN>0 : SEC=60+SEC; MIN=MIN-1;
    if SEC>0 and MIN<0 : MIN=60+MIN;
    if SEC<0 and MIN<0 : SEC=60+SEC; MIN=60+MIN-1;
    print '----END-----------------------------------------------[time:',Finishing,', duration:',MIN,'MIN:',SEC,'SEC]---------\n'
