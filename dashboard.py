import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ─────────────────────────────────────────────
# PAGE CONFIGURATION & ENTERPRISE THEME
# ─────────────────────────────────────────────
st.set_page_config(page_title="Real-Time PR Command Center", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family:'Inter', sans-serif; background:#0f172a; color: #e2e8f0; }
    .stApp { background:#0f172a; }
    
    /* Live Indicator Pulse */
    .live-indicator { display: inline-block; width: 12px; height: 12px; background-color: #ef4444; border-radius: 50%; margin-right: 8px; box-shadow: 0 0 8px #ef4444; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
    
    /* Enterprise Cards */
    .metric-card { background:#1e293b; border:1px solid #334155; border-radius:6px; padding:1.25rem; margin-bottom:1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .metric-title { color:#94a3b8; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; }
    .metric-value { color:#f8fafc; font-size:2.2rem; font-weight:700; margin-top:0.4rem; letter-spacing:-0.02em; }
    
    /* Status Badges */
    .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
    .badge-positive { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-negative { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-neutral { background: rgba(148, 163, 184, 0.1); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA ACQUISITION
# ─────────────────────────────────────────────
def load_live_data():
    try:
        # Read the live CSV file. We grab the last 200 rows to keep the UI snappy
        df = pd.read_csv("live_mentions.csv")
        return df.tail(200)
    except FileNotFoundError:
        return pd.DataFrame()

df = load_live_data()

# ─────────────────────────────────────────────
# DASHBOARD UI: HEADER & KPIs
# ─────────────────────────────────────────────
c_header1, c_header2 = st.columns([4, 1])
with c_header1:
    st.markdown("<h1 style='color:#f8fafc; font-size:1.8rem; margin-bottom:0;'>SOCIAL LISTENING COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em;'>Real-Time Brand Perception & PR Alerting</p>", unsafe_allow_html=True)
with c_header2:
    st.markdown("<div style='text-align:right; margin-top:1rem;'><span class='live-indicator'></span><span style='color:#ef4444; font-weight:bold; letter-spacing:1px;'>LIVE FEED</span></div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#334155; margin-top:0.5rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)

if df.empty:
    st.warning("Awaiting live data stream... Ensure data_streamer.py is running.")
    st.stop()

# Calculate live metrics
total_mentions = len(df)
current_sentiment = df['Compound_Score'].mean()
positive_ratio = (len(df[df['Sentiment_Label'] == 'Positive']) / total_mentions) * 100 if total_mentions > 0 else 0

# Determine PR Status
if current_sentiment < -0.15:
    status_text = "CRITICAL: PR CRISIS"
    status_color = "#ef4444"
elif current_sentiment > 0.15:
    status_text = "HEALTHY"
    status_color = "#10b981"
else:
    status_text = "NEUTRAL / MONITORING"
    status_color = "#facc15"

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Active Mentions (Last Window)</div><div class='metric-value'>{total_mentions}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Global Sentiment Score</div><div class='metric-value'>{current_sentiment:.2f}</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Positive Sentiment Ratio</div><div class='metric-value'>{positive_ratio:.1f}%</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card' style='border-color:{status_color};'><div class='metric-title'>System PR Status</div><div class='metric-value' style='color:{status_color}; font-size:1.6rem; padding-top:0.4rem;'>{status_text}</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DASHBOARD UI: VISUALIZATIONS
# ─────────────────────────────────────────────
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em;'>Live Sentiment Trajectory</h3>", unsafe_allow_html=True)
    
    # Calculate a rolling average to smooth out the jagged live data
    df['Rolling_Sentiment'] = df['Compound_Score'].rolling(window=10, min_periods=1).mean()
    
    fig_line = px.line(
        df, 
        x='Timestamp', 
        y='Rolling_Sentiment',
        color_discrete_sequence=['#38bdf8']
    )
    
    # Add a red zone for negative sentiment
    fig_line.add_hrect(y0=-1, y1=-0.05, line_width=0, fillcolor="red", opacity=0.1)
    # Add a green zone for positive sentiment
    fig_line.add_hrect(y0=0.05, y1=1, line_width=0, fillcolor="green", opacity=0.05)
    
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="", showgrid=False, tickfont=dict(color='#94a3b8'), showticklabels=False), # Hide messy timestamp labels
        yaxis=dict(title="Sentiment Score (-1 to 1)", showgrid=True, gridcolor='#334155', tickfont=dict(color='#f8fafc'), range=[-1, 1]),
        margin=dict(l=0, r=0, t=20, b=0),
        height=350
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.markdown("<h3 style='color:#f8fafc; font-size:1.0rem; text-transform:uppercase; letter-spacing:0.05em;'>Competitor Overview</h3>", unsafe_allow_html=True)
    
    bank_sentiment = df.groupby('Bank')['Compound_Score'].mean().reset_index()
    bank_sentiment = bank_sentiment.sort_values(by='Compound_Score')
    
    # Dynamically color bars based on score
    bank_sentiment['Color'] = bank_sentiment['Compound_Score'].apply(lambda x: '#ef4444' if x < 0 else '#10b981')
    
    fig_bar = px.bar(
        bank_sentiment, 
        y='Bank', 
        x='Compound_Score', 
        orientation='h',
        color='Color',
        color_discrete_map="identity"
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Avg Score", showgrid=True, gridcolor='#334155', tickfont=dict(color='#94a3b8'), range=[-1, 1]),
        yaxis=dict(title="", showgrid=False, tickfont=dict(color='#f8fafc')),
        margin=dict(l=0, r=0, t=20, b=0),
        height=350
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# DASHBOARD UI: THE LIVE FIREHOSE TWEET FEED
# ─────────────────────────────────────────────
st.markdown("<h3 style='color:#f8fafc; font-size:1.1rem; text-transform:uppercase; letter-spacing:0.05em; margin-top:2rem;'>Live Mention Feed</h3>", unsafe_allow_html=True)

# Get the 8 most recent tweets, reverse the order so newest is at the top
recent_tweets = df.tail(8).iloc[::-1]

feed_html = ""
for _, row in recent_tweets.iterrows():
    if row['Sentiment_Label'] == 'Positive':
        badge = "<span class='badge badge-positive'>POSITIVE</span>"
    elif row['Sentiment_Label'] == 'Negative':
        badge = "<span class='badge badge-negative'>NEGATIVE</span>"
    else:
        badge = "<span class='badge badge-neutral'>NEUTRAL</span>"
        
    feed_html += f"""
    <div style='background:#1e293b; border-left:4px solid {"#10b981" if row['Sentiment_Label'] == 'Positive' else "#ef4444" if row['Sentiment_Label'] == 'Negative' else "#94a3b8"}; border-radius:4px; padding:1rem; margin-bottom:0.8rem;'>
        <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
            <span style='color:#38bdf8; font-weight:600; font-size:0.9rem;'>@{row['Bank'].lower()}_user</span>
            <div>{badge} <span style='color:#94a3b8; font-size:0.8rem; margin-left:10px;'>{row['Timestamp']}</span></div>
        </div>
        <div style='color:#e2e8f0; font-size:0.95rem;'>{row['Mention_Text']}</div>
    </div>
    """

st.markdown(feed_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# THE LIVE HEARTBEAT (AUTO-REFRESH)
# ─────────────────────────────────────────────
# Pauses the script for 3 seconds, then forces Streamlit to re-run from top to bottom
time.sleep(3)
st.rerun()