import pandas as pd


def parse_nse_chain(json_data):
    records = []

    underlying = json_data["records"].get("underlyingValue")
    timestamp = pd.to_datetime(json_data["records"].get("timestamp"))

    for row in json_data["records"]["data"]:
        strike = row["strikePrice"]
        expiry = row["expiryDate"]

        if "CE" in row:
            ce = row["CE"]
            records.append({
                "type": "C",
                "strike": strike,
                "expiry": expiry,
                "price": ce.get("lastPrice"),
                "iv": ce.get("impliedVolatility"),
                "oi": ce.get("openInterest")
            })

        if "PE" in row:
            pe = row["PE"]
            records.append({
                "type": "P",
                "strike": strike,
                "expiry": expiry,
                "price": pe.get("lastPrice"),
                "iv": pe.get("impliedVolatility"),
                "oi": pe.get("openInterest")
            })

    df = pd.DataFrame(records)
    df["expiry"] = pd.to_datetime(df["expiry"])

    return df, underlying, timestamp
