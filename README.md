# Bitcoin Sentiment & Trader Performance Analysis

This project performs an exploratory data analysis (EDA) to investigate the relationship between **Bitcoin Market Sentiment** (Fear & Greed Index) and **Trader Performance** (Historical execution data from Hyperliquid).

##  Goal
To identify hidden correlations and behavior patterns that can help design better trading strategies based on market sentiment.

##  Datasets
1.  **Bitcoin Fear & Greed Index**: Daily sentiment classification (Extreme Fear, Fear, Neutral, Greed, Extreme Greed).
2.  **Historical Trader Data**: Detailed trade execution logs including PnL, size, side, and leverage.

##  Key Findings
*   **Best Performance**: Traders achieve the highest Win Rate (~46.5%) and profitability during **Extreme Greed**.
*   **Buying the Dip**: The largest average trade sizes occur during **Fear** periods, indicating aggressive contrarian betting.
*   **The Danger Zone**: **Extreme Fear** correlates with the lowest win rates (~37%), suggesting that catching "falling knives" is risky.

##  Installation & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Analysis**:
    ```bash
    python analyze_crypto_sentiment.py
    ```
   

3.  **View Results**:
    *   Metrics are saved to `output/sentiment_performance_metrics.csv`.
    *   Visualizations are generated in the `output/` directory.

##  Visualizations
The analysis generates charts for:
*   Total PnL by Sentiment
*   Win Rate by Sentiment
*   Average Trade Size by Sentiment
*   PnL Distribution

