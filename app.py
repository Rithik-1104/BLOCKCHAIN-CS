import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Blockchain Decision Dashboard", layout="wide")

# -----------------------------
# FETCH LIVE DATA (CoinGecko)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1
    }
    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data)[[
        "name","symbol","current_price","market_cap","total_volume","price_change_percentage_24h","image"
    ]]
    return df

df_live = load_data()

# -----------------------------
# MANUAL BLOCKCHAIN DATA (REALISTIC)
# -----------------------------
info = {
    "Ethereum": {"SmartContracts":1,"WalletUI":"Metamask","Use":"Apps & DeFi"},
    "Bitcoin": {"SmartContracts":0,"WalletUI":"Basic Wallet","Use":"Money"},
    "Solana": {"SmartContracts":1,"WalletUI":"Phantom","Use":"Fast Apps"},
    "Cardano": {"SmartContracts":1,"WalletUI":"Daedalus","Use":"Secure Apps"},
    "Polkadot": {"SmartContracts":1,"WalletUI":"Polkadot.js","Use":"Connect Chains"},
    "Avalanche": {"SmartContracts":1,"WalletUI":"Core Wallet","Use":"DeFi"},
    "Polygon": {"SmartContracts":1,"WalletUI":"Metamask","Use":"Scaling"},
    "TRON": {"SmartContracts":1,"WalletUI":"TronLink","Use":"Content"},
    "Tezos": {"SmartContracts":1,"WalletUI":"Temple","Use":"Governance"},
    "BNB": {"SmartContracts":1,"WalletUI":"Trust Wallet","Use":"DeFi"}
}

# Merge logic
df_live["SmartContracts"] = df_live["name"].map(lambda x: info.get(x, {}).get("SmartContracts",1))
df_live["Wallet"] = df_live["name"].map(lambda x: info.get(x, {}).get("WalletUI","Generic"))
df_live["Use"] = df_live["name"].map(lambda x: info.get(x, {}).get("Use","General"))

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 Blockchain Decision Dashboard (Real Data)")

# -----------------------------
# SIMPLE EXPLANATION (FOR NON-TECH USERS)
# -----------------------------
st.info("""
💡 This dashboard helps you choose a blockchain:
- Speed → How fast transactions happen  
- Market Cap → How big & trusted it is  
- Volume → How actively used it is  
""")

# -----------------------------
# FILTER
# -----------------------------
selected = st.multiselect("Compare Blockchains", df_live["name"].head(10), default=["Ethereum","Bitcoin"])

compare_df = df_live[df_live["name"].isin(selected)]

# -----------------------------
# CARDS (VISUAL)
# -----------------------------
st.subheader("🔍 Overview")

cols = st.columns(len(compare_df))

for i, row in compare_df.iterrows():
    with cols[i % len(compare_df)]:
        st.image(row["image"], width=80)
        st.write(f"### {row['name']}")
        st.write(f"💰 Price: ${row['current_price']}")
        st.write(f"📊 Market Cap: {row['market_cap']:,}")
        st.write(f"📈 24h Change: {row['price_change_percentage_24h']:.2f}%")
        st.write(f"📜 Smart Contracts: {'Yes' if row['SmartContracts'] else 'No'}")
        st.write(f"👛 Wallet: {row['Wallet']}")
        st.caption(f"Use: {row['Use']}")

# -----------------------------
# COMPARISON GRAPH (REAL DATA)
# -----------------------------
st.subheader("📊 Market Comparison")

fig = px.bar(compare_df, x="name", y="market_cap", color="name")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SMART CONTRACT VISUAL (DIFFERENT PER PLATFORM)
# -----------------------------
st.subheader("📜 Smart Contract Capability")

for _, row in compare_df.iterrows():
    if row["SmartContracts"] == 1:
        st.success(f"{row['name']} → Supports smart contracts (apps, DeFi)")
    else:
        st.error(f"{row['name']} → No smart contracts (only payments)")

# -----------------------------
# WALLET VISUAL (REALISTIC)
# -----------------------------
st.subheader("👛 Wallet Experience")

wallet = st.selectbox("Choose Wallet Type", compare_df["Wallet"].unique())

st.markdown(f"""
### {wallet}

- Send / Receive crypto  
- Connect to apps  
- Sign transactions securely  

🔐 Simulated UI:
""")

amount = st.slider("Amount",1,100,10)

if st.button("Send Transaction"):
    st.success(f"{amount} tokens sent using {wallet} ✅")

# -----------------------------
# SMART RECOMMENDATION
# -----------------------------
st.subheader("🤖 Recommendation Engine")

goal = st.selectbox("Your Goal", ["Investment","Fast Transactions","Apps/Smart Contracts"])

if st.button("Get Recommendation"):
    if goal == "Investment":
        best = df_live.sort_values("market_cap", ascending=False).iloc[0]
    elif goal == "Fast Transactions":
        best = df_live.sort_values("total_volume", ascending=False).iloc[0]
    else:
        best = df_live[df_live["SmartContracts"]==1].iloc[0]

    st.success(f"Best Choice: {best['name']}")
    st.write("Based on real market data + usage")

# -----------------------------
# DARK MODE
# -----------------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown("<style>body {background-color:#0e1117;color:white;}</style>", unsafe_allow_html=True)
