create table if not exists ohlc_monthly
(
    ticker         text           not null,
    year           integer        not null,
    month          integer        not null check ( month between 1 and 12),
    last_refreshed date           not null,
    open           numeric(21, 6) not null,
    high           numeric(21, 6) not null,
    low            numeric(21, 6) not null,
    close          numeric(21, 6) not null,
    volume         integer        not null,
    primary key (ticker, year, month)
);

vacuum;