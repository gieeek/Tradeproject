import warnings
if __name__ == '__main__':
    import pandas as pd
    df=pd.DataFrame([])

def rename_df(df,**kwargs):
    dfcopy=df.copy()
    #if len(kwargs) < len(df.columns):
    #    warnings.warn("Not all the columns were rename")
    #for key, val in kwargs.items():
    dfcopy.rename(str.lower,axis='columns')

    return dfcopy