import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

st.set_page_config(page_title="Blockchain Dashboard", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency":"usd","order":"market_cap_desc","per_page":10,"page":1}
        res = requests.get(url, params=params, timeout=10)
        df = pd.DataFrame(res.json())

        return df[[
            "name","current_price","market_cap",
            "total_volume","price_change_percentage_24h","image"
        ]]
    except:
        return pd.DataFrame([
            ["Ethereum",1800,200000000000,10000000000,2.5,"https://cryptologos.cc/logos/ethereum-eth-logo.png"],
            ["Bitcoin",30000,600000000000,20000000000,1.2,"https://cryptologos.cc/logos/bitcoin-btc-logo.png"]
        ], columns=[
            "name","current_price","market_cap",
            "total_volume","price_change_percentage_24h","image"
        ])

df = load_data()

# -----------------------------
# EXTRA INFO
# -----------------------------
info = {
    "Ethereum": ["Yes","MetaMask","Apps & DeFi"],
    "Bitcoin": ["No","Bitcoin Wallet","Payments"],
    "Solana": ["Yes","Phantom","Fast Apps"],
    "Cardano": ["Yes","Daedalus","Secure Apps"],
    "Polkadot": ["Yes","Polkadot.js","Interoperability"],
    "Avalanche": ["Yes","Core Wallet","DeFi"],
    "Polygon": ["Yes","MetaMask","Scaling"],
    "BNB": ["Yes","Trust Wallet","DeFi"],
    "TRON": ["Yes","TronLink","Content"],
    "Tezos": ["Yes","Temple Wallet","Governance"]
}

df["SmartContracts"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[0])
df["Wallet"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[1])
df["Use"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[2])

# -----------------------------
# WALLET UI (YOUR IMAGES)
# -----------------------------
wallet_ui = {
    "Bitcoin": "images/bitcoin.png",
    "Ethereum": "images/ethereum.jpg",
    "Solana": "images/solana.webp",
    "Cardano": "images/cardano.jpg",
    "Polkadot": "images/polkadot.jpg",
    "Avalanche": "images/avalanche.jpg",
    "Polygon": "images/polygon.png",
    "BNB": "images/binance.png",
    "TRON": "images/tron.jpg",
    "Tezos": "images/tezos.jpg"
}

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 Blockchain Comparison Dashboard")

selected = st.multiselect("Select Blockchains", df["name"], default=list(df["name"][:3]))
df_sel = df[df["name"].isin(selected)]

# -----------------------------
# OVERVIEW
# -----------------------------
st.subheader("🔍 Overview")

cols = st.columns(len(df_sel))

for i, row in df_sel.iterrows():
    with cols[i % len(df_sel)]:
        st.image(row["image"], width=60)
        st.markdown(f"### {row['name']}")
        st.write(f"💰 ${row['current_price']}")
        st.write(f"📊 Cap: {row['market_cap']:,}")
        st.write(f"📈 {row['price_change_percentage_24h']:.2f}%")

# -----------------------------
# COMPARISON
# -----------------------------
st.subheader("📊 Comparison")
st.dataframe(df_sel.set_index("name"), use_container_width=True)

# -----------------------------
# GRAPH
# -----------------------------
fig = px.bar(df_sel, x="name", y="market_cap", color="name")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SMART CONTRACT
# -----------------------------
st.subheader("📜 Smart Contracts")

for _, row in df_sel.iterrows():
    if row["SmartContracts"] == "Yes":
        st.success(f"{row['name']} → Supports Smart Contracts")
    else:
        st.error(f"{row['name']} → No Smart Contracts")

# -----------------------------
# WALLET UI (FINAL PERFECT)
# -----------------------------
st.subheader("👛 Wallet Interface")

selected_chain = st.selectbox("Choose Blockchain", df_sel["name"])

img_path = wallet_ui.get(selected_chain)

if img_path and os.path.exists(img_path):
    st.image(img_path, use_column_width=True)
else:
    st.warning("Wallet UI image not found")

# -----------------------------
# SIMULATION
# -----------------------------
address = st.text_input("Recipient Address", "0xABC123...")
amount = st.number_input("Amount", min_value=1, value=10)

if st.button("Send Transaction"):
    st.success(f"{amount} tokens sent on {selected_chain} ✅")

# -----------------------------
# SUMMARY
# -----------------------------
st.subheader("🧠 Simple Explanation")

summaries = {
    "Bitcoin": "Digital gold → store money",
    "Ethereum": "Runs apps & smart contracts",
    "Solana": "Very fast blockchain",
    "Cardano": "Secure blockchain",
    "Polygon": "Makes Ethereum faster"
}

for _, row in df_sel.iterrows():
    st.info(f"{row['name']} → {summaries.get(row['name'], 'General blockchain')}")

# -----------------------------
# DARK MODE
# -----------------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown("<style>body {background:#0e1117;color:white}</style>", unsafe_allow_html=True)
