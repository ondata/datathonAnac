import pandas as pd


def redflag_01 (df, releaseId, procMethod, competitiveList):

    df_competitive = df.loc[df[procMethod].isin(competitiveList)] 

    if df_competitive.empty:

         df_redflag = pd.DataFrame(columns=['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description'])
    
    else:

        tot_participants = df_competitive.shape[0] + 1
        tot_id =  df_competitive[releaseId].nunique()

        mean_participants = round(tot_participants/tot_id, 2)
    
        npart = df_competitive.groupby([releaseId]).size()
        df_redflag = npart.to_frame()
        df_redflag.reset_index(inplace=True)
        
        df_redflag.columns=['ocds:releases/0/id','appaltipop:releases/0/tender/participants/total']
        df_redflag['appaltipop:rf1/totalParticipants'] = tot_participants
        df_redflag['appaltipop:rf1/meanParticipants'] = mean_participants
        
        df_redflag.loc[df_redflag['appaltipop:rf1/meanParticipants'] <= 10, 'appaltipop:releases/0/redflag/code'] = '01'
        df_redflag.loc[df_redflag['appaltipop:rf1/meanParticipants'] <= 10, 'appaltipop:releases/0/redflag/description'] = 'Basso numero di offerenti medi di gara per processi competitivi'
    
        df_redflag = df_redflag[df_redflag['appaltipop:releases/0/redflag/code'].notna()]
  

    return  df_redflag[['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description']]
 

    #return df_competitive



def redflag_02 (df, releaseId, procMethod, competitiveList):

    df_competitive = df.loc[df[procMethod].isin(competitiveList)] 

    if df_competitive.empty:

        df_redflag = pd.DataFrame(columns=['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description'])
    
    else:    

        tot_competitive_tenders =  df_competitive[releaseId].nunique()
        
        tot_tenders =  df[releaseId].nunique()
    
        threshold = round(tot_competitive_tenders * 100/tot_tenders, 2)
        
        npart = df_competitive.groupby([releaseId]).size()
        df_redflag = npart.to_frame()
        df_redflag.reset_index(inplace=True)
        
        df_redflag.columns=['ocds:releases/0/id','appaltipop:releases/0/tender/participants/total']
        df_redflag['appaltipop:rf2/totalCompetitiveTenders'] = tot_competitive_tenders
        df_redflag['appaltipop:rf2/totalTenders'] = tot_tenders
        df_redflag['appaltipop:rf2/threshold'] = threshold
        
        
        df_redflag.loc[df_redflag['appaltipop:rf2/threshold'] <= 50.0, 'appaltipop:releases/0/redflag/code'] = '02'
        df_redflag.loc[df_redflag['appaltipop:rf2/threshold'] <= 50.0, 'appaltipop:releases/0/redflag/description'] = 'Bassa percentuale di offerte aggiudicate mediante procedure competitive'
        df_redflag = df_redflag[df_redflag['appaltipop:releases/0/redflag/code'].notna()]
    
    return  df_redflag[['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description']]
    
    #return  df_redflag_02




def redflag_03 (df, releaseId, procMethod, directList):


    df_direct = df.loc[df[procMethod].isin(directList) == False]

    if df_direct.empty:

        df_redflag = pd.DataFrame(columns=['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description'])
    
    else:  
        npart = df_direct.groupby([releaseId]).size()
        df_redflag = npart.to_frame()
        df_redflag.reset_index(inplace=True)
        
        df_redflag.columns=['ocds:releases/0/id','appaltipop:releases/0/tender/participants/total']
        
        
        df_redflag.loc[df_redflag['appaltipop:releases/0/tender/participants/total'] == 1, 'appaltipop:releases/0/redflag/code'] = '03'
        df_redflag.loc[df_redflag['appaltipop:releases/0/tender/participants/total'] == 1, 'appaltipop:releases/0/redflag/description'] = 'Questa gara presenta un solo offerente'
        df_redflag = df_redflag[df_redflag['appaltipop:releases/0/redflag/code'].notna()]
    
    return  df_redflag[['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description']]
    
    #return  df_redflag



def redflag_04 (df_tenderers_input, df_suppliers, partiesId, releasesId):

    df_tenderers = df_tenderers_input.copy()
               
    df_tenderers['sequence'] = df_tenderers_input.groupby([partiesId]).cumcount()+1   

    #df_tenderers['key'] = df_tenderers[partiesId]
    #df_suppliers['key'] = df_suppliers[partiesId]

 
    df_tenderers = df_tenderers[df_tenderers['sequence'] == 1]
    df_redflag = pd.merge(df_suppliers, df_tenderers, how='inner', 
                   left_on=[partiesId, releasesId], 
                  right_on=[partiesId, releasesId])
    
    
    df_redflag['appaltipop:releases/0/redflag/code'] = '04'
    df_redflag['appaltipop:releases/0/redflag/description'] = 'Il partecipante che non ha mai fatto un\'offerta in precedenza vince la gara'
    
    df_redflag.rename(columns={releasesId: 'ocds:releases/0/id'}, inplace=True)
    

    return  df_redflag[['ocds:releases/0/id', 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description']]
    
    
  




def redflag_05 (df_suppliers, releasesId, amount):

               
       
    
    df_suppliers_nan = df_suppliers[(df_suppliers['releases/0/parties/0/id'] == 'IT-CF-NAN') & (df_suppliers['releases/0/awards/0/value/amount'] == 0) & (df_suppliers['releases/0/id'].str.contains('IDM') == False)]

    df_suppliers_nan['appaltipop:releases/0/redflag/code'] = '05'
    df_suppliers_nan['appaltipop:releases/0/redflag/description'] = 'L\'appalto presenta un vincitore con codice fiscale nullo'

    df_redflag = df_suppliers_nan[[releasesId, 'appaltipop:releases/0/redflag/code', 'appaltipop:releases/0/redflag/description']]
    df_redflag.rename(columns={releasesId: 'ocds:releases/0/id'})
    
    return df_redflag
    
    