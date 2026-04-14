import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Blockchain Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (SAFE)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency":"usd","order":"market_cap_desc","per_page":10,"page":1}

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
            ["Solana",150,60000000000,5000000000,3.1,"https://cryptologos.cc/logos/solana-sol-logo.png"]
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
    "Polygon": ["Yes","MetaMask","Scaling"]
}

df["SmartContracts"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[0])
df["Wallet"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[1])
df["Use"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[2])

# -----------------------------
# REAL WALLET UI IMAGES (FIXED)
# -----------------------------
wallet_ui = {
    "MetaMask": "https://miro.medium.com/v2/resize:fit:1200/1*9p6W3jTz6kKIhxX3sI5YtQ.png",
    "Phantom": "https://miro.medium.com/v2/resize:fit:1200/1*4R2tQeMgsQUK91tIbp1K2Q.png",
    "Daedalus": "https://iohk.io/en/blog/posts/2020/08/20/daedalus-wallet/",
    "Bitcoin Wallet": "https://bitcoin.org/img/screenshots/en/bitcoin-core.png",
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
# OVERVIEW (LOGOS FIXED)
# -----------------------------
st.subheader("🔍 Overview")

cols = st.columns(len(df_sel))

for i, row in df_sel.iterrows():
    with cols[i % len(df_sel)]:
        st.image(row["image"], width=60)  # PLATFORM LOGO BACK
        st.markdown(f"### {row['name']}")
        st.write(f"💰 ${row['current_price']}")
        st.write(f"📊 Cap: {row['market_cap']:,}")
        st.write(f"📈 {row['price_change_percentage_24h']:.2f}%")

# -----------------------------
# COMPARISON TABLE
# -----------------------------
st.subheader("📊 Comparison")
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
        st.markdown(f"### {row['name']}")
        st.success("User → Wallet → Smart Contract → Blockchain → Result")
    else:
        st.markdown(f"### {row['name']}")
        st.error("Only Transaction → No Smart Contract")

# -----------------------------
# WALLET SIMULATION (REAL UI)
# -----------------------------
st.subheader("👛 Wallet Interface")

selected_chain = st.selectbox("Choose Blockchain", df_sel["name"])
wallet = df[df["name"] == selected_chain]["Wallet"].values[0]

st.markdown(f"### 🔐 {wallet} UI")

# SHOW REAL UI SCREENSHOT
img_url = wallet_ui.get(wallet, wallet_ui["Generic"])
st.image(img_url, caption=f"{wallet} Interface", use_column_width=True)

# SIMULATION
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
# SUMMARY
# -----------------------------
st.subheader("🧠 Simple Explanation")

summaries = {
    "Bitcoin": "Digital gold → store money",
    "Ethereum": "Runs smart contracts & apps",
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
