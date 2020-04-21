import pandas as pd

class Tweets():
    def __init__(self,path='./data/',pattern='AI'):
        self.path=path
        self.pattern=pattern
        
        ##### TABLES PARAMS ##### 
        self.df_tpc=pd.read_csv(f'{path}{pattern}_topics.csv', index_col=0)
        self.selected_topics=[tpc.lower() for tpc in self.df_tpc.index.values]
        self.topic_title=f'Top 50 Hashtags for #{pattern}'
        self.topic_label='Nr Tweets'

        # AUTHOR table
        self.df_aut=pd.read_csv(f'{path}{pattern}_authors.csv', index_col=0)
        self.col_entity='original_user' 
        self.default_category='ai' 
        self.authors_limit=30
        self.authors_title='Nr Tweets by Author per Hashatag'
        
        # TIMELINE table
        df_tim=pd.read_csv(f'{path}{pattern}_time.csv', index_col=0)
        df_tim['time']=df_tim.time.apply(lambda x: x[:5])
        self.df_tim=df_tim

        # GEO table
        geo_cols_rename={'id':'Tweets', 'term': 'Term'}
        df_geo=pd.read_csv(f'{path}{pattern}_geo.csv', index_col=0)
        df_geo=df_geo.rename(columns=geo_cols_rename)
        #df_geo=df_geo[['term','id','Geolocation','lat','lon']].copy()
        self.df_geo=df_geo      

        # BODY table
        self.txt_sort_col='Favs'
        self.txt_sort_ascending=False
        txt_cols_rename={'Favorite Count': 'Favs','Retweet Count': 'RT',
                         'User': 'Author', 'Full Text': 'Content'}

        df_txt=pd.read_csv(f'{path}{pattern}_body.csv', index_col=0)
        
        df_txt=df_txt.rename(columns=txt_cols_rename)
        df_txt['Content']=df_txt.Content.apply(lambda x: x[:250])
        df_txt['Hashtags_lower']=df_txt.Hashtags.apply(lambda x: [z.lower() for z in eval(x)])
        self.df_txt=df_txt
        self.cols_from_txt=['Author','Favs','RT','Content', 'Created At', 'Location']

ai=Tweets()
tea=Tweets(pattern='TEA')
cof=Tweets(pattern='COFFEE')
mind=Tweets(pattern='MINDSET')
fert=Tweets(pattern='FERTILITY')
food=Tweets(pattern='FOOD')

def select_tw(title):
    if title.startswith('#TEA'):
        tw=tea
    elif title.startswith('#COFFEE'):
        tw=cof
    elif title.startswith('#MINDSET'):
        tw=mind
    elif title.startswith('#FERTILITY'):
        tw=fert
    elif title.startswith('#FOOD'):
        tw=food
    else:
        tw=ai

    return tw