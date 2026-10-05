TOOLS = [
    {
        "name": "get_stock_price",
        "description": "Get the current stock price and daily change for a company.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol, e.g. AAPL, MSFT, TSLA."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_historical_prices",
        "description": "Get daily historical stock prices for a company.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol, e.g. AAPL, MSFT, TSLA."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_company_info",
        "description": "Get general company information and financial metrics.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol, e.g. AAPL, MSFT, TSLA."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_company_news",
        "description": "Get recent news articles and sentiment information for a company.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol, e.g. AAPL, MSFT, TSLA."
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_exchange_rate",
        "description": "Get the current exchange rate between two currencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_currency": {
                    "type": "string",
                    "description": "The three-letter currency code to convert from, e.g. USD, EUR, GBP."
                },
                "to_currency": {
                    "type": "string",
                    "description": "The three-letter currency code to convert to, e.g. USD, EUR, GBP."
                }
            },
            "required": ["from_currency", "to_currency"]
        }
    }
]
