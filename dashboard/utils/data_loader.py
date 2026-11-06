
from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Original dataset (used locally)
DATA_PATH = PROJECT_ROOT / "dataset" / "APL_Logistics_dataset.csv"

# Synthetic dataset (used when deploying)
DEMO_DATA_PATH = PROJECT_ROOT / "deployment" / "demo_dataset.csv"


@st.cache_data
def load_data():

    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)

    elif DEMO_DATA_PATH.exists():
        df = pd.read_csv(DEMO_DATA_PATH)

    else:
        raise FileNotFoundError("No dataset found.")

    df["Net Revenue"] = df["Order Item Total"]

    df["Profit Status"] = df["Benefit per order"].apply(
        lambda x: (
            "Profitable" if x > 0
            else "Loss-making" if x < 0
            else "Zero Profit"
        )
    )

    return df
