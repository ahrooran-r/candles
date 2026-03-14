create table if not exists ohlc_monthly
(
    ticker            text           not null,
    year              integer        not null,
    month             integer        not null,
    last_trading_date date           not null,
    high              numeric(21, 6) not null,
    low               numeric(21, 6) not null,
    volume            integer        not null,
    primary key (ticker, year, month)
);

vacuum;