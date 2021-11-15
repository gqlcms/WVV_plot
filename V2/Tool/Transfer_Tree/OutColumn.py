if self.MC:
    # ===================================== event level =====================================
    self.OutColumn += [
        "weight",
        "ST", "MJJlv", "HT",
        "nb_l_deep_ex","nb_m_deep_ex","nb_t_deep_ex","nb_l_deep_in","nb_m_deep_in","nb_t_deep_in",
    ]
    # ===================================== event level =====================================

    # ===================================== FJ1,2 P4 =====================================
    self.OutColumn += [
        "Lep1fatJet2_FatJet_msoftdrop","Lep1fatJet2_FatJet_pt","Lep1fatJet2_FatJet_eta","Lep1fatJet2_FatJet_phi","Lep1fatJet2_FatJet_msoftdrop_2","Lep1fatJet2_FatJet_pt_2","Lep1fatJet2_FatJet_eta_2","Lep1fatJet2_FatJet_phi_2",
    ]
    # ===================================== FJ1,2 P4 =====================================

    # ===================================== FJ1,2 tagger =====================================
    self.OutColumn += [
        "Lep1fatJet2_FatJet_deepTagMD_TvsQCD","Lep1fatJet2_FatJet_deepTagMD_WvsQCD","Lep1fatJet2_FatJet_deepTag_TvsQCD","Lep1fatJet2_FatJet_deepTag_WvsQCD","Lep1fatJet2_FatJet_particleNet_TvsQCD","Lep1fatJet2_FatJet_particleNet_WvsQCD","Lep1fatJet2_FatJet_particleNetMD_WvsQCD","Lep1fatJet2_FatJet_tau21","Lep1fatJet2_FatJet_deepTagMD_TvsQCD_2","Lep1fatJet2_FatJet_deepTagMD_WvsQCD_2","Lep1fatJet2_FatJet_deepTag_TvsQCD_2","Lep1fatJet2_FatJet_deepTag_WvsQCD_2","Lep1fatJet2_FatJet_particleNet_TvsQCD_2","Lep1fatJet2_FatJet_particleNet_WvsQCD_2","Lep1fatJet2_FatJet_particleNetMD_WvsQCD_2","Lep1fatJet2_FatJet_tau21_2",
    ]
    # ===================================== FJ1,2 tagger =====================================

    # ===================================== leptonic W =====================================
    self.OutColumn += [
        "Lep1fatJet2_LeptonicWPt","Lep1fatJet2_LeptonicWEta","Lep1fatJet2_LeptonicWPhi","Lep1fatJet2_LeptonicWM","Lep1fatJet2_LeptonicWMt","Lep1fatJet2_LeptonicWMt_2",
    ]
    # ===================================== leptonic W =====================================

    # ===================================== MET =====================================
    self.OutColumn += [
        "Lep1fatJet2_MET_pt","Lep1fatJet2_MET_phi",
    ]
    # ===================================== MET =====================================


    # ===================================== Lepton =====================================
    self.OutColumn += [
        "Lep1fatJet2_LeptonPt","Lep1fatJet2_LeptonEta","Lep1fatJet2_LeptonPhi","Lep1fatJet2_LeptonE",
    ]
    # ===================================== Lepton =====================================


