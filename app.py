import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Blockchain Decision Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (SAFE API + FALLBACK)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency":"usd","order":"market_cap_desc","per_page":15,"page":1}

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        df = pd.DataFrame(data)

        return df[[
            "name","current_price","market_cap",
            "total_volume","price_change_percentage_24h","image"
        ]]
    except:
        return pd.DataFrame([
            ["Ethereum",1800,200000000000,10000000000,2.5,"https://cryptologos.cc/logos/ethereum-eth-logo.png"],
            ["Bitcoin",30000,600000000000,20000000000,1.2,"https://cryptologos.cc/logos/bitcoin-btc-logo.png"],
            ["Solana",150,60000000000,5000000000,3.1,"https://cryptologos.cc/logos/solana-sol-logo.png"],
            ["Cardano",0.5,20000000000,2000000000,1.8,"https://cryptologos.cc/logos/cardano-ada-logo.png"],
            ["Polygon",1.2,10000000000,1500000000,2.0,"https://cryptologos.cc/logos/polygon-matic-logo.png"]
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
    "Bitcoin": ["No","Bitcoin Wallet","Digital Money"],
    "Solana": ["Yes","Phantom","Fast Apps"],
    "Cardano": ["Yes","Daedalus","Secure Apps"],
    "Polygon": ["Yes","MetaMask","Scaling"]
}

df["SmartContracts"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[0])
df["Wallet"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[1])
df["Use"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[2])

# -----------------------------
# WALLET IMAGE MAP (FIXED)
# -----------------------------
wallet_images = {
    "MetaMask": "https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg",
    "Phantom": "https://cryptologos.cc/logos/phantom-wallet.png",
    "Daedalus": "https://cryptologos.cc/logos/cardano-ada-logo.png",
    "Bitcoin Wallet": "https://cryptologos.cc/logos/bitcoin-btc-logo.png",
    "Generic": "https://cdn-icons-png.flaticon.com/512/2830/2830284.png"
}

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 Blockchain Comparison Dashboard")

# -----------------------------
# SELECT
# -----------------------------
selected = st.multiselect("Select Blockchains", df["name"], default=list(df["name"][:3]))
df_sel = df[df["name"].isin(selected)]

# -----------------------------
# OVERVIEW CARDS
# -----------------------------
st.subheader("🔍 Overview")

cols = st.columns(len(df_sel))

for i, row in df_sel.iterrows():
    with cols[i % len(df_sel)]:
        st.image(row["image"], width=70)
        st.markdown(f"### {row['name']}")
        st.write(f"💰 ${row['current_price']}")
        st.write(f"📊 Cap: {row['market_cap']:,}")
        st.write(f"📈 {row['price_change_percentage_24h']:.2f}%")

# -----------------------------
# COMPARISON
# -----------------------------
st.subheader("📊 Comparison Table")
st.dataframe(df_sel.set_index("name"), use_container_width=True)

# -----------------------------
# GRAPH
# -----------------------------
fig = px.bar(df_sel, x="name", y="market_cap", color="name")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SMART CONTRACT VISUAL
# -----------------------------
st.subheader("📜 Smart Contract Flow")

for _, row in df_sel.iterrows():
    if row["SmartContracts"] == "Yes":
        st.success(f"{row['name']} → Supports Smart Contracts (Apps, DeFi)")
    else:
        st.error(f"{row['name']} → No Smart Contracts (Only Payments)")

# -----------------------------
# WALLET SIMULATION (FINAL FIXED)
# -----------------------------
st.subheader("👛 Wallet Simulation")

selected_chain = st.selectbox("Select Blockchain", df_sel["name"])
wallet = df[df["name"] == selected_chain]["Wallet"].values[0]

st.markdown(f"### 🔐 {wallet} Wallet")

# SHOW CORRECT IMAGE
st.image(wallet_images.get(wallet, wallet_images["Generic"]), width=120)

address = st.text_input("Recipient Address", "0xABC123...")
amount = st.number_input("Amount", min_value=1, value=10)

if st.button("Send Transaction"):
    st.info("Connecting wallet...")
    st.info("Signing transaction...")
    st.success(f"{amount} tokens sent via {wallet} ✅")

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("📊 Insights")

best = df_sel.loc[df_sel["market_cap"].idxmax()]
growth = df_sel.loc[df_sel["price_change_percentage_24h"].idxmax()]

st.success(f"🏆 Most Trusted: {best['name']}")
st.info(f"📈 Fastest Growing: {growth['name']}")

# -----------------------------
# RECOMMENDATION
# -----------------------------
st.subheader("🤖 Recommendation")

goal = st.selectbox("Goal", ["Investment","Growth","Apps"])

if st.button("Suggest Best"):
    if goal == "Investment":
        res = df_sel.sort_values("market_cap", ascending=False).iloc[0]
    elif goal == "Growth":
        res = df_sel.sort_values("price_change_percentage_24h", ascending=False).iloc[0]
    else:
        res = df_sel[df_sel["SmartContracts"]=="Yes"].iloc[0]

    st.success(f"Best: {res['name']}")

# -----------------------------
# BEGINNER SUMMARY
# -----------------------------
st.subheader("🧠 Simple Explanation")

summaries = {
    "Bitcoin": "Digital gold → store money",
    "Ethereum": "Runs apps & smart contracts",
    "Solana": "Very fast blockchain",
    "Cardano": "Secure & research-based",
    "Polygon": "Makes Ethereum faster"
}

for _, row in df_sel.iterrows():
    st.info(f"{row['name']} → {summaries.get(row['name'], 'General blockchain')}")

# -----------------------------
# DARK MODE
# -----------------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown("<style>body {background:#0e1117;color:white}</style>", unsafe_allow_html=True)
