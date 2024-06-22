

"""

Plan is to 
- ingest any API with stock and crypto live data. 
- Maintain a portfolio of stocks and crypto [The entire wallet of liquidity pool, and also all investments with net worth]
- Record all transactions and trades


APIs for different exchanges:
- Crypto: CoinGecko API, Binance API,
- Indian Stocks: Kite Connect [ Zerodha ], 
- US Stocks: Yahoo Finance API, Alpaca API,


Steps:
- Ingest data from APIs and store in a database. This should cache all data since the begining till date.
    - Maybe make it modular because I want to learn building modules and packages.
- Create a postfolio, with all the investments and liquidity pool.
- Record all transactions and trades.
- Execute Trades based on calls from Shark
- Track and Log Performance
    - Calculate and log performance metrics (portfolio value, returns, etc.)
    - Monitor and log the health and performance of the bot
    - Set up alerts for significant events or failures (optional)

"""

