import yfinance as yf
import pandas as pd
from textblob import TextBlob
import finnhub
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import argparse

# Load env variables
load_dotenv()
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")
client = finnhub.Client(api_key=FINNHUB_KEY) if FINNHUB_KEY else None

WATCHLIST = ['IONQ', 'QBTS', 'RGTI', 'NVDA', 'TSLA', 'PLTR', 'PATH', 'SYM', 'GOOG', 'AMD', 'AI', 'ISRG', 'MSFT', 'AAPL', 'AMZN', 'SERV', 'META', 'NIO']

def get_sentiment_score(ticker):
    if not client: return 0
    try:
        start = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        end = datetime.now().strftime('%Y-%m-%d')
        news = client.company_news(ticker, _from=start, to=end)
        
        valid_headlines = []
        for n in news:
            t = n['headline']
            if "?" in t or "Why" in t: continue # Filter garbage
            valid_headlines.append(t)
            if len(valid_headlines) >= 3: break
        
        if not valid_headlines: return 0
        scores = [TextBlob(h).sentiment.polarity for h in valid_headlines]
        return sum(scores) / len(scores)
    except: return 0

def calculate_score(row):
    # Base Score: 50
    score = 50
    
    # 1. Reward/Risk Bonus (Max +20)
    rr_ratio = (row['TARGET'] - row['Price']) / (row['Price'] - row['STOP'])
    if rr_ratio > 3.0: score += 20
    elif rr_ratio > 2.0: score += 10
    
    # 2. Relative Strength Bonus (Max +20)
    # If RS is positive (beating SPY), add points
    if row['RS_Raw'] > 0.10: score += 20
    elif row['RS_Raw'] > 0: score += 10
    
    # 3. RSI "Deep Dip" Bonus (Max +10)
    # We want oversold, but not dead. 30-40 is the sweet spot.
    if 30 < row['RSI'] < 40: score += 10
    
    return min(score, 100) # Cap at 100

def run_scored_analysis(skip_filters: bool = False):
    print(f"--- 🛡️ SCORING ENGINE ACTIVATED: {datetime.now().date()} ---")
    results = []
    
    # Benchmark Data
    spy = yf.Ticker('SPY').history(period='1y')['Close']
    
    for ticker in WATCHLIST:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y")
            # Minimum history requirements:
            # - default mode: require 200 days for SMA200 calculations
            # - skip_filters mode: allow shorter history (20) so we can still compute ATR/SMA20
            if not skip_filters and len(df) < 200:
                continue
            if skip_filters and len(df) < 20:
                continue
            
            # Technicals
            curr = df.iloc[-1]
            sma200 = df['Close'].rolling(200).mean().iloc[-1]
            sma20 = df['Close'].rolling(20).mean().iloc[-1]
            atr = (df['High'] - df['Low']).rolling(14).mean().iloc[-1]
            
            # RS Calculation
            stock_ret = (curr['Close'] / df['Close'].iloc[-63]) - 1
            spy_ret = (spy.iloc[-1] / spy.iloc[-63]) - 1
            rs_raw = stock_ret - spy_ret
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
            
            # Compute recommended levels
            entry = curr['High'] * 1.005
            stop = curr['Close'] - (2 * atr)
            target = curr['Close'] + (4 * atr)

            if skip_filters:
                # Bypass technical + sentiment gates — useful for quickly inspecting levels
                trade = {
                    'Ticker': ticker,
                    'Price': round(curr['Close'], 2),
                    'RSI': round(rsi, 1),
                    'RS_Raw': rs_raw,
                    'Sentiment': 'Skipped',
                    'BUY_AT': round(entry, 2),
                    'STOP': round(stop, 2),
                    'TARGET': round(target, 2)
                }
                trade['SCORE'] = calculate_score(trade)
                results.append(trade)
            else:
                # Filters: Uptrend + Pullback
                if curr['Close'] > sma200 and curr['Close'] < sma20:
                    sentiment = get_sentiment_score(ticker)
                    
                    if sentiment > -0.05:
                        trade = {
                            'Ticker': ticker,
                            'Price': round(curr['Close'], 2),
                            'RSI': round(rsi, 1),
                            'RS_Raw': rs_raw, # Hidden helper for math
                            'Sentiment': round(sentiment, 2),
                            'BUY_AT': round(entry, 2),
                            'STOP': round(stop, 2),
                            'TARGET': round(target, 2)
                        }
                        trade['SCORE'] = calculate_score(trade)
                        results.append(trade)
                    
        except Exception: continue

    if results:
        df = pd.DataFrame(results)
        
        # FIX: Sort by Score, then reset the numbering to start at 0, 1, 2...
        df = df.sort_values(by='SCORE', ascending=False).reset_index(drop=True)
        
        # Optional: Start counting at 1 instead of 0 for a "Top 10" look
        df.index = df.index + 1
        
        print("\n🏆 RANKED OPPORTUNITIES:")
        print(df[['Ticker', 'SCORE', 'Price', 'BUY_AT', 'STOP', 'TARGET']])
    else:
        print("No trades found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the lazy investor scanner.")
    parser.add_argument('--all', '--skip-filters', dest='all', action='store_true',
                        help='Bypass technical and sentiment filters and show levels for all tickers.')
    args = parser.parse_args()
    run_scored_analysis(skip_filters=args.all)
    