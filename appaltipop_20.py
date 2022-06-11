
import pandas as pd
import numpy as np
import subprocess
import json
import os
import flattentool


def flattenocds (pathocds, pathworkdir):

    a = subprocess.Popen('jq -sc ".|{releases:.}" '+ pathocds, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    b = a.stdout.read().decode('UTF-8')
    #b = a.stdout.read()
    a.stdout.close()

    z=json.dumps(b)
    y=json.loads(z)

    tmp_ocds = os.path.join(pathworkdir, "ocds_rf.json")
   

    with open(tmp_ocds, 'w', encoding='utf-8') as outfile_filtred:
        
        outfile_filtred.write(y)


    ocds_flat_path = os.path.join(pathworkdir, 'ocds_flat')


    flattentool.flatten(tmp_ocds, 
                            output_name = ocds_flat_path,
                            input_format='json',
                            root_id='ocid',
                            root_list_path='releases',
                            )
    excel_path = os.path.join(pathworkdir, 'ocds_flat.xlsx')

    return excel_path



def create_final_all (df_final_suppliers, df_final_buyers, df_final_redflags, df_final_flat):

    df_final_a = pd.merge(df_final_suppliers, df_final_buyers, how='inner', 
                   left_on='ocds:releases/0/id', 
                    right_on='ocds:releases/0/id')

    df_final_array = pd.merge(df_final_a, df_final_redflags, how='inner', 
                    left_on='ocds:releases/0/id', 
                        right_on='ocds:releases/0/id')              

    df_final_all = pd.merge(df_final_array, df_final_flat, how='inner', 
                   left_on='ocds:releases/0/id', 
                    right_on='ocds:releases/0/id')

    df_final_all.loc[df_final_all['ocds:releases/0/id'].str.startswith('IDM', na=False), 'ocds:releases/0/id'] = '0000000000'
    df_final_all['appaltipop:releases/0/tender/participants/total'] = df_final_all['appaltipop:releases/0/tender/participants/total'].fillna(0)
    df_final_all['appaltipop:releases/0/participants/total'] = df_final_all['appaltipop:releases/0/participants/total'].fillna(0)
    df_final_all['appaltipop:releases/0/participants/mean'] = df_final_all['appaltipop:releases/0/participants/mean'].fillna(0)
    df_final_all['ocds:releases/0/tender/title'] = df_final_all['ocds:releases/0/tender/title'].fillna('no title')
    #df_final_all['ocds:releases/0/tender/contractPeriod/endDate'] = df_final_all['ocds:releases/0/tender/contractPeriod/endDate'].fillna(0)
    #df_final_all['ocds:releases/0/tender/contractPeriod/startDate'] = df_final_all['ocds:releases/0/tender/contractPeriod/startDate'].fillna(0)
        


    return df_final_all 




def create_final_suppliers (df_releases, df_suppliers, df_amountByBuyer, df_nContracts):

    
    df_suppliers = df_suppliers[df_suppliers['releases/0/parties/0/id'] != 'IT-CF-NAN']
    
    df_suppliers_a =  pd.merge(df_releases, df_suppliers, how='inner', 
                    left_on='releases/0/id', 
                    right_on='releases/0/id')

    df_suppliers_b =  pd.merge(df_suppliers_a, df_amountByBuyer, how='inner', 
                    left_on=['releases/0/id', 'releases/0/parties/0/id'], 
                    right_on=['ocds:releases/0/id', 'ocds:releases/0/parties/0/id'])

    df_suppliers_c=  pd.merge(df_suppliers_b, df_nContracts, how='inner', 
                    left_on='ocds:releases/0/parties/0/id', 
                    right_on='ocds:releases/0/parties/0/id')

    df_suppliers_complete = df_suppliers_c[['releases/0/id', 'releases/0/parties/0/id','releases/0/parties/0/name', 'appaltipop:releases/0/supplier/amountByBuyers/total', 'appaltipop:releases/0/supplier/tendersByBuyers/total'
    ]]

    df_suppliers_complete.columns = ['ocds:releases/0/id','ocds:releases/0/parties/0/id','ocds:releases/0/parties/0/name', 'appaltipop:releases/0/supplier/amountByBuyers/total', 'appaltipop:releases/0/supplier/tendersByBuyers/total']

    
    
    df_suppliers_complete = df_suppliers_complete.copy()
    
    df_suppliers_complete['ocds:releases/0/parties/0/name'] = df_suppliers_complete['ocds:releases/0/parties/0/name'].fillna('no name')


    df_suppliers_array = (df_suppliers_complete.groupby(['ocds:releases/0/id'])
             .apply(lambda x: x[['ocds:releases/0/parties/0/id','ocds:releases/0/parties/0/name', 'appaltipop:releases/0/supplier/amountByBuyers/total', 'appaltipop:releases/0/supplier/tendersByBuyers/total']].to_dict('r')) 
             .reset_index()
             .rename(columns={0:'appaltipop:releases/0/suppliers'}))

    df_suppliers_nan =  pd.merge(df_releases, df_suppliers_array, how='left', 
                   left_on='releases/0/id', 
                   right_on='ocds:releases/0/id')


    df_suppliers_nan2 = df_suppliers_nan [['releases/0/id', 'appaltipop:releases/0/suppliers']]

    df_suppliers_nan2 = df_suppliers_nan2.copy()
    df_suppliers_nan2['sup'] = [np.empty(0,dtype=float)]*len(df_suppliers_nan2)
    df_suppliers_nan2['sup'] = np.where(df_suppliers_nan2['appaltipop:releases/0/suppliers'].notnull(), df_suppliers_nan2['appaltipop:releases/0/suppliers'], df_suppliers_nan2['sup'])
    df_final_suppliers = df_suppliers_nan2[['releases/0/id', 'sup']]

    df_final_suppliers.columns = ['ocds:releases/0/id', 'appaltipop:releases/0/suppliers']

    


    return df_final_suppliers 





def create_final_buyers (df_releases_buyer):

    df_final_buyers = (df_releases_buyer.groupby(['ocds:releases/0/id'])
            .apply(lambda x: x[['ocds:releases/0/buyer/id','ocds:releases/0/buyer/name']].to_dict('r'))
             .reset_index()
             .rename(columns={0:'appaltipop:releases/0/buyers'}))


    return df_final_buyers



def create_nContracts (df_suppliers):


    numero_contratti = df_suppliers.groupby(['releases/0/parties/0/id']).size()


    df_nContracts = numero_contratti.to_frame()
    df_nContracts.reset_index(inplace=True)
    df_nContracts.columns=['ocds:releases/0/parties/0/id','appaltipop:releases/0/supplier/tendersByBuyers/total']
    df_nContracts.sort_values(by=['appaltipop:releases/0/supplier/tendersByBuyers/total'], inplace=True, ascending=False)

    return df_nContracts





def create_participants(df_tenderers):

    totale_partecipanti = df_tenderers.shape[0] + 1

    totale_cig = df_tenderers['releases/0/id'].nunique()

    media_partecipanti = round(totale_partecipanti/totale_cig, 2)

    partecipanti = df_tenderers.groupby(['releases/0/id']).size()


    df_participants = partecipanti.to_frame()
    df_participants.reset_index(inplace=True)
    df_participants.columns=['ocds:releases/0/id','appaltipop:releases/0/tender/participants/total']
    df_participants['appaltipop:releases/0/participants/total'] = totale_partecipanti
    df_participants['appaltipop:releases/0/participants/mean'] = media_partecipanti



    return df_participants




def create_suppliers(df_parties):

    df_suppliers = df_parties[df_parties['releases/0/parties/0/roles'] == 'supplier']


    return df_suppliers


def create_rel(df_releases, df_awards,  df_trans, df_suppliers):



    df_all = pd.merge(df_releases, df_suppliers, how='outer', 
                    left_on='releases/0/id', 
                    right_on='releases/0/id')
        
    df_a = df_all[['releases/0/id', 'releases/0/buyer/name', 'releases/0/buyer/id', 'releases/0/tender/description', 'releases/0/tender/procurementMethodDetails',
             'releases/0/tender/tenderPeriod/startDate', 'releases/0/tender/tenderPeriod/endDate', 
             'releases/0/tender/value/amount', 'releases/0/parties/0/id',
             'releases/0/parties/0/name'
    ]]

    df_a.columns = ['ocds:releases/0/id', 'ocds:releases/0/buyer/name', 'ocds:releases/0/buyer/id','ocds:releases/0/tender/title', 'ocds:releases/0/tender/procurementMethodDetails', 'ocds:releases/0/tender/contractPeriod/startDate', 'ocds:releases/0/tender/contractPeriod/endDate',  'ocds:releases/0/awards/0/value/amount', 'ocds:releases/0/parties/0/id',
                'ocds:releases/0/parties/0/name']


    a = df_a.groupby(['ocds:releases/0/id', 'ocds:releases/0/buyer/id', 'ocds:releases/0/parties/0/id'])['ocds:releases/0/awards/0/value/amount'].sum()


    df_amountByBuyer = a.to_frame()
    df_amountByBuyer.reset_index(inplace=True)
    df_amountByBuyer.rename(columns={'ocds:releases/0/awards/0/value/amount':'appaltipop:releases/0/supplier/amountByBuyers/total'}, inplace=True)
    
    return df_amountByBuyer





def create_final(df_releases, df_awards,  df_trans, df_participants):

    #df_rel_awards =  pd.merge(df_releases, df_awards, how='left', 
    #            left_on='releases/0/id', 
    #                right_on='releases/0/id')

    #df_rel_awards_trans = pd.merge(df_rel_awards, df_trans, how='left', 
    #                left_on='releases/0/id', 
    #                    right_on='releases/0/id')

    
    df_final = pd.merge(df_releases, df_participants, how='outer', 
                    left_on='releases/0/id', 
                        right_on='ocds:releases/0/id')

    
    df_final_flat = df_final[['releases/0/id', 'releases/0/tender/description', 'releases/0/tender/procurementMethodDetails',
             'releases/0/tender/tenderPeriod/startDate', 'releases/0/tender/tenderPeriod/endDate', 
             'releases/0/tender/value/amount', 'appaltipop:releases/0/tender/participants/total',
             'appaltipop:releases/0/participants/total', 'appaltipop:releases/0/participants/mean'
    ]]

    df_final_flat.columns = ['ocds:releases/0/id', 'ocds:releases/0/tender/title', 'ocds:releases/0/tender/procurementMethodDetails',
                'ocds:releases/0/tender/contractPeriod/startDate', 'ocds:releases/0/tender/contractPeriod/endDate', 
                'ocds:releases/0/awards/0/value/amount', 'appaltipop:releases/0/tender/participants/total',
                'appaltipop:releases/0/participants/total', 'appaltipop:releases/0/participants/mean']
        
    
    return df_final_flat