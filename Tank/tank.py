

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
- Create a portfolio, with all the investments and liquidity pool.
    - Params to define:
        - Initial Investment
        - Liquidity Pool
        
    - Portfolio:
        - Investments
        - Net Worth
        - Portfolio Value
        - Portfolio Performance
        - Portfolio Composition
        - Portfolio Returns
        - Portfolio Risk

- Record all transactions and trades.
    Record all transactions and trades in a database.
    - Params to record:
        - Date
        - Type of Transaction
        - Asset
        - Quantity
        - Price
        - Fees
        - Total Amount

- Execute Trades based on calls from Shark
- Track and Log Performance
    - Calculate and log performance metrics (portfolio value, returns, etc.)
    - Monitor and log the health and performance of the bot
    - Set up alerts for significant events or failures (optional)

"""

