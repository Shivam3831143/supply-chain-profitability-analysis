# Supply Chain Profitability Analytics

An interactive data analytics dashboard built using **Python, Pandas, NumPy, Streamlit, and Plotly** to analyze supply chain performance, customer value, product profitability, and discount impact.

## Project Overview

Supply Chain Profitability Analytics helps explore business performance through interactive visualizations and data-driven insights.

The project analyzes transaction-level logistics data to understand revenue, profit, customer behavior, product performance, market contribution, and discount strategies.

## Features

### 1. Main Dashboard
- Gross Sales and Net Revenue analysis
- Total Profit and Profit Margin
- Transaction and customer KPIs
- Profitability distribution
- Market-wise revenue and profit
- Category-wise profit analysis

### 2. Customer Analysis
- Customer-level revenue and profit analysis
- Customer segmentation
- Customer Value Index (CVI)
- High, Medium, Low, and Loss-making customer categories
- Top profitable and loss-making customers
- Customer segment performance

### 3. Product Analysis
- Top and bottom products by profit
- Category-wise profitability
- Product revenue versus profit comparison
- Product profit margin analysis
- Market, segment, category, and product filters

### 4. Discount Analysis
- Profit margin across discount bands
- Loss-making transaction rate
- Customer segment discount analysis
- Category-wise discount impact
- Product-wise discount impact
- Interactive discount performance summary

## Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Jupyter Notebook
- Git and GitHub

## Dataset

The project uses `APL_Logistics_dataset.csv`.

The dataset is maintained locally and is not included in this repository because it contains customer-related information.

To run the application, create a `dataset` folder in the project root and place the CSV file inside it:

```text
dataset/APL_Logistics_dataset.csv
```

## Project Structure

```text
Supply Chain Profitability Analytics/
│
├── .streamlit/
│   └── config.toml
│
├── dashboard/
│   ├── app.py
│   ├── requirements.txt
│   │
│   ├── pages/
│   │   ├── 1_Customer_Analysis.py
│   │   ├── 2_Product_Analysis.py
│   │   └── 3_Discount_Analysis.py
│   │
│   └── utils/
│       ├── data_loader.py
│       └── style.py
│
├── notebooks/
│   └── data_understand.ipynb
│
├── results/
│
├── .gitignore
└── README.md
```

**Note:** The `dataset/` folder is created locally and is not included in the GitHub repository.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Shivam3831143/supply-chain-profitability-analysis.git
```

### 2. Navigate to the Project Folder

```bash
cd supply-chain-profitability-analysis
```

### 3. Install Dependencies

```bash
pip install -r dashboard/requirements.txt
```

### 4. Add the Dataset

Create a folder named `dataset` in the project root and place `APL_Logistics_dataset.csv` inside it.

### 5. Run the Dashboard

```bash
python -m streamlit run dashboard/app.py
```

The dashboard will open in your browser at:

```text
http://localhost:8501
```

## Analytical Methodology

### Customer Value Index (CVI)

A custom Customer Value Index is calculated using three components:

- Profit Score: 50%
- Revenue Score: 30%
- Purchase Frequency Score: 20%

The resulting score is used to categorize customers into High Value, Medium Value, and Low Value groups. Customers with negative aggregate profit are classified separately as Loss-making.

**Note:** CVI is a custom project-specific scoring method, not an industry-standard metric.

### Discount Analysis

Transactions are grouped into six discount bands:

- 0% Discount
- Above 0–5%
- Above 5–10%
- Above 10–15%
- Above 15–20%
- Above 20–25%

Profit margin and loss-making transaction rates are compared across these bands.

## Key Dataset Insights

Based on the exploratory analysis:

- Total transactions analyzed: 180,519
- Unique customers: 20,652
- Total Net Revenue: 33,054,402.04
- Total Profit: 3,966,902.97
- Overall Profit Margin: approximately 12.00%
- Profitable transactions: 145,558
- Loss-making transactions: 33,784

These findings describe the analyzed dataset and may change when dashboard filters are applied.

## Dashboard Design

The application uses a dark professional theme with:

- Interactive Plotly visualizations
- KPI cards
- Sidebar filters
- Multi-page navigation
- Consistent chart styling
- Interactive tables and comparisons

## Future Improvements

- Predictive sales and profitability analysis
- Customer churn prediction
- Demand forecasting
- Advanced product recommendations
- Automated business insight generation
- Deployment to a cloud platform

## Author

Computer Engineering Student

Interested in Data Analytics, Artificial Intelligence, and Machine Learning.

## License

This project is intended for educational and portfolio purposes.
internship