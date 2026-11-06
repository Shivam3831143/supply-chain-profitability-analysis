
from pathlib import Path

import pandas as pd
import streamlit as st


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATA_PATH = PROJECT_ROOT / "dataset" / "APL_Logistics_dataset.csv"


@st.cache_data
def load_data():
    """
    Load and prepare the supply chain dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # Create Net Revenue column
    df["Net Revenue"] = df["Order Item Total"]

    # Create Profit Status column
    df["Profit Status"] = df["Benefit per order"].apply(
        lambda x: (
            "Profitable" if x > 0
            else "Loss-making" if x < 0
            else "Zero Profit"
        )
    )

    return df
