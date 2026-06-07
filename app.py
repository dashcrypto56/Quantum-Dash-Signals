# ============================================================
# DASH QUANTUM TRADING COMMAND CENTER
# Master Signal Engine · DNT System · HWR Filter · Coach
# FOR EDUCATION AND PAPER TRADING ONLY - NOT FINANCIAL ADVICE
# ============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import time
import os
from datetime import datetime, timedelta

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="DASH QUANTUM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');

/* Dark terminal base */
html, body, .stApp {
    background: #020408 !important;
    color: #c8d8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #050a12 !important;
    border-right: 1px solid #0d1f35 !important;
}
[data-testid="stSidebar"] * { color: #c8d8f0 !important; }

/* ── TOP HEADER BAR ── */
.quantum-header {
    background: linear-gradient(135deg, #020408 0%, #050d1a 50%, #020408 100%);
    border-bottom: 1px solid #0d2040;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.quantum-title {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 900;
    background: linear-gradient(90deg, #00ff88, #00ccff, #00ff88);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    letter-spacing: 3px;
}
@keyframes shimmer { to { background-position: 200% center; } }
.quantum-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: #3a5a80;
    letter-spacing: 2px;
    margin-top: 2px;
}

/* ── API STATUS DOTS ── */
.api-dots {
    display: flex;
    gap: 8px;
    align-items: center;
}
.dot-connected {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 8px #00ff88;
    animation: pulse-dot 2s infinite;
}
.dot-disconnected {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #ff3355;
    box-shadow: 0 0 8px #ff3355;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── STAT BAR ── */
.stat-bar {
    background: #030810;
    border-bottom: 1px solid #0d2040;
    padding: 8px 24px;
    display: flex;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
}
.stat-item { display: flex; align-items: center; gap: 6px; }
.stat-label { color: #2a4060; }
.stat-num { font-weight: bold; font-size: 16px; }
.stat-green { color: #00ff88; }
.stat-red { color: #ff3355; }
.stat-yellow { color: #ffcc00; }
.stat-blue { color: #00ccff; }
.stat-gray { color: #445566; }
.stat-orange { color: #ff8800; }

/* ── FILTER TABS ── */
.filter-row {
    background: #030810;
    padding: 8px 24px;
    display: flex;
    gap: 8px;
    border-bottom: 1px solid #0d2040;
}
.filter-btn {
    background: #0a1520;
    border: 1px solid #0d2040;
    color: #445566;
    padding: 4px 14px;
    border-radius: 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    cursor: pointer;
    font-weight: bold;
    letter-spacing: 1px;
}
.filter-btn-active {
    background: #00ff8815;
    border: 1px solid #00ff8840;
    color: #00ff88;
}

/* ── SIGNAL CARDS ── */
.card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding: 16px 24px;
}
@media (max-width: 1200px) { .card-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 900px) { .card-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .card-grid { grid-template-columns: 1fr; } }

.signal-card {
    background: #040c18;
    border: 1px solid #0d2040;
    border-radius: 12px;
    padding: 14px;
    position: relative;
    transition: all 0.2s;
    font-family: 'Share Tech Mono', monospace;
}
.signal-card:hover { border-color: #1a3a60; transform: translateY(-1px); }
.card-strong-call { border-color: #00ff4430; box-shadow: 0 0 20px #00ff4410; }
.card-watch-call  { border-color: #00aa3330; }
.card-strong-put  { border-color: #ff003330; box-shadow: 0 0 20px #ff003310; }
.card-watch-put   { border-color: #aa002230; }
.card-dnt         { border-color: #ff880030; }
.card-chop        { border-color: #ffcc0030; }

/* Card header */
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
}
.card-ticker {
    font-family: 'Orbitron', monospace;
    font-size: 16px;
    font-weight: 700;
    color: #e0f0ff;
    letter-spacing: 1px;
}
.card-price {
    font-family: 'Orbitron', monospace;
    font-size: 15px;
    color: #c8d8f0;
    font-weight: 700;
}
.card-score {
    font-size: 10px;
    color: #2a4060;
    text-align: right;
}

/* Signal badges */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1px;
    font-family: 'Orbitron', monospace;
}
.badge-strong-call { background: #00ff4420; color: #00ff44; border: 1px solid #00ff4440; }
.badge-watch-call  { background: #00aa2220; color: #00cc44; border: 1px solid #00aa3330; }
.badge-strong-put  { background: #ff003320; color: #ff3355; border: 1px solid #ff003340; }
.badge-watch-put   { background: #aa002220; color: #cc2244; border: 1px solid #aa002230; }
.badge-dnt         { background: #ff880020; color: #ff8800; border: 1px solid #ff880040; }
.badge-chop        { background: #ffcc0020; color: #ffcc00; border: 1px solid #ffcc0030; }
.badge-no-trade    { background: #33445520; color: #445566; border: 1px solid #33445530; }
.badge-liq         { background: #aa00ff20; color: #cc44ff; border: 1px solid #aa00ff40; }
.badge-absorb      { background: #0088ff20; color: #44aaff; border: 1px solid #0088ff40; }
.badge-reject      { background: #ff440020; color: #ff6644; border: 1px solid #ff440040; }

/* DNT warning */
.dnt-warning {
    background: #ff880010;
    border: 1px solid #ff880030;
    border-radius: 6px;
    padding: 6px 10px;
    margin: 8px 0;
    font-size: 10px;
    color: #ff8800;
    display: flex;
    align-items: center;
    gap: 6px;
}
.dnt-trigger {
    background: #ff330010;
    border: 1px solid #ff330020;
    border-radius: 4px;
    padding: 4px 8px;
    margin: 4px 0;
    font-size: 9px;
    color: #ff4455;
}

/* Mini stats row */
.mini-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    margin: 8px 0;
}
.mini-stat {
    background: #020810;
    border: 1px solid #0a1a2a;
    border-radius: 4px;
    padding: 4px 6px;
    text-align: center;
}
.mini-stat-label { font-size: 8px; color: #2a4060; display: block; }
.mini-stat-value { font-size: 12px; font-weight: bold; display: block; }
.val-green { color: #00ff88; }
.val-red   { color: #ff3355; }
.val-blue  { color: #00ccff; }
.val-yellow{ color: #ffcc00; }
.val-gray  { color: #445566; }
.val-white { color: #c8d8f0; }

/* VWAP / EMA row */
.vwap-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    margin: 4px 0;
    font-size: 10px;
}
.vwap-item { text-align: center; }
.vwap-label { color: #2a4060; font-size: 8px; display: block; }
.vwap-above { color: #00ff88; font-weight: bold; }
.vwap-below { color: #ff3355; font-weight: bold; }

/* Triggers */
.triggers-list { margin: 8px 0; }
.trigger-bull {
    font-size: 10px;
    color: #00cc66;
    padding: 1px 0;
    display: flex;
    align-items: center;
    gap: 4px;
}
.trigger-bear {
    font-size: 10px;
    color: #ff4466;
    padding: 1px 0;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Contract box */
.contract-box {
    background: #020810;
    border: 1px solid #0a1a2a;
    border-radius: 6px;
    padding: 8px;
    margin: 8px 0;
    font-size: 10px;
}
.contract-label { color: #2a4060; font-size: 9px; letter-spacing: 1px; margin-bottom: 4px; }
.contract-strike { color: #ffcc00; font-weight: bold; font-size: 12px; }
.contract-detail { color: #445566; font-size: 10px; }

/* Trade setup grid */
.trade-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
    margin: 6px 0;
}
.trade-cell {
    background: #020810;
    border: 1px solid #0a1a2a;
    border-radius: 4px;
    padding: 4px 6px;
    text-align: center;
}
.trade-label { font-size: 8px; color: #2a4060; display: block; }
.trade-entry  { color: #ffcc00; font-size: 11px; font-weight: bold; }
.trade-stop   { color: #ff4466; font-size: 11px; font-weight: bold; }
.trade-tp1    { color: #00ff88; font-size: 11px; font-weight: bold; }
.trade-tp2    { color: #00ccff; font-size: 11px; font-weight: bold; }
.trade-rr     { color: #cc44ff; font-size: 11px; font-weight: bold; }
.trade-atr    { color: #ff8800; font-size: 11px; font-weight: bold; }

/* Position sizing */
.pos-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 4px;
    margin: 4px 0;
}
.pos-cell {
    background: #020810;
    border: 1px solid #0a1a2a;
    border-radius: 4px;
    padding: 4px 6px;
}
.pos-label { font-size: 8px; color: #2a4060; display: block; }
.pos-value { font-size: 11px; color: #c8d8f0; font-weight: bold; }

/* Section labels */
.section-label {
    font-size: 8px;
    color: #2a4060;
    letter-spacing: 2px;
    margin: 8px 0 4px 0;
    text-transform: uppercase;
}

/* Rescan button */
.rescan-btn {
    width: 100%;
    background: #0a1a2a;
    border: 1px solid #0d2040;
    color: #2a5080;
    padding: 6px;
    border-radius: 6px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    cursor: pointer;
    margin-top: 8px;
    text-align: center;
}

/* Market context */
.market-bar {
    background: #030810;
    border-bottom: 1px solid #0d2040;
    padding: 6px 24px;
    display: flex;
    gap: 16px;
    align-items: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    flex-wrap: wrap;
}
.market-mood-on  { color: #00ff88; font-weight: bold; font-size: 13px; }
.market-mood-off { color: #ff3355; font-weight: bold; font-size: 13px; }
.market-mood-neu { color: #ffcc00; font-weight: bold; font-size: 13px; }
.market-idx { display: flex; align-items: center; gap: 6px; }
.idx-label { color: #2a4060; }
.idx-up   { color: #00ff88; }
.idx-down { color: #ff3355; }
.vix-high { color: #ff8800; }
.vix-low  { color: #00ff88; }

/* Crypto cards */
.crypto-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 8px 0;
}
.crypto-card {
    background: #040c18;
    border: 1px solid #0d2040;
    border-radius: 8px;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.crypto-name { font-size: 12px; color: #c8d8f0; font-weight: bold; }
.crypto-price { font-size: 11px; color: #445566; }
.crypto-up   { color: #00ff88; font-weight: bold; font-size: 12px; }
.crypto-down { color: #ff3355; font-weight: bold; font-size: 12px; }

/* Risk warning */
.risk-warn {
    background: #ff880008;
    border: 1px solid #ff880020;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 9px;
    color: #665533;
    margin-top: 8px;
    text-align: center;
    letter-spacing: 1px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #020408; }
::-webkit-scrollbar-thumb { background: #0d2040; border-radius: 2px; }

/* Streamlit overrides */
.stButton > button {
    background: #0a1a2a !important;
    border: 1px solid #0d2040 !important;
    color: #2a5080 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    border-radius: 6px !important;
    padding: 4px 12px !important;
    width: 100% !important;
}
.stButton > button:hover {
    border-color: #00ff8840 !important;
    color: #00ff88 !important;
}
.stExpander {
    background: #020810 !important;
    border: 1px solid #0a1a2a !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CONFIGURATION & DEFAULTS
# ══════════════════════════════════════════════════════════════

DEFAULT_TICKERS = [
    "SPY","QQQ","AAPL","MSFT","NVDA","TSLA","META","AMD","AMZN","GOOGL",
    "COIN","PLTR","SOFI","MARA","RIOT","MSTR","IONQ","RGTI","AVGO","MU",
    "SMCI","ARM","RKLX","HOOD","SOUN","INTC","CRM","NET","SNOW","DDOG"
]

CRYPTO_IDS = [
    ("bitcoin","BTC"),("ethereum","ETH"),("solana","SOL"),
    ("dogecoin","DOGE"),("ripple","XRP"),("cardano","ADA"),
    ("avalanche-2","AVAX"),("chainlink","LINK"),("the-open-network","TON"),
    ("pepe","PEPE")
]

# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════

if "scan_results" not in st.session_state:
    st.session_state.scan_results = []
if "last_scan" not in st.session_state:
    st.session_state.last_scan = None
if "filter_mode" not in st.session_state:
    st.session_state.filter_mode = "ALL"
if "crypto_data" not in st.session_state:
    st.session_state.crypto_data = {}
if "market_ctx" not in st.session_state:
    st.session_state.market_ctx = {}

# ══════════════════════════════════════════════════════════════
# API HELPERS
# ══════════════════════════════════════════════════════════════

def get_finnhub_key():
    return os.environ.get("FINNHUB_API_KEY","")

def check_finnhub():
    key = get_finnhub_key()
    if not key: return False
    try:
        r = requests.get(f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={key}", timeout=4)
        return r.status_code == 200
    except: return False

def get_finnhub_quote(symbol):
    key = get_finnhub_key()
    if not key: return None
    try:
        r = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}", timeout=4)
        if r.status_code == 200:
            d = r.json()
            return {"price": d.get("c",0), "change": d.get("d",0),
                    "pct": d.get("dp",0), "high": d.get("h",0), "low": d.get("l",0)}
    except: pass
    return None

def get_finnhub_sentiment(symbol):
    key = get_finnhub_key()
    if not key: return None
    try:
        r = requests.get(f"https://finnhub.io/api/v1/news-sentiment?symbol={symbol}&token={key}", timeout=4)
        if r.status_code == 200:
            d = r.json()
            bull = d.get("sentiment",{}).get("bullishPercent", 0.5)
            return {"positive": bull > 0.55, "negative": bull < 0.45, "score": bull}
    except: pass
    return None

def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "1h,24h,7d"
        }
        r = requests.get(url, params=params, timeout=6)
        if r.status_code == 200:
            return r.json()
    except: pass
    return []

def get_crypto_gainers_losers():
    data = get_crypto_data()
    if not data: return [], []
    valid = [c for c in data if c.get("price_change_percentage_24h") is not None]
    gainers = sorted(valid, key=lambda x: x["price_change_percentage_24h"], reverse=True)[:5]
    losers  = sorted(valid, key=lambda x: x["price_change_percentage_24h"])[:5]
    return gainers, losers

# ══════════════════════════════════════════════════════════════
# TECHNICAL ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════════

def compute_indicators(df):
    ind = {}
    close = df["Close"].squeeze()
    high  = df["High"].squeeze()
    low   = df["Low"].squeeze()
    vol   = df["Volume"].squeeze()

    # EMAs
    for p in [9, 20, 50, 200]:
        ind[f"ema{p}"] = float(close.ewm(span=p).mean().iloc[-1])

    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, 1e-9)
    rsi_series = 100 - (100 / (1 + rs))
    ind["rsi"] = float(rsi_series.iloc[-1])

    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9).mean()
    ind["macd"]       = float(macd_line.iloc[-1])
    ind["macd_sig"]   = float(signal_line.iloc[-1])
    ind["macd_hist"]  = float((macd_line - signal_line).iloc[-1])
    ind["macd_prev"]  = float(macd_line.iloc[-2]) if len(macd_line) > 1 else 0
    ind["macd_sig_prev"] = float(signal_line.iloc[-2]) if len(signal_line) > 1 else 0

    # ATR
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    ind["atr"] = float(tr.rolling(14).mean().iloc[-1])

    # VWAP (intraday approx)
    typical = (high + low + close) / 3
    vwap_val = (typical * vol).rolling(20).sum() / vol.rolling(20).sum()
    ind["vwap"] = float(vwap_val.iloc[-1])

    # Volume
    ind["vol_now"] = float(vol.iloc[-1])
    ind["vol_avg"] = float(vol.rolling(20).mean().iloc[-1])
    ind["rel_vol"] = round(ind["vol_now"] / max(ind["vol_avg"], 1), 2)

    # Bollinger Bands
    sma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    ind["bb_upper"]  = float((sma20 + 2*std20).iloc[-1])
    ind["bb_lower"]  = float((sma20 - 2*std20).iloc[-1])
    ind["bb_middle"] = float(sma20.iloc[-1])
    ind["bb_squeeze"]= (ind["bb_upper"] - ind["bb_lower"]) / max(ind["bb_middle"], 1) < 0.04

    # Support / Resistance
    ind["resistance"] = float(high.rolling(20).max().iloc[-1])
    ind["support"]    = float(low.rolling(20).min().iloc[-1])

    # Fibonacci
    h50 = float(high.tail(50).max())
    l50 = float(low.tail(50).min())
    diff = h50 - l50
    ind["fib_618"] = h50 - diff * 0.618
    ind["fib_382"] = h50 - diff * 0.382
    ind["fib_500"] = h50 - diff * 0.500
    ind["fib_786"] = h50 - diff * 0.786
    ind["fib_high"] = h50
    ind["fib_low"]  = l50

    # Candle patterns
    last_open  = float(df["Open"].squeeze().iloc[-1])
    last_close = float(close.iloc[-1])
    last_high  = float(high.iloc[-1])
    last_low   = float(low.iloc[-1])
    body = abs(last_close - last_open)
    rng  = last_high - last_low
    ind["absorption_bull"] = (last_close > last_open and
                               body > rng * 0.6 and
                               ind["rel_vol"] > 1.3)
    ind["rejection_bear"]  = (last_close < last_open and
                               body > rng * 0.6 and
                               ind["rel_vol"] > 1.2)

    # Liquidity sweep
    prev_high = float(high.iloc[-2]) if len(high) > 1 else last_high
    prev_low  = float(low.iloc[-2])  if len(low)  > 1 else last_low
    ind["liq_sweep_up"]   = last_high > prev_high and last_close < prev_high
    ind["liq_sweep_down"] = last_low  < prev_low  and last_close > prev_low

    # Trap detection
    ind["bull_trap"] = (last_close > ind["resistance"] and
                         last_close < last_open and
                         ind["rel_vol"] < 0.8)
    ind["bear_trap"] = (last_close < ind["support"] and
                         last_close > last_open and
                         ind["rel_vol"] < 0.8)

    return ind

# ══════════════════════════════════════════════════════════════
# SCORING ENGINE
# ══════════════════════════════════════════════════════════════

def score_ticker(symbol, price, ind, market_bull, sentiment=None):
    call_score = 0
    put_score  = 0
    call_reasons = []
    put_reasons  = []

    e9, e20, e50, e200 = ind["ema9"], ind["ema20"], ind["ema50"], ind["ema200"]
    rsi   = ind["rsi"]
    macd  = ind["macd"]
    msig  = ind["macd_sig"]
    mhist = ind["macd_hist"]
    vwap  = ind["vwap"]
    atr   = ind["atr"]
    rv    = ind["rel_vol"]

    # ── CALL scoring ──
    if e9 > e20 > e50:
        call_score += 15; call_reasons.append("EMA stack bullish")
    if price > e200:
        call_score += 10; call_reasons.append("Above EMA200")
    if price > vwap:
        call_score += 10; call_reasons.append("Above VWAP")
    if 50 < rsi < 70:
        call_score += 10; call_reasons.append("RSI bullish zone")
    if 28 <= rsi <= 42:
        call_score += 15; call_reasons.append("RSI bouncing from oversold")
    if macd > msig:
        call_score += 8; call_reasons.append("MACD bullish")
    if mhist > 0 and mhist > ind["macd_prev"] - ind["macd_sig_prev"]:
        call_score += 7; call_reasons.append("MACD momentum rising")
    if rv > 1.3:
        call_score += 12; call_reasons.append(f"Rel vol {rv}x avg")
    if price > ind["resistance"]:
        call_score += 10; call_reasons.append("Breaking above resistance")
    if ind["fib_618"] <= price <= ind["fib_500"]:
        call_score += 8; call_reasons.append("Above 0.618 fib")
    if ind["absorption_bull"]:
        call_score += 8; call_reasons.append("Bullish absorption candle")
    if ind["liq_sweep_down"]:
        call_score += 7; call_reasons.append("Liquidity sweep below lows")
    if market_bull:
        call_score += 8; call_reasons.append("Market trend bullish (SPY/QQQ)")
    if sentiment and sentiment.get("positive"):
        call_score += 5; call_reasons.append("Positive news sentiment")
    if ind["bull_trap"]:
        call_score = max(0, call_score - 25)
        call_reasons.append("⚠ Bull trap detected")

    # ── PUT scoring ──
    if e9 < e20 < e50:
        put_score += 15; put_reasons.append("EMA stack bearish")
    if price < e200:
        put_score += 10; put_reasons.append("Below EMA200")
    if price < vwap:
        put_score += 10; put_reasons.append("Below VWAP")
    if 30 < rsi < 50:
        put_score += 10; put_reasons.append("RSI bearish zone")
    if 68 <= rsi <= 82:
        put_score += 15; put_reasons.append("RSI rejected near overbought")
    if macd < msig:
        put_score += 8; put_reasons.append("MACD bearish")
    if mhist < 0:
        put_score += 7; put_reasons.append("MACD momentum falling")
    if rv > 1.3:
        put_score += 12; put_reasons.append(f"Rel vol {rv}x avg")
    if price < ind["support"]:
        put_score += 10; put_reasons.append("Breakdown under support")
    if price < ind["fib_382"]:
        put_score += 8; put_reasons.append("Lost key fib structure")
    if ind["rejection_bear"]:
        put_score += 8; put_reasons.append("Bearish rejection candle")
    if ind["liq_sweep_up"]:
        put_score += 7; put_reasons.append("Liquidity sweep above highs")
    if not market_bull:
        put_score += 8; put_reasons.append("Market trend bearish (SPY/QQQ)")
    if sentiment and sentiment.get("negative"):
        put_score += 5; put_reasons.append("Negative news sentiment")
    if ind["bear_trap"]:
        put_score = max(0, put_score - 25)
        put_reasons.append("⚠ Bear trap detected")

    call_score = min(100, call_score)
    put_score  = min(100, put_score)

    # ── DNT system ──
    dnt_triggers = []
    if rsi > 78: dnt_triggers.append(f"RSI overbought ({rsi:.0f} > 78)")
    if rsi < 22: dnt_triggers.append(f"RSI oversold ({rsi:.0f} < 22)")
    vwap_pct = abs(price - vwap) / max(vwap, 1) * 100
    if vwap_pct > 2.5: dnt_triggers.append(f"Price {vwap_pct:.1f}% from VWAP — chasing")
    if rv < 0.5: dnt_triggers.append(f"Rel vol {rv}x — no conviction")
    if call_score > 55 and put_score > 55: dnt_triggers.append("Mixed signals — choppy tape")
    if ind["bull_trap"]: dnt_triggers.append("Bull trap active")
    if ind["bear_trap"]: dnt_triggers.append("Bear trap active")
    candle_range = ind.get("atr", 1)
    if candle_range < atr * 0.3: dnt_triggers.append("Tight range vs ATR")

    is_dnt = len(dnt_triggers) >= 2

    # ── Signal label ──
    if is_dnt:
        signal = "DO NOT TRADE"
    elif call_score >= 80 and put_score < 60:
        signal = "STRONG CALL"
    elif call_score >= 65 and put_score < 60:
        signal = "WATCH CALL"
    elif put_score >= 80 and call_score < 60:
        signal = "STRONG PUT"
    elif put_score >= 65 and call_score < 60:
        signal = "WATCH PUT"
    elif call_score > 55 and put_score > 55:
        signal = "CHOP"
    else:
        signal = "NO TRADE"

    top_score = max(call_score, put_score)

    # ── Trade plan ──
    if "CALL" in signal:
        entry   = round(price * 1.001, 4)
        stop    = round(price - atr * 0.75, 4)
        tp1     = round(price + atr * 1.5, 4)
        tp2     = round(price + atr * 2.5, 4)
        rr      = round((tp1 - entry) / max(entry - stop, 0.01), 1)
    elif "PUT" in signal:
        entry   = round(price * 0.999, 4)
        stop    = round(price + atr * 0.75, 4)
        tp1     = round(price - atr * 1.5, 4)
        tp2     = round(price - atr * 2.5, 4)
        rr      = round((entry - tp1) / max(stop - entry, 0.01), 1)
    else:
        entry = stop = tp1 = tp2 = price
        rr = 0

    # ── Options suggestion ──
    direction = "CALL" if "CALL" in signal else "PUT" if "PUT" in signal else None
    strike_call = round(price * 1.01 / 5) * 5
    strike_put  = round(price * 0.99 / 5) * 5
    if direction == "CALL":
        opt_strike = strike_call
        opt_type   = "CALL"
        if top_score >= 90: dte = "0-3"; conf = 90
        elif top_score >= 80: dte = "7-14"; conf = 80
        else: dte = "7-14"; conf = 75
    elif direction == "PUT":
        opt_strike = strike_put
        opt_type   = "PUT"
        if top_score >= 90: dte = "0-3"; conf = 90
        elif top_score >= 80: dte = "7-14"; conf = 80
        else: dte = "7-14"; conf = 75
    else:
        opt_strike = round(price / 5) * 5
        opt_type = "-"; dte = "-"; conf = 0

    return {
        "symbol": symbol,
        "price": price,
        "signal": signal,
        "call_score": call_score,
        "put_score": put_score,
        "top_score": top_score,
        "call_reasons": call_reasons,
        "put_reasons": put_reasons,
        "dnt_triggers": dnt_triggers,
        "is_dnt": is_dnt,
        "indicators": ind,
        "sentiment": sentiment,
        "trade": {"entry": entry, "stop": stop, "tp1": tp1, "tp2": tp2, "rr": rr, "atr": atr},
        "option": {"strike": opt_strike, "type": opt_type, "dte": dte, "conf": conf},
    }

# ══════════════════════════════════════════════════════════════
# SCANNER
# ══════════════════════════════════════════════════════════════

def run_scan(tickers, interval, account, risk_pct, max_opt_pct):
    results = []
    fh_ok = check_finnhub()

    # Market context
    try:
        spy = yf.download("SPY", period="2d", interval="1d", progress=False)
        qqq = yf.download("QQQ", period="2d", interval="1d", progress=False)
        vix = yf.download("^VIX", period="2d", interval="1d", progress=False)
        spy_price = float(spy["Close"].squeeze().iloc[-1])
        spy_prev  = float(spy["Close"].squeeze().iloc[-2])
        qqq_price = float(qqq["Close"].squeeze().iloc[-1])
        qqq_prev  = float(qqq["Close"].squeeze().iloc[-2])
        vix_val   = float(vix["Close"].squeeze().iloc[-1])
        spy_bull  = spy_price > spy_prev
        qqq_bull  = qqq_price > qqq_prev
        market_bull = spy_bull and qqq_bull and vix_val < 25
        mood = "RISK-ON" if market_bull else "RISK-OFF" if not spy_bull and not qqq_bull else "NEUTRAL"
        st.session_state.market_ctx = {
            "mood": mood, "market_bull": market_bull,
            "spy": spy_price, "spy_chg": round((spy_price-spy_prev)/spy_prev*100,2),
            "qqq": qqq_price, "qqq_chg": round((qqq_price-qqq_prev)/qqq_prev*100,2),
            "vix": vix_val, "fh_ok": fh_ok
        }
    except:
        market_bull = True
        st.session_state.market_ctx = {"mood":"NEUTRAL","market_bull":True,
                                         "spy":0,"spy_chg":0,"qqq":0,"qqq_chg":0,"vix":0,"fh_ok":fh_ok}

    risk_amt    = account * (risk_pct / 100)
    max_opt_amt = account * (max_opt_pct / 100)

    for sym in tickers:
        try:
            df = yf.download(sym, period="60d", interval=interval, progress=False)
            if len(df) < 50: continue
            df.dropna(inplace=True)

            price = float(df["Close"].squeeze().iloc[-1])
            chg_pct = float((df["Close"].squeeze().iloc[-1] - df["Close"].squeeze().iloc[-2]) /
                             df["Close"].squeeze().iloc[-2] * 100)

            ind = compute_indicators(df)

            # Finnhub sentiment
            sentiment = None
            if fh_ok:
                sentiment = get_finnhub_sentiment(sym)

            result = score_ticker(sym, price, ind, market_bull, sentiment)
            result["chg_pct"] = round(chg_pct, 2)
            result["risk_amt"] = risk_amt
            result["max_opt"]  = max_opt_amt
            result["shares"]   = int(risk_amt / max(ind["atr"] * 0.75, 0.01))
            result["position"] = round(result["shares"] * price, 2)
            results.append(result)
        except Exception as e:
            continue

    results.sort(key=lambda x: x["top_score"], reverse=True)
    return results

# ══════════════════════════════════════════════════════════════
# CARD RENDERER
# ══════════════════════════════════════════════════════════════

def card_class(signal):
    if "STRONG CALL" in signal: return "card-strong-call"
    if "WATCH CALL"  in signal: return "card-watch-call"
    if "STRONG PUT"  in signal: return "card-strong-put"
    if "WATCH PUT"   in signal: return "card-watch-put"
    if "DO NOT"      in signal: return "card-dnt"
    if "CHOP"        in signal: return "card-chop"
    return ""

def badge_class(signal):
    if "STRONG CALL" in signal: return "badge-strong-call"
    if "WATCH CALL"  in signal: return "badge-watch-call"
    if "STRONG PUT"  in signal: return "badge-strong-put"
    if "WATCH PUT"   in signal: return "badge-watch-put"
    if "DO NOT"      in signal: return "badge-dnt"
    if "CHOP"        in signal: return "badge-chop"
    return "badge-no-trade"

def signal_arrow(signal):
    if "CALL" in signal: return "↑"
    if "PUT"  in signal: return "↓"
    if "CHOP" in signal: return "↔"
    if "DO NOT" in signal: return "⛔"
    return "—"

def render_card(r, account):
    sym    = r["symbol"]
    price  = r["price"]
    signal = r["signal"]
    score  = r["top_score"]
    cs     = r["call_score"]
    ps     = r["put_score"]
    ind    = r["indicators"]
    trade  = r["trade"]
    opt    = r["option"]
    sent   = r.get("sentiment")
    chg    = r.get("chg_pct", 0)
    chg_col = "val-green" if chg >= 0 else "val-red"
    chg_str = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"

    rsi_col  = "val-red" if ind["rsi"] > 70 else "val-green" if ind["rsi"] < 30 else "val-white"
    macd_col = "val-green" if ind["macd"] > ind["macd_sig"] else "val-red"
    rv_col   = "val-green" if ind["rel_vol"] > 1.3 else "val-yellow" if ind["rel_vol"] > 0.8 else "val-red"
    vwap_pos = "vwap-above" if price > ind["vwap"] else "vwap-below"
    vwap_txt = "Above" if price > ind["vwap"] else "Below"
    ema_pos  = "vwap-above" if price > ind["ema200"] else "vwap-below"
    ema_txt  = "Above" if price > ind["ema200"] else "Below"

    # Decide which reasons to show
    reasons = r["call_reasons"] if "CALL" in signal else r["put_reasons"]

    is_call = "CALL" in signal
    is_put  = "PUT" in signal

    coach_text = ""
    if signal == "STRONG CALL":
        coach_text = f"🚀 Strong bullish confluence on {sym}. EMAs stacked, volume confirming. Look for entry above ${trade['entry']:.2f} with stop at ${trade['stop']:.2f}."
    elif signal == "WATCH CALL":
        coach_text = f"👀 Bullish setup building on {sym}. Wait for volume confirmation and MACD crossover before entering."
    elif signal == "STRONG PUT":
        coach_text = f"🔻 Strong bearish confluence on {sym}. Price breaking down with volume. Entry below ${trade['entry']:.2f}, stop ${trade['stop']:.2f}."
    elif signal == "WATCH PUT":
        coach_text = f"👀 Bearish setup developing on {sym}. Wait for confirmation before shorting."
    elif signal == "DO NOT TRADE":
        coach_text = f"⛔ {sym} has {len(r['dnt_triggers'])} active warning(s). Stand aside and wait for conditions to clear."
    elif signal == "CHOP":
        coach_text = f"↔ {sym} is in a choppy range. Both bulls and bears are fighting. No edge — wait."
    else:
        coach_text = f"⚪ {sym} has no strong edge right now. Move on and look for better setups."

    fib_text = f"""
    🔵 High: ${ind['fib_high']:.2f} | Low: ${ind['fib_low']:.2f}<br>
    Fib 0.786: ${ind['fib_786']:.2f}<br>
    Fib 0.618: ${ind['fib_618']:.2f} (Golden)<br>
    Fib 0.500: ${ind['fib_500']:.2f}<br>
    Fib 0.382: ${ind['fib_382']:.2f}
    """

    html = f"""
<div class="signal-card {card_class(signal)}">
  <!-- Header -->
  <div class="card-header">
    <div>
      <div class="card-ticker">{sym}</div>
      <div style="font-size:11px; color:#445566;">${price:,.2f} <span class="{chg_col}">{chg_str}</span></div>
    </div>
    <div style="text-align:right;">
      <span class="badge {badge_class(signal)}">{signal_arrow(signal)} {signal}</span><br>
      <div class="card-score">{score}/100</div>
    </div>
  </div>
"""

    # DNT warnings
    if r["is_dnt"]:
        html += f'<div class="dnt-warning">⛔ DO NOT TRADE — {len(r["dnt_triggers"])} TRIGGER{"S" if len(r["dnt_triggers"])>1 else ""} ACTIVE</div>'
        for t in r["dnt_triggers"][:2]:
            html += f'<div class="dnt-trigger">● {t}</div>'

    # Special badges
    badges = []
    if ind.get("liq_sweep_down") or ind.get("liq_sweep_up"):
        sweep_dir = "below lows" if ind.get("liq_sweep_down") else "above highs"
        badges.append(f'<span class="badge badge-liq">↯ Liquidity sweep {sweep_dir}</span>')
    if ind.get("absorption_bull"):
        badges.append(f'<span class="badge badge-absorb">⬛ Absorption candle</span>')
    if ind.get("rejection_bear"):
        badges.append(f'<span class="badge badge-reject">⬛ Rejection candle</span>')
    if badges:
        html += f'<div style="margin:4px 0;">{" ".join(badges)}</div>'

    # Mini stats
    macd_disp = f"+{ind['macd']:.2f}" if ind["macd"] >= 0 else f"{ind['macd']:.2f}"
    html += f"""
  <div class="mini-stats">
    <div class="mini-stat">
      <span class="mini-stat-label">RSI</span>
      <span class="mini-stat-value {rsi_col}">{ind['rsi']:.1f}</span>
    </div>
    <div class="mini-stat">
      <span class="mini-stat-label">MACD</span>
      <span class="mini-stat-value {macd_col}">{macd_disp}</span>
    </div>
    <div class="mini-stat">
      <span class="mini-stat-label">REL VOL</span>
      <span class="mini-stat-value {rv_col}">{ind['rel_vol']}x</span>
    </div>
  </div>
  <div class="vwap-row">
    <div class="vwap-item">
      <span class="vwap-label">VWAP</span>
      <span class="{vwap_pos}">{vwap_txt}</span>
    </div>
    <div class="vwap-item">
      <span class="vwap-label">EMA200</span>
      <span class="{ema_pos}">{ema_txt}</span>
    </div>
    <div class="vwap-item">
      <span class="vwap-label">ATR</span>
      <span class="vwap-above">${ind['atr']:.2f}</span>
    </div>
  </div>
"""

    # Triggers
    if reasons:
        html += '<div class="section-label">TRIGGERS</div><div class="triggers-list">'
        trigger_cls = "trigger-bull" if is_call else "trigger-bear"
        arrow = "▶" if is_call else "▶"
        for reason in reasons[:6]:
            html += f'<div class="{trigger_cls}">{arrow} {reason}</div>'
        html += '</div>'

    # Suggested contract
    if is_call or is_put:
        html += f"""
  <div class="section-label">SUGGESTED CONTRACT</div>
  <div class="contract-box">
    <span class="contract-strike">Strike ${opt['strike']} {opt['type']}</span>
    <span class="contract-detail"> &nbsp; Exp {opt['dte']} DTE</span><br>
    <span class="contract-detail">Delta 0.35-0.55 &nbsp; Conf <span style="color:#ffcc00;">{opt['conf']}%</span></span>
  </div>
"""

    # Trade setup
    if is_call or is_put:
        html += f"""
  <div class="section-label">TRADE SETUP</div>
  <div class="trade-grid">
    <div class="trade-cell"><span class="trade-label">ENTRY</span><span class="trade-entry">${trade['entry']:,.2f}</span></div>
    <div class="trade-cell"><span class="trade-label">STOP</span><span class="trade-stop">${trade['stop']:,.2f}</span></div>
    <div class="trade-cell"><span class="trade-label">R:R</span><span class="trade-rr">1:{trade['rr']}</span></div>
    <div class="trade-cell"><span class="trade-label">TP1</span><span class="trade-tp1">${trade['tp1']:,.2f}</span></div>
    <div class="trade-cell"><span class="trade-label">TP2</span><span class="trade-tp2">${trade['tp2']:,.2f}</span></div>
    <div class="trade-cell"><span class="trade-label">ATR</span><span class="trade-atr">${trade['atr']:.2f}</span></div>
  </div>
  <div class="section-label">POSITION SIZING</div>
  <div class="pos-grid">
    <div class="pos-cell"><span class="pos-label">MAX RISK</span><span class="pos-value">${r['risk_amt']:.0f}</span></div>
    <div class="pos-cell"><span class="pos-label">MAX OPTIONS</span><span class="pos-value">${r['max_opt']:.0f}</span></div>
    <div class="pos-cell"><span class="pos-label">POSITION</span><span class="pos-value">${r['position']:,.0f}</span></div>
    <div class="pos-cell"><span class="pos-label">SHARES</span><span class="pos-value">{r['shares']}</span></div>
  </div>
"""

    html += '</div>'
    return html

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:16px; font-weight:900;
    background:linear-gradient(90deg,#00ff88,#00ccff);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    letter-spacing:2px; margin-bottom:4px;">⚡ DASH QUANTUM</div>
    <div style="font-size:9px; color:#2a4060; letter-spacing:2px; margin-bottom:16px;">TRADING COMMAND CENTER</div>
    """, unsafe_allow_html=True)

    # API status dots
    fh_connected = check_finnhub()
    dots_html = '<div class="api-dots">'
    dots_html += f'<div class="dot-{"connected" if fh_connected else "disconnected"}"></div>'
    dots_html += '<div class="dot-connected"></div>'  # yfinance always on
    dots_html += '<div class="dot-connected"></div>'  # CoinGecko always on
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)
    st.markdown('<div style="font-size:9px; color:#2a4060; margin-bottom:12px;">DATA FEEDS</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Tickers
    st.markdown('<div style="font-size:10px; color:#2a4060; letter-spacing:2px;">TICKERS</div>', unsafe_allow_html=True)
    custom = st.text_input("", value=",".join(DEFAULT_TICKERS[:20]),
                            placeholder="SPY,QQQ,AAPL...", label_visibility="collapsed")
    tickers = [t.strip().upper() for t in custom.split(",") if t.strip()]

    # Timeframe
    st.markdown('<div style="font-size:10px; color:#2a4060; letter-spacing:2px; margin-top:8px;">TIMEFRAME</div>', unsafe_allow_html=True)
    interval = st.selectbox("", ["15m","5m","30m","1h","1d"], label_visibility="collapsed")

    st.markdown("---")

    # Risk settings
    st.markdown('<div style="font-size:10px; color:#2a4060; letter-spacing:2px;">RISK SETTINGS</div>', unsafe_allow_html=True)
    account = st.number_input("Account Size ($)", value=3500.0, min_value=100.0, step=100.0)
    risk_pct    = st.slider("Risk per Trade (%)", 1, 5, 2)
    max_opt_pct = st.slider("Max Option Spend (%)", 2, 20, 10)

    st.markdown("---")

    # Filters
    st.markdown('<div style="font-size:10px; color:#2a4060; letter-spacing:2px;">FILTERS</div>', unsafe_allow_html=True)
    min_score = st.slider("Min Score", 0, 100, 60)
    hwr_on    = st.checkbox("HWR Filter (High Win-Rate)", value=False)
    show_dnt  = st.checkbox("Show DNT Cards", value=True)

    st.markdown("---")

    # Scan button
    scan_now = st.button("⚡ SCAN NOW")

    # Auto refresh
    auto_refresh = st.checkbox("Auto Refresh (60s)", value=False)

    st.markdown("---")
    st.markdown('<div class="risk-warn">FOR EDUCATION & PAPER TRADING ONLY — NOT FINANCIAL ADVICE</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════

# Auto refresh logic
if auto_refresh:
    if (st.session_state.last_scan is None or
        (datetime.now() - st.session_state.last_scan).seconds > 60):
        scan_now = True

# Run scan
if scan_now or not st.session_state.scan_results:
    with st.spinner("⚡ QUANTUM SCAN RUNNING..."):
        st.session_state.scan_results = run_scan(
            tickers, interval, account, risk_pct, max_opt_pct)
        st.session_state.last_scan = datetime.now()
        gainers, losers = get_crypto_gainers_losers()
        st.session_state.crypto_data = {"gainers": gainers, "losers": losers}

results = st.session_state.scan_results
ctx     = st.session_state.market_ctx
crypto  = st.session_state.crypto_data

# ── HEADER ───────────────────────────────────────────────────
fh_ok = ctx.get("fh_ok", False)
st.markdown(f"""
<div class="quantum-header">
  <div>
    <div class="quantum-title">⚡ DASH / SCANNER</div>
    <div class="quantum-subtitle">MASTER SIGNAL ENGINE · DNT SYSTEM · HWR FILTER · 15 INDICATORS · COACH</div>
  </div>
  <div style="display:flex; align-items:center; gap:20px;">
    <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#2a4060;">
      $ ACCOUNT &nbsp;<span style="color:#00ff88; font-size:14px; font-weight:bold;">{account:,.0f}</span>
    </div>
    <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#2a4060;">
      ⏱ {st.session_state.last_scan.strftime("%H:%M:%S") if st.session_state.last_scan else "--:--"}
    </div>
    <div class="api-dots">
      <div class="dot-{"connected" if fh_ok else "disconnected"}"></div>
      <div class="dot-connected"></div>
      <div class="dot-connected"></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MARKET CONTEXT BAR ───────────────────────────────────────
mood     = ctx.get("mood","—")
mood_cls = "market-mood-on" if mood=="RISK-ON" else "market-mood-off" if mood=="RISK-OFF" else "market-mood-neu"
spy_chg  = ctx.get("spy_chg",0)
qqq_chg  = ctx.get("qqq_chg",0)
vix_val  = ctx.get("vix",0)
vix_cls  = "vix-high" if vix_val > 25 else "vix-low"

st.markdown(f"""
<div class="market-bar">
  <span class="{mood_cls}">{mood}</span>
  <span style="color:#0d2040;">|</span>
  <div class="market-idx">
    <span class="idx-label">SPY</span>
    <span style="color:#c8d8f0;">${ctx.get('spy',0):.2f}</span>
    <span class="{"idx-up" if spy_chg>=0 else "idx-down"}">{'+' if spy_chg>=0 else ''}{spy_chg:.2f}%</span>
  </div>
  <div class="market-idx">
    <span class="idx-label">QQQ</span>
    <span style="color:#c8d8f0;">${ctx.get('qqq',0):.2f}</span>
    <span class="{"idx-up" if qqq_chg>=0 else "idx-down"}">{'+' if qqq_chg>=0 else ''}{qqq_chg:.2f}%</span>
  </div>
  <div class="market-idx">
    <span class="idx-label">VIX</span>
    <span class="{vix_cls}">{vix_val:.2f}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STAT BAR ─────────────────────────────────────────────────
n_total = len(results)
n_sc = sum(1 for r in results if r["signal"]=="STRONG CALL")
n_wc = sum(1 for r in results if r["signal"]=="WATCH CALL")
n_sp = sum(1 for r in results if r["signal"]=="STRONG PUT")
n_wp = sum(1 for r in results if r["signal"]=="WATCH PUT")
n_ch = sum(1 for r in results if r["signal"]=="CHOP")
n_nt = sum(1 for r in results if r["signal"]=="NO TRADE")
n_dt = sum(1 for r in results if r["signal"]=="DO NOT TRADE")

st.markdown(f"""
<div class="stat-bar">
  <div class="stat-item"><span class="stat-label">MONITORED</span><span class="stat-num stat-blue">{n_total}</span></div>
  <span style="color:#0d2040;">|</span>
  <div class="stat-item"><span class="stat-label">STRONG CALL</span><span class="stat-num stat-green">{n_sc}</span></div>
  <div class="stat-item"><span class="stat-label">WATCH CALL</span><span class="stat-num" style="color:#00aa44;">{n_wc}</span></div>
  <span style="color:#0d2040;">|</span>
  <div class="stat-item"><span class="stat-label">STRONG PUT</span><span class="stat-num stat-red">{n_sp}</span></div>
  <div class="stat-item"><span class="stat-label">WATCH PUT</span><span class="stat-num" style="color:#aa2244;">{n_wp}</span></div>
  <span style="color:#0d2040;">|</span>
  <div class="stat-item"><span class="stat-label">CHOP</span><span class="stat-num stat-yellow">{n_ch}</span></div>
  <div class="stat-item"><span class="stat-label">NO TRADE</span><span class="stat-num stat-gray">{n_nt}</span></div>
  <div class="stat-item"><span class="stat-label">DNT</span><span class="stat-num stat-orange">{n_dt}</span></div>
</div>
""", unsafe_allow_html=True)

# ── FILTER TABS ──────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("ALL"):         st.session_state.filter_mode = "ALL"
with col2:
    if st.button("SIGNALS"):     st.session_state.filter_mode = "SIGNALS"
with col3:
    if st.button("CALLS"):       st.session_state.filter_mode = "CALLS"
with col4:
    if st.button("PUTS"):        st.session_state.filter_mode = "PUTS"
with col5:
    if st.button(f"HWR ({'ON' if hwr_on else 'OFF'})"):
        st.session_state.filter_mode = "HWR"

# ── FILTER RESULTS ───────────────────────────────────────────
fm = st.session_state.filter_mode
filtered = []
for r in results:
    sig = r["signal"]
    score = r["top_score"]
    if score < min_score: continue
    if not show_dnt and r["is_dnt"]: continue
    if fm == "SIGNALS" and sig in ["NO TRADE","CHOP","DO NOT TRADE"]: continue
    if fm == "CALLS"   and "CALL" not in sig: continue
    if fm == "PUTS"    and "PUT"  not in sig: continue
    if fm == "HWR":
        if "CALL" not in sig and "PUT" not in sig: continue
        if r["is_dnt"]: continue
        if r["trade"]["rr"] < 2.0: continue
        if score < max(min_score, 70): continue
    filtered.append(r)

# ── CARD GRID ────────────────────────────────────────────────
if not filtered:
    st.markdown("""
    <div style="text-align:center; padding:40px; color:#2a4060;
    font-family:'Share Tech Mono',monospace; font-size:14px;">
    ⚡ NO SIGNALS MATCH CURRENT FILTERS<br>
    <span style="font-size:11px; color:#1a2a40;">Try lowering min score or changing filter mode</span>
    </div>
    """, unsafe_allow_html=True)
else:
    cols = st.columns(4)
    for i, r in enumerate(filtered):
        with cols[i % 4]:
            st.markdown(render_card(r, account), unsafe_allow_html=True)
            with st.expander("💬 COACH"):
                st.markdown(f'<div style="font-size:11px; color:#8ab0d0; font-family:\'Share Tech Mono\',monospace; line-height:1.6;">{r["indicators"].get("coach","")}</div>', unsafe_allow_html=True)
                st.write(r.get("_coach", ""))
                # Coach message
                sig = r["signal"]
                price = r["price"]
                trade = r["trade"]
                if sig == "STRONG CALL":
                    st.success(f"🚀 Strong bullish confluence. Entry above ${trade['entry']:.2f}, stop ${trade['stop']:.2f}. Target ${trade['tp1']:.2f} then ${trade['tp2']:.2f}.")
                elif sig == "WATCH CALL":
                    st.info(f"👀 Bullish setup building. Wait for volume + MACD confirmation.")
                elif sig == "STRONG PUT":
                    st.error(f"🔻 Strong bearish. Entry below ${trade['entry']:.2f}, stop ${trade['stop']:.2f}. Target ${trade['tp1']:.2f}.")
                elif sig == "WATCH PUT":
                    st.warning(f"👀 Bearish setup. Wait for breakdown confirmation.")
                elif sig == "DO NOT TRADE":
                    st.error(f"⛔ {len(r['dnt_triggers'])} warning(s) active. Stand aside.")
                else:
                    st.info("⚪ No edge. Look for better setups.")
            with st.expander("📐 FIBONACCI"):
                ind = r["indicators"]
                st.markdown(f"""
                <div style="font-family:'Share Tech Mono',monospace; font-size:11px; color:#445566; line-height:2;">
                🔵 High: ${ind['fib_high']:.2f} &nbsp;|&nbsp; Low: ${ind['fib_low']:.2f}<br>
                Fib 0.786: <span style="color:#ff8800;">${ind['fib_786']:.2f}</span> (Invalidation)<br>
                Fib 0.618: <span style="color:#00ff88;">${ind['fib_618']:.2f}</span> (Golden Pocket)<br>
                Fib 0.500: <span style="color:#00ccff;">${ind['fib_500']:.2f}</span> (Mid)<br>
                Fib 0.382: <span style="color:#ffcc00;">${ind['fib_382']:.2f}</span> (Key Level)
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"🔄 RESCAN", key=f"rescan_{r['symbol']}"):
                st.rerun()

# ── CRYPTO SECTION ───────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-family:'Orbitron',monospace; font-size:14px; font-weight:700;
color:#00ccff; letter-spacing:2px; padding:8px 0;">
🔮 CRYPTO PULSE
</div>
""", unsafe_allow_html=True)

gainers = crypto.get("gainers", [])
losers  = crypto.get("losers",  [])

if gainers or losers:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="font-size:10px; color:#00ff88; letter-spacing:2px; margin-bottom:6px;">📈 TOP GAINERS 24H</div>', unsafe_allow_html=True)
        for coin in gainers:
            chg = coin.get("price_change_percentage_24h", 0)
            price = coin.get("current_price", 0)
            name  = coin.get("symbol","").upper()
            st.markdown(f"""
            <div class="crypto-card">
              <div>
                <div class="crypto-name">{name}</div>
                <div class="crypto-price">${price:,.4f}</div>
              </div>
              <div class="crypto-up">+{chg:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="font-size:10px; color:#ff3355; letter-spacing:2px; margin-bottom:6px;">📉 TOP LOSERS 24H</div>', unsafe_allow_html=True)
        for coin in losers:
            chg = coin.get("price_change_percentage_24h", 0)
            price = coin.get("current_price", 0)
            name  = coin.get("symbol","").upper()
            st.markdown(f"""
            <div class="crypto-card">
              <div>
                <div class="crypto-name">{name}</div>
                <div class="crypto-price">${price:,.4f}</div>
              </div>
              <div class="crypto-down">{chg:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
else:
    if st.button("🔮 Load Crypto Data"):
        gainers, losers = get_crypto_gainers_losers()
        st.session_state.crypto_data = {"gainers": gainers, "losers": losers}
        st.rerun()

# ── FOOTER ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px; font-family:'Share Tech Mono',monospace;
font-size:9px; color:#0d2040; letter-spacing:2px; margin-top:20px;">
⚡ DASH QUANTUM TRADING COMMAND CENTER — FOR EDUCATION AND PAPER TRADING ONLY<br>
NOT FINANCIAL ADVICE · NO GUARANTEED PROFITS · ALWAYS MANAGE YOUR OWN RISK
</div>
""", unsafe_allow_html=True)
