import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Blockchain Decision Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (SAFE)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency":"usd","order":"market_cap_desc","per_page":15,"page":1}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        df = pd.DataFrame(data)
        return df[["name","current_price","market_cap","total_volume","price_change_percentage_24h","image"]]
    except:
        return pd.DataFrame([
            ["Ethereum",1800,200000000000,10000000000,2.5,"https://cryptologos.cc/logos/ethereum-eth-logo.png"],
            ["Bitcoin",30000,600000000000,20000000000,1.2,"https://cryptologos.cc/logos/bitcoin-btc-logo.png"],
            ["Solana",150,60000000000,5000000000,3.1,"https://cryptologos.cc/logos/solana-sol-logo.png"]
        ], columns=["name","current_price","market_cap","total_volume","price_change_percentage_24h","image"])

df = load_data()

# -----------------------------
# EXTRA INFO
# -----------------------------
info = {
    "Ethereum": ["Yes","MetaMask","Apps & DeFi"],
    "Bitcoin": ["No","Basic Wallet","Payments"],
    "Solana": ["Yes","Phantom","Fast Apps"]
}

df["SmartContracts"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[0])
df["Wallet"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[1])
df["Use"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[2])

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 Blockchain Comparison Dashboard")

st.markdown("Compare blockchain platforms visually and choose the best based on your needs.")

# -----------------------------
# SELECT
# -----------------------------
selected = st.multiselect("Select Blockchains", df["name"], default=df["name"][:3])
df_sel = df[df["name"].isin(selected)]

# -----------------------------
# CARDS UI
# -----------------------------
st.subheader("🔍 Overview")

cols = st.columns(len(df_sel))

for i, row in df_sel.iterrows():
    with cols[i % len(df_sel)]:
        st.image(row["image"], width=70)
        st.markdown(f"### {row['name']}")
        st.write(f"💰 ${row['current_price']}")
        st.write(f"📊 Cap: {row['market_cap']:,}")
        st.write(f"📈 24h: {row['price_change_percentage_24h']:.2f}%")
        st.progress(min(row["total_volume"]/1e10,1.0))

# -----------------------------
# COMPARISON MATRIX (IMPORTANT)
# -----------------------------
st.subheader("📊 Side-by-Side Comparison")

st.dataframe(df_sel.set_index("name"), use_container_width=True)

# -----------------------------
# GRAPH
# -----------------------------
st.subheader("📊 Market Cap Comparison")

fig = px.bar(df_sel, x="name", y="market_cap", color="name")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SMART CONTRACT VISUAL
# -----------------------------
st.subheader("📜 Smart Contracts")

for _, row in df_sel.iterrows():
    if row["SmartContracts"] == "Yes":
        st.success(f"{row['name']} supports smart contracts → Apps, DeFi")
    else:
        st.error(f"{row['name']} does NOT support smart contracts")

# -----------------------------
# WALLET UI MOCK
# -----------------------------
st.subheader("👛 Wallet Simulation")

wallet = st.selectbox("Select Wallet", df_sel["Wallet"].unique())

st.markdown(f"""
### {wallet} Wallet

- Connect  
- Sign transaction  
- Send crypto  
""")

amount = st.slider("Amount",1,100,10)

if st.button("Send Transaction"):
    st.success(f"{amount} tokens sent using {wallet} ✅")

# -----------------------------
# RECOMMENDATION
# -----------------------------
st.subheader("🤖 Recommendation")

goal = st.selectbox("Goal", ["Investment","Speed","Apps"])

if st.button("Get Best"):
    if goal == "Investment":
        best = df_sel.sort_values("market_cap", ascending=False).iloc[0]
    elif goal == "Speed":
        best = df_sel.sort_values("total_volume", ascending=False).iloc[0]
    else:
        best = df_sel[df_sel["SmartContracts"]=="Yes"].iloc[0]

    st.success(f"Best Choice: {best['name']}")

# -----------------------------
# DARK MODE
# -----------------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown("<style>body {background:#0e1117;color:white}</style>", unsafe_allow_html=True)
