# 📡 DASH AI TRADING COACH COMMAND CENTER

> **FOR EDUCATION AND PAPER TRADING ONLY — NOT FINANCIAL ADVICE**

A professional-grade Python trading scanner and signal dashboard.  
Scan stocks, crypto, and ETFs with multi-timeframe analysis, Fibonacci detection,  
liquidity sweeps, trap detection, and a built-in AI trading coach.

---

## 🚀 What This App Does

| Feature | Description |
|---------|-------------|
| **Multi-TF Analysis** | Analyzes your chosen timeframe + a higher timeframe for trend bias |
| **Indicator Engine** | EMA 9/20/50/200, SMA, RSI, MACD, VWAP, ATR, Relative Volume |
| **Signal Scoring** | 0–100 CALL and PUT scores with transparent reasoning |
| **Signal Labels** | STRONG CALL / WATCH CALL / STRONG PUT / WATCH PUT / CHOP / NO TRADE |
| **Fibonacci** | Auto-detected swing high/low, golden pocket (50–61.8%), 0.786 invalidation |
| **Absorption Candles** | Detects bullish absorption and bearish rejection candles |
| **Liquidity Sweeps** | Detects smart-money sweeps above highs and below lows |
| **Trap Detection** | Bull trap and bear trap alerts with confidence reduction |
| **Risk Engine** | Entry, stop, TP1, TP2, max risk $, options budget, R:R ratio |
| **Options Guidance** | DTE, delta, strike guidance for calls and puts |
| **Coach Voice** | Plain-English coach explanation for every signal |
| **Full Chart** | Plotly candlestick with all overlays, Fib levels, trade plan lines |
| **Summary Table** | Sortable scanner table with all key stats |

---

## 📦 Installation

### Option 1 — Local (VS Code / Terminal)

```bash
# 1. Clone or create folder
mkdir dash-trading && cd dash-trading

# 2. Paste app.py, requirements.txt, README.md into folder

# 3. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run
streamlit run app.py
```

### Option 2 — Replit

1. Go to https://replit.com and create a new **Python** Repl
2. Upload `app.py` and `requirements.txt`
3. In the Shell tab: `pip install -r requirements.txt`
4. Run: `streamlit run app.py --server.port 8080`

### Option 3 — Google Colab (with ngrok tunnel)

```python
!pip install streamlit yfinance pandas numpy ta plotly -q
!nohup streamlit run app.py &
# Use ngrok or localtunnel to expose the port
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

---

## 📈 Default Ticker List (70+ tickers)

### Stocks
```
SPY, QQQ, AAPL, MSFT, NVDA, AMD, META, AMZN, GOOGL, TSLA,
AVGO, QCOM, MU, MRVL, TSM, INTC, SMCI, ON, AMAT, LRCX,
PLTR, ORCL, CRM, SNOW, DDOG, NET, PATH, AI, SOUN, BBAI,
IONQ, RGTI, QUBT, QBTS, ARQQ,
COIN, MARA, RIOT, MSTR, CLSK, HUT, IREN, BTBT,
RKLB, LUNR, SPCE, LMT, RTX, NOC,
SOFI, HOOD, NBIS, ACHR, JOBY,
CEG, VST, NRG, LEU, SMR, OKLO
```

### Crypto
```
BTC-USD, ETH-USD, SOL-USD, BNB-USD, XRP-USD,
ADA-USD, AVAX-USD, DOGE-USD, LINK-USD, DOT-USD,
UNI-USD, AAVE-USD, FET-USD, RENDER-USD, GRT-USD,
ARB-USD, OP-USD, INJ-USD, NEAR-USD, TON-USD,
SHIB-USD, PEPE-USD, LTC-USD, BCH-USD
```

### ETFs
```
SOXL, TQQQ, SPXL, SOXS, SQQQ, UVXY,
XLK, XLF, XLE, SMH, ARKK, IBIT
```

---

## ➕ Adding Custom Tickers

In the **sidebar**, type any ticker(s) into the **Custom Tickers** box:

```
META, HIMS, RCAT, NVDX, BTC-USD
```

Custom tickers appear **first** in the scan.

---

## ⚙️ Sidebar Controls

| Control | What it does |
|---------|-------------|
| **Ticker checkboxes** | Toggle stocks / crypto / ETFs on or off |
| **Custom tickers** | Add your own comma-separated tickers |
| **Analysis timeframe** | 1m / 5m / 15m / 30m / 1h / 1d |
| **Account size** | Your paper trading account size |
| **Risk per trade %** | Default 1% — max dollar risk per trade |
| **Max option spend %** | Max % of account on a single options contract |
| **R:R target** | Reward-to-risk ratio target |
| **ATR stop multiplier** | How far below entry to place stop (in ATR units) |
| **ATR TP1 / TP2** | Take-profit distances in ATR units |
| **Min score filter** | Only show tickers above this score |
| **Auto-refresh** | Refreshes scan every 60 seconds |
| **Scan Now** | Manual refresh button |

---

## 📊 Understanding the Signals

| Signal | Meaning |
|--------|---------|
| `STRONG CALL / LONG` | High-confidence bullish setup (CALL score ≥ 80) |
| `WATCH CALL / LONG` | Building bullish — wait for confirmation |
| `STRONG PUT / SHORT` | High-confidence bearish setup (PUT score ≥ 80) |
| `WATCH PUT / SHORT` | Building bearish — wait for confirmation |
| `CHOP / DANGER` | Both scores elevated — mixed signals, avoid |
| `NO TRADE` | No edge — both scores low |
| `WAIT FOR CONFIRMATION` | Developing setup, not ready yet |

---

## 🧠 Scoring System

Each score is built from these factors (max 100):

**CALL Score:**
- +15 EMAs stacked bullish (9 > 20 > 50)
- +10 Price above EMA 200
- +10 Price above VWAP
- +10 RSI in bullish zone (50–70)
- +10 MACD above signal
- +10 MACD histogram rising
- +15 Relative volume > 1.3×
- +10 Breaking above resistance
- +10 Price in / reclaiming golden pocket
- +10 Bullish absorption candle
- +10 Higher timeframe bias bullish
- -25 Bull trap detected

---

## ⚠️ Risk Warning

- This app is **for education and paper trading only**.
- Signals are based on technical analysis — **not guaranteed to be profitable**.
- No algorithm predicts the market with certainty.
- Always apply your own judgment.
- Use a paper trading account to practice before using real money.
- Never risk money you cannot afford to lose.
- Options trading involves **substantial risk of loss**.

---

## 💡 How to Use This App Like a Coach

1. **Start with the summary table** — sort by highest score
2. **Look for STRONG signals** with a score ≥ 70
3. **Check the higher TF bias** — trade WITH the trend, not against it
4. **Look for volume confirmation** — rel vol > 1.3× means real participation
5. **Read the coach message** — it explains the setup in plain English
6. **Set your stop BEFORE you enter** — discipline saves accounts
7. **Take partial profit at TP1**, trail stop to entry, target TP2 for runners
8. **Never chase** — if you missed the entry trigger, wait for the next setup
9. **Use the trap and sweep warnings** — they flag when to stand down
10. **Trust the NO TRADE signal** — no edge is a valid edge

---

## 🛠️ Tech Stack

- `streamlit` — interactive web dashboard
- `yfinance` — free market data via Yahoo Finance
- `pandas` / `numpy` — data processing
- `plotly` — interactive candlestick charts
- `ta` — technical analysis library (optional supplement)
- `requests` — HTTP utilities

---

## 📄 License

MIT — free to use, modify, and distribute.  
Attribution appreciated but not required.

---

*Built by Dash AI Trading Coach. Not affiliated with any broker or financial institution.*
