# Lazy Investor
Automatically helps you select stocks to invest in, with entry points and exit points suggestions. Designed specifically for **swing trading**.

## Design
The script uses strategies that are well tested and proven to have a high success rate.

### Step 1: Initial Filtering
Check if the stock currently has an uptrend and had a recent pullback. We can use the 200 day moving average to check for an uptrend and the 20 day moving average to check for a recent pullback. We only allow stocks that have these properties to advance to the next steps.

### Step 2: News sentiment
Using the **finnhub** API, we can retrive some headlines about each ticker and determine the sentiment using **textblob**.

### Step 3: Technical Analysis
Assign a score to each ticker based on some technical analysis indicators.

### Step 4: Output results
Sort the stocks based on their scores and then output the results.

## Example Output:
```
🏆 RANKED OPPORTUNITIES:
Ticker  SCORE   Price  BUY_AT    STOP  TARGET
1     AMD     80  215.61  217.13  200.60  245.64
2    PATH     80   16.85   17.45   15.17   20.21
3    ISRG     80  575.40  583.40  555.88  614.44
4      AI     70   13.95   14.47   12.68   16.50
5    AMZN     70  232.07  233.76  225.06  246.09
6    AAPL     70  273.76  275.73  265.82  289.64
7    GOOG     70  314.39  316.54  301.33  340.50
8    QBTS     70   26.15   26.89   20.98   36.49
9    META     60  658.69  663.55  626.44  723.20
10   SERV     60    9.81   10.30    8.11   13.22
11   IONQ     60   45.25   46.99   37.84   60.06
12    SYM     60   59.82   60.36   52.87   73.72
13   TSLA     60  459.64  471.75  427.54  523.84
14   RGTI     60   22.27   22.88   18.45   29.90
15    NIO     60    5.34    5.41    5.04    5.94
16   MSFT     50  487.10  490.79  474.79  511.71
17   PLTR     50  184.18  188.14  171.18  210.17
18   NVDA     50  188.22  189.70  179.78  205.10
```