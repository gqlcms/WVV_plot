int matching[2] = {-99};

float ptgenwl[5][15] = {-99.};
int Windex = 0;

float ptgentl[5][13] = {-99.};
int Tindex = 0;

float ptgengqf[14][4] = {-99.};
int gqindex = 0;

std::vector<int> FirstCopy_g;
int PDGIDqg[6] = {1,2,3,4,5,21};

for(size_t ik=0; ik<Lep1fatJet2_GenPart_pt.size();ik++){
    // W
    if ( abs(Lep1fatJet2_GenPart_pdgId[ik]) == 24 ){
        if (not (Lep1fatJet2_GenPart_statusFlags[ik]&(1<<13))) continue; // isLastCopy
        if( Windex < 5 ){

            ptgenwl[Windex][0] = Lep1fatJet2_GenPart_pt[ik];
            ptgenwl[Windex][1] = Lep1fatJet2_GenPart_eta[ik];
            ptgenwl[Windex][2] = Lep1fatJet2_GenPart_phi[ik];
            ptgenwl[Windex][3] = Lep1fatJet2_GenPart_mass[ik];
            ptgenwl[Windex][14] = ik;

            vector<int> W_daughter_index;
            for (size_t id=0; id<Lep1fatJet2_GenPart_pt.size();id++){
                if (Lep1fatJet2_GenPart_genPartIdxMother[id] == ik){
                    W_daughter_index.push_back(id);
                }
            }
            int NW_daughter = W_daughter_index.size();
            if ( NW_daughter == 2){
                ptgenwl[Windex][4] = Lep1fatJet2_GenPart_pt[W_daughter_index[0]];
                ptgenwl[Windex][5] = Lep1fatJet2_GenPart_eta[W_daughter_index[0]];
                ptgenwl[Windex][6] = Lep1fatJet2_GenPart_phi[W_daughter_index[0]];
                ptgenwl[Windex][7] = Lep1fatJet2_GenPart_mass[W_daughter_index[0]];
                ptgenwl[Windex][8] = Lep1fatJet2_GenPart_pdgId[W_daughter_index[0]];

                ptgenwl[Windex][9]  = Lep1fatJet2_GenPart_pt[W_daughter_index[1]];
                ptgenwl[Windex][10] = Lep1fatJet2_GenPart_eta[W_daughter_index[1]];
                ptgenwl[Windex][11] = Lep1fatJet2_GenPart_phi[W_daughter_index[1]];
                ptgenwl[Windex][12] = Lep1fatJet2_GenPart_mass[W_daughter_index[1]];
                ptgenwl[Windex][13] = Lep1fatJet2_GenPart_pdgId[W_daughter_index[1]];
            }
            Windex++;
        }
    }

    // q,g
    for(size_t igq=0; igq<6;igq++){
        int PGDID = PDGIDqg[igq];
        if (abs(Lep1fatJet2_GenPart_pdgId[ik]) == PGDID ){
            if( Lep1fatJet2_GenPart_pt[ik] > 50 ){
                if( gqindex < 15 ){
                    bool overlap = false;
                    int FirstCopy = -99;
                    int LoopID = ik;
                    bool From_WZTop = false;
                    while(abs(Lep1fatJet2_GenPart_pdgId[LoopID]) == PGDID){
                        FirstCopy = LoopID;
                        LoopID = Lep1fatJet2_GenPart_genPartIdxMother[LoopID];
                    }
                    while( LoopID >= 0 ){
                        if( abs(Lep1fatJet2_GenPart_pdgId[LoopID]) == 24 || abs(Lep1fatJet2_GenPart_pdgId[LoopID]) == 23 || abs(Lep1fatJet2_GenPart_pdgId[LoopID]) == 6 ){
                            From_WZTop = true;
                        }
                        LoopID = Lep1fatJet2_GenPart_genPartIdxMother[LoopID];
                    }
                    if(From_WZTop) continue;
                    for(unsigned int inum = 0; inum < FirstCopy_g.size() ; ++inum){
                        if( FirstCopy == FirstCopy_g[inum] ){
                            overlap = true;
                        }
                    }
                    if(overlap) continue;
                    FirstCopy_g.push_back(FirstCopy);
                    ptgengqf[gqindex][0] = Lep1fatJet2_GenPart_pt[FirstCopy];
                    ptgengqf[gqindex][1] = Lep1fatJet2_GenPart_eta[FirstCopy];
                    ptgengqf[gqindex][2] = Lep1fatJet2_GenPart_phi[FirstCopy];
                    ptgengqf[gqindex][3] = Lep1fatJet2_GenPart_mass[FirstCopy];
                    gqindex++;
                }
            }
        }
    }
}

for(size_t ik=0; ik<Lep1fatJet2_GenPart_pt.size();ik++){
    // Top
    if ( abs(Lep1fatJet2_GenPart_pdgId[ik]) == 6 ){
        if( Tindex < 4 ){
            bool lastcopy = true;
            vector<int> T_daughter_index;
            for (size_t id=0; id<Lep1fatJet2_GenPart_pt.size();id++){
                if (Lep1fatJet2_GenPart_genPartIdxMother[id] == ik){
                    T_daughter_index.push_back(id);
                }
            }
            int NT_daughter = T_daughter_index.size();
            for (size_t id=0; id<NT_daughter;id++){
                if(abs(Lep1fatJet2_GenPart_pdgId[T_daughter_index[id]])==6){
                    lastcopy = false;
                }
            }
            if(!lastcopy) continue;

            ptgentl[Tindex][0] = Lep1fatJet2_GenPart_pt[ik];
            ptgentl[Tindex][1] = Lep1fatJet2_GenPart_eta[ik];
            ptgentl[Tindex][2] = Lep1fatJet2_GenPart_phi[ik];
            ptgentl[Tindex][3] = Lep1fatJet2_GenPart_mass[ik];
            
            if ( NT_daughter == 2){
                int W_daughter = -99;
                int bdaughter = -99;
                if( abs(Lep1fatJet2_GenPart_pdgId[T_daughter_index[0]]) == 24 ){
                    W_daughter = T_daughter_index[0];
                }
                if( abs(Lep1fatJet2_GenPart_pdgId[T_daughter_index[1]]) == 24 ){
                    W_daughter = T_daughter_index[1];
                }
                if( abs(Lep1fatJet2_GenPart_pdgId[T_daughter_index[0]]) == 5 ){
                    bdaughter = T_daughter_index[0];
                }
                if( abs(Lep1fatJet2_GenPart_pdgId[T_daughter_index[1]]) == 5 ){
                    bdaughter = T_daughter_index[1];
                }

                for(size_t iw=0; iw<5;iw++){
                    if(ptgenwl[iw][0] > 0){
                        int LoopIDW = ptgenwl[iw][14];
                        bool W_From_T = false;
                        while( LoopIDW > 0 ){
                            if( LoopIDW == W_daughter ){
                                W_From_T = true;
                            }
                            cout << "W ID :" << LoopIDW << endl;
                            LoopIDW = Lep1fatJet2_GenPart_genPartIdxMother[LoopIDW];
                            cout << "W Mother ID :" << LoopIDW << endl;
                        }
                        if(W_From_T){
                            ptgentl[Tindex][4] = iw;
                        }
                    }
                }
                
                ptgentl[Tindex][5] = Lep1fatJet2_GenPart_pt[bdaughter];
                ptgentl[Tindex][6] = Lep1fatJet2_GenPart_eta[bdaughter];
                ptgentl[Tindex][7] = Lep1fatJet2_GenPart_phi[bdaughter];
                ptgentl[Tindex][8] = Lep1fatJet2_GenPart_mass[bdaughter];

                ptgentl[Tindex][9] = Lep1fatJet2_GenPart_pt[W_daughter];
                ptgentl[Tindex][10] = Lep1fatJet2_GenPart_eta[W_daughter];
                ptgentl[Tindex][11] = Lep1fatJet2_GenPart_phi[W_daughter];
                ptgentl[Tindex][12] = Lep1fatJet2_GenPart_mass[W_daughter];
            }

            TLorentzVector GenW2,GenW,Genb;
            cout << "Top pt :" << ptgentl[Tindex][0] << endl;
            cout << "Top mass :" << ptgentl[Tindex][3] << endl;
            int W_index = ptgentl[Tindex][4];
            GenW.SetPtEtaPhiM(ptgenwl[W_index][0],ptgenwl[W_index][1],ptgenwl[W_index][2],ptgenwl[W_index][3]);
            Genb.SetPtEtaPhiM(ptgentl[Tindex][5],ptgentl[Tindex][6],ptgentl[Tindex][7],ptgentl[Tindex][8]);
            cout << "W,b pt :" << (GenW+Genb).Pt() << endl;
            GenW2.SetPtEtaPhiM(ptgentl[Tindex][9],ptgentl[Tindex][10],ptgentl[Tindex][11],ptgentl[Tindex][12]);
            cout << "Wf,b pt :" << (GenW2+Genb).Pt() << endl;

            Tindex++;
        }
    }
}

TLorentzVector Genpart, Genpartd1, Genpartd2, Genpartd1d1, Genpartd1d2, fJ1, fJ2, lepton;
 
fJ1.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt, Lep1fatJet2_FatJet_eta, Lep1fatJet2_FatJet_phi, Lep1fatJet2_FatJet_msoftdrop );
fJ2.SetPtEtaPhiM( Lep1fatJet2_FatJet_pt_2, Lep1fatJet2_FatJet_eta_2, Lep1fatJet2_FatJet_phi_2, Lep1fatJet2_FatJet_msoftdrop_2 );
lepton.SetPtEtaPhiE( Lep1fatJet2_LeptonPt, Lep1fatJet2_LeptonEta, Lep1fatJet2_LeptonPhi, Lep1fatJet2_LeptonE );

for(size_t ik=0; ik<5;ik++){
    if(ptgenwl[ik][0] > 0){
        Genpart.SetPtEtaPhiM( ptgenwl[ik][0], ptgenwl[ik][1], ptgenwl[ik][2], ptgenwl[ik][3] );
        Genpartd1.SetPtEtaPhiM( ptgenwl[ik][4], ptgenwl[ik][5], ptgenwl[ik][6], ptgenwl[ik][7] );
        Genpartd2.SetPtEtaPhiM( ptgenwl[ik][9], ptgenwl[ik][10], ptgenwl[ik][11], ptgenwl[ik][12] );
        if( fabs(Genpart.DeltaR(fJ1)) < 0.6 ){
            matching[0] = 1;
            if( fabs(Genpartd1.DeltaR(fJ1)) < 0.8 && fabs(Genpartd2.DeltaR(fJ1)) < 0.8 ){
                matching[0] = 2;
            }
            if( ((fabs(Genpartd1.DeltaR(fJ1)) < 0.8) + (fabs(Genpartd2.DeltaR(fJ1)) < 0.8)) == 1 ){
                matching[0] = 4;
            }
        }
        if( Genpart.DeltaR(fJ2) < 0.6 ){
            matching[1] = 1;
            if( fabs(Genpartd1.DeltaR(fJ2)) < 0.8 && fabs(Genpartd2.DeltaR(fJ2)) < 0.8 ){
                matching[1] = 2;
            }
            if( ((fabs(Genpartd1.DeltaR(fJ2)) < 0.8) + (fabs(Genpartd2.DeltaR(fJ2)) < 0.8)) == 1 ){
                matching[1] = 4;
            }
        }
    }
}

for(size_t ik=0; ik<15;ik++){
    if(ptgengqf[ik][0] > 50){
        Genpart.SetPtEtaPhiM( ptgengqf[ik][0], ptgengqf[ik][1], ptgengqf[ik][2], ptgengqf[ik][3] );
        if( fabs(Genpart.DeltaR(fJ1)) < 0.6 ){
            matching[0] = 3;
        }
        if( fabs(Genpart.DeltaR(fJ2)) < 0.6 ){
            matching[1] = 3;
        }
    }
}

for(size_t ik=0; ik<4;ik++){
    if(ptgentl[ik][0] > 0){
        Genpart.SetPtEtaPhiM( ptgentl[ik][0], ptgentl[ik][1], ptgentl[ik][2], ptgentl[ik][3] );
        int W_index = ptgentl[ik][4];
        Genpartd1.SetPtEtaPhiM( ptgenwl[W_index][0], ptgenwl[W_index][1], ptgenwl[W_index][2], ptgenwl[W_index][3] );
        Genpartd2.SetPtEtaPhiM( ptgentl[ik][5], ptgenwl[ik][6], ptgenwl[ik][7], ptgenwl[ik][8] );
        Genpartd1d1.SetPtEtaPhiM( ptgenwl[W_index][4], ptgenwl[W_index][5], ptgenwl[W_index][6], ptgenwl[W_index][7] );
        Genpartd1d2.SetPtEtaPhiM( ptgenwl[W_index][9], ptgenwl[W_index][10], ptgenwl[W_index][11], ptgenwl[W_index][12] );

        if( fabs(Genpart.DeltaR(fJ1)) < 0.6 ){
            if( fabs(Genpartd1d1.DeltaR(fJ1)) < 0.8 && fabs(Genpartd1d2.DeltaR(fJ1)) < 0.8 && fabs(Genpartd2.DeltaR(fJ1)) < 0.8 ){
                matching[0] = 5;
            }
            if( ( (fabs(Genpartd1d1.DeltaR(fJ1)) < 0.8)+(fabs(Genpartd1d2.DeltaR(fJ1)) < 0.8) )==1 && fabs(Genpartd2.DeltaR(fJ1)) < 0.8 ){
                matching[0] = 6;
            }
        }

        if( fabs(Genpart.DeltaR(fJ2)) < 0.6 ){
            if( fabs(Genpartd1d1.DeltaR(fJ2)) < 0.8 && fabs(Genpartd1d2.DeltaR(fJ2)) < 0.8 && fabs(Genpartd2.DeltaR(fJ2)) < 0.8 ){
                matching[1] = 5;
            }
            if( ( (fabs(Genpartd1d1.DeltaR(fJ2)) < 0.8)+(fabs(Genpartd1d2.DeltaR(fJ2)) < 0.8) )==1 && fabs(Genpartd2.DeltaR(fJ2)) < 0.8 ){
                matching[1] = 6;
            }
        }

    }
}

// 1 : matching with GenW
// 2 : matching with GenW, d1, d2
// 3 : matching with q,g
// 4 : matching with GenW, d1 or d2
// 5 : matching with T, W, b, Wd1, Wd2
// 6 : matching with T, W, b, Wd1 or Wd2

if(ptgentl[0][0] > 0){
    cout << "matching[0]" << matching[0] << endl;
    cout << "matching[1]" << matching[1] << endl;
}

// return matching;
return matching;