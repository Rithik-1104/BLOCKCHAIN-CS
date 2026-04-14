import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

st.set_page_config(page_title="Blockchain Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (API + FALLBACK)
# -----------------------------
@st.cache_data
def load_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency":"usd","order":"market_cap_desc","per_page":20,"page":1}
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if not isinstance(data, list):
            raise Exception("Bad API")

        df = pd.DataFrame(data)

        return df[[
            "name","current_price","market_cap",
            "total_volume","price_change_percentage_24h","image"
        ]]
    except:
        return pd.DataFrame([
            ["Bitcoin",30000,600000000000,20000000000,1.2,"https://cryptologos.cc/logos/bitcoin-btc-logo.png"],
            ["Ethereum",1800,200000000000,10000000000,2.5,"https://cryptologos.cc/logos/ethereum-eth-logo.png"],
            ["Solana",150,60000000000,5000000000,3.1,"https://cryptologos.cc/logos/solana-sol-logo.png"],
            ["Cardano",0.5,20000000000,2000000000,1.8,"https://cryptologos.cc/logos/cardano-ada-logo.png"],
            ["Polkadot",5,8000000000,1000000000,1.5,"https://cryptologos.cc/logos/polkadot-new-dot-logo.png"],
            ["Avalanche",20,15000000000,2000000000,2.0,"https://cryptologos.cc/logos/avalanche-avax-logo.png"],
            ["Polygon",1.2,10000000000,1500000000,2.0,"https://cryptologos.cc/logos/polygon-matic-logo.png"],
            ["BNB",300,50000000000,5000000000,1.7,"https://cryptologos.cc/logos/bnb-bnb-logo.png"],
            ["TRON",0.1,9000000000,1200000000,1.3,"https://cryptologos.cc/logos/tron-trx-logo.png"],
            ["Tezos",1.0,1000000000,200000000,1.1,"https://cryptologos.cc/logos/tezos-xtz-logo.png"]
        ], columns=[
            "name","current_price","market_cap",
            "total_volume","price_change_percentage_24h","image"
        ])

df = load_data()

# -----------------------------
# FILTER ONLY REQUIRED PLATFORMS
# -----------------------------
valid_platforms = [
    "Bitcoin","Ethereum","Solana","Cardano",
    "Polkadot","Avalanche","Polygon",
    "BNB","TRON","Tezos"
]

df = df[df["name"].isin(valid_platforms)]

# -----------------------------
# EXTRA INFO
# -----------------------------
info = {
    "Ethereum": ["Yes","MetaMask","Apps & DeFi"],
    "Bitcoin": ["No","Bitcoin Wallet","Digital Money"],
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
# NORMALIZE NAME FOR IMAGE MATCH
# -----------------------------
def normalize_name(name):
    name = name.lower()
    if "bitcoin" in name: return "bitcoin"
    if "ethereum" in name: return "ethereum"
    if "solana" in name: return "solana"
    if "cardano" in name: return "cardano"
    if "polkadot" in name: return "polkadot"
    if "avalanche" in name: return "avalanche"
    if "polygon" in name: return "polygon"
    if "bnb" in name: return "binance"
    if "tron" in name: return "tron"
    if "tezos" in name: return "tezos"
    return None

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 Blockchain Comparison Dashboard")

# -----------------------------
# SELECT
# -----------------------------
selected = st.multiselect(
    "Select Blockchains",
    df["name"],
    default=list(df["name"][:3])
)

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
# TABLE
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
# WALLET UI (YOUR IMAGES)
# -----------------------------
st.subheader("👛 Wallet Interface")

selected_chain = st.selectbox("Choose Blockchain", df_sel["name"])
normalized = normalize_name(selected_chain)

if normalized:
    img_path = f"images/{normalized}.png"

    if not os.path.exists(img_path):
        for ext in ["jpg","jpeg","webp"]:
            alt = f"images/{normalized}.{ext}"
            if os.path.exists(alt):
                img_path = alt
                break

    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True)
    else:
        st.warning("Image not found")

# -----------------------------
# SIMULATION
# -----------------------------
address = st.text_input("Recipient Address", "0xABC123...")
amount = st.number_input("Amount", min_value=1, value=10)

if st.button("Send Transaction"):
    st.success(f"{amount} tokens sent on {selected_chain} ✅")

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("📊 Insights")

best = df_sel.loc[df_sel["market_cap"].idxmax()]
growth = df_sel.loc[df_sel["price_change_percentage_24h"].idxmax()]

st.success(f"🏆 Most Trusted: {best['name']}")
st.info(f"📈 Fastest Growing: {growth['name']}")

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
