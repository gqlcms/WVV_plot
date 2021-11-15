ST = '''
return ( Lep1fatJet2_LeptonPt + Lep1fatJet2_FatJet_pt + Lep1fatJet2_FatJet_pt_2 ) ; 
'''

HT = '''
return ( Lep1fatJet2_FatJet_pt + Lep1fatJet2_FatJet_pt_2 ) ; 
'''

MJJlv = '''
TLorentzVector AK8_1, AK8_2, leptonicW; 
AK8_1.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt, Lep1fatJet2_FatJet_eta , Lep1fatJet2_FatJet_phi, Lep1fatJet2_FatJet_msoftdrop ); 
AK8_2.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt_2, Lep1fatJet2_FatJet_eta_2 , Lep1fatJet2_FatJet_phi_2, Lep1fatJet2_FatJet_msoftdrop_2 ); 
leptonicW.SetPtEtaPhiM( Lep1fatJet2_LeptonicWPt, Lep1fatJet2_LeptonicWEta , Lep1fatJet2_LeptonicWPhi, Lep1fatJet2_LeptonicWM ); 
return ( AK8_1 + AK8_2 + leptonicW ).M();
'''

