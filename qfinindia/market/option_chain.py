import pandas as pd
from dataclasses import dataclass
from typing import Optional


REQUIRED_COLUMNS = {"type", "strike", "expiry", "price"}
OPTION_TYPES = {"C", "P"}


# ---------- Helpers ----------

def _normalize_option_types(series: pd.Series) -> pd.Series:
    """
    Normalize option type labels to C/P.
    Accepts: call, put, c, p, CE, PE, Call, Put, etc.
    """
    mapping = {
        "call": "C",
        "put": "P",
        "c": "C",
        "p": "P",
        "ce": "C",
        "pe": "P",
    }

    normalized = (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )

    return normalized


@dataclass
class OptionChain:
    data: pd.DataFrame
    underlying: Optional[float] = None
    timestamp: Optional[pd.Timestamp] = None

    # ---------- Constructors ----------

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, underlying=None, timestamp=None):
        df = df.copy()

        # normalize option types BEFORE validation
        df["type"] = _normalize_option_types(df["type"])

        # normalize expiry to datetime
        df["expiry"] = pd.to_datetime(df["expiry"])

        cls._validate_schema(df)
        return cls(df, underlying, timestamp)

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
        return cls.from_dataframe(df, underlying, timestamp)

    # ---------- Validation ----------

    @staticmethod
    def _validate_schema(df: pd.DataFrame):
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        if df["type"].isna().any():
            bad = df.loc[df["type"].isna(), "type"]
            raise ValueError(
                f"Invalid option type values found: {bad.unique()} "
                f"(allowed: call/put/CE/PE/c/p)"
            )

        if not set(df["type"].unique()).issubset(OPTION_TYPES):
            raise ValueError("Option type must normalize to C or P")

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
