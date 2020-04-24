import pandas as pd

class News():
    def __init__(self,path='./data/',pattern='macro'):
        self.path=path
        self.pattern=pattern
        
        ##### TABLES PARAMS ##### 
        self.df_tpc=pd.read_csv(f'{path}{pattern}_topics.csv', index_col=0)
        self.selected_topics=[str(tpc).lower() for tpc in self.df_tpc.index.values]
        self.topic_title='Top Mentions in the News'

        # AUTHOR table
        self.df_aut=pd.read_csv(f'{path}{pattern}_authors.csv', index_col=0)
        self.col_entity='ner_company' #'original_user'
        self.default_category='us' #'ai' --> needs to be lowercase
        self.authors_limit=30
        self.authors_title='Nr Articles by Company in topic'
        

        df_tim=pd.read_csv(f'{path}{pattern}_time.csv', index_col=0)
        df_tim['time']=df_tim.time.apply(lambda x: x[:5])
        self.df_tim=df_tim

        # BODY table
        self.sort_col='Date' # 'Favs'
        self.sort_ascending=False
        txt_cols_rename={'publisher': 'Publisher','date_pres': 'Date',
                            'title':'Title', 
                         'ner_company': 'Companies', 'body': 'Content'}

        df_txt=pd.read_csv(f'{path}{pattern}_body.csv', index_col=0)
        df_txt=df_txt.rename(columns=txt_cols_rename)

        df_txt['Date']=df_txt.Date.apply(lambda x: x[:5])
        df_txt['Content']=df_txt.Content.apply(lambda x: str(x)[:250])
        df_txt['Hashtags_lower']=df_txt.ner_othr.apply(lambda x: [z.lower() for z in eval(x)])
        self.df_txt=df_txt
        self.cols_from_txt=['url','Publisher','Title','Content', 'Date', 'Companies']

nws_m=News(pattern='macro')
nws_c=News(pattern='company')


def select_nws(title):
    if title.upper().startswith('COMPANY'):
        n=nws_c
    elif title.upper().startswith('MACRO'):
        n=nws_m

    return n