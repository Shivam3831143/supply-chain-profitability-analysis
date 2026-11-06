
import html
import streamlit as st  # type: ignore[import-not-found]


def apply_dashboard_style():

    st.markdown("""
    <style>

    /* Main application background */
    .stApp {
        background-color: #0E1117;
        color: #F1F5F9;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161B26;
        border-right: 1px solid #293244;
    }

    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    /* Paragraphs and labels */
    p, label {
        color: #CBD5E1;
    }

    /* KPI card */
    .kpi-card {
        background: linear-gradient(145deg, #1E293B, #172033);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.20);
    }

    .kpi-label {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 12px;
    }

    .kpi-value {
        color: #F8FAFC;
        font-size: 25px;
        font-weight: 700;
        overflow-wrap: anywhere;
    }

    .kpi-delta {
        color: #38BDF8;
        font-size: 12px;
        margin-top: 8px;
    }

    /* Chart containers */
    [data-testid="stPlotlyChart"] {
        background-color: #161B26;
        border: 1px solid #293244;
        border-radius: 12px;
        padding: 8px;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #293244;
        border-radius: 10px;
    }

    /* Dividers */
    hr {
        border-color: #293244;
    }

    </style>
    """, unsafe_allow_html=True)


def render_kpi_card(label, value, delta=None):

    label = html.escape(str(label))
    value = html.escape(str(value))
    delta_html = ""

    if delta is not None:
        delta = html.escape(str(delta))
        delta_html = f'<div class="kpi-delta">{delta}</div>'

    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)



def apply_chart_style(fig, title=None):

    fig.update_layout(
        title=dict(
            text=title if title else fig.layout.title.text,
            font=dict(size=18, color="#F8FAFC")
        ),
        paper_bgcolor="#161B26",
        plot_bgcolor="#161B26",
        font=dict(
            family="Arial",
            size=12,
            color="#CBD5E1"
        ),
        margin=dict(l=30, r=30, t=60, b=30),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1")
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="#CBD5E1"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#293244",
            zeroline=False,
            color="#CBD5E1"
        )
    )

    return fig
