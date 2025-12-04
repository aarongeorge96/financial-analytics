-- 1. Basic stock overview: Average price and volume by ticker
SELECT 
    ticker,
    COUNT(*) as trading_days,
    ROUND(AVG(close), 2) as avg_close,
    ROUND(MIN(close), 2) as min_close,
    ROUND(MAX(close), 2) as max_close,
    ROUND(AVG(volume), 0) as avg_volume
FROM financial_data.stock_prices
GROUP BY ticker
ORDER BY avg_close DESC;


-- 2. Daily returns: Calculate percentage change day over day
SELECT 
    ticker,
    date,
    close,
    LAG(close) OVER (PARTITION BY ticker ORDER BY date) as prev_close,
    ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
        / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) as daily_return_pct
FROM financial_data.stock_prices
ORDER BY ticker, date;


-- 3. Most volatile stocks: Highest standard deviation in daily returns
WITH daily_returns AS (
    SELECT 
        ticker,
        date,
        (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
            / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100 as daily_return
    FROM financial_data.stock_prices
)
SELECT 
    ticker,
    ROUND(STDDEV(daily_return), 2) as volatility,
    ROUND(AVG(daily_return), 2) as avg_daily_return,
    ROUND(MIN(daily_return), 2) as worst_day,
    ROUND(MAX(daily_return), 2) as best_day
FROM daily_returns
WHERE daily_return IS NOT NULL
GROUP BY ticker
ORDER BY volatility DESC;


-- 4. Economic indicators overview
SELECT 
    indicator,
    COUNT(*) as observations,
    ROUND(AVG(value), 2) as avg_value,
    ROUND(MIN(value), 2) as min_value,
    ROUND(MAX(value), 2) as max_value
FROM financial_data.economic_indicators
GROUP BY indicator;


-- 5. Latest economic readings
SELECT 
    indicator,
    date,
    value
FROM financial_data.economic_indicators
WHERE date = (SELECT MAX(date) FROM financial_data.economic_indicators WHERE indicator = economic_indicators.indicator)
ORDER BY indicator;