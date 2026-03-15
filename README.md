# candles

Note: I have used Claude to format English and organize the content of this ReadMe file

### Project Overview

A REST API that fetches monthly market data from [Alpha Vantage](https://www.alphavantage.co/documentation/#monthly),
caches it in a local SQLite database, and exposes an endpoint that returns the annual high price, low price, and total
trading volume for a given symbol and year.

### Tech Stack

1. **Python 3.14**
2. **FastAPI** — REST API framework
3. **Uvicorn** — ASGI server
4. **SQLite** — local database (no ORM, raw SQL queries)
5. **uv** — package manager and virtual environment tool

### Reason for choosing uv as a build tool

I am not familiar with Python at all. I chose this simply because it was recommended in
the [FastAPI docs](https://fastapi.tiangolo.com/virtual-environments/#__tabbed_1_2)

### Setting up the project

**Prerequisites:** Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

**1. Install dependencies**

On Windows (PowerShell):

```powershell
.\activate.ps1
```

On Linux (I have used WSL to test. This script may fail in an actual Linux environment.
Please [refer](https://fastapi.tiangolo.com/virtual-environments/#__tabbed_1_2) here for troubleshooting):

```bash
source ./activate.sh
```

**2. Set your Alpha Vantage API key**

Open `config/alphavantage.env` and replace the value of `API_KEY`:

```env
API_KEY=your_api_key_here
```

Get a free key at https://www.alphavantage.co/support/#api-key

**3. (Optional) Configure the server**

The server runs on port `8001` by default. The HTTP Basic Auth password is set in `config/server.env`. You can change
either value there.

**4. Start the API**

The database schema is initialized automatically on startup — no separate step required.

On Windows (PowerShell):

```powershell
.\run.ps1
```

On Linux:

```bash
./run.sh
```

The API will be available at `http://localhost:8001`.

Interactive docs: `http://localhost:8001/docs`

### Request and Response

The endpoint requires HTTP Basic Auth. The password is set in `config/server.env` (default shown below). Any username is
accepted.

**Request:**

```bash
curl -L 'http://localhost:8001/symbols/IBM/annual/2025' -H 'Authorization: Basic YWhyb29yYW46XjZAV2JANGM1QEJxQTc='
```

**Response:**

```json
{
  "high": "324.9",
  "low": "214.5",
  "volume": "1189781215"
}
```

**Validation:**

- `symbol` must be between 1 and 50 non-blank characters (automatically uppercased)

- I chose 50 as upper bound because I am used to working with several exchanges that have their own symbol convention.

- For example, OPRA options support 21 character length tickers

- `year` must be between the current year minus 25 and the current year (inclusive)

- This is due to the fact that alphavantage only supports last [20+ year](https://www.alphavantage.co/documentation/#monthly)  historical data

- Since we are using free API key and limit is only 25 times per day, I don't want to waste API requests when invalid year / symbol are provided. Hence the aggressive limitation.

### Additional Architectural Decisions

**Caching behavior**

- On each request, the SQLite database is checked first.
- If no data is found for the requested symbol and year, all available monthly data for that symbol is fetched from Alpha Vantage and upserted into the database before aggregating the result.
- For the **current year**, the cache is considered stale if the latest stored `last_trading_date` in DB does not match the
  last known trading day (weekends are skipped). In that case, only the current year's monthly data is refreshed — past
  years already in the database are left untouched.
- For **past years**, data is only ever fetched once and is served from the database on all subsequent requests.
- I am assuming Alphavantage does not update a month's data once it is passed.

**Error handling**

- HTTP 401 is returned if the Basic Auth password is incorrect.
- HTTP 422 is returned for invalid path parameters (blank symbol, out-of-range year).
- `CandlesNotFoundError` is raised internally if aggregation is attempted on an empty dataset (e.g. the symbol does not
  exist in Alpha Vantage's data).
- Alpha Vantage HTTP errors are surfaced via `httpx`'s `raise_for_status()`.
- Connection and request timeouts are configurable in `config/alphavantage.env` (`CONNECT_TIMEOUT`, `REQUEST_TIMEOUT`).
