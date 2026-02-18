class VolSurface:

    def __init__(self, df, underlying=None):
        self.df = df
        self.underlying = underlying

    @classmethod
    def from_chain(cls, chain):
        df = chain.to_dataframe().dropna(subset=["iv"])
        return cls(df, chain.underlying)
