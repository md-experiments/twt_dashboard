import pandas as pd
import os

class News():
    def __init__(self,path='./data/',pattern='macro',default_category='us', lookup_column='ner_othr'):
        """
        
        pattern: used to load the relevant files
        """
        if 'ufo' in pattern.lower():
            topics_title = 'in disclosures'
            ### FOR BODY
            self.sort_col='All Entities' # 'Favs'
            self.sort_ascending=False
            txt_cols_rename={'doc_id': 'Doc ID','date': 'Date','paragraph_id':'Par. #',
                    'ppl_orgs': 'Entities', 'paragraph': 'Content', 'all_ents': 'All Entities'}
            self.cols_from_txt=['Doc ID','Par. #','Content', 'Date', 'Entities']
        else:
            topics_title = 'in the news'
            ### FOR BODY
            self.sort_col='Date' # 'Favs'
            self.sort_ascending=False
            txt_cols_rename={'publisher': 'Publisher','date_utc': 'Date',
                    'title':'Title', 'ent_name': 'Entities', 'body': 'Content', 'tickers_ls': 'Tickers'}
            self.cols_from_txt=['Publisher','Title','Content', 'Date', 'Entities', 'Tickers']

        self.path=path
        self.pattern=pattern
        #self.default_category=default_category #'ai' --> needs to be lowercase

        ##### TABLES PARAMS ##### 
        if os.path.exists(f'{path}{pattern}_topics.csv'):
            self.df_tpc=pd.read_csv(f'{path}{pattern}_topics.csv', index_col=0, lineterminator='\n')
            self.default_category=str(self.df_tpc.index[0]).lower() 

        else:
            self.df_tpc = pd.DataFrame([],columns=[])   
        self.selected_topics=[str(tpc).lower() for tpc in self.df_tpc.index.values]
        self.topic_title=f'Top Mentions {topics_title}'

        # AUTHOR table
        if os.path.exists(f'{path}{pattern}_authors.csv'):
            self.df_aut=pd.read_csv(f'{path}{pattern}_authors.csv', index_col=0, lineterminator='\n')
        else:
            self.df_aut=pd.DataFrame([],columns=[])
        self.col_entity='ent_name' #'original_user'

        self.authors_limit=30
        self.authors_title='Nr Articles by entities within the topic'
        
        # TIMELINE table
        if os.path.exists(f'{path}{pattern}_time.csv'):
            df_tim=pd.read_csv(f'{path}{pattern}_time.csv', index_col=0, lineterminator='\n')
            if len(df_tim)>0:
                df_tim = df_tim.sort_values('time',)
            self.df_tim=df_tim
        else:
            self.df_tim=pd.DataFrame([],columns=[])

        # GEO table
        if os.path.exists(f'{path}{pattern}_geo.csv'):
            geo_cols_rename={'id':'Mentions', 'term': 'Term', 'ent_loc': 'location'}
            df_geo=pd.read_csv(f'{path}{pattern}_geo.csv', index_col=0, lineterminator='\n')
            df_geo=df_geo.rename(columns=geo_cols_rename)
            #df_geo=df_geo[['term','id','Geolocation','lat','lon']].copy()
            self.df_geo=df_geo      
        else:
            self.df_geo=pd.DataFrame([],columns=[])

        #Knowledge Graph
        if os.path.exists(f'{path}{pattern}_graph.csv'):
            df_grph=pd.read_csv(f'{path}{pattern}_graph.csv', index_col=0, lineterminator='\n')
            df_grph['Hashtags_lower']=df_grph['ent_graph'].apply(lambda x: [z.lower() for z in eval(x)])
            self.df_grph=df_grph  
        else:
            self.df_grph=pd.DataFrame([],columns=[])
        # BODY table


        if os.path.exists(f'{path}{pattern}_body.csv'):
            df_txt=pd.read_csv(f'{path}{pattern}_body.csv', index_col=0, lineterminator='\n').fillna('')
            df_txt=df_txt.rename(columns=txt_cols_rename)

            df_txt['Date']=df_txt.Date.apply(lambda x: str(x))
            df_txt['Content']=df_txt.Content.apply(lambda x: str(x))
            df_txt['Entities']=df_txt.Entities.apply(lambda x: ', '.join(eval(x)).replace('\xa0',''))
            if 'Tickers' in df_txt.columns:
                df_txt['Tickers']=df_txt.Tickers.apply(lambda x: ', '.join(eval(x)).replace('\xa0',''))
            df_txt['Hashtags_lower']=df_txt[lookup_column].apply(lambda x: [z.lower() for z in eval(x)])
            self.df_txt=df_txt
        else:
            self.df_txt=pd.DataFrame([],columns=[]) 
        

#nws_m=News(pattern='macro', default_category='trump', lookup_column='ent_othr')
#nws_c=News(pattern='company', default_category='nyse', lookup_column='ent_org')

class StockTwt():
    def __init__(self,path='./data/',pattern='macro',lookup_column='ner_othr', nr_topics=50, caveats=''):

        self.path=path
        self.pattern=pattern
        self.caveats=caveats

        ##### TABLES PARAMS ##### 
        self.nr_topics=nr_topics
        ##### TABLES PARAMS ##### 
        if os.path.exists(f'{path}{pattern}_topics.csv'):
            df_tpc=pd.read_csv(f'{path}{pattern}_topics.csv', index_col=0, lineterminator='\n')
            df_tpc=df_tpc.head(self.nr_topics).copy()
            self.df_tpc=df_tpc
            self.default_category=str(self.df_tpc.index[0]).lower() #'ai' --> needs to be lowercase
        else:
            self.df_tpc = pd.DataFrame([],columns=[])
            self.default_category=''
        self.selected_topics=[str(tpc).lower() for tpc in self.df_tpc.index.values]
        self.topic_title='Top Twitter Mentions 48hrs rolling'


        # AUTHOR table
        if os.path.exists(f'{path}{pattern}_authors.csv'):
            self.df_aut=pd.read_csv(f'{path}{pattern}_authors.csv', index_col=0, lineterminator='\n')
            self.col_entity='hashtags' #'original_user'
        else:
            self.df_aut = pd.DataFrame([])
        self.authors_limit=30
        self.authors_title='Nr Articles by entities within the topic'
        
        if os.path.exists(f'{path}{pattern}_time.csv'):
            df_tim=pd.read_csv(f'{path}{pattern}_time.csv', index_col=0, lineterminator='\n')
            df_tim['time']=df_tim.time.apply(lambda x: x)
            self.df_tim=df_tim
        else:
            self.df_tim=pd.DataFrame([],columns=[])

        # GEO table
        if os.path.exists(f'{path}{pattern}_geo.csv'):
            geo_cols_rename={'id':'Mentions', 'term': 'Term'}
            df_geo=pd.read_csv(f'{path}{pattern}_geo.csv', index_col=0, lineterminator='\n')
            df_geo=df_geo.rename(columns=geo_cols_rename)
            #df_geo=df_geo[['term','id','Geolocation','lat','lon']].copy()
            self.df_geo=df_geo   
        else:
            self.df_geo=pd.DataFrame([],columns=[])
        #Knowledge Graph
        #df_grph=pd.read_csv(f'{path}{pattern}_graph.csv', index_col=0)
        #df_grph['Hashtags_lower']=df_grph['ent_graph'].apply(lambda x: [z.lower() for z in eval(x)])
        #self.df_grph=df_grph  

        # BODY table
        self.sort_col='Favs'
        self.sort_ascending=False
        txt_cols_rename={'favorite_count': 'Favs','retweet_count': 'RT', 'created': 'Created', 'location': 'Location',
                        'user': 'Author', 'full_text': 'Content', 'sentiment': 'Sentiment'}
        if os.path.exists(f'{path}{pattern}_body.csv'):
            df_txt=pd.read_csv(f'{path}{pattern}_body.csv', index_col=0, lineterminator='\n').fillna('')
            df_txt=df_txt.rename(columns=txt_cols_rename)

            df_txt['Created']=df_txt.Created.apply(lambda x: str(x))
            df_txt['Content']=df_txt.Content.apply(lambda x: str(x).replace('amp;',''))
            #df_txt['Entities']=df_txt.Entities.apply(lambda x: ', '.join(eval(x)).replace('\xa0',''))
            #df_txt['Tickers']=df_txt.Tickers.apply(lambda x: ', '.join(eval(x)).replace('\xa0',''))
            df_txt['Hashtags_lower']=df_txt[lookup_column].apply(lambda x: [z.lower() for z in eval(x)])
            self.df_txt=df_txt
        else:
            self.df_txt=pd.DataFrame([],columns=[]) 
        self.cols_from_txt=['Author','Favs','RT','Content', 'Created', 'Location', 'Sentiment']

#nws_m=News(pattern='macro', default_category='trump', lookup_column='ent_othr')
#nws_c=News(pattern='company', default_category='nyse', lookup_column='ent_org')

def select_nws(title):
    if title.upper().startswith('COMPANY'):
        n=News(pattern='company', default_category='', lookup_column='ent_org')
    elif title.upper().startswith('MACRO'):
        n=News(pattern='macro', default_category='', lookup_column='ent_othr')
    elif title.upper().startswith('UFO (CIA)'):
        n=News(pattern='UFO_CIA', default_category='', lookup_column='All Entities')
    elif title.upper().startswith('NASDAQ100'):
        caveats='''__Caveats:__ NASDAQ run follows the S&P500 run, hence companies present in both will appear mostly on S&P 500 page'''
        n=StockTwt(pattern='NASDAQ100', lookup_column='matched_symbols',caveats=caveats)
    elif title.upper().startswith('SPX'):
        n=StockTwt(pattern='SPX', lookup_column='matched_symbols')
    elif title.upper().startswith('TSX'):
        n=StockTwt(pattern='TSX', lookup_column='matched_symbols')
    elif title.upper().startswith('ASX'):
        n=StockTwt(pattern='ASX', lookup_column='matched_symbols')
    elif title.upper().startswith('STOXX600'):
        caveats='''__Caveats:__ SPX is a ticker from STOXX600, however, here this is mostly in reference to S&P500'''
        n=StockTwt(pattern='STOXX600', lookup_column='matched_symbols', caveats=caveats)
    elif title.upper().startswith('FTSE100'):
        n=StockTwt(pattern='FTSE100', lookup_column='matched_symbols')
    return n
