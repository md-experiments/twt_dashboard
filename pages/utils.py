import numpy as np
import pandas as pd

class FrameStacker():
    def __init__(self):
        self.stack_cols=[]
        self.stack_values=[]

    def append(self,df):
        self.stack_values.append(df.values)
        self.stack_cols.append(df.columns)

    def stack(self):
        dt=np.vstack(self.stack_values)
        assert(all([all(self.stack_cols[i]==self.stack_cols[i+1]) \
            for i in range(len(self.stack_cols[:-1]))]))
        df_lrg=pd.DataFrame(dt, columns=self.stack_cols[0])
        self.df_lrg=df_lrg
        return df_lrg
