'''
Lep1fatJet2_FatJet_tau1
Lep1fatJet2_FatJet_tau2
Lep1fatJet2_FatJet_tau3
Lep1fatJet2_FatJet_tau4
Lep1fatJet2_FatJet_deepTagMD_TvsQCD
Lep1fatJet2_FatJet_deepTagMD_WvsQCD
Lep1fatJet2_FatJet_deepTag_TvsQCD
Lep1fatJet2_FatJet_deepTag_WvsQCD
Lep1fatJet2_FatJet_particleNetMD_QCD
Lep1fatJet2_FatJet_particleNetMD_Xbb
Lep1fatJet2_FatJet_particleNetMD_Xcc
Lep1fatJet2_FatJet_particleNetMD_Xqq
Lep1fatJet2_FatJet_particleNet_TvsQCD
Lep1fatJet2_FatJet_particleNet_WvsQCD

For W vs QCD tagging, (Xcc+Xqq)/(Xcc+Xqq+QCD)
'''

Lep1fatJet2_FatJet_particleNetMD_WvsQCD = '''
return (Lep1fatJet2_FatJet_particleNetMD_Xcc+Lep1fatJet2_FatJet_particleNetMD_Xqq)/(Lep1fatJet2_FatJet_particleNetMD_Xcc+Lep1fatJet2_FatJet_particleNetMD_Xqq+Lep1fatJet2_FatJet_particleNetMD_QCD);
'''

Lep1fatJet2_FatJet_particleNetMD_WvsQCD_2 = '''
return (Lep1fatJet2_FatJet_particleNetMD_Xcc_2+Lep1fatJet2_FatJet_particleNetMD_Xqq_2)/(Lep1fatJet2_FatJet_particleNetMD_Xcc_2+Lep1fatJet2_FatJet_particleNetMD_Xqq_2+Lep1fatJet2_FatJet_particleNetMD_QCD_2);
'''

Lep1fatJet2_FatJet_tau21 = '''
return Lep1fatJet2_FatJet_tau2/Lep1fatJet2_FatJet_tau1;
'''

Lep1fatJet2_FatJet_tau21_2 = '''
return Lep1fatJet2_FatJet_tau2_2/Lep1fatJet2_FatJet_tau1_2;
'''