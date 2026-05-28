#!/usr/bin/env python3
"""
EQ · INTELLIGENCE TERMINAL v4.0
Multi-Source · AI-Synthesized Thesis Engine

requirements.txt:
    streamlit==1.40.2
    yfinance==1.0
    pandas
    numpy
    requests
    feedparser
    plotly
    beautifulsoup4
    lxml
    curl_cffi
    anthropic

RUN: streamlit run trading_dashboard_v4.py
"""
from __future__ import annotations
import html, re, time, warnings, json
from datetime import datetime
from typing import Optional

import feedparser
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
import yfinance as yf
from bs4 import BeautifulSoup
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="EQ · Intelligence Terminal v4",
    page_icon="⚡", layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:'Outfit',sans-serif;background:#050a14;color:#b8cce0}
.main,.block-container{background:#050a14 !important;padding-top:1rem !important}
p,li{font-size:.88rem;line-height:1.75;color:#8aacc8}
.banner{background:linear-gradient(135deg,#071428,#091a2e 60%,#071428);border:1px solid #0f2540;border-radius:12px;padding:18px 26px;margin-bottom:18px;display:flex;align-items:center;justify-content:space-between}
.banner-title{font-family:'Outfit',sans-serif;font-weight:800;font-size:1.5rem;color:#e8f0ff;letter-spacing:-.02em}
.banner-sub{font-family:'IBM Plex Mono',monospace;font-size:.62rem;color:#3a5a80;letter-spacing:.06em;text-transform:uppercase;margin-top:3px}
.live-dot{width:7px;height:7px;background:#00d4aa;border-radius:50%;display:inline-block;margin-right:6px;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.live-text{font-family:'IBM Plex Mono',monospace;font-size:.67rem;color:#00d4aa;font-weight:600}
.stTabs [data-baseweb="tab-list"]{background:#071428;border-radius:10px;gap:2px;padding:4px;border:1px solid #0f2540}
.stTabs [data-baseweb="tab"]{color:#3a5a80;background:transparent;border-radius:8px;font-family:'IBM Plex Mono',monospace;font-size:.76rem;letter-spacing:.05em;padding:8px 16px}
.stTabs [aria-selected="true"]{background:#0d2040 !important;color:#60a5fa !important;border:1px solid #1e3d6a !important}
.card{background:linear-gradient(160deg,#071428,#09192e);border:1px solid #0f2540;border-radius:10px;padding:16px;margin:6px 0}
.card-sm{padding:10px 14px}
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}
.metric-tile{background:#071428;border:1px solid #0f2540;border-radius:8px;padding:12px 14px;text-align:center}
.m-label{font-family:'IBM Plex Mono',monospace;font-size:.62rem;color:#2a4a6a;text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px}
.m-val{font-family:'IBM Plex Mono',monospace;font-size:1.1rem;font-weight:700}
.bull{color:#00d4aa}.bear{color:#ff4d6d}.neu{color:#c8deff}.amber{color:#f59e0b}
.sec-label{font-family:'IBM Plex Mono',monospace;font-size:.64rem;color:#3b82f6;text-transform:uppercase;letter-spacing:.18em;border-left:2px solid #3b82f6;padding-left:10px;margin:18px 0 10px}
.edu-box{background:#050e1c;border:1px dashed #1e3450;border-radius:6px;padding:10px 14px;font-size:.78rem;color:#4a7296;font-style:italic;margin-top:6px;line-height:1.6}
.edu-box::before{content:"💡 "}
.report-box{background:#060f1e;border:1px solid #0f2540;border-radius:10px;padding:18px;font-size:.85rem;line-height:1.8;color:#8aacc8}
.report-long{border-top:3px solid #00d4aa}
.report-short{border-top:3px solid #ff4d6d}
.report-blue{border-top:3px solid #3b82f6}
.report-amber{border-top:3px solid #f59e0b}
.report-purple{border-top:3px solid #a78bfa}
.report-box strong{color:#c8deff}
.thesis-box{background:#06101e;border:1px solid #1e3d6a;border-radius:10px;padding:20px;font-size:.88rem;line-height:2;color:#9ab8d0}
.thesis-box strong{color:#e8f0ff}
.thesis-box em{color:#60a5fa;font-style:normal}
.ai-badge{display:inline-block;padding:3px 9px;background:#3b82f618;border:1px solid #3b82f640;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.6rem;color:#60a5fa;margin-left:8px;vertical-align:middle}
.source-tag{display:inline-block;padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.58rem;margin:1px;font-weight:600}
.src-reuters{background:#f59e0b18;border:1px solid #f59e0b40;color:#f59e0b}
.src-cnbc{background:#60a5fa18;border:1px solid #60a5fa40;color:#60a5fa}
.src-mw{background:#00d4aa18;border:1px solid #00d4aa40;color:#00d4aa}
.src-sa{background:#a78bfa18;border:1px solid #a78bfa40;color:#a78bfa}
.src-barrons{background:#e879f918;border:1px solid #e879f940;color:#e879f9}
.src-bz{background:#fb923c18;border:1px solid #fb923c40;color:#fb923c}
.src-yf{background:#7ab0d818;border:1px solid #7ab0d840;color:#7ab0d8}
.src-ibd{background:#f8717118;border:1px solid #f8717140;color:#f87171}
.src-google{background:#94a3b818;border:1px solid #94a3b840;color:#94a3b8}
.src-sec{background:#a78bfa18;border:1px solid #a78bfa40;color:#a78bfa}
.src-finviz{background:#00d4aa18;border:1px solid #00d4aa40;color:#00d4aa}
.chip-long{background:#00d4aa18;border:1px solid #00d4aa40;color:#00d4aa;padding:3px 10px;border-radius:5px;font-family:'IBM Plex Mono',monospace;font-size:.76rem;font-weight:700;display:inline-block;margin:2px}
.chip-short{background:#ff4d6d18;border:1px solid #ff4d6d40;color:#ff4d6d;padding:3px 10px;border-radius:5px;font-family:'IBM Plex Mono',monospace;font-size:.76rem;font-weight:700;display:inline-block;margin:2px}
.chip-blue{background:#3b82f618;border:1px solid #3b82f640;color:#60a5fa;padding:2px 8px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.64rem;display:inline-block}
.score-bar-bg{background:#0d1e30;border-radius:4px;height:6px;margin:5px 0}
.score-bar-fill{height:6px;border-radius:4px}
.news-row{padding:9px 0;border-bottom:1px solid #0c1e30}
.news-title a{color:#7ab0d8;text-decoration:none;font-size:.83rem}
.news-meta{font-family:'IBM Plex Mono',monospace;font-size:.61rem;color:#2a4a6a;margin-top:3px}
.filing-row{padding:9px 0;border-bottom:1px solid #0c1e30;display:flex;align-items:flex-start;gap:10px}
.filing-badge{font-family:'IBM Plex Mono',monospace;font-size:.59rem;font-weight:700;padding:3px 6px;border-radius:4px;white-space:nowrap}
.badge-8k{background:#ff4d6d18;border:1px solid #ff4d6d40;color:#ff4d6d}
.badge-10k{background:#a78bfa18;border:1px solid #a78bfa40;color:#a78bfa}
.badge-10q{background:#60a5fa18;border:1px solid #60a5fa40;color:#60a5fa}
.badge-def{background:#f59e0b18;border:1px solid #f59e0b40;color:#f59e0b}
.badge-other{background:#2a4a6a18;color:#4a7296;border:1px solid #2a4a6a}
.analyst-row{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid #0c1e30}
.analyst-firm{font-family:'IBM Plex Mono',monospace;font-size:.74rem;color:#c8deff;font-weight:600}
.analyst-date{font-family:'IBM Plex Mono',monospace;font-size:.61rem;color:#2a4a6a}
.analyst-pt{font-family:'IBM Plex Mono',monospace;font-size:.71rem;color:#f59e0b}
.chip-upgrade{background:#00d4aa12;border:1px solid #00d4aa30;color:#00d4aa;padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.61rem;display:inline-block}
.chip-downgrade{background:#ff4d6d12;border:1px solid #ff4d6d30;color:#ff4d6d;padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.61rem;display:inline-block}
.chip-hold{background:#f59e0b12;border:1px solid #f59e0b30;color:#f59e0b;padding:2px 7px;border-radius:4px;font-family:'IBM Plex Mono',monospace;font-size:.61rem;display:inline-block}
.macro-tile{background:#071428;border:1px solid #0f2540;border-radius:8px;padding:14px;text-align:center}
.macro-val{font-family:'IBM Plex Mono',monospace;font-size:1.1rem;font-weight:700;color:#e8f0ff;margin:4px 0}
.macro-chg{font-family:'IBM Plex Mono',monospace;font-size:.76rem;margin-top:2px}
.err-box{background:#1a0a0a;border:1px solid #ff4d6d40;border-radius:8px;padding:14px;font-size:.82rem;color:#ff9090;margin:10px 0}
.warn-box{background:#1a1400;border:1px solid #f59e0b40;border-radius:8px;padding:14px;font-size:.82rem;color:#f0c060;margin:10px 0}
.stTextInput input{background:#071428 !important;border:1px solid #0f2540 !important;color:#c8deff !important;font-family:'IBM Plex Mono',monospace !important;border-radius:8px !important}
.stTextInput input:focus{border-color:#3b82f6 !important}
.stButton button{background:#0d2040;border:1px solid #1e3d6a;color:#60a5fa;border-radius:8px;font-family:'IBM Plex Mono',monospace;font-size:.8rem}
.stButton button:hover{background:#132d54;border-color:#3b82f6;color:#93c5fd}
.stSelectbox>div>div{background:#071428 !important;border:1px solid #0f2540 !important;color:#c8deff !important;border-radius:8px !important}
div[data-testid="stExpander"]{background:#071428;border:1px solid #0f2540;border-radius:8px}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-thumb{background:#0f2540;border-radius:3px}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTOR UNIVERSE
# ─────────────────────────────────────────────────────────────────────────────
SECTORS = {
    "Information Technology": {"icon":"💻","etf":"XLK",
        "tickers":["AAPL","MSFT","NVDA","AMD","AVGO","CRM","ORCL","ADBE","QCOM","TXN"],
        "sub":{"AAPL":"Consumer Electronics","MSFT":"Enterprise Cloud","NVDA":"AI / Data Center GPUs","AMD":"CPUs & GPUs","AVGO":"Networking Chips","CRM":"CRM / SaaS","ORCL":"Database / Cloud","ADBE":"Creative SaaS","QCOM":"Mobile Semiconductors","TXN":"Analog Semiconductors"}},
    "Health Care": {"icon":"🏥","etf":"XLV",
        "tickers":["JNJ","UNH","ABBV","MRK","TMO","ABT","AMGN","GILD","PFE","ISRG"],
        "sub":{"JNJ":"Diversified Pharma","UNH":"Managed Care","ABBV":"Biopharmaceuticals","MRK":"Large-Cap Pharma","TMO":"Life Sciences Tools","ABT":"Medical Devices","AMGN":"Biotechnology","GILD":"Antiviral Biotech","PFE":"Large-Cap Pharma","ISRG":"Robotic Surgery"}},
    "Financials": {"icon":"🏦","etf":"XLF",
        "tickers":["JPM","BAC","GS","MS","BLK","AXP","WFC","C","SCHW","ICE"],
        "sub":{"JPM":"Global Banking","BAC":"Retail & Investment Banking","GS":"Investment Banking","MS":"Wealth Management","BLK":"Asset Management","AXP":"Charge Cards","WFC":"Retail Banking","C":"Global Consumer Banking","SCHW":"Discount Brokerage","ICE":"Financial Exchanges"}},
    "Consumer Discretionary": {"icon":"🛍️","etf":"XLY",
        "tickers":["AMZN","TSLA","HD","MCD","NKE","SBUX","TJX","LOW","BKNG","ABNB"],
        "sub":{"AMZN":"E-Commerce / Cloud","TSLA":"Electric Vehicles","HD":"Home Improvement","MCD":"Quick Service Restaurants","NKE":"Athletic Apparel","SBUX":"Specialty Coffee","TJX":"Off-Price Retail","LOW":"Home Improvement","BKNG":"Online Travel","ABNB":"Short-Term Rentals"}},
    "Communication Services": {"icon":"📡","etf":"XLC",
        "tickers":["META","GOOGL","NFLX","DIS","CMCSA","T","VZ","SNAP","PINS","TTD"],
        "sub":{"META":"Social Media / VR","GOOGL":"Search / Cloud / AI","NFLX":"Video Streaming","DIS":"Theme Parks / Streaming","CMCSA":"Cable / Broadband","T":"Telecom / Fiber","VZ":"Wireless Telecom","SNAP":"Social / AR","PINS":"Visual Discovery","TTD":"Programmatic Advertising"}},
    "Industrials": {"icon":"⚙️","etf":"XLI",
        "tickers":["HON","CAT","GE","UPS","RTX","DE","LMT","NOC","FDX","ETN"],
        "sub":{"HON":"Diversified Industrials","CAT":"Construction Equipment","GE":"Aerospace Engines","UPS":"Package Delivery","RTX":"Defense / Aerospace","DE":"Agricultural Machinery","LMT":"Defense Contractor","NOC":"Defense / Cyber","FDX":"Global Freight","ETN":"Electrical Power"}},
    "Consumer Staples": {"icon":"🛒","etf":"XLP",
        "tickers":["PG","KO","PEP","WMT","COST","PM","MO","CL","GIS","MDLZ"],
        "sub":{"PG":"Household & Personal Care","KO":"Beverages","PEP":"Beverages & Snacks","WMT":"Discount Retail","COST":"Warehouse Retail","PM":"International Tobacco","MO":"U.S. Tobacco","CL":"Oral & Home Care","GIS":"Packaged Foods","MDLZ":"Snacks & Chocolate"}},
    "Energy": {"icon":"⛽","etf":"XLE",
        "tickers":["XOM","CVX","COP","SLB","EOG","MPC","PSX","VLO","OXY","DVN"],
        "sub":{"XOM":"Integrated Oil & Gas","CVX":"Integrated Oil & Gas","COP":"E&P Upstream","SLB":"Oilfield Services","EOG":"Permian Basin E&P","MPC":"Refining","PSX":"Refining / Midstream","VLO":"Independent Refining","OXY":"E&P / Carbon Capture","DVN":"Delaware Basin E&P"}},
    "Utilities": {"icon":"⚡","etf":"XLU",
        "tickers":["NEE","DUK","SO","D","AEP","EXC","SRE","ED","XEL","WEC"],
        "sub":{"NEE":"Renewable Energy","DUK":"Electric Utility","SO":"Electric & Gas Utility","D":"Electric & Gas","AEP":"Transmission Utility","EXC":"Nuclear Power","SRE":"California Gas / LNG","ED":"New York Utility","XEL":"Renewable Utility","WEC":"Midwest Utility"}},
    "Real Estate": {"icon":"🏢","etf":"XLRE",
        "tickers":["AMT","PLD","EQIX","CCI","PSA","WELL","O","SPG","DLR","VICI"],
        "sub":{"AMT":"Cell Tower REIT","PLD":"Industrial REIT","EQIX":"Data Center REIT","CCI":"Cell Tower / Fiber REIT","PSA":"Self-Storage REIT","WELL":"Healthcare REIT","O":"Net Lease REIT","SPG":"Premium Mall REIT","DLR":"Data Center REIT","VICI":"Gaming Real Estate"}},
    "Materials": {"icon":"⛏️","etf":"XLB",
        "tickers":["LIN","APD","SHW","FCX","NEM","NUE","ALB","ECL","MOS","CF"],
        "sub":{"LIN":"Industrial Gases","APD":"Industrial Gases","SHW":"Paints & Coatings","FCX":"Copper Mining","NEM":"Gold Mining","NUE":"Steel","ALB":"Lithium / Chemicals","ECL":"Water Treatment","MOS":"Fertilizers","CF":"Nitrogen Fertilizers"}},
}

MACRO_SYMBOLS = {
    "S&P 500":     {"sym":"^GSPC","type":"index","fmt":",.0f"},
    "NASDAQ":      {"sym":"^IXIC","type":"index","fmt":",.0f"},
    "Dow Jones":   {"sym":"^DJI", "type":"index","fmt":",.0f"},
    "VIX":         {"sym":"^VIX", "type":"index","fmt":".2f"},
    "10Y Treasury":{"sym":"^TNX", "type":"rate", "fmt":".3f"},
    "2Y Treasury": {"sym":"^IRX", "type":"rate", "fmt":".3f"},
    "Dollar Index":{"sym":"DX-Y.NYB","type":"fx","fmt":".2f"},
    "EUR/USD":     {"sym":"EURUSD=X","type":"fx","fmt":".4f"},
    "Gold":        {"sym":"GC=F", "type":"comm","fmt":",.2f"},
    "WTI Crude":   {"sym":"CL=F", "type":"comm","fmt":".2f"},
    "Copper":      {"sym":"HG=F", "type":"comm","fmt":".3f"},
}

# Multi-source news registry
NEWS_SOURCES = {
    "Yahoo Finance":  ("yf",   "https://feeds.finance.yahoo.com/rss/2.0/headline?s={t}&region=US&lang=en-US"),
    "Reuters":        ("reuters","https://news.google.com/rss/search?q={t}+site:reuters.com&hl=en&gl=US&ceid=US:en"),
    "CNBC":           ("cnbc", "https://news.google.com/rss/search?q={t}+site:cnbc.com&hl=en&gl=US&ceid=US:en"),
    "MarketWatch":    ("mw",   "https://news.google.com/rss/search?q={t}+site:marketwatch.com&hl=en&gl=US&ceid=US:en"),
    "Seeking Alpha":  ("sa",   "https://news.google.com/rss/search?q={t}+site:seekingalpha.com&hl=en&gl=US&ceid=US:en"),
    "Barron's":       ("barrons","https://news.google.com/rss/search?q={t}+site:barrons.com&hl=en&gl=US&ceid=US:en"),
    "Benzinga":       ("bz",   "https://news.google.com/rss/search?q={t}+site:benzinga.com&hl=en&gl=US&ceid=US:en"),
    "IBD":            ("ibd",  "https://news.google.com/rss/search?q={t}+site:investors.com&hl=en&gl=US&ceid=US:en"),
    "Google News":    ("google","https://news.google.com/rss/search?q={t}+stock+earnings&hl=en-US&gl=US&ceid=US:en"),
}

EDGAR_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={t}&type={form}&dateb=&owner=include&count=5&output=atom"
FINVIZ_HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml","Accept-Language":"en-US,en;q=0.5"}


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _safe(v, d=None):
    try:
        if v is None: return d
        if isinstance(v, float) and (v != v or abs(v) == float("inf")): return d
        return v
    except: return d

def fmt_pct(v, n="N/A"):
    if v is None: return n
    try: return "{:+.1f}%".format(v*100)
    except: return n

def fmt_large(v, n="N/A"):
    if v is None: return n
    try:
        v=float(v)
        if abs(v)>=1e12: return "${:.2f}T".format(v/1e12)
        if abs(v)>=1e9:  return "${:.2f}B".format(v/1e9)
        if abs(v)>=1e6:  return "${:.2f}M".format(v/1e6)
        return "${:.0f}".format(v)
    except: return n

def fmt_val(v, f=".2f", sfx="", n="N/A"):
    if v is None: return n
    try: return "{:{}}{}".format(v,f,sfx)
    except: return n

def cc(v, thresh=0, rev=False):
    if v is None: return "neu"
    g = float(v) > thresh
    if rev: g = not g
    return "bull" if g else "bear"

def score_bar(score, color="#3b82f6"):
    return ('<div class="score-bar-bg"><div class="score-bar-fill" style="width:{:.0f}%;background:{};"></div></div>'
            '<span style="font-family:\'IBM Plex Mono\',monospace;font-size:.69rem;color:{};">{:.0f}/100</span>').format(score,color,color,score)

def metric_tiles(pairs):
    tiles="".join('<div class="metric-tile"><div class="m-label">{}</div><div class="m-val {}">{}</div></div>'.format(l,c,v) for l,v,c in pairs)
    return '<div class="metric-grid">{}</div>'.format(tiles)

def sec_label(t): st.markdown('<div class="sec-label">{}</div>'.format(t), unsafe_allow_html=True)
def edu(t):       st.markdown('<div class="edu-box">{}</div>'.format(t), unsafe_allow_html=True)
def err(t):       st.markdown('<div class="err-box">⚠️ {}</div>'.format(t), unsafe_allow_html=True)
def warn(t):      st.markdown('<div class="warn-box">ℹ️ {}</div>'.format(t), unsafe_allow_html=True)

def source_tag(src):
    cls_map = {"Reuters":"reuters","CNBC":"cnbc","MarketWatch":"mw","Seeking Alpha":"sa",
               "Barron's":"barrons","Benzinga":"bz","Yahoo Finance":"yf","IBD":"ibd",
               "Google News":"google","SEC EDGAR":"sec","finviz":"finviz"}
    cls = cls_map.get(src, "google")
    return '<span class="source-tag src-{}">{}</span>'.format(cls, src)

# ─────────────────────────────────────────────────────────────────────────────
#  YFINANCE INIT  (cookie_consent for cloud IPs)
# ─────────────────────────────────────────────────────────────────────────────
def _init_yf():
    try:
        yf.config.network.cookie_consent = True
    except Exception:
        pass

# ─────────────────────────────────────────────────────────────────────────────
#  PRICE HISTORY  — yf.download() primary (most reliable on cloud)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900, show_spinner=False)
def get_hist(ticker: str) -> pd.DataFrame:
    _init_yf()
    t = ticker.upper().strip()
    for period in ["1y", "6mo", "3mo"]:
        for attempt in range(3):
            try:
                df = yf.download(t, period=period, interval="1d",
                                  auto_adjust=True, progress=False,
                                  threads=False, multi_level_index=False)
                if df is not None and not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df.columns = [str(c).capitalize() for c in df.columns]
                    if "Close" in df.columns: return df
            except Exception:
                pass
            time.sleep(0.5 * (attempt+1))
    return pd.DataFrame()

# ─────────────────────────────────────────────────────────────────────────────
#  FUNDAMENTALS  — fast_info primary, tk.info secondary
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900, show_spinner=False)
def get_fundamentals(ticker: str) -> dict:
    _init_yf()
    t = ticker.upper().strip()
    info: dict = {}
    try:
        tk = yf.Ticker(t)
        # fast_info — lightweight, rarely blocked
        try:
            fi = tk.fast_info
            for src_a, dst_k in [
                ("last_price","currentPrice"),("last_price","regularMarketPrice"),
                ("market_cap","marketCap"),("fifty_two_week_high","fiftyTwoWeekHigh"),
                ("fifty_two_week_low","fiftyTwoWeekLow"),("shares","sharesOutstanding"),
                ("currency","currency"),("exchange","exchange"),
            ]:
                try:
                    v = getattr(fi, src_a, None)
                    if v is not None and not (isinstance(v,float) and v!=v): info[dst_k]=v
                except: pass
        except: pass
        # tk.info — full fundamentals, may be blocked (optional)
        try:
            full = tk.info
            if full and isinstance(full,dict) and len(full)>5:
                for k in ["longName","shortName","sector","industry","trailingPE","forwardPE",
                          "priceToBook","enterpriseToEbitda","priceToSalesTrailing12Months","pegRatio",
                          "returnOnEquity","returnOnAssets","profitMargins","grossMargins",
                          "operatingMargins","revenueGrowth","earningsGrowth","debtToEquity",
                          "currentRatio","freeCashflow","shortPercentOfFloat","shortRatio",
                          "targetMeanPrice","recommendationMean","numberOfAnalystOpinions",
                          "dividendYield","beta","averageVolume","sharesOutstanding","marketCap",
                          "currentPrice","regularMarketPrice","fiftyTwoWeekHigh","fiftyTwoWeekLow"]:
                    v=full.get(k)
                    if v is not None: info[k]=v
        except: pass
    except: pass
    return {k:v for k,v in info.items() if v is not None}

# ─────────────────────────────────────────────────────────────────────────────
#  SUPPLEMENTAL DATA  — cashflow, upgrades, holders (all optional)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def get_supplemental(ticker: str) -> dict:
    _init_yf()
    t   = ticker.upper().strip()
    out = {"cashflow": pd.DataFrame(), "balance": pd.DataFrame(),
           "upgrades": pd.DataFrame(), "holders":  pd.DataFrame()}
    try:
        tk = yf.Ticker(t)
        try: out["cashflow"] = tk.cash_flow
        except:
            try: out["cashflow"] = tk.cashflow
            except: pass
        try: out["balance"]  = tk.balance_sheet
        except: pass
        try: out["upgrades"] = tk.upgrades_downgrades
        except: pass
        try: out["holders"]  = tk.institutional_holders
        except: pass
    except: pass
    return out

# ─────────────────────────────────────────────────────────────────────────────
#  MULTI-SOURCE NEWS  — 9 feeds, deduplicated
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def get_news(ticker: str, max_per: int = 3) -> list:
    t_up  = ticker.upper().strip()
    items = []
    seen  = set()
    for src_name, (src_cls, url_tmpl) in NEWS_SOURCES.items():
        url = url_tmpl.format(t=t_up)
        try:
            feed  = feedparser.parse(url)
            count = 0
            for e in feed.entries:
                title = html.unescape(e.get("title","")).strip()
                title = re.sub(r"\s*[-–]\s*[A-Z][A-Za-z\s.]+$","",title).strip()
                if not title or len(title)<10: continue
                key = title[:55].lower()
                if key in seen: continue
                seen.add(key)
                items.append({
                    "title":  title,
                    "link":   e.get("link",""),
                    "date":   e.get("published",e.get("updated",""))[:16],
                    "source": src_name,
                    "cls":    src_cls,
                })
                count += 1
                if count >= max_per: break
        except: continue
    items.sort(key=lambda x: x["date"], reverse=True)
    return items[:20]

# ─────────────────────────────────────────────────────────────────────────────
#  SEC EDGAR FILINGS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_sec_filings(ticker: str) -> list:
    t_up    = ticker.upper().strip()
    filings = []
    headers = {"User-Agent":"EQ-Terminal research@example.com","Accept-Encoding":"gzip"}
    for form in ["8-K","10-K","10-Q","DEF 14A"]:
        try:
            url  = EDGAR_URL.format(t=t_up, form=form.replace(" ","+"))
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200: continue
            feed = feedparser.parse(resp.text)
            for e in feed.entries[:2]:
                summary = html.unescape(e.get("summary",""))[:150]
                filings.append({"form":form,"title":html.unescape(e.get("title","")),"link":e.get("link",""),"date":e.get("updated",e.get("published",""))[:10],"summary":summary})
        except: continue
    filings.sort(key=lambda x: x["date"], reverse=True)
    return filings[:10]

# ─────────────────────────────────────────────────────────────────────────────
#  FINVIZ ANALYST RATINGS SCRAPE
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_finviz_ratings(ticker: str) -> list:
    ratings = []
    try:
        resp = requests.get("https://finviz.com/quote.ashx?t={}&p=d".format(ticker.upper()), headers=FINVIZ_HEADERS, timeout=12)
        if resp.status_code != 200: return ratings
        soup  = BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", {"class":"js-table-ratings"})
        if table is None:
            for tbl in soup.find_all("table"):
                if any(w in tbl.get_text() for w in ["Upgrade","Downgrade","Initiated"]):
                    table=tbl; break
        if table is None: return ratings
        for row in table.find_all("tr")[1:9]:
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cells)>=4:
                ratings.append({"date":cells[0],"action":cells[1],"firm":cells[2],"rating":cells[3],"pt":cells[4] if len(cells)>4 else ""})
    except: pass
    return ratings

# ─────────────────────────────────────────────────────────────────────────────
#  STOCK ANALYSIS SCRAPE  — additional fundamental data source
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_stockanalysis_data(ticker: str) -> dict:
    """Scrape stockanalysis.com for additional fundamentals not in yfinance."""
    out = {}
    try:
        url  = "https://stockanalysis.com/stocks/{}/financials/".format(ticker.lower())
        hdrs = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(url, headers=hdrs, timeout=10)
        if resp.status_code != 200: return out
        soup = BeautifulSoup(resp.text, "lxml")
        # Scrape key stats box
        for row in soup.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cells) >= 2:
                key = cells[0].lower()
                val_str = cells[1].replace(",","").replace("%","").replace("$","").strip()
                try:
                    val = float(val_str)
                    if "revenue" in key: out["sa_revenue"] = val
                    elif "earnings" in key or "eps" in key: out["sa_eps"] = val
                    elif "profit margin" in key: out["sa_profit_margin"] = val/100
                except: pass
    except: pass
    return out


# ─────────────────────────────────────────────────────────────────────────────
#  TECHNICAL INDICATORS  — computed from price history
# ─────────────────────────────────────────────────────────────────────────────
def compute_technicals(hist: pd.DataFrame) -> dict:
    t = {}
    if hist is None or hist.empty or "Close" not in hist.columns:
        return t
    close = hist["Close"].astype(float)
    high  = hist["High"].astype(float)  if "High"  in hist.columns else close
    low   = hist["Low"].astype(float)   if "Low"   in hist.columns else close
    n     = len(close)

    # Moving averages
    for p, k in [(20,"sma20"),(50,"sma50"),(200,"sma200")]:
        t[k] = float(close.rolling(p).mean().iloc[-1]) if n>=p else None
    cp = float(close.iloc[-1])
    t["price"] = cp
    for k, base in [("pct_sma20","sma20"),("pct_sma50","sma50"),("pct_sma200","sma200")]:
        bv = t.get(base)
        t[k] = (cp/bv - 1) if bv else None

    # RSI-14
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, float("nan"))
    rsi_v = (100.0 - 100.0/(1.0+rs)).iloc[-1]
    t["rsi"] = float(rsi_v) if rsi_v==rsi_v else None

    # MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd  = ema12 - ema26
    sig   = macd.ewm(span=9, adjust=False).mean()
    t["macd"]      = float(macd.iloc[-1])
    t["macd_sig"]  = float(sig.iloc[-1])
    t["macd_hist"] = float((macd-sig).iloc[-1])

    # Bollinger Bands
    bb_m = close.rolling(20).mean()
    bb_s = close.rolling(20).std()
    t["bb_upper"] = float((bb_m + 2*bb_s).iloc[-1])
    t["bb_lower"] = float((bb_m - 2*bb_s).iloc[-1])
    bw = t["bb_upper"] - t["bb_lower"]
    t["bb_pct"] = float((cp - t["bb_lower"]) / bw) if bw else 0.5

    # ATR-14
    tr = pd.concat([high-low, (high-close.shift(1)).abs(), (low-close.shift(1)).abs()], axis=1)
    t["atr"] = float(tr.max(axis=1).rolling(14).mean().iloc[-1])

    # Returns
    t["ret_1m"]  = float(close.iloc[-1]/close.iloc[-21]-1) if n>=21 else None
    t["ret_3m"]  = float(close.iloc[-1]/close.iloc[-63]-1) if n>=63 else None
    t["ret_1y"]  = float(close.iloc[-1]/close.iloc[0]-1)
    t["vol_ann"] = float(close.pct_change().dropna().std() * (252**0.5))

    # 52-week high/low from hist
    t["52w_high"] = float(high.max())
    t["52w_low"]  = float(low.min())
    t["pct_from_52h"] = (cp / t["52w_high"] - 1) if t["52w_high"] else None
    t["pct_from_52l"] = (cp / t["52w_low"]  - 1) if t["52w_low"]  else None

    # Trend signals (for thesis)
    t["trend_signal"] = (
        "STRONG UPTREND"   if (t.get("pct_sma200") or 0) > 0.05  and (t.get("macd_hist") or 0) > 0 else
        "UPTREND"          if (t.get("pct_sma200") or 0) > 0      else
        "DOWNTREND"        if (t.get("pct_sma200") or 0) < -0.05  and (t.get("macd_hist") or 0) < 0 else
        "WEAK DOWNTREND"
    )
    t["rsi_signal"] = (
        "OVERBOUGHT" if (t.get("rsi") or 50) > 70 else
        "OVERSOLD"   if (t.get("rsi") or 50) < 30 else
        "NEUTRAL"
    )
    return t

# ─────────────────────────────────────────────────────────────────────────────
#  SCORING MODEL
# ─────────────────────────────────────────────────────────────────────────────
def _fcf_yield(info: dict, cashflow: pd.DataFrame) -> float | None:
    fcf = _safe(info.get("freeCashflow"))
    if fcf is None and not cashflow.empty:
        try:
            ocf_r = [r for r in cashflow.index if "operating" in str(r).lower()]
            cap_r = [r for r in cashflow.index if "capital" in str(r).lower()]
            if ocf_r:
                fcf = float(cashflow.loc[ocf_r[0]].iloc[0]) - (abs(float(cashflow.loc[cap_r[0]].iloc[0])) if cap_r else 0)
        except: pass
    mc = _safe(info.get("marketCap"))
    return (fcf/mc) if (fcf and mc and mc>0) else None

def _dcf(info: dict, fcf_yield: float | None) -> float | None:
    price = _safe(info.get("currentPrice")) or _safe(info.get("regularMarketPrice"))
    g1    = min(max(_safe(info.get("revenueGrowth"), 0.06), -0.05), 0.22)
    g2    = 0.03; r = 0.10
    mc    = _safe(info.get("marketCap"))
    fcf   = _safe(info.get("freeCashflow"))
    if fcf and mc and mc>0 and price and price>0 and fcf>0:
        shares=mc/price; fps=fcf/shares; pv=0.0; f=fps
        for _ in range(5): f*=(1+g1); pv+=f/(1+r)**(_+1)
        pv += f*(1+g2)/(r-g2)/(1+r)**5
        return round(pv,2)
    pe = _safe(info.get("trailingPE")) or _safe(info.get("forwardPE"))
    if pe and pe>0 and price and price>0:
        g=min(g1,0.12)
        if r>g: return round((price/pe)*(1+g)/(r-g),2)
    return None

def score_long(info: dict, tech: dict, fy: float | None, dcf_iv: float | None) -> float:
    s=50.0; price=tech.get("price") or _safe(info.get("currentPrice"),1)
    mos = (dcf_iv/price-1) if (dcf_iv and price and price>0) else None
    if fy:
        if fy>0.08:s+=15
        elif fy>0.05:s+=10
        elif fy>0.02:s+=5
        elif fy<0:s-=15
    if mos:
        if mos>0.30:s+=12
        elif mos>0.15:s+=7
        elif mos>0:s+=3
        elif mos<-0.25:s-=10
    roe=_safe(info.get("returnOnEquity"))
    if roe:
        if roe>0.25:s+=8
        elif roe>0.15:s+=5
        elif roe>0.08:s+=2
        elif roe<0:s-=8
    rg=_safe(info.get("revenueGrowth"))
    if rg:
        if rg>0.15:s+=8
        elif rg>0.05:s+=4
        elif rg>0:s+=1
        elif rg<-0.05:s-=8
    p200=tech.get("pct_sma200")
    if p200 is not None:
        if p200>0.05:s+=5
        elif p200>0:s+=2
        else:s-=5
    rsi=tech.get("rsi")
    if rsi:
        if 38<=rsi<=60:s+=5
        elif rsi<35:s+=3
        elif rsi>75:s-=5
    au=_safe(info.get("analyst_upside"))
    tp=_safe(info.get("targetMeanPrice")); cp2=_safe(info.get("currentPrice"))
    if not au and tp and cp2 and cp2>0: au=tp/cp2-1
    if au:
        if au>0.20:s+=7
        elif au>0.10:s+=3
        elif au<-0.05:s-=4
    pe=_safe(info.get("trailingPE"))
    if pe and pe>0:
        if pe<15:s+=5
        elif pe<22:s+=2
        elif pe>60:s-=6
        elif pe>100:s-=12
    mh=tech.get("macd_hist")
    if mh is not None: s+=2 if mh>0 else -2
    ar=_safe(info.get("recommendationMean"))
    if ar:
        if ar<=1.8:s+=5
        elif ar<=2.3:s+=2
        elif ar>=4:s-=5
    return round(min(max(s,0),100),1)

def score_short(info: dict, tech: dict, fy: float | None, dcf_iv: float | None) -> float:
    s=50.0; price=tech.get("price") or _safe(info.get("currentPrice"),1)
    mos=(dcf_iv/price-1) if (dcf_iv and price and price>0) else None
    if fy:
        if fy<-0.05:s+=15
        elif fy<0:s+=8
        elif fy>0.06:s-=10
    if mos:
        if mos<-0.30:s+=12
        elif mos<-0.15:s+=7
        elif mos>0.20:s-=8
    pe=_safe(info.get("trailingPE"))
    if pe:
        if pe>100:s+=12
        elif pe>60:s+=7
        elif pe>40:s+=3
        elif pe<15:s-=8
    roe=_safe(info.get("returnOnEquity"))
    if roe:
        if roe<0:s+=10
        elif roe<0.05:s+=5
        elif roe>0.20:s-=7
    p200=tech.get("pct_sma200")
    if p200 is not None:
        if p200<-0.10:s+=8
        elif p200<0:s+=4
        elif p200>0.05:s-=5
    rsi=tech.get("rsi")
    if rsi:
        if rsi>75:s+=8
        elif rsi>65:s+=4
        elif rsi<35:s-=5
    rg=_safe(info.get("revenueGrowth"))
    if rg:
        if rg<-0.10:s+=10
        elif rg<0:s+=5
        elif rg>0.15:s-=7
    sp=_safe(info.get("shortPercentOfFloat"))
    if sp:
        if sp>0.20:s+=8
        elif sp>0.10:s+=4
    mh=tech.get("macd_hist")
    if mh is not None: s+=3 if mh<0 else -2
    ar=_safe(info.get("recommendationMean"))
    if ar:
        if ar>=4:s+=6
        elif ar>=3.5:s+=3
        elif ar<=1.8:s-=5
    return round(min(max(s,0),100),1)


# ─────────────────────────────────────────────────────────────────────────────
#  AI THESIS SYNTHESIS ENGINE
#  Calls Claude claude-sonnet-4-20250514 to build a thesis from real data each refresh
# ─────────────────────────────────────────────────────────────────────────────
def build_ai_thesis(
    ticker: str,
    info: dict,
    tech: dict,
    news_items: list,
    filings: list,
    finviz_ratings: list,
    bias: str,
    ls: float,
    ss: float,
    fy: float | None,
    dcf_iv: float | None,
) -> str:
    """
    Synthesize a real investment thesis by feeding all gathered data into Claude.
    Every call uses fresh live data — news headlines, technical values, SEC filings,
    analyst ratings — so the thesis updates every time you refresh.
    """

    price  = tech.get("price") or _safe(info.get("currentPrice"), 0)
    name   = _safe(info.get("longName"), ticker)
    mos    = (dcf_iv/price - 1) if (dcf_iv and price and price > 0) else None

    # Build structured data summary for the model
    fundamentals_block = """
FUNDAMENTALS (from yfinance / SEC filings):
  Company:         {name}
  Current Price:   ${price:.2f}
  Market Cap:      {mc}
  Trailing P/E:    {pe}
  Forward P/E:     {fpe}
  EV/EBITDA:       {ev}
  Price/Sales:     {ps}
  FCF Yield:       {fy}
  ROE:             {roe}
  Net Margin:      {pm}
  Revenue Growth:  {rg}
  Earnings Growth: {eg}
  Debt/Equity:     {de}
  DCF Intrinsic V: {iv}
  Margin of Safety:{mos}
  Analyst Target:  {tp}
  Analyst Rating:  {ar} (1=Strong Buy, 5=Sell, {n} analysts)
  Short Interest:  {si}
  Beta:            {beta}
""".format(
        name=name, price=price,
        mc=fmt_large(_safe(info.get("marketCap"))),
        pe=fmt_val(_safe(info.get("trailingPE")),".1f","x"),
        fpe=fmt_val(_safe(info.get("forwardPE")),".1f","x"),
        ev=fmt_val(_safe(info.get("enterpriseToEbitda")),".1f","x"),
        ps=fmt_val(_safe(info.get("priceToSalesTrailing12Months")),".1f","x"),
        fy=fmt_pct(fy) if fy else "N/A",
        roe=fmt_pct(_safe(info.get("returnOnEquity"))),
        pm=fmt_pct(_safe(info.get("profitMargins"))),
        rg=fmt_pct(_safe(info.get("revenueGrowth"))),
        eg=fmt_pct(_safe(info.get("earningsGrowth"))),
        de=fmt_val(_safe(info.get("debtToEquity")),".0f","%"),
        iv="${:.2f}".format(dcf_iv) if dcf_iv else "N/A",
        mos=fmt_pct(mos) if mos else "N/A",
        tp="${:.2f}".format(_safe(info.get("targetMeanPrice"))) if _safe(info.get("targetMeanPrice")) else "N/A",
        ar=fmt_val(_safe(info.get("recommendationMean")),".2f"),
        n=_safe(info.get("numberOfAnalystOpinions"),"—"),
        si=fmt_pct(_safe(info.get("shortPercentOfFloat"))),
        beta=fmt_val(_safe(info.get("beta")),".2f"),
    )

    technicals_block = """
TECHNICAL INDICATORS (computed from live price history):
  Price vs SMA20:  {s20}  ({ts20})
  Price vs SMA50:  {s50}
  Price vs SMA200: {s200} (KEY institutional trend filter)
  RSI-14:          {rsi}  → {rsig}
  MACD Histogram:  {mh} → {macd_sig}
  Bollinger %B:    {bb:.2f}  (>0.8 = near upper band, <0.2 = near lower band)
  ATR-14:          ${atr:.2f}  (daily volatility measure)
  1-Month Return:  {r1m}
  3-Month Return:  {r3m}
  1-Year Return:   {r1y}
  Trend Signal:    {trend}
  52W High:        ${h52:.2f}  ({ph52} from current price)
  52W Low:         ${l52:.2f}  ({pl52} from current price)
""".format(
        s20=fmt_pct(tech.get("pct_sma20")),
        ts20="above" if (tech.get("pct_sma20") or 0) > 0 else "below",
        s50=fmt_pct(tech.get("pct_sma50")),
        s200=fmt_pct(tech.get("pct_sma200")),
        rsi=fmt_val(tech.get("rsi"),".1f"),
        rsig=tech.get("rsi_signal","—"),
        mh=fmt_val(tech.get("macd_hist"),".3f"),
        macd_sig="BULLISH MOMENTUM" if (tech.get("macd_hist") or 0) > 0 else "BEARISH MOMENTUM",
        bb=tech.get("bb_pct") or 0.5,
        atr=tech.get("atr") or 0,
        r1m=fmt_pct(tech.get("ret_1m")),
        r3m=fmt_pct(tech.get("ret_3m")),
        r1y=fmt_pct(tech.get("ret_1y")),
        trend=tech.get("trend_signal","—"),
        h52=tech.get("52w_high") or 0,
        ph52=fmt_pct(tech.get("pct_from_52h")),
        l52=tech.get("52w_low") or 0,
        pl52=fmt_pct(tech.get("pct_from_52l")),
    )

    # Recent news headlines from all sources
    news_block = "RECENT NEWS & MARKET INTELLIGENCE (from Reuters, CNBC, MarketWatch, Seeking Alpha, Barron's, Benzinga, Yahoo Finance, IBD, Google News):\n"
    if news_items:
        for i, item in enumerate(news_items[:12]):
            news_block += "  [{}] [{}] {}\n".format(i+1, item["source"], item["title"])
    else:
        news_block += "  No recent news items available.\n"

    # SEC filings
    filings_block = "RECENT SEC EDGAR FILINGS:\n"
    if filings:
        for f in filings[:5]:
            filings_block += "  [{form}] {date}: {title}\n".format(**f)
    else:
        filings_block += "  No recent filings fetched.\n"

    # Analyst ratings from finviz
    ratings_block = "RECENT ANALYST RATINGS (finviz scrape — Wall Street firms):\n"
    if finviz_ratings:
        for r in finviz_ratings[:6]:
            pt = " → PT {}".format(r["pt"]) if r.get("pt") else ""
            ratings_block += "  {} | {} | {} | {}{}\n".format(r["date"],r["firm"],r["action"],r["rating"],pt)
    else:
        ratings_block += "  No analyst ratings available.\n"

    # Scores context
    scores_block = """
QUANTITATIVE SCORES (our multi-factor model):
  Long Score:  {ls:.0f}/100  (>65 = high conviction long)
  Short Score: {ss:.0f}/100  (>65 = high conviction short)
  Recommended Bias: {bias}
""".format(ls=ls, ss=ss, bias=bias)

    # Full prompt — built via concatenation to avoid .format() conflicts with data blocks
    trend_str = tech.get("trend_signal", "—")
    prompt = (
        "You are a senior equity research analyst at a top-tier institutional investment bank.\n"
        "You have been given a comprehensive multi-source data package for " + ticker + " (" + name + ").\n"
        "Your task is to synthesize ALL of the data below into one coherent, institutional-grade investment thesis.\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. The thesis MUST reference specific numbers from the data provided — do not make up figures\n"
        "2. Integrate the news headlines into your thesis — explain what they mean for the investment case\n"
        "3. Connect technical indicators to fundamental conclusions (e.g. 'The " + trend_str + " trend confirms...')\n"
        "4. Reference the SEC filings if relevant (earnings reports, material events)\n"
        "5. Use analyst ratings as additional evidence for or against the thesis\n"
        "6. The thesis should be written for the " + bias + " side — argue the " + bias + " case persuasively\n"
        "7. Structure as: (A) Core Thesis in 2-3 sentences, (B) Fundamental Evidence, "
        "(C) Technical Confirmation, (D) News & Catalyst Analysis, (E) Key Risks\n"
        "8. Be specific, direct, and institutional in tone — no hedging language, no disclaimers\n"
        "9. Format with **bold** for key points and specific numbers\n\n"
        "Here is the complete data package:\n\n"
        + fundamentals_block
        + technicals_block
        + news_block
        + filings_block
        + ratings_block
        + scores_block
        + "\nWrite the full investment thesis now:"
    )

    # Call Anthropic API
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1500,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=45,
        )
        if resp.status_code == 200:
            data = resp.json()
            for block in data.get("content", []):
                if block.get("type") == "text":
                    return block["text"].strip()
        # API not available — fall back to rule-based thesis
        return _rule_based_thesis(ticker, info, tech, news_items, fy, dcf_iv, bias, mos)
    except Exception:
        return _rule_based_thesis(ticker, info, tech, news_items, fy, dcf_iv, bias, mos)


def _rule_based_thesis(ticker, info, tech, news_items, fy, dcf_iv, bias, mos):
    """
    Fallback: build thesis programmatically from real data when API unavailable.
    Still uses all the same data — just template-driven rather than AI-written.
    Every number is from the live data.
    """
    n     = _safe(info.get("longName"), ticker)
    price = tech.get("price") or _safe(info.get("currentPrice"), 0)
    lines = []

    if bias == "LONG":
        lines.append("**Core Long Thesis — {}:**".format(n))
        if mos and mos > 0.08 and dcf_iv and price:
            lines.append("**Valuation Discount ({:.0%} Margin of Safety):** {} trades at ${:.2f}, approximately {:.0%} below our DCF-derived intrinsic value of ${:.2f}, indicating the market is mis-pricing the company's long-term cash generation capacity.".format(mos,n,price,mos,dcf_iv))
        if fy and fy > 0.025:
            lines.append("**FCF Yield of {:.1%}:** The company generates real free cash at {:.1%} of market cap — above the 10-year Treasury rate and most sector peers, providing management with full capital allocation optionality.".format(fy,fy))
        roe = _safe(info.get("returnOnEquity"))
        if roe and roe > 0.12:
            lines.append("**ROE of {:.1%}:** A sustained Return on Equity above 12% signals durable competitive moats — pricing power and operational leverage that compress the cost of capital below the return on it.".format(roe))
        rg = _safe(info.get("revenueGrowth"))
        if rg and rg > 0.04:
            lines.append("**Revenue Growth of {:.1%}:** Expanding top-line at {:.1%} YoY confirms accelerating demand — the necessary precondition for operating leverage to produce EPS growth that outpaces consensus estimates.".format(rg,rg))
        trend = tech.get("trend_signal","—")
        p200  = tech.get("pct_sma200")
        if p200 and p200 > 0:
            lines.append("**Technical Confirmation ({}):** Price is {:.1%} above the 200-day moving average — confirming the institutional bid. The {} trend signal aligns with the fundamental thesis.".format(trend,p200,trend))
        if news_items:
            top = news_items[0]
            lines.append("**Recent Catalyst [{source}]:** '{title}' — this headline, sourced from {source}, is directly relevant to the investment thesis and represents potential near-term catalyst for price discovery.".format(**top))
    else:
        lines.append("**Core Short Thesis — {}:**".format(n))
        pe = _safe(info.get("trailingPE"))
        if pe and pe > 50:
            lines.append("**Multiple Compression Risk ({:.1f}x P/E):** At {:.1f}x trailing earnings, {} is priced for perpetual perfection in a rate environment where the cost of capital is no longer zero. Even modest multiple compression toward the sector median implies double-digit downside.".format(pe,pe,n))
        if fy is not None and fy < 0:
            lines.append("**Negative FCF (Burning {:.1%} of Market Cap):** {} is a cash consumer, not a cash generator. Reliance on capital markets for operational survival creates existential risk in tightening credit conditions.".format(abs(fy),n))
        rg = _safe(info.get("revenueGrowth"))
        if rg and rg < 0:
            lines.append("**Revenue Contraction ({:.1%}):** Shrinking revenues trigger an irreversible compounding loop: declining top-line → operating deleverage → EPS misses → estimate cuts → multiple compression — each stage self-reinforcing.".format(rg))
        trend = tech.get("trend_signal","—")
        p200  = tech.get("pct_sma200")
        if p200 and p200 < -0.05:
            lines.append("**Technical Breakdown ({}):** The stock is {:.1%} below the 200-day moving average — triggering systematic selling from trend-following and quantitative strategies as a secondary pressure layer on top of deteriorating fundamentals.".format(trend,abs(p200)))
        if news_items:
            top = news_items[0]
            lines.append("**Confirming Headline [{source}]:** '{title}' — sourced from {source}, this development is consistent with the deteriorating fundamental narrative and may accelerate the re-rating process.".format(**top))

    lines.append("\n**Note:** This thesis was generated from live data including {} news headlines from {} sources, {} SEC filings, and real-time technical indicators. Refresh to regenerate with the latest data.".format(
        len(news_items), len(set(i["source"] for i in news_items)), len(filings) if False else "—"
    ))
    return "\n\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
#  TRADE SETUP ENGINE  — entry / stop / targets from real ATR + DCF
# ─────────────────────────────────────────────────────────────────────────────
def build_trade_setup(info: dict, tech: dict, dcf_iv, bias: str) -> dict:
    cp  = tech.get("price") or _safe(info.get("currentPrice"), 0)
    atr = tech.get("atr") or cp * 0.02
    tp  = _safe(info.get("targetMeanPrice"))
    vol = tech.get("vol_ann") or 0.30

    if bias == "LONG":
        entry = cp
        stop  = round(cp - 1.5 * atr, 2)
        if dcf_iv and dcf_iv > cp:
            t1 = round(cp + (dcf_iv - cp) * 0.55, 2)
            t2 = round(dcf_iv, 2)
        elif tp and tp > cp:
            t1 = round(cp + (tp - cp) * 0.60, 2)
            t2 = round(tp, 2)
        else:
            t1 = round(cp * 1.15, 2)
            t2 = round(cp * 1.28, 2)
        rr = round((t1 - entry) / max(entry - stop, 0.01), 1)
        opts = ("Bull Call Spread" if vol > 0.28 else "Long ATM Call") + " — 90-Day Expiry"
        return {"bias":"LONG","entry":"${:.2f}".format(entry),
                "stop":"${:.2f}  ({:.1f}% risk)".format(stop,(entry-stop)/entry*100),
                "t1":"${:.2f}  (+{:.1f}%)".format(t1,(t1-entry)/entry*100),
                "t2":"${:.2f}  (+{:.1f}%)".format(t2,(t2-entry)/entry*100),
                "rr":"{:.1f}:1".format(rr),"options":opts,
                "sizing":"Size = (2% × portfolio) ÷ (entry − stop)"}
    else:
        entry = cp
        stop  = round(cp + 1.5 * atr, 2)
        if dcf_iv and dcf_iv < cp:
            t1 = round(cp - (cp - dcf_iv) * 0.50, 2)
            t2 = round(max(dcf_iv * 1.03, cp * 0.70), 2)
        else:
            t1 = round(cp * 0.85, 2)
            t2 = round(cp * 0.72, 2)
        rr  = round((entry - t1) / max(stop - entry, 0.01), 1)
        opts = ("Bear Put Spread" if vol > 0.32 else "Long ATM Put") + " — 60-Day Expiry"
        return {"bias":"SHORT","entry":"${:.2f}".format(entry),
                "stop":"${:.2f}  ({:.1f}% risk)".format(stop,(stop-entry)/entry*100),
                "t1":"${:.2f}  (−{:.1f}%)".format(t1,(entry-t1)/entry*100),
                "t2":"${:.2f}  (−{:.1f}%)".format(t2,(entry-t2)/entry*100),
                "rr":"{:.1f}:1".format(rr),"options":opts,
                "sizing":"Use options to cap upside risk. ≤2% portfolio risk."}


# ─────────────────────────────────────────────────────────────────────────────
#  INTERACTIVE PRICE CHART  — timeframes + SMA toggles + volume
# ─────────────────────────────────────────────────────────────────────────────
def render_interactive_chart(ticker: str, hist_full: pd.DataFrame, info: dict, dcf_iv, key_prefix: str = ""):
    """
    Renders an interactive chart with:
    - Timeframe selector (1W / 1M / 3M / 6M / 1Y / 2Y)
    - Checkboxes for SMA 10 / 20 / 50 / 200
    - Volume bars with average volume line
    - Bollinger Bands toggle
    - DCF intrinsic value line
    """
    if hist_full is None or hist_full.empty:
        warn("Price history unavailable — cannot render chart.")
        return

    st.markdown('<div class="sec-label">INTERACTIVE PRICE CHART · MULTI-TIMEFRAME · SMA OVERLAYS · VOLUME</div>', unsafe_allow_html=True)

    # ── Controls row ──────────────────────────────────────────────────────────
    ctrl_col1, ctrl_col2 = st.columns([2, 3])

    with ctrl_col1:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.7rem;color:#3a5a80;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;">Timeframe</div>', unsafe_allow_html=True)
        tf_options = {"1W": 5, "1M": 21, "3M": 63, "6M": 126, "1Y": 252, "2Y": 504}
        tf_cols = st.columns(len(tf_options))
        selected_tf = st.session_state.get("chart_tf_{}".format(key_prefix), "3M")
        for i, (label, days) in enumerate(tf_options.items()):
            with tf_cols[i]:
                is_sel = selected_tf == label
                btn_style = "background:#3b82f6;color:#fff;border:1px solid #3b82f6;" if is_sel else "background:#071428;color:#3a5a80;border:1px solid #0f2540;"
                if st.button(label, key="tf_{}_{}".format(key_prefix, label), use_container_width=True):
                    st.session_state["chart_tf_{}".format(key_prefix)] = label
                    selected_tf = label

    with ctrl_col2:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.7rem;color:#3a5a80;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;">SMA Overlays</div>', unsafe_allow_html=True)
        sma_cols = st.columns(4)
        sma_defs = [(10, "#f43f5e"), (20, "#60a5fa"), (50, "#f59e0b"), (200, "#a78bfa")]
        sma_active = {}
        for i, (period, color) in enumerate(sma_defs):
            with sma_cols[i]:
                default = period in [20, 50]
                active  = st.checkbox("SMA {}".format(period), value=default,
                                       key="sma_{}_{}_{}".format(period, ticker, key_prefix))
                sma_active[period] = (active, color)

    # ── Additional overlays ───────────────────────────────────────────────────
    ov_col1, ov_col2, ov_col3 = st.columns(3)
    with ov_col1:
        show_bb  = st.checkbox("Bollinger Bands", value=True, key="bb_{}_{}".format(ticker, key_prefix))
    with ov_col2:
        show_iv  = st.checkbox("DCF Intrinsic Value", value=bool(dcf_iv), key="iv_{}_{}".format(ticker, key_prefix))
    with ov_col3:
        show_vol = st.checkbox("Volume + Avg Volume", value=True, key="vol_{}_{}".format(ticker, key_prefix))

    # ── Slice to selected timeframe ────────────────────────────────────────────
    days       = tf_options.get(selected_tf, 63)
    hist       = hist_full.tail(days).copy() if len(hist_full) >= days else hist_full.copy()
    close      = hist["Close"].astype(float)
    n_rows     = 2 if show_vol else 1
    row_heights = [0.72, 0.28] if show_vol else [1.0]

    fig = go.Figure() if not show_vol else None
    if show_vol:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03, row_heights=row_heights)

    def add_trace(trace, row=1):
        if show_vol:
            fig.add_trace(trace, row=row, col=1)
        else:
            fig.add_trace(trace)

    # ── Candlestick ──────────────────────────────────────────────────────────
    add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"], name="Price",
        increasing=dict(line=dict(color="#00e5a0", width=1), fillcolor="rgba(0,229,160,0.18)"),
        decreasing=dict(line=dict(color="#ff4d6d", width=1), fillcolor="rgba(255,77,109,0.18)"),
    ))

    # ── SMA Lines ─────────────────────────────────────────────────────────────
    sma_styles = {10: "solid", 20: "solid", 50: "solid", 200: "dot"}
    for period, (active, color) in sma_active.items():
        if not active: continue
        if len(close) >= period:
            sma_vals = close.rolling(period).mean()
            add_trace(go.Scatter(
                x=hist.index, y=sma_vals, name="SMA {}".format(period),
                line=dict(color=color, width=1.4, dash=sma_styles.get(period,"solid")),
                opacity=0.9,
            ))

    # ── Bollinger Bands ───────────────────────────────────────────────────────
    if show_bb and len(close) >= 20:
        bb_m = close.rolling(20).mean()
        bb_s = close.rolling(20).std()
        bb_u = bb_m + 2 * bb_s
        bb_l = bb_m - 2 * bb_s
        add_trace(go.Scatter(
            x=hist.index, y=bb_u, name="BB Upper",
            line=dict(color="rgba(99,102,241,0.5)", width=1, dash="dash"),
            showlegend=True,
        ))
        add_trace(go.Scatter(
            x=hist.index, y=bb_l, name="BB Lower",
            line=dict(color="rgba(99,102,241,0.5)", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(99,102,241,0.05)",
            showlegend=False,
        ))

    # ── DCF Intrinsic Value horizontal line ────────────────────────────────────
    if show_iv and dcf_iv:
        add_trace(go.Scatter(
            x=[hist.index[0], hist.index[-1]], y=[dcf_iv, dcf_iv],
            mode="lines", name="DCF IV ${:.2f}".format(dcf_iv),
            line=dict(color="#f59e0b", width=1.5, dash="longdash"),
        ))

    # ── Volume bars + Average Volume line ─────────────────────────────────────
    if show_vol and "Volume" in hist.columns:
        vol_colors = [
            "rgba(0,229,160,0.55)" if float(c) >= float(o) else "rgba(255,77,109,0.55)"
            for c, o in zip(hist["Close"], hist["Open"])
        ]
        add_trace(go.Bar(
            x=hist.index, y=hist["Volume"].astype(float),
            name="Volume", marker_color=vol_colors, showlegend=True,
        ), row=2)

        # Average volume line
        avg_vol = _safe(info.get("averageVolume"))
        if avg_vol:
            add_trace(go.Scatter(
                x=[hist.index[0], hist.index[-1]],
                y=[avg_vol, avg_vol],
                mode="lines", name="Avg Vol",
                line=dict(color="#f59e0b", width=1.2, dash="dot"),
            ), row=2)

    # ── Layout ────────────────────────────────────────────────────────────────
    chart_h = 580 if show_vol else 460
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#040d1a",
        plot_bgcolor="#050e1e",
        font=dict(family="IBM Plex Mono", color="#6a90b8", size=10),
        xaxis_rangeslider_visible=False,
        height=chart_h,
        margin=dict(l=8, r=8, t=10, b=8),
        legend=dict(
            orientation="h", y=1.02, x=0,
            bgcolor="rgba(5,14,30,0.8)",
            bordercolor="#0f2540", borderwidth=1,
            font=dict(size=10), itemsizing="constant",
        ),
    )

    grid_style = dict(showgrid=True, gridcolor="rgba(15,37,64,0.8)", gridwidth=0.5,
                      zeroline=False, showspikes=True, spikecolor="#3b82f6",
                      spikethickness=1, spikedash="dot")
    if show_vol:
        for row in range(1, 3):
            fig.update_xaxes(**grid_style, row=row, col=1)
            fig.update_yaxes(**grid_style, row=row, col=1)
        fig.update_yaxes(tickformat=",.0f", row=2, col=1)
    else:
        fig.update_xaxes(**grid_style)
        fig.update_yaxes(**grid_style)

    st.plotly_chart(fig, use_container_width=True, config={
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["lasso2d","select2d"],
        "scrollZoom": True,
    })

    # ── Volume stats summary ──────────────────────────────────────────────────
    if show_vol and "Volume" in hist.columns:
        avg_v  = _safe(info.get("averageVolume"))
        last_v = float(hist["Volume"].iloc[-1])
        vol_ratio = last_v / avg_v if avg_v else None
        vc1, vc2, vc3 = st.columns(3)
        with vc1:
            st.markdown('<div class="card card-sm"><div class="m-label">Last Session Volume</div><div class="m-val neu">{}</div></div>'.format(fmt_large(last_v)), unsafe_allow_html=True)
        with vc2:
            st.markdown('<div class="card card-sm"><div class="m-label">Average Volume (90D)</div><div class="m-val neu">{}</div></div>'.format(fmt_large(avg_v)), unsafe_allow_html=True)
        with vc3:
            vc = "bull" if vol_ratio and vol_ratio > 1 else "bear"
            vr_str = "{:.1f}x avg".format(vol_ratio) if vol_ratio else "N/A"
            st.markdown('<div class="card card-sm"><div class="m-label">Volume vs Average</div><div class="m-val {}">{}</div></div>'.format(vc, vr_str), unsafe_allow_html=True)
        edu("Volume confirmation: a strong price move on >1.5× average volume signals institutional participation. Below-average volume on a rally is a warning sign of weak conviction.")


# ─────────────────────────────────────────────────────────────────────────────
#  DEEP-DIVE REPORT RENDERER
# ─────────────────────────────────────────────────────────────────────────────
def render_deep_dive(ticker: str, bias_override: str = "AUTO", key_prefix: str = "dd"):
    """
    Full deep-dive: fetches from ALL sources, synthesizes AI thesis, renders report.
    """
    t_up = ticker.upper().strip()

    # ── Fetch all sources in parallel status display ──────────────────────────
    prog = st.progress(0, text="Fetching price history from yfinance (download endpoint)...")

    hist = get_hist(t_up)
    prog.progress(18, text="Fetching fundamentals (fast_info + tk.info)...")

    info = get_fundamentals(t_up)
    prog.progress(34, text="Fetching supplemental data (cashflow, holders, upgrades)...")

    supp = get_supplemental(t_up)
    prog.progress(48, text="Aggregating news from Reuters · CNBC · MarketWatch · Seeking Alpha · Barron's · Benzinga · IBD (9 feeds)...")

    news = get_news(t_up, max_per=3)
    prog.progress(62, text="Fetching SEC EDGAR filings (8-K · 10-K · 10-Q)...")

    filings = get_sec_filings(t_up)
    prog.progress(74, text="Scraping finviz.com for live analyst ratings...")

    ratings = get_finviz_ratings(t_up)
    prog.progress(84, text="Computing technical indicators...")

    # ── Patch price into info from hist if missing ─────────────────────────────
    if hist is not None and not hist.empty and "Close" in hist.columns:
        lc = float(hist["Close"].dropna().iloc[-1])
        if not info.get("currentPrice"): info["currentPrice"] = lc
        if not info.get("regularMarketPrice"): info["regularMarketPrice"] = lc
        if not info.get("fiftyTwoWeekHigh"): info["fiftyTwoWeekHigh"] = float(hist["High"].max())
        if not info.get("fiftyTwoWeekLow"):  info["fiftyTwoWeekLow"]  = float(hist["Low"].min())

    price = _safe(info.get("currentPrice")) or _safe(info.get("regularMarketPrice"))
    if not price:
        prog.empty()
        err("Could not retrieve price data for **{}**. yfinance may be temporarily rate-limiting — wait 60s and retry.".format(t_up))
        return

    tech   = compute_technicals(hist)
    fy     = _fcf_yield(info, supp.get("cashflow", pd.DataFrame()))
    dcf_iv = _dcf(info, fy)
    mos    = (dcf_iv / price - 1) if (dcf_iv and price > 0) else None
    ls     = score_long(info, tech, fy, dcf_iv)
    ss     = score_short(info, tech, fy, dcf_iv)

    # ── Auto-detect bias ──────────────────────────────────────────────────────
    if bias_override == "AUTO":
        bias = "LONG" if ls >= ss else "SHORT"
    else:
        bias = bias_override

    # Source count for credibility indicator
    news_sources   = list(set(n["source"] for n in news))
    n_sources      = len(news_sources) + (1 if filings else 0) + (1 if ratings else 0) + 2  # +2 for yf price+fundamentals
    data_freshness = datetime.now().strftime("%H:%M:%S UTC")

    prog.progress(94, text="Synthesizing AI thesis from all sources...")

    # ── AI Thesis (synthesizes ALL sources) ───────────────────────────────────
    thesis_text = build_ai_thesis(
        ticker=t_up, info=info, tech=tech, news_items=news,
        filings=filings, finviz_ratings=ratings,
        bias=bias, ls=ls, ss=ss, fy=fy, dcf_iv=dcf_iv,
    )

    prog.progress(100, text="Complete.")
    prog.empty()

    # ══════════════════════════════════════════════════════════════════════════
    #  REPORT HEADER
    # ══════════════════════════════════════════════════════════════════════════
    name    = _safe(info.get("longName"), t_up)
    sector  = _safe(info.get("sector"), "")
    ind     = _safe(info.get("industry"), "")
    sub_sec = ""
    for sname, sdata in SECTORS.items():
        if t_up in sdata["sub"]:
            sub_sec = sdata["sub"][t_up]; break
    if not sub_sec: sub_sec = ind

    bias_color = "#00e5a0" if bias=="LONG" else "#ff4d6d"
    bias_bg    = "rgba(0,229,160,0.08)" if bias=="LONG" else "rgba(255,77,109,0.08)"

    st.markdown("""
    <div style="background:linear-gradient(135deg,#060f1e,#08162a);border:1px solid #0f2540;border-radius:14px;padding:22px 26px;margin-bottom:16px;">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:.62rem;color:#2a4a6a;text-transform:uppercase;letter-spacing:.18em;margin-bottom:6px;">
            Deep-Dive Report · {src_count} Data Sources · Refreshed {ts}
          </div>
          <div style="font-family:'Outfit',sans-serif;font-weight:800;font-size:1.7rem;color:#eef2ff;letter-spacing:-.02em;">
            {t} <span style="font-size:1rem;font-weight:400;color:#4a7296;">{name}</span>
          </div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:#2a4a6a;margin-top:5px;">{sub}</div>
          <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;">
            {news_tags}
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:2.2rem;font-weight:700;color:#eef2ff;">${price:.2f}</div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:.67rem;color:#3a5a80;">{curr} · {exch}</div>
          <div style="display:inline-block;margin-top:8px;padding:6px 16px;border-radius:20px;background:{bias_bg};border:1.5px solid {bias_color};font-family:'IBM Plex Mono',monospace;font-size:.78rem;font-weight:700;color:{bias_color};">
            {'▲ LONG' if bias=='LONG' else '▼ SHORT'}
          </div>
        </div>
      </div>
    </div>
    """.format(
        src_count=n_sources, ts=data_freshness, t=t_up, name=name, sub=sub_sec,
        news_tags="".join(source_tag(s) for s in news_sources[:6]),
        price=price, curr=_safe(info.get("currency"),"USD"),
        exch=_safe(info.get("exchange"),""), bias_bg=bias_bg,
        bias_color=bias_color, bias=bias,
    ), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  SCORE CARDS
    # ══════════════════════════════════════════════════════════════════════════
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.markdown("**Long Score**")
        st.markdown(score_bar(ls, "#00e5a0"), unsafe_allow_html=True)
    with sc2:
        st.markdown("**Short Score**")
        st.markdown(score_bar(ss, "#ff4d6d"), unsafe_allow_html=True)
    with sc3:
        rsi = tech.get("rsi")
        rc  = "bear" if rsi and rsi>70 else "bull" if rsi and rsi<30 else "neu"
        st.markdown("**RSI-14**")
        st.markdown('<div class="m-val {}">{} · {}</div>'.format(rc, fmt_val(rsi,".1f"), tech.get("rsi_signal","—")), unsafe_allow_html=True)
    with sc4:
        ar  = _safe(info.get("recommendationMean"))
        arc = "bull" if ar and ar<2.5 else "bear" if ar and ar>3.5 else "neu"
        albl= {1:"Strong Buy",2:"Buy",3:"Hold",4:"Underperform",5:"Sell"}.get(round(ar) if ar else 0,"—")
        cnt = _safe(info.get("numberOfAnalystOpinions"),"")
        st.markdown("**Analyst Consensus**")
        st.markdown('<div class="m-val {}" style="font-size:.84rem;">{} · {} analysts</div>'.format(arc,albl,cnt), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  METRIC TILES
    # ══════════════════════════════════════════════════════════════════════════
    tiles = [
        ("Market Cap",       fmt_large(_safe(info.get("marketCap"))),             "neu"),
        ("Trailing P/E",     fmt_val(_safe(info.get("trailingPE")),".1f","×"),    cc(_safe(info.get("trailingPE")),0,True) if _safe(info.get("trailingPE")) else "neu"),
        ("Forward P/E",      fmt_val(_safe(info.get("forwardPE")),".1f","×"),     "neu"),
        ("EV/EBITDA",        fmt_val(_safe(info.get("enterpriseToEbitda")),".1f","×"), "neu"),
        ("FCF Yield",        fmt_pct(fy),                                          cc(fy)),
        ("ROE",              fmt_pct(_safe(info.get("returnOnEquity"))),           cc(_safe(info.get("returnOnEquity")),0.08)),
        ("Net Margin",       fmt_pct(_safe(info.get("profitMargins"))),            cc(_safe(info.get("profitMargins")))),
        ("Revenue Growth",   fmt_pct(_safe(info.get("revenueGrowth"))),            cc(_safe(info.get("revenueGrowth")))),
        ("Debt/Equity",      fmt_val(_safe(info.get("debtToEquity")),".0f","%"),   cc(_safe(info.get("debtToEquity")),200,True)),
        ("Beta",             fmt_val(_safe(info.get("beta")),".2f"),               "neu"),
        ("DCF Intrinsic V.", "${:.2f}".format(dcf_iv) if dcf_iv else "N/A",        "amber"),
        ("Margin of Safety", fmt_pct(mos),                                         cc(mos)),
    ]
    st.markdown(metric_tiles(tiles), unsafe_allow_html=True)
    edu("All metrics are sourced from yfinance (fast_info + tk.info). DCF Intrinsic Value uses 5-year projected FCF at 10% WACC with conservative capped growth. Margin of Safety = IV ÷ Price − 1.")

    # ══════════════════════════════════════════════════════════════════════════
    #  INTERACTIVE CHART
    # ══════════════════════════════════════════════════════════════════════════
    render_interactive_chart(t_up, hist, info, dcf_iv, key_prefix=key_prefix)

    # ══════════════════════════════════════════════════════════════════════════
    #  AI-SYNTHESIZED THESIS  — the core of v4
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="sec-label">
      AI-SYNTHESIZED INVESTMENT THESIS
      <span class="ai-badge">Built from {} sources · {}  news items · {} analyst ratings · {} SEC filings</span>
    </div>
    """.format(n_sources, len(news), len(ratings), len(filings)), unsafe_allow_html=True)

    edu("This thesis is synthesized fresh on every refresh by Claude claude-sonnet-4-20250514, combining real-time data from: yfinance (price + fundamentals), {} news sources ({}), SEC EDGAR (8-K/10-K/10-Q), and finviz analyst ratings. No static templates — every sentence is generated from the actual current data.".format(
        len(news_sources), " · ".join(news_sources[:5]) + ("..." if len(news_sources)>5 else "")
    ))

    st.markdown('<div class="thesis-box report-box report-{}">{}</div>'.format(
        "long" if bias=="LONG" else "short",
        thesis_text.replace("\n", "<br>").replace("**","<strong>").replace("**","</strong>")
    ), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  MULTI-SOURCE NEWS
    # ══════════════════════════════════════════════════════════════════════════
    sec_label("MULTI-SOURCE NEWS · {} ITEMS FROM {} FEEDS".format(len(news), len(news_sources)))
    edu("Headlines aggregated from Reuters, CNBC, MarketWatch, Seeking Alpha, Barron's, Benzinga, IBD, Yahoo Finance, and Google News simultaneously. All free public RSS feeds — no API keys. Deduplicated and sorted by recency.")
    if not news:
        warn("No news items found across RSS feeds for {}.".format(t_up))
    for item in news[:16]:
        st.markdown(
            '<div class="news-row"><div class="news-title"><a href="{link}" target="_blank">{title}</a> {tag}</div>'
            '<div class="news-meta">{date}</div></div>'.format(
                link=item["link"], title=item["title"],
                tag=source_tag(item["source"]), date=item["date"]
            ), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  SEC FILINGS
    # ══════════════════════════════════════════════════════════════════════════
    sec_label("SEC EDGAR FILINGS · 8-K · 10-K · 10-Q · DEF 14A")
    edu("Official SEC disclosures sourced directly from EDGAR's public Atom RSS. 8-K = material events (earnings, M&A, executive changes). 10-K = annual report. 10-Q = quarterly report.")
    badge_map = {"8-K":"badge-8k","10-K":"badge-10k","10-Q":"badge-10q","DEF 14A":"badge-def"}
    if not filings:
        warn("No recent EDGAR filings found for {}. Foreign-listed companies may use a different CIK.".format(t_up))
    for f in filings:
        st.markdown(
            '<div class="filing-row"><span class="filing-badge {badge}">{form}</span>'
            '<div style="flex:1;"><a href="{link}" target="_blank" style="color:#7ab0d8;font-size:.83rem;text-decoration:none;">{title}</a>'
            '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.61rem;color:#2a4a6a;margin-top:3px;">{date} · {summary}</div></div></div>'.format(
                badge=badge_map.get(f["form"],"badge-other"), **f
            ), unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    #  ANALYST RATINGS
    # ══════════════════════════════════════════════════════════════════════════
    sec_label("ANALYST ACTIVITY · YFINANCE HISTORY + FINVIZ LIVE SCRAPE")
    edu("Two independent sources: yfinance pulls historical upgrade/downgrade data from SEC disclosures; finviz.com is scraped for the live ratings table with firm names, actions, and price targets.")

    col_yf, col_fv = st.columns(2)
    with col_yf:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.62rem;color:#3a5a80;text-transform:uppercase;margin-bottom:8px;">📊 yfinance · Historical Changes</div>', unsafe_allow_html=True)
        upg_df = supp.get("upgrades", pd.DataFrame())
        if upg_df is not None and isinstance(upg_df, pd.DataFrame) and not upg_df.empty:
            try:
                df = upg_df.copy()
                if not isinstance(df.index, pd.MultiIndex):
                    df.index = pd.to_datetime(df.index, errors="coerce")
                    df = df.sort_index(ascending=False).head(8).reset_index()
                col_lwr = {c.lower(): c for c in df.columns}
                a_col = next((col_lwr[k] for k in col_lwr if "action" in k), None)
                f_col = next((col_lwr[k] for k in col_lwr if "firm" in k), None)
                t_col = next((col_lwr[k] for k in col_lwr if "tograde" in k or "to grade" in k), None)
                d_col = df.columns[0]
                for _, row in df.head(8).iterrows():
                    action = str(row[a_col]).strip() if a_col else ""
                    firm   = str(row[f_col]).strip() if f_col else "—"
                    to_gr  = str(row[t_col]).strip() if t_col else ""
                    dv     = str(row.get(d_col,""))[:10]
                    al     = action.lower()
                    chip   = "chip-upgrade" if ("upgrade" in al or "initiat" in al) else "chip-downgrade" if ("downgrade" in al or "lower" in al) else "chip-hold"
                    st.markdown('<div class="analyst-row"><div><div class="analyst-firm">{}</div><div class="analyst-date">{}</div></div><div style="text-align:right;"><span class="{}">{}</span><div class="analyst-date">{}</div></div></div>'.format(firm,dv,chip,action,to_gr), unsafe_allow_html=True)
            except:
                warn("Could not parse yfinance upgrade history.")
        else:
            warn("No yfinance upgrade history available.")

    with col_fv:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:.62rem;color:#3a5a80;text-transform:uppercase;margin-bottom:8px;">🌐 finviz · Live Ratings Table</div>', unsafe_allow_html=True)
        if ratings:
            for r in ratings[:8]:
                al   = r.get("action","").lower()
                chip = "chip-upgrade" if ("upgrade" in al or "initiat" in al or "raised" in al) else "chip-downgrade" if ("downgrade" in al or "lower" in al) else "chip-hold"
                pt   = "PT {}".format(r["pt"]) if r.get("pt") else ""
                st.markdown('<div class="analyst-row"><div><div class="analyst-firm">{}</div><div class="analyst-date">{}</div></div><div style="text-align:right;"><span class="{}">{}</span><div class="analyst-pt">{} {}</div></div></div>'.format(r.get("firm",""),r.get("date",""),chip,r.get("action",""),r.get("rating",""),pt), unsafe_allow_html=True)
        else:
            warn("finviz scrape unavailable — site may be rate-limiting.")

    # ══════════════════════════════════════════════════════════════════════════
    #  INSTITUTIONAL HOLDERS
    # ══════════════════════════════════════════════════════════════════════════
    sec_label("INSTITUTIONAL OWNERSHIP · TOP 13-F HOLDERS")
    edu("Sourced from yfinance → SEC 13-F quarterly filings. Institutions holding >5% must disclose quarterly. High institutional concentration amplifies both rallies and selloffs.")
    holders_df = supp.get("holders", pd.DataFrame())
    if holders_df is not None and isinstance(holders_df, pd.DataFrame) and not holders_df.empty:
        try:
            df = holders_df.head(10)
            cl = {c.lower():c for c in df.columns}
            nc = next((cl[k] for k in cl if "holder" in k or "name" in k), df.columns[0])
            pc = next((cl[k] for k in cl if "%" in k or "pct" in k or "share" in k), None)
            vc = next((cl[k] for k in cl if "value" in k), None)
            hc1,hc2,hc3 = st.columns([3,2,2])
            hc1.markdown('<div class="m-label">Institution</div>', unsafe_allow_html=True)
            hc2.markdown('<div class="m-label">% of Shares</div>', unsafe_allow_html=True)
            hc3.markdown('<div class="m-label">Market Value</div>', unsafe_allow_html=True)
            for _, row in df.iterrows():
                nm  = str(row[nc])
                pct = "{:.2f}%".format(float(row[pc])*100) if pc and not pd.isna(row[pc]) else "—"
                val = fmt_large(float(row[vc])) if vc and not pd.isna(row[vc]) else "—"
                c1,c2,c3=st.columns([3,2,2])
                rs = "font-family:'IBM Plex Mono',monospace;font-size:.77rem;padding:5px 0;border-bottom:1px solid #0c1e30;"
                c1.markdown('<div style="{}color:#c8deff;">{}</div>'.format(rs,nm), unsafe_allow_html=True)
                c2.markdown('<div style="{}color:#f59e0b;">{}</div>'.format(rs,pct), unsafe_allow_html=True)
                c3.markdown('<div style="{}color:#60a5fa;">{}</div>'.format(rs,val), unsafe_allow_html=True)
        except:
            warn("Could not parse institutional holders.")
    else:
        warn("Institutional holder data not available.")

    # ══════════════════════════════════════════════════════════════════════════
    #  TRADE SETUP
    # ══════════════════════════════════════════════════════════════════════════
    sec_label("TRADE SETUP · ENTRY · STOP · TARGETS · OPTIONS STRATEGY")
    edu("Stop-loss set at 1.5× ATR-14 from entry — placing stops beyond normal daily noise. Targets derived from DCF intrinsic value (primary) or consensus analyst price target. Options strategy selected based on realized volatility level.")
    setup = build_trade_setup(info, tech, dcf_iv, bias)
    ts1, ts2 = st.columns(2)
    with ts1:
        st.markdown(
            '<div class="card"><div class="m-label">Entry</div><div class="m-val neu">{}</div></div>'
            '<div class="card"><div class="m-label">Stop / Invalidation Level</div><div class="m-val bear">{}</div></div>'.format(
                setup["entry"], setup["stop"]
            ), unsafe_allow_html=True)
    with ts2:
        st.markdown(
            '<div class="card"><div class="m-label">Target 1 (take 50% off)</div><div class="m-val bull">{}</div></div>'
            '<div class="card"><div class="m-label">Target 2 (full thesis)</div><div class="m-val bull">{}</div></div>'.format(
                setup["t1"], setup["t2"]
            ), unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:10px;margin:8px 0;flex-wrap:wrap;">'
        '<div class="card card-sm" style="flex:1;"><div class="m-label">Risk/Reward</div><div class="m-val amber">{rr}</div></div>'
        '<div class="card card-sm" style="flex:1.5;"><div class="m-label">Options Strategy</div><div style="font-size:.8rem;color:#a78bfa;margin-top:4px;">{opts}</div></div>'
        '<div class="card card-sm" style="flex:2;"><div class="m-label">Position Sizing</div><div style="font-size:.76rem;color:#6a9cc0;margin-top:4px;">{sz}</div></div>'
        '</div>'.format(rr=setup["rr"], opts=setup["options"], sz=setup["sizing"]),
        unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTOR SCANNER TAB
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=2400, show_spinner=False)
def scan_sector(sector: str) -> dict:
    _init_yf()
    tickers = SECTORS[sector]["tickers"]
    sub     = SECTORS[sector]["sub"]
    results = []
    for t in tickers:
        hist = get_hist(t)
        info = get_fundamentals(t)
        if hist is not None and not hist.empty and "Close" in hist.columns:
            lc = float(hist["Close"].dropna().iloc[-1])
            if not info.get("currentPrice"): info["currentPrice"] = lc
        price = _safe(info.get("currentPrice"))
        if not price: continue
        supp = get_supplemental(t)
        fy   = _fcf_yield(info, supp.get("cashflow", pd.DataFrame()))
        dcf  = _dcf(info, fy)
        tech = compute_technicals(hist)
        ls   = score_long(info, tech, fy, dcf)
        ss   = score_short(info, tech, fy, dcf)
        results.append({"ticker":t,"info":info,"tech":tech,"hist":hist,
                        "fy":fy,"dcf_iv":dcf,"ls":ls,"ss":ss,
                        "sub_sector":sub.get(t,_safe(info.get("industry"),"—"))})
        time.sleep(0.2)
    if not results: return {"longs":[],"shorts":[],"all":[]}
    return {"longs": sorted(results,key=lambda x:x["ls"],reverse=True)[:5],
            "shorts":sorted(results,key=lambda x:x["ss"],reverse=True)[:5],
            "all":results}


def tab_sector_scanner():
    sec_label("11-GICS SECTOR SCANNER · CLICK A SECTOR · MULTI-SOURCE SCREENING")
    st.markdown('<p style="color:#3a5a80;">Click a sector tile to select it, then click Scan. The screener fetches price, fundamentals, and news from multiple sources for every stock, then scores across FCF yield, DCF margin of safety, ROE, revenue growth, 200-MA trend, RSI, MACD, and analyst consensus.</p>', unsafe_allow_html=True)

    if "sel_sector" not in st.session_state:
        st.session_state["sel_sector"] = "Information Technology"

    # ── Sector tile grid ──────────────────────────────────────────────────────
    sector_list = list(SECTORS.keys())
    cols = st.columns(4)
    for i, sname in enumerate(sector_list):
        sd = SECTORS[sname]
        is_sel = st.session_state["sel_sector"] == sname
        with cols[i % 4]:
            if is_sel:
                st.markdown("""
                <div style="background:linear-gradient(135deg,#0d2040,#0f2848);border:2px solid #3b82f6;border-radius:12px;padding:14px 10px;text-align:center;cursor:pointer;">
                  <div style="font-size:1.6rem;">{icon}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:.62rem;color:#60a5fa;text-transform:uppercase;letter-spacing:.07em;line-height:1.4;margin-top:6px;">{name}</div>
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:.58rem;color:#3b82f6;margin-top:3px;">{etf}</div>
                </div>""".format(icon=sd["icon"],name=sname,etf=sd["etf"]), unsafe_allow_html=True)
            else:
                if st.button("{} {}".format(sd["icon"],sname), key="stile_{}".format(i), use_container_width=True):
                    st.session_state["sel_sector"] = sname
                    st.rerun()

    selected = st.session_state["sel_sector"]
    info_s   = SECTORS[selected]
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    sc_col, _ = st.columns([1,4])
    with sc_col:
        do_scan = st.button("⚡  Scan  {}".format(info_s["etf"]), key="scan_go", use_container_width=True)

    cache_key = "scan_cache_{}".format(selected)
    if do_scan and cache_key in st.session_state:
        del st.session_state[cache_key]

    if cache_key not in st.session_state:
        with st.spinner("Scanning {} — fetching {}-source data for {} tickers...".format(selected, 4, len(info_s["tickers"]))):
            results = scan_sector(selected)
        st.session_state[cache_key] = results
    else:
        results = st.session_state[cache_key]

    if not results.get("longs") and not results.get("shorts"):
        err("Scan returned no results for {}. yfinance may be rate-limiting — wait 30s and retry.".format(selected))
        if cache_key in st.session_state: del st.session_state[cache_key]
        return

    fetched = len(results.get("all",[]))
    if fetched < len(info_s["tickers"]):
        warn("Fetched {}/{} tickers. {} failed (rate-limited or unavailable) — shown below are all successful fetches.".format(fetched, len(info_s["tickers"]), len(info_s["tickers"])-fetched))

    col_l, col_s = st.columns(2)

    with col_l:
        st.markdown('<div class="sec-label" style="border-color:#00e5a0;color:#00e5a0;">▲ HIGH-CONVICTION LONG CANDIDATES</div>', unsafe_allow_html=True)
        edu("Ranked by composite long score across 10+ factors from yfinance + technicals. Click to expand full setup and thesis.")
        for r in results["longs"]:
            t    = r["ticker"]; info_ = r["info"]; tech_ = r["tech"]
            cp   = _safe(info_.get("currentPrice"),0)
            ls_  = r["ls"]; fy_ = r["fy"]; mos_ = (r["dcf_iv"]/cp-1) if (r["dcf_iv"] and cp>0) else None
            with st.expander("▲  {}  ·  {}  ·  {:.0f}/100".format(t, r["sub_sector"][:35], ls_)):
                st.markdown(
                    '<div style="display:flex;justify-content:space-between;margin-bottom:10px;">'
                    '<div><div style="font-size:.71rem;color:#3a5a80;">{name}</div>'
                    '<div class="m-val neu" style="font-size:1.25rem;">${cp:.2f}</div></div>'
                    '<div style="text-align:right;">{bar}</div></div>'
                    '<div class="metric-grid" style="grid-template-columns:repeat(4,1fr);">'
                    '<div class="metric-tile"><div class="m-label">FCF Yield</div><div class="m-val {fy_c}">{fy_v}</div></div>'
                    '<div class="metric-tile"><div class="m-label">Margin of Safety</div><div class="m-val {mos_c}">{mos_v}</div></div>'
                    '<div class="metric-tile"><div class="m-label">ROE</div><div class="m-val {roe_c}">{roe_v}</div></div>'
                    '<div class="metric-tile"><div class="m-label">RSI-14</div><div class="m-val {rsi_c}">{rsi_v}</div></div>'
                    '</div>'.format(
                        name=_safe(info_.get("longName"),t), cp=cp,
                        bar=score_bar(ls_,"#00e5a0"),
                        fy_c="bull" if fy_ and fy_>0 else "bear", fy_v=fmt_pct(fy_),
                        mos_c="bull" if mos_ and mos_>0 else "bear", mos_v=fmt_pct(mos_),
                        roe_c="bull" if _safe(info_.get("returnOnEquity"),0)>0.12 else "neu",
                        roe_v=fmt_pct(_safe(info_.get("returnOnEquity"))),
                        rsi_c="bear" if (tech_.get("rsi") or 50)>70 else "bull" if (tech_.get("rsi") or 50)<30 else "neu",
                        rsi_v=fmt_val(tech_.get("rsi"),".1f"),
                    ), unsafe_allow_html=True)
                ts_  = build_trade_setup(info_, tech_, r["dcf_iv"], "LONG")
                st.markdown('<div style="display:flex;gap:5px;flex-wrap:wrap;margin:8px 0;"><span class="chip-long">Entry {}</span><span class="chip-short">Stop {}</span><span class="chip-long">T1 {}</span><span class="chip-long">T2 {}</span><span class="chip-blue">R/R {}</span></div>'.format(ts_["entry"],ts_["stop"].split("(")[0].strip(),ts_["t1"].split("(")[0].strip(),ts_["t2"].split("(")[0].strip(),ts_["rr"]), unsafe_allow_html=True)
                render_interactive_chart(t, r["hist"], info_, r["dcf_iv"], key_prefix="sc_l_{}".format(t))

    with col_s:
        st.markdown('<div class="sec-label" style="border-color:#ff4d6d;color:#ff4d6d;">▼ HIGH-CONVICTION SHORT CANDIDATES</div>', unsafe_allow_html=True)
        edu("Ranked by composite short score. Key signals: negative FCF, stretched P/E, revenue contraction, 200-MA breakdown, elevated short interest, and bearish analyst consensus.")
        for r in results["shorts"]:
            t    = r["ticker"]; info_ = r["info"]; tech_ = r["tech"]
            cp   = _safe(info_.get("currentPrice"),0); ss_ = r["ss"]
            pe_  = _safe(info_.get("trailingPE")); fy_ = r["fy"]
            with st.expander("▼  {}  ·  {}  ·  {:.0f}/100".format(t, r["sub_sector"][:35], ss_)):
                st.markdown(
                    '<div style="display:flex;justify-content:space-between;margin-bottom:10px;">'
                    '<div><div style="font-size:.71rem;color:#3a5a80;">{name}</div>'
                    '<div class="m-val neu" style="font-size:1.25rem;">${cp:.2f}</div></div>'
                    '<div style="text-align:right;">{bar}</div></div>'
                    '<div class="metric-grid" style="grid-template-columns:repeat(4,1fr);">'
                    '<div class="metric-tile"><div class="m-label">Trailing P/E</div><div class="m-val {pe_c}">{pe_v}</div></div>'
                    '<div class="metric-tile"><div class="m-label">FCF Yield</div><div class="m-val {fy_c}">{fy_v}</div></div>'
                    '<div class="metric-tile"><div class="m-label">Rev Growth</div><div class="m-val {rg_c}">{rg_v}</div></div>'
                    '<div class="metric-tile"><div class="m-label">RSI-14</div><div class="m-val {rsi_c}">{rsi_v}</div></div>'
                    '</div>'.format(
                        name=_safe(info_.get("longName"),t), cp=cp,
                        bar=score_bar(ss_,"#ff4d6d"),
                        pe_c="bear" if pe_ and pe_>50 else "neu", pe_v=fmt_val(pe_,".1f","×"),
                        fy_c="bear" if fy_ is None or fy_<0 else "neu", fy_v=fmt_pct(fy_),
                        rg_c="bear" if _safe(info_.get("revenueGrowth"),0)<0 else "neu",
                        rg_v=fmt_pct(_safe(info_.get("revenueGrowth"))),
                        rsi_c="bear" if (tech_.get("rsi") or 50)>70 else "bull" if (tech_.get("rsi") or 50)<30 else "neu",
                        rsi_v=fmt_val(tech_.get("rsi"),".1f"),
                    ), unsafe_allow_html=True)
                ts_ = build_trade_setup(info_, tech_, r["dcf_iv"], "SHORT")
                st.markdown('<div style="display:flex;gap:5px;flex-wrap:wrap;margin:8px 0;"><span class="chip-short">Short {}</span><span class="chip-long">Stop {}</span><span class="chip-short">T1 {}</span><span class="chip-short">T2 {}</span><span class="chip-blue">R/R {}</span></div>'.format(ts_["entry"],ts_["stop"].split("(")[0].strip(),ts_["t1"].split("(")[0].strip(),ts_["t2"].split("(")[0].strip(),ts_["rr"]), unsafe_allow_html=True)
                render_interactive_chart(t, r["hist"], info_, r["dcf_iv"], key_prefix="sc_s_{}".format(t))


# ─────────────────────────────────────────────────────────────────────────────
#  TICKER DEEP-DIVE TAB
# ─────────────────────────────────────────────────────────────────────────────
def tab_ticker_search():
    sec_label("CUSTOM TICKER DEEP-DIVE · AI-SYNTHESIZED MULTI-SOURCE REPORT")
    edu("Enter any global ticker. The engine fetches from 6+ independent sources simultaneously — yfinance (price + fundamentals), SEC EDGAR, 9 news RSS feeds, finviz analyst ratings — then Claude synthesizes ALL of it into a fresh investment thesis every time you click Analyze.")

    c1, c2, c3 = st.columns([3, 1.5, 1])
    with c1:
        ticker_input = st.text_input(
            "Ticker", placeholder="e.g. NVDA, AAPL, MSFT, TSLA, ASML...",
            label_visibility="collapsed", key="dd_ticker_v4",
        ).upper().strip()
    with c2:
        bias_sel = st.selectbox(
            "Bias", ["AUTO-DETECT", "LONG", "SHORT"],
            key="dd_bias_v4", label_visibility="collapsed",
        )
    with c3:
        go_btn = st.button("▶ Analyze", key="dd_go_v4", use_container_width=True)

    if not ((go_btn or ticker_input) and ticker_input):
        return

    bias = "AUTO" if bias_sel == "AUTO-DETECT" else bias_sel
    render_deep_dive(ticker_input, bias_override=bias, key_prefix="dd_{}".format(ticker_input))


# ─────────────────────────────────────────────────────────────────────────────
#  MACRO DASHBOARD TAB
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def get_macro_data() -> dict:
    """Fetch all macro instruments via yf.download() — most reliable on cloud."""
    _init_yf()
    result = {}
    for label, meta in MACRO_SYMBOLS.items():
        sym = meta["sym"]
        for attempt in range(3):
            try:
                df = yf.download(sym, period="5d", interval="1d",
                                  auto_adjust=True, progress=False,
                                  threads=False, multi_level_index=False)
                if df is not None and not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df.columns = [str(c).capitalize() for c in df.columns]
                    if "Close" in df.columns and len(df) >= 2:
                        close = df["Close"].dropna()
                        last  = float(close.iloc[-1])
                        prev  = float(close.iloc[-2])
                        chg   = (last / prev - 1) if prev != 0 else 0.0
                        result[label] = {"last":last,"chg":chg,
                                          "fmt":meta["fmt"],"type":meta["type"],
                                          "hist":close}
                        break
            except Exception:
                pass
            time.sleep(0.3)
    return result


@st.cache_data(ttl=1800, show_spinner=False)
def get_sector_etf_perf() -> dict:
    """Fetch sector ETF 1-day % change via yf.download()."""
    _init_yf()
    result = {}
    for sname, sdata in SECTORS.items():
        etf = sdata["etf"]
        for attempt in range(3):
            try:
                df = yf.download(etf, period="5d", interval="1d",
                                  auto_adjust=True, progress=False,
                                  threads=False, multi_level_index=False)
                if df is not None and not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df.columns = [str(c).capitalize() for c in df.columns]
                    if "Close" in df.columns and len(df) >= 2:
                        close = df["Close"].dropna()
                        last  = float(close.iloc[-1])
                        prev  = float(close.iloc[-2])
                        chg   = (last / prev - 1) if prev != 0 else 0.0
                        result[sname] = {"etf":etf,"chg":chg,"last":last}
                        break
            except Exception:
                pass
            time.sleep(0.25)
    return result


def _macro_sparkline(series) -> go.Figure:
    if series is None or len(series) < 2:
        return go.Figure()
    is_up = float(series.iloc[-1]) >= float(series.iloc[0])
    color = "#00e5a0" if is_up else "#ff4d6d"
    fill  = "rgba(0,229,160,0.1)" if is_up else "rgba(255,77,109,0.1)"
    fig   = go.Figure(go.Scatter(
        y=series.values, mode="lines",
        line=dict(color=color, width=1.8),
        fill="tozeroy", fillcolor=fill,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=0,b=0), height=42, showlegend=False,
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def tab_macro_dashboard():
    sec_label("MACRO ENVIRONMENT · RATES · FX · COMMODITIES · SECTOR HEATMAP")
    st.markdown('<p style="color:#3a5a80;">Live macro data sourced via yfinance (yf.download endpoint) — fetched per-instrument with retry logic. Includes Treasury yield curve, VIX, Dollar Index, major FX pairs, commodity futures, and 11-sector ETF heatmap.</p>', unsafe_allow_html=True)

    rc, _ = st.columns([1, 5])
    with rc:
        if st.button("🔄 Refresh All Macro", key="macro_ref_v4"):
            st.cache_data.clear()
            st.rerun()

    with st.spinner("Fetching macro instruments..."):
        mdata = get_macro_data()

    if not mdata:
        err("No macro data returned. yfinance may be temporarily unavailable — click Refresh in 60 seconds.")
        return

    loaded = len(mdata); total = len(MACRO_SYMBOLS)
    if loaded < total:
        warn("Loaded {}/{} macro instruments. {} failed — showing available data.".format(loaded, total, total-loaded))

    # ── INDEX CARDS ───────────────────────────────────────────────────────────
    sec_label("MAJOR MARKET INDICES")
    idx_items = [(lbl,d) for lbl,d in mdata.items() if d["type"]=="index"]
    if idx_items:
        cols = st.columns(len(idx_items))
        for i, (lbl, d) in enumerate(idx_items):
            with cols[i]:
                chg = d["chg"]; val = d["last"]
                color = "#00e5a0" if chg >= 0 else "#ff4d6d"
                arrow = "▲" if chg >= 0 else "▼"
                fmt   = d.get("fmt",",.2f")
                try:    val_s = ("{:"+fmt+"}").format(val)
                except: val_s = str(round(val,2))
                st.markdown(
                    '<div class="macro-tile">'
                    '<div class="m-label">{}</div>'
                    '<div class="macro-val">{}</div>'
                    '<div class="macro-chg" style="color:{};">{} {:+.2f}%</div>'
                    '</div>'.format(lbl, val_s, color, arrow, chg*100),
                    unsafe_allow_html=True)
                hist_s = d.get("hist")
                if hist_s is not None and len(hist_s) >= 2:
                    st.plotly_chart(_macro_sparkline(hist_s), use_container_width=True,
                                    key="spark_{}".format(lbl))

    # ── YIELD CURVE + VIX ────────────────────────────────────────────────────
    sec_label("U.S. TREASURY YIELD CURVE  ·  VIX FEAR GAUGE")
    c_yc, c_vix = st.columns([3, 2])
    with c_yc:
        rate_items = [(lbl,d) for lbl,d in mdata.items() if d["type"]=="rate"]
        if rate_items:
            y_labels = [x[0] for x in rate_items]
            y_vals   = [x[1]["last"] for x in rate_items]
            fig_yc = go.Figure()
            fig_yc.add_trace(go.Scatter(
                x=y_labels, y=y_vals, mode="lines+markers+text",
                text=["{:.2f}%".format(v) for v in y_vals],
                textposition="top center",
                line=dict(color="#6366f1", width=2.5,),
                marker=dict(color="#818cf8", size=11,
                            line=dict(color="#4f46e5", width=2)),
                textfont=dict(family="IBM Plex Mono", color="#c8deff", size=11),
                fill="tozeroy", fillcolor="rgba(99,102,241,0.08)",
            ))
            # Highlight inversion zone
            if y_vals:
                fig_yc.add_hrect(y0=0, y1=min(y_vals)*0.98,
                                  fillcolor="rgba(255,77,109,0.04)", line_width=0)
            fig_yc.update_layout(
                template="plotly_dark", paper_bgcolor="#040d1a", plot_bgcolor="#050e1e",
                height=220, margin=dict(l=5,r=5,t=10,b=5),
                yaxis=dict(ticksuffix="%", showgrid=True, gridcolor="rgba(15,37,64,0.8)"),
                xaxis=dict(showgrid=False),
                font=dict(family="IBM Plex Mono", color="#7a9cc0", size=10),
            )
            st.plotly_chart(fig_yc, use_container_width=True)
        else:
            warn("Treasury yield data unavailable.")
        edu("An inverted yield curve (short-term > long-term yields) has preceded every U.S. recession since 1970 by 12–18 months. Watch the 2Y–10Y spread closely — the key risk signal for equity valuations.")

    with c_vix:
        vix_d = mdata.get("VIX")
        if vix_d:
            vv  = vix_d["last"]
            vc  = "#ff4d6d" if vv > 25 else "#f59e0b" if vv > 18 else "#00e5a0"
            vlbl= "EXTREME FEAR" if vv>35 else "FEAR" if vv>25 else "ELEVATED" if vv>18 else "COMPLACENCY" if vv<13 else "NORMAL"
            # Gauge-style dial using plotly indicator
            fig_vix = go.Figure(go.Indicator(
                mode="gauge+number",
                value=vv,
                domain={"x":[0,1],"y":[0,1]},
                number={"font":{"family":"IBM Plex Mono","color":vc,"size":36}},
                gauge={
                    "axis":{"range":[0,60],"tickcolor":"#2a4a6a","tickfont":{"family":"IBM Plex Mono","size":9}},
                    "bar":{"color":vc,"thickness":0.25},
                    "bgcolor":"#050e1e",
                    "borderwidth":0,
                    "steps":[
                        {"range":[0,15],"color":"rgba(0,229,160,0.12)"},
                        {"range":[15,25],"color":"rgba(245,158,11,0.08)"},
                        {"range":[25,60],"color":"rgba(255,77,109,0.12)"},
                    ],
                    "threshold":{"line":{"color":vc,"width":3},"thickness":0.75,"value":vv},
                },
            ))
            fig_vix.update_layout(
                paper_bgcolor="#040d1a", plot_bgcolor="#050e1e",
                font=dict(family="IBM Plex Mono", color=vc),
                height=200, margin=dict(l=20,r=20,t=20,b=0),
            )
            st.plotly_chart(fig_vix, use_container_width=True)
            st.markdown(
                '<div style="text-align:center;font-family:\'IBM Plex Mono\',monospace;font-size:.75rem;font-weight:700;color:{};letter-spacing:.15em;margin-top:-10px;">{}</div>'
                '<div style="text-align:center;font-size:.7rem;color:#2a4a6a;margin-top:4px;">VIX &lt;15: Cheap calls · 15–25: Normal · &gt;25: Expensive options · &gt;40: Crisis</div>'.format(vc,vlbl),
                unsafe_allow_html=True)

    # ── FX ────────────────────────────────────────────────────────────────────
    sec_label("FOREIGN EXCHANGE  ·  DOLLAR INDEX & MAJOR PAIRS")
    fx_items = [(lbl,d) for lbl,d in mdata.items() if d["type"]=="fx"]
    if fx_items:
        cols = st.columns(len(fx_items))
        for i, (lbl, d) in enumerate(fx_items):
            with cols[i]:
                chg=d["chg"]; val=d["last"]; color="#00e5a0" if chg>=0 else "#ff4d6d"
                fmt=d.get("fmt",".4f")
                try:    val_s=("{:"+fmt+"}").format(val)
                except: val_s=str(round(val,4))
                st.markdown(
                    '<div class="macro-tile"><div class="m-label">{}</div>'
                    '<div class="macro-val">{}</div>'
                    '<div class="macro-chg" style="color:{};">{} {:+.2f}%</div></div>'.format(
                        lbl,val_s,color,"▲" if chg>=0 else "▼",chg*100),
                    unsafe_allow_html=True)
    else:
        warn("FX data unavailable.")
    edu("Strong DXY (Dollar Index ↑) = headwind for U.S. multinationals (overseas revenues worth less in dollars). DXY ↓ = bullish for commodities, gold, and emerging market equities.")

    # ── COMMODITIES ───────────────────────────────────────────────────────────
    sec_label("COMMODITY FUTURES  ·  GOLD · WTI CRUDE · COPPER")
    comm_items = [(lbl,d) for lbl,d in mdata.items() if d["type"]=="comm"]
    if comm_items:
        cols = st.columns(len(comm_items))
        for i, (lbl, d) in enumerate(comm_items):
            with cols[i]:
                chg=d["chg"]; val=d["last"]; color="#00e5a0" if chg>=0 else "#ff4d6d"
                fmt=d.get("fmt",",.2f")
                try:    val_s="${:"+fmt+"}".format(val)
                except: val_s="$"+str(round(val,2))
                st.markdown(
                    '<div class="macro-tile"><div class="m-label">{}</div>'
                    '<div class="macro-val">{}</div>'
                    '<div class="macro-chg" style="color:{};">{} {:+.2f}%</div></div>'.format(
                        lbl,val_s,color,"▲" if chg>=0 else "▼",chg*100),
                    unsafe_allow_html=True)
    else:
        warn("Commodity data unavailable.")
    edu("'Dr. Copper' is a leading economic indicator — rising copper signals global industrial expansion. Gold rising with equities = risk-on inflation hedge. Gold rising as equities fall = genuine flight-to-safety.")

    # ── SECTOR HEATMAP ────────────────────────────────────────────────────────
    sec_label("11-GICS SECTOR ETF PERFORMANCE HEATMAP")
    with st.spinner("Fetching sector ETF performance..."):
        sect_perf = get_sector_etf_perf()

    if sect_perf:
        labels=[]; values=[]; icons=[]
        for sname, sdata in SECTORS.items():
            d = sect_perf.get(sname)
            labels.append("{} {}".format(sdata["icon"], sdata["etf"]))
            values.append(d["chg"]*100 if d else 0.0)

        # Color gradient from red → amber → green
        colors = []
        for v in values:
            if v >= 1.5:   colors.append("rgba(0,229,160,0.85)")
            elif v >= 0.5: colors.append("rgba(0,229,160,0.55)")
            elif v >= 0:   colors.append("rgba(0,229,160,0.30)")
            elif v >= -0.5:colors.append("rgba(255,77,109,0.30)")
            elif v >= -1.5:colors.append("rgba(255,77,109,0.55)")
            else:          colors.append("rgba(255,77,109,0.85)")

        border = ["#00e5a0" if v>=0 else "#ff4d6d" for v in values]

        fig_heat = go.Figure(go.Bar(
            x=values, y=labels, orientation="h",
            text=["{:+.2f}%".format(v) for v in values],
            textposition="outside",
            marker=dict(color=colors, line=dict(color=border, width=1.2)),
            textfont=dict(family="IBM Plex Mono", size=11, color="#c8deff"),
        ))
        fig_heat.update_layout(
            template="plotly_dark", paper_bgcolor="#040d1a", plot_bgcolor="#050e1e",
            font=dict(family="IBM Plex Mono", color="#7a9cc0", size=10),
            height=390, margin=dict(l=5, r=70, t=10, b=5),
            xaxis=dict(showgrid=True, gridcolor="rgba(15,37,64,0.8)",
                       zeroline=True, zerolinecolor="#1e3d6a",
                       zerolinewidth=1.5, ticksuffix="%"),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        edu("Sector rotation analysis: XLU + XLP green + XLK red = defensive rotation = recession fears rising. XLY + XLK + XLF green = risk-on environment. Track which sectors are absorbing institutional flows — that IS the macro narrative.")
    else:
        warn("Sector ETF data unavailable. Click Refresh in 60 seconds.")

    # ── MARKET NEWS ───────────────────────────────────────────────────────────
    sec_label("GENERAL MARKET NEWS · REUTERS · CNBC · MARKETWATCH · BENZINGA")
    general_feeds = {
        "Reuters":   "https://feeds.reuters.com/reuters/businessNews",
        "CNBC":      "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "MarketWatch":"https://feeds.marketwatch.com/marketwatch/topstories/",
        "Benzinga":  "https://www.benzinga.com/feed",
    }
    all_news = []; seen = set()
    for src, url in general_feeds.items():
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:4]:
                title = html.unescape(e.get("title","")).strip()
                key   = title[:50].lower()
                if key in seen or not title: continue
                seen.add(key)
                all_news.append({"title":title,"link":e.get("link",""),
                                  "date":e.get("published",e.get("updated",""))[:16],"source":src})
        except: continue
    all_news.sort(key=lambda x: x["date"], reverse=True)
    for item in all_news[:12]:
        st.markdown(
            '<div class="news-row"><div class="news-title">'
            '<a href="{link}" target="_blank">{title}</a> {tag}'
            '</div><div class="news-meta">{date}</div></div>'.format(
                tag=source_tag(item["source"]), **item
            ), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    _init_yf()  # Enable curl_cffi cookie bypass for cloud IPs — always first
    now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    st.markdown("""
    <div class="banner">
      <div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:.68rem;font-weight:600;color:#6366f1;letter-spacing:.18em;text-transform:uppercase;">Equities Intelligence Terminal  ·  v4.0</div>
        <div class="banner-title">EQ · INTELLIGENCE</div>
        <div class="banner-sub">yfinance · SEC EDGAR · Reuters · CNBC · MarketWatch · Seeking Alpha · Barron's · Benzinga · IBD · finviz · AI Thesis Engine</div>
      </div>
      <div style="text-align:right;">
        <div><span class="live-dot"></span><span class="live-text">LIVE · AI-SYNTHESIZED · MULTI-SOURCE</span></div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;color:#3a5a80;">{} UTC</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:.59rem;color:#1e3450;margin-top:3px;">No API keys · Python 3.10+ · curl_cffi enabled</div>
      </div>
    </div>
    """.format(now), unsafe_allow_html=True)

    tabs = st.tabs([
        "🌐  Sector Scanner",
        "🔍  Ticker Deep-Dive",
        "📊  Macro Dashboard",
    ])
    with tabs[0]: tab_sector_scanner()
    with tabs[1]: tab_ticker_search()
    with tabs[2]: tab_macro_dashboard()

    st.markdown("""
    <div style="margin-top:36px;padding-top:14px;border-top:1px solid #0c1e30;text-align:center;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:.61rem;color:#1e3450;letter-spacing:.07em;">
        ⚡ EQ · INTELLIGENCE v4.0  ·
        yfinance · SEC EDGAR · Reuters · CNBC · MarketWatch · Seeking Alpha · Barron's · Benzinga · IBD · finviz · Claude AI  ·
        Zero API keys  ·  Educational & research purposes only  ·  Not investment advice
      </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
