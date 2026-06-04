import pandas as pd

def calculate_health_score(df):

    df["Health Score"] = (
        (df["Revenue (M USD)"] * 0.4) +
        (df["Market Share (%)"] * 0.3) +
        (df["Funding Amount (M USD)"] * 0.3)
    )

    return df


def top_industries(df):

    return (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )


def unicorn_candidates(df):

    return df[
        df["Valuation (M USD)"] >= 1000
    ]
