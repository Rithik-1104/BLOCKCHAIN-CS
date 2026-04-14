import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Blockchain Decision Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (API + FALLBACK SAFE)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency":"usd","order":"market_cap_desc","per_page":15,"page":1}

    try:
        res = requests.get(url, params=params, timeout=10)

        if res.status_code != 200:
            raise Exception("API failed")

        data = res.json()

        if not isinstance(data, list):
            raise Exception("Invalid response")

        df = pd.DataFrame(data)

        cols = [
            "name","current_price","market_cap",
            "total_volume","price_change_percentage_24h","image"
        ]

        if not all(col in df.columns for col in cols):
            raise Exception("Missing columns")

        return df[cols]

    except:
        # fallback (never crash)
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

if df.empty:
    st.error("No data available")
    st.stop()

# -----------------------------
# EXTRA INFO (SMART CONTRACT + WALLET + USE CASE)
# -----------------------------
info = {
    "Ethereum": ["Yes","MetaMask","Apps & DeFi"],
    "Bitcoin": ["No","Basic Wallet","Digital Money"],
    "Solana": ["Yes","Phantom","Fast Apps"],
    "Cardano": ["Yes","Daedalus","Secure Apps"],
    "Polygon": ["Yes","MetaMask","Scaling"]
}

df["SmartContracts"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[0])
df["Wallet"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[1])
df["Use"] = df["name"].map(lambda x: info.get(x,["Yes","Generic","General"])[2])

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 Blockchain Comparison Dashboard")

st.info("""
This tool helps you compare blockchains using real data:
- Market Cap → Trust & popularity  
- Volume → Activity  
- Smart Contracts → App capability  
""")

# -----------------------------
# SELECT BLOCKCHAINS
# -----------------------------
selected = st.multiselect(
    "Select Blockchains to Compare",
    df["name"],
    default=list(df["name"][:3])
)

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
        st.write(f"💰 Price: ${row['current_price']}")
        st.write(f"📊 Market Cap: {row['market_cap']:,}")
        st.write(f"📈 24h Change: {row['price_change_percentage_24h']:.2f}%")
        st.progress(min(row["total_volume"]/1e10,1.0))

# -----------------------------
# SIDE BY SIDE COMPARISON
# -----------------------------
st.subheader("📊 Detailed Comparison")

st.dataframe(df_sel.set_index("name"), use_container_width=True)

# -----------------------------
# GRAPH
# -----------------------------
st.subheader("📊 Market Cap Comparison")

fig = px.bar(df_sel, x="name", y="market_cap", color="name")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# SMART CONTRACT VISUAL (REAL)
# -----------------------------
st.subheader("📜 Smart Contract Working")

for _, row in df_sel.iterrows():
    st.markdown(f"### 🔗 {row['name']}")

    if row["SmartContracts"] == "Yes":
        st.markdown("""
        👤 User → 👛 Wallet → 📜 Smart Contract → ⛓️ Blockchain → ✅ Result  
        
        ✔ Executes automatically  
        ✔ No middleman  
        ✔ Used in apps, DeFi, NFTs  
        """)
    else:
        st.markdown("""
        👤 User → 💸 Transaction → ⛓️ Blockchain  
        
        ❌ No smart contracts  
        ✔ Only payments supported  
        """)

# -----------------------------
# WALLET SIMULATION (REALISTIC)
# -----------------------------
st.subheader("👛 Wallet Simulation")

wallet = st.selectbox("Choose Wallet", df_sel["Wallet"].unique())

st.markdown(f"""
### {wallet} Wallet Flow

1. Connect Wallet  
2. Enter Address  
3. Enter Amount  
4. Confirm  
""")

address = st.text_input("Recipient Address", "0xABC123...")
amount = st.number_input("Amount", min_value=1, value=10)

if st.button("🔐 Send Transaction"):
    st.info("Connecting to wallet...")
    st.info("Signing transaction...")
    st.success(f"{amount} tokens sent via {wallet} ✅")

# wallet image
st.image(
    "https://miro.medium.com/v2/resize:fit:1200/1*GzHcK8rXh9vDOMkMt2rt7A.png",
    caption="Example Wallet Interface"
)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("📊 Key Insights")

best_cap = df_sel.loc[df_sel["market_cap"].idxmax()]
best_growth = df_sel.loc[df_sel["price_change_percentage_24h"].idxmax()]

st.success(f"🏆 Most Trusted: {best_cap['name']}")
st.info(f"📈 Fastest Growing: {best_growth['name']}")

# -----------------------------
# RECOMMENDATION ENGINE
# -----------------------------
st.subheader("🤖 Recommendation")

goal = st.selectbox("Your Goal", ["Investment","Fast Growth","Apps/Smart Contracts"])

if st.button("Get Recommendation"):
    if goal == "Investment":
        best = df_sel.sort_values("market_cap", ascending=False).iloc[0]
    elif goal == "Fast Growth":
        best = df_sel.sort_values("price_change_percentage_24h", ascending=False).iloc[0]
    else:
        best = df_sel[df_sel["SmartContracts"]=="Yes"].iloc[0]

    st.success(f"Best Choice: {best['name']}")

# -----------------------------
# BEGINNER SUMMARY (VERY IMPORTANT)
# -----------------------------
st.subheader("🧠 Simple Explanation (Beginner Friendly)")

summaries = {
    "Bitcoin": "💰 Digital gold. Best for storing money.",
    "Ethereum": "🧠 Runs apps and smart contracts.",
    "Solana": "⚡ Very fast and cheap transactions.",
    "Cardano": "🔬 Secure and research-driven blockchain.",
    "Polygon": "🚀 Makes Ethereum faster and cheaper."
}

for _, row in df_sel.iterrows():
    text = summaries.get(row["name"], "General blockchain platform.")
    st.info(f"{row['name']} → {text}")

# -----------------------------
# DARK MODE
# -----------------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown("<style>body {background:#0e1117;color:white}</style>", unsafe_allow_html=True)
