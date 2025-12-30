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
