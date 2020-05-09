import pandas as pd

class News():
    def __init__(self,path='./data/',pattern='macro',default_category='us', lookup_column='ner_othr'):
        self.path=path
        self.pattern=pattern
        self.default_category=default_category #'ai' --> needs to be lowercase

        ##### TABLES PARAMS ##### 
        self.df_tpc=pd.read_csv(f'{path}{pattern}_topics.csv', index_col=0)
        self.selected_topics=[str(tpc).lower() for tpc in self.df_tpc.index.values]
        self.topic_title='Top Mentions in the News'

        # AUTHOR table
        self.df_aut=pd.read_csv(f'{path}{pattern}_authors.csv', index_col=0)
        self.col_entity='ent_name' #'original_user'

        self.authors_limit=30
        self.authors_title='Nr Articles by entities within the topic'
        

        df_tim=pd.read_csv(f'{path}{pattern}_time.csv', index_col=0)
        df_tim['time']=df_tim.time.apply(lambda x: x)
        self.df_tim=df_tim

        # GEO table
        geo_cols_rename={'id':'Mentions', 'term': 'Term'}
        df_geo=pd.read_csv(f'{path}{pattern}_geo.csv', index_col=0)
        df_geo=df_geo.rename(columns=geo_cols_rename)
        #df_geo=df_geo[['term','id','Geolocation','lat','lon']].copy()
        self.df_geo=df_geo   

        #Knowledge Graph
        df_grph=pd.read_csv(f'{path}{pattern}_graph.csv', index_col=0)
        df_grph['Hashtags_lower']=df_grph['ent_graph'].apply(lambda x: [z.lower() for z in eval(x)])
        self.df_grph=df_grph  

        # BODY table
        self.sort_col='Date' # 'Favs'
        self.sort_ascending=False
        txt_cols_rename={'publisher': 'Publisher','date_utc': 'Date',
                            'title':'Title', 'ent_name': 'Entities', 'body': 'Content', 'tickers_ls': 'Tickers'}

        df_txt=pd.read_csv(f'{path}{pattern}_body.csv', index_col=0).fillna('')
        df_txt=df_txt.rename(columns=txt_cols_rename)

        df_txt['Date']=df_txt.Date.apply(lambda x: str(x))
        df_txt['Content']=df_txt.Content.apply(lambda x: str(x))
        df_txt['Entities']=df_txt.Entities.apply(lambda x: ', '.join(eval(x)).replace('\xa0',''))
        df_txt['Tickers']=df_txt.Tickers.apply(lambda x: ', '.join(eval(x)).replace('\xa0',''))
        df_txt['Hashtags_lower']=df_txt[lookup_column].apply(lambda x: [z.lower() for z in eval(x)])
        self.df_txt=df_txt
        self.cols_from_txt=['url','Publisher','Title','Content', 'Date', 'Entities', 'Tickers']

nws_m=News(pattern='macro', default_category='trump', lookup_column='ent_othr')
nws_c=News(pattern='company', default_category='nyse', lookup_column='ent_org')


def select_nws(title):
    if title.upper().startswith('COMPANY'):
        n=nws_c
    elif title.upper().startswith('MACRO'):
        n=nws_m

    return n