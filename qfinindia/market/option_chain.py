import pandas as pd
from dataclasses import dataclass
from typing import Optional


REQUIRED_COLUMNS = {"type", "strike", "expiry", "price"}
OPTION_TYPES = {"C", "P"}


@dataclass
class OptionChain:
    data: pd.DataFrame
    underlying: Optional[float] = None
    timestamp: Optional[pd.Timestamp] = None

    # ---------- Constructors ----------

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, underlying=None, timestamp=None):
        cls._validate_schema(df)
        return cls(df.copy(), underlying, timestamp)

    @classmethod
    def from_csv(cls, path: str, **kwargs):
        df = pd.read_csv(path)
        return cls.from_dataframe(df, **kwargs)

    @classmethod
    def from_dict(cls, data: dict, **kwargs):
        df = pd.DataFrame(data)
        return cls.from_dataframe(df, **kwargs)

    @classmethod
    def from_nse(cls, json_data: dict):
        from qfinindia.data.nse import parse_nse_chain
        df, underlying, timestamp = parse_nse_chain(json_data)
        return cls(df, underlying, timestamp)

    # ---------- Validation ----------

    @staticmethod
    def _validate_schema(df: pd.DataFrame):
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        if not set(df["type"].unique()).issubset(OPTION_TYPES):
            raise ValueError("Option type must be C or P")

        df["expiry"] = pd.to_datetime(df["expiry"])

    # ---------- Filters ----------

    def calls(self):
        return OptionChain(
            self.data[self.data.type == "C"],
            self.underlying,
            self.timestamp
        )

    def puts(self):
        return OptionChain(
            self.data[self.data.type == "P"],
            self.underlying,
            self.timestamp
        )

    def expiry(self, expiry):
        expiry = pd.to_datetime(expiry)
        return OptionChain(
            self.data[self.data.expiry == expiry],
            self.underlying,
            self.timestamp
        )

    # ---------- Accessors ----------

    def strikes(self):
        return self.data["strike"].values

    def prices(self):
        return self.data["price"].values

    def iv(self):
        if "iv" not in self.data.columns:
            raise ValueError("IV column missing")
        return self.data["iv"].values

    def to_dataframe(self):
        return self.data.copy()
