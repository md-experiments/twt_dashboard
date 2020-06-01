

import json
import datetime
import pandas as pd

import os
from elasticsearch import Elasticsearch, helpers


def norm_int(i,nr_digits=6):
    res=str(i)
    res='0'*(nr_digits-len(res))+res
    return res



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    path='./data/'

    es_file='elastic_details'
    t0=datetime.datetime.now()
    with open(es_file,'r') as f:
        es_details=json.load(f)

    es=Elasticsearch(es_details['url'])

    ls_aggs=['topics','authors','time','geo','body','graph','-rpts-length']
    reports=['macro','company']

    for report in reports:
        len_files=es.get(index='cc-aggs-latest--rpts-length',id=report)['_source']
        
        for agg in ls_aggs[:6]:
            if len_files[agg]>0:
                id_ls=[report+'doc'+norm_int(i,nr_digits=6) for i in range(len_files[agg])]

                res=es.mget(index = f'cc-aggs-latest-{agg}',body = {'ids': id_ls})
                to_ls=[r.get('_source','') for r in res['docs'] if r.get('_source','')!='']
                df=pd.DataFrame.from_dict(to_ls)
                if agg=='topics':
                    df=df.set_index('Category').sort_values('Mentions', ascending=False)
                df.to_csv(f'{path}{report}_{agg}.csv')
            print(agg,len_files[agg])

    rpt_type='twt'
    ls_aggs=['topics','authors','time','geo','body']
    reports=['SPX','NASDAQ100','TSX','stoxx600','ASX','IBOV']

    for report in reports:
        len_files=es.get(index=f'{rpt_type}-aggs-latest--rpts-length',id=report)['_source']
        
        for agg in ls_aggs:
            if len_files[agg]>0:
                id_ls=[report+'doc'+norm_int(i,nr_digits=6) for i in range(len_files[agg])]

                res=es.mget(index = f'{rpt_type}-aggs-latest-{agg}',body = {'ids': id_ls})
                to_ls=[r.get('_source','') for r in res['docs'] if r.get('_source','')!='']
                df=pd.DataFrame.from_dict(to_ls)
                if agg=='topics':
                    df=df.set_index('Category').sort_values('Mentions', ascending=False)
                df.to_csv(f'{path}{report.upper()}_{agg}.csv')
            print(agg,len_files[agg])