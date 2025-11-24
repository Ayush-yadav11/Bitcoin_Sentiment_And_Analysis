import pandas as pd
import os

# Define file paths
fear_greed_path = 'c:/Users/hi/Desktop/fear greed classification/fear_greed_index.csv'
historical_data_path = 'c:/Users/hi/Desktop/fear greed classification/historical_data .csv'

# Check if files exist
if not os.path.exists(fear_greed_path):
    print(f"File not found: {fear_greed_path}")
else:
    print(f"Loading {fear_greed_path}...")
    try:
        df_fg = pd.read_csv(fear_greed_path)
        print("Fear & Greed Index Head:")
        print(df_fg.head())
        print("\nFear & Greed Index Info:")
        print(df_fg.info())
    except Exception as e:
        print(f"Error loading {fear_greed_path}: {e}")

print("-" * 30)

if not os.path.exists(historical_data_path):
    print(f"File not found: {historical_data_path}")
else:
    print(f"Loading {historical_data_path}...")
    try:
        df_hist = pd.read_csv(historical_data_path)
        print("Historical Data Head:")
        print(df_hist.head())
        print("\nHistorical Data Info:")
        print(df_hist.info())
    except Exception as e:
        print(f"Error loading {historical_data_path}: {e}")
