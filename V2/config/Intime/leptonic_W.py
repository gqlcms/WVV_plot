'''
Lep1fatJet2_MET_pt
Lep1fatJet2_MET_phi
Lep1fatJet2_LeptonPt
Lep1fatJet2_LeptonEta
Lep1fatJet2_LeptonPhi
Lep1fatJet2_LeptonE
'''

Lep1fatJet2_LeptonicWMt_2 = '''
return TMath::Sqrt(2*Lep1fatJet2_LeptonPt*Lep1fatJet2_MET_pt*(1.0-TMath::Cos(Lep1fatJet2_LeptonPhi-Lep1fatJet2_MET_phi)));
'''
