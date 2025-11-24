print("Starting script...")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Set plot style
sns.set(style="whitegrid")

# File paths
# File paths
fear_greed_path = 'fear_greed_index.csv'
historical_data_path = 'historical_data .csv'
output_dir = 'output'

def load_and_clean_data():
    print("Loading datasets...")
    
    # Load Fear & Greed Index
    try:
        print(f"Reading {fear_greed_path}...")
        df_fg = pd.read_csv(fear_greed_path)
        # Convert date to datetime
        df_fg['date'] = pd.to_datetime(df_fg['date'])
        print(f"Fear & Greed data loaded: {df_fg.shape}")
        print(df_fg.head())
    except Exception as e:
        print(f"Error loading Fear & Greed data: {e}")
        return None, None

    # Load Historical Trader Data
    try:
        print(f"Reading {historical_data_path}...")
        # Read only necessary columns to save memory/time if needed, but let's try full first
        df_hist = pd.read_csv(historical_data_path, low_memory=False)
        print(f"Historical data loaded: {df_hist.shape}")
        
        print("Converting dates...")
        # Convert Timestamp IST to datetime
        # Format appears to be DD-MM-YYYY HH:MM
        # We use dayfirst=True which is often faster/more accurate for this format
        df_hist['datetime'] = pd.to_datetime(df_hist['Timestamp IST'], dayfirst=True, errors='coerce')
        
        # Check for failed conversions
        failed_dates = df_hist['datetime'].isnull().sum()
        print(f"Failed date conversions: {failed_dates}")
        
        # Extract date for merging
        df_hist['date'] = df_hist['datetime'].dt.normalize()
        
        # Ensure numeric columns are actually numeric
        numeric_cols = ['Closed PnL', 'Size USD', 'Execution Price', 'Fee']
        for col in numeric_cols:
            df_hist[col] = pd.to_numeric(df_hist[col], errors='coerce')
            
        print("Historical data processing complete.")
    except Exception as e:
        print(f"Error loading Historical data: {e}")
        return None, None

    return df_fg, df_hist

def merge_datasets(df_fg, df_hist):
    print("Merging datasets...")
    merged_df = pd.merge(df_hist, df_fg[['date', 'value', 'classification']], on='date', how='left')
    
    missing_sentiment = merged_df['classification'].isnull().sum()
    print(f"Trades with missing sentiment data: {missing_sentiment}")
    
    return merged_df

def analyze_performance(df):
    print("\n--- Performance Analysis by Sentiment ---")
    
    sentiment_groups = df.groupby('classification')
    
    metrics = sentiment_groups.agg({
        'Closed PnL': ['count', 'sum', 'mean', 'median', 'std'],
        'Size USD': ['mean', 'sum']
    })
    
    metrics.columns = ['_'.join(col).strip() for col in metrics.columns.values]
    metrics = metrics.reset_index()
    
    win_rates = []
    for sentiment in metrics['classification']:
        group_df = df[df['classification'] == sentiment]
        wins = group_df[group_df['Closed PnL'] > 0].shape[0]
        total = group_df.shape[0]
        win_rate = (wins / total) * 100 if total > 0 else 0
        win_rates.append(win_rate)
    
    metrics['Win_Rate'] = win_rates
    
    print(metrics.sort_values('Closed PnL_sum', ascending=False))
    return metrics

def visualize_results(df, metrics):
    print(f"Saving plots to {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. Total PnL by Sentiment
        plt.figure(figsize=(10, 6))
        sns.barplot(x='classification', y='Closed PnL_sum', data=metrics, palette='viridis')
        plt.title('Total PnL by Market Sentiment')
        plt.ylabel('Total Closed PnL ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/pnl_by_sentiment.png')
        plt.close()
        
        # 2. Win Rate by Sentiment
        plt.figure(figsize=(10, 6))
        sns.barplot(x='classification', y='Win_Rate', data=metrics, palette='coolwarm')
        plt.title('Win Rate by Market Sentiment')
        plt.ylabel('Win Rate (%)')
        plt.ylim(0, 100)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/win_rate_by_sentiment.png')
        plt.close()

        # 3. Average Trade Size by Sentiment
        plt.figure(figsize=(10, 6))
        sns.barplot(x='classification', y='Size USD_mean', data=metrics, palette='magma')
        plt.title('Average Trade Size (USD) by Market Sentiment')
        plt.ylabel('Average Size ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/avg_size_by_sentiment.png')
        plt.close()
        
        # 4. PnL Distribution Boxplot
        plt.figure(figsize=(12, 8))
        lower = df['Closed PnL'].quantile(0.05)
        upper = df['Closed PnL'].quantile(0.95)
        filtered_df = df[(df['Closed PnL'] > lower) & (df['Closed PnL'] < upper)]
        
        sns.boxplot(x='classification', y='Closed PnL', data=filtered_df, palette='Set2')
        plt.title('PnL Distribution by Sentiment (5th-95th Percentile)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/pnl_distribution.png')
        plt.close()
        
        print("Plots saved successfully.")
    except Exception as e:
        print(f"Error generating plots: {e}")

def main():
    df_fg, df_hist = load_and_clean_data()
    if df_fg is None or df_hist is None:
        return
    
    merged_df = merge_datasets(df_fg, df_hist)
    
    merged_df_clean = merged_df.dropna(subset=['classification'])
    print(f"Data points for analysis: {merged_df_clean.shape[0]}")
    
    if merged_df_clean.empty:
        print("No overlapping data found!")
        return

    metrics = analyze_performance(merged_df_clean)
    visualize_results(merged_df_clean, metrics)
    
    metrics.to_csv(f'{output_dir}/sentiment_performance_metrics.csv', index=False)
    print("Analysis complete.")

if __name__ == "__main__":
    main()
