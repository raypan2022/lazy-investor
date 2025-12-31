gonna start a quick dev journal to recap what i did and write down the thought process behind my design choices

day 1 + 2: 
started the general scaffolding of my project. trying to make this project more structured than my previous investing project (ai-investing-tool, that i worked on over the summer). 

The problem with that project was that it became way too bloated and over engineered that it became difficult to add new features to it. The other issue is that i didn't get my design correct before i began implementing. I was using tools like llms to generate arbitrary stock price forecasts for me, when i should have relied on more deterministic rules/scoring methods to determine the best stocks to buy. in addition, i had no automation for sourcing stocks, which is a major deal breaker because i'm lazy and i don't want to do research to find which stocks to buy.

day 3:
doing some brainstorming for ways to source tickers, analyze news fairly, and determine the current market regime. I realized two major flaws with my current design. first, if the market conditions and economy aren't favourable at the moment, maybe it's not a good idea to swing trade at all. i need to add a filter to put this into consideration. second, not all news are created equal. some news, like "will tsla have a bullrun in 2026?" and "3 quantum stocks that could make you a fortune" are absolute garbage and should not contribute towards general sentiment of the ticker. in addition, maybe it's worth considering also scraping reddit (wallstreetbets) for sourcing stocks and sentiment analysis. all of which could contribute towards some kind of score system with each attribute have a certain weight assigned to it.
