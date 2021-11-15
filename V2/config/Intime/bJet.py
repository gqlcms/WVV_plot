'''
Lep1fatJet2_Jet_pt
Lep1fatJet2_Jet_eta
Lep1fatJet2_Jet_phi
Lep1fatJet2_Jet_hadronFlavour
Lep1fatJet2_Jet_partonFlavour
Lep1fatJet2_Jet_btagDeepB
Lep1fatJet2_Jet_btagDeepC
Lep1fatJet2_Jet_btagDeepFlavC
Lep1fatJet2_Jet_btagDeepFlavB

float bWPloose  = 0.0614;// https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
float bWPmedium = 0.3093;// https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
float bWPtight  = 0.7221;// https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
'''

nb_l_deep_ex = '''
float bWPloose  = 0.0614;
float bWPmedium = 0.3093;
float bWPtight  = 0.7221;

int nb_l_deep_ex = 0;
TLorentzVector Jet, fJ1, fJ2; 
fJ1.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt, Lep1fatJet2_FatJet_eta, Lep1fatJet2_FatJet_phi, Lep1fatJet2_FatJet_msoftdrop );
fJ2.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt_2, Lep1fatJet2_FatJet_eta_2, Lep1fatJet2_FatJet_phi_2, Lep1fatJet2_FatJet_msoftdrop_2 );

for ( Int_t i = 0 ; i < Lep1fatJet2_Jet_pt.size() ; i++ ) {
    Jet.SetPtEtaPhiE( Lep1fatJet2_Jet_pt[i], Lep1fatJet2_Jet_eta[i], Lep1fatJet2_Jet_phi[i], Lep1fatJet2_Jet_e[i] );
    float deltaR1 = Jet.DeltaR(fJ1);
    float deltaR2 = Jet.DeltaR(fJ2);
    if ( deltaR1 > 1.0 && deltaR2 > 1.0 && Lep1fatJet2_Jet_btagDeepFlavB[i] > bWPloose ) {
        nb_l_deep_ex ++;
    }
}

return nb_l_deep_ex;
'''

nb_m_deep_ex = '''
float bWPloose  = 0.0614;
float bWPmedium = 0.3093;
float bWPtight  = 0.7221;

int nb_m_deep_ex = 0;
TLorentzVector Jet, fJ1, fJ2; 
fJ1.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt, Lep1fatJet2_FatJet_eta, Lep1fatJet2_FatJet_phi, Lep1fatJet2_FatJet_msoftdrop );
fJ2.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt_2, Lep1fatJet2_FatJet_eta_2, Lep1fatJet2_FatJet_phi_2, Lep1fatJet2_FatJet_msoftdrop_2 );

for ( Int_t i = 0 ; i < Lep1fatJet2_Jet_pt.size() ; i++ ) {
    Jet.SetPtEtaPhiE( Lep1fatJet2_Jet_pt[i], Lep1fatJet2_Jet_eta[i], Lep1fatJet2_Jet_phi[i], Lep1fatJet2_Jet_e[i] );
    float deltaR1 = Jet.DeltaR(fJ1);
    float deltaR2 = Jet.DeltaR(fJ2);
    if ( deltaR1 > 1.0 && deltaR2 > 1.0 && Lep1fatJet2_Jet_btagDeepFlavB[i] > bWPmedium ) {
        nb_m_deep_ex ++;
    }
}

return nb_m_deep_ex;
'''


nb_t_deep_ex = '''
float bWPloose  = 0.0614;
float bWPmedium = 0.3093;
float bWPtight  = 0.7221;

int nb_t_deep_ex = 0;
TLorentzVector Jet, fJ1, fJ2; 
fJ1.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt, Lep1fatJet2_FatJet_eta, Lep1fatJet2_FatJet_phi, Lep1fatJet2_FatJet_msoftdrop );
fJ2.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt_2, Lep1fatJet2_FatJet_eta_2, Lep1fatJet2_FatJet_phi_2, Lep1fatJet2_FatJet_msoftdrop_2 );

for ( Int_t i = 0 ; i < Lep1fatJet2_Jet_pt.size() ; i++ ) {
    Jet.SetPtEtaPhiE( Lep1fatJet2_Jet_pt[i], Lep1fatJet2_Jet_eta[i], Lep1fatJet2_Jet_phi[i], Lep1fatJet2_Jet_e[i] );
    float deltaR1 = Jet.DeltaR(fJ1);
    float deltaR2 = Jet.DeltaR(fJ2);
    if ( deltaR1 > 1.0 && deltaR2 > 1.0 && Lep1fatJet2_Jet_btagDeepFlavB[i] > bWPtight ) {
        nb_t_deep_ex ++;
    }
}

return nb_t_deep_ex;
'''


nb_l_deep_in = '''
float bWPloose  = 0.0614;
float bWPmedium = 0.3093;
float bWPtight  = 0.7221;

int nb_l_deep_in = 0;

for ( Int_t i = 0 ; i < Lep1fatJet2_Jet_pt.size() ; i++ ) {
    if ( Lep1fatJet2_Jet_btagDeepFlavB[i] > bWPloose ) {
        nb_l_deep_in ++;
    }
}

return nb_l_deep_in;
'''

nb_m_deep_in = '''
float bWPloose  = 0.0614;
float bWPmedium = 0.3093;
float bWPtight  = 0.7221;

int nb_m_deep_in = 0;

for ( Int_t i = 0 ; i < Lep1fatJet2_Jet_pt.size() ; i++ ) {
    if ( Lep1fatJet2_Jet_btagDeepFlavB[i] > bWPmedium ) {
        nb_m_deep_in ++;
    }
}

return nb_m_deep_in;
'''

nb_t_deep_in = '''
float bWPloose  = 0.0614;
float bWPmedium = 0.3093;
float bWPtight  = 0.7221;

int nb_t_deep_in = 0;

for ( Int_t i = 0 ; i < Lep1fatJet2_Jet_pt.size() ; i++ ) {
    if ( Lep1fatJet2_Jet_btagDeepFlavB[i] > bWPtight ) {
        nb_t_deep_in ++;
    }
}

return nb_t_deep_in;
'''