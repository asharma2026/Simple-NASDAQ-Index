import pandas as pd

def avgvoldf(file):
    """
    input: NASDAQ HLCV csv
    output: Dataframe of Ticker|Volume
    """
    df = pd.read_csv(file)
    df=df[['Symbol','Volume']]
    df.rename(columns={'Symbol': 'Ticker'})
    return df