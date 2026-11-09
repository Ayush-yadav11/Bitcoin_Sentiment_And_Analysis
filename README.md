# Bitcoin Sentiment & Trader Performance Analysis

An exploratory analysis of 211,218 Hyperliquid trade fills, each matched to that day's reading of the Bitcoin Fear & Greed Index.

**[See the interactive project page →](https://ayush-yadav11.github.io/Bitcoin_Sentiment_And_Analysis/)** · [Read the full report](analysis_report.md)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)

## Goal

Find patterns between market sentiment and how these traders did, to inform strategies that take sentiment into account.

## Key findings

| Sentiment | Days in the index | Fills | Fills in profit | Closed PnL per fill | Average fill size |
|---|---|---|---|---|---|
| Extreme Greed | 326 | 39,992 | **46.49%** | **$67.89** | $3,112 |
| Greed | 633 | 50,303 | 38.48% | $42.74 | $5,737 |
| Neutral | 396 | 37,686 | 39.70% | $34.31 | $4,783 |
| Fear | 781 | 61,837 | 42.08% | $54.29 | **$7,816** |
| Extreme Fear | 508 | 21,400 | 37.06% | $34.54 | $5,350 |

- **Extreme Greed days** had the highest share of fills closed in profit (46.49%) and the most closed PnL per fill.
- **Fear days** had the most fills, the largest average size and the most closed PnL in total ($3.36M).
- **Extreme Fear days** had the lowest share of fills in profit (37.06%).

A "win" is a fill with closed PnL above zero. Opening fills book no PnL, so each rate is a share of all fills, not of closed trades. The data shows when these accounts closed in profit, not why.

## Datasets

1. **Bitcoin Fear & Greed Index** (`fear_greed_index.csv`): 2,644 daily readings from 1 February 2018 to 2 May 2025, each with its class (Extreme Fear 0 to 24, Fear 25 to 44, Neutral 45 to 54, Greed 55 to 74, Extreme Greed 75 to 100).
2. **Hyperliquid trade history** (`historical_data.csv`): one row per fill with its time (IST), price, size in USD, fee and closed PnL. The full file is not stored in this repository; place it beside the script to rerun the analysis.

## Run it

```bash
pip install -r requirements.txt
python analyze_crypto_sentiment.py
```

Metrics go to `output/sentiment_performance_metrics.csv` and the charts (total PnL, win rate, average size and PnL distribution by sentiment) to `output/`.

## Project structure

```
analyze_crypto_sentiment.py   merge on date, group by sentiment, metrics and charts
analysis_report.md            the written report with every chart
output/                       metric tables and charts
site/                         the project page (GitHub Pages) and its data/sentiment.json
```

## Author

**Ayush Yadav** · [Portfolio](https://ayush-yadav.me/) · [GitHub](https://github.com/Ayush-yadav11) · [LinkedIn](https://www.linkedin.com/in/ayushyadav2611/)
