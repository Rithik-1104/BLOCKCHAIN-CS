import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Blockchain Intelligence Dashboard", layout="wide")

# -------------------------
# DATA
# -------------------------
df = pd.DataFrame([
["Ethereum","PoS",30,3,"High","Smart Contracts","Yes","High","Medium","https://cryptologos.cc/logos/ethereum-eth-logo.png"],
["Bitcoin","PoW",7,2,"High","Currency","No","High","Low","https://cryptologos.cc/logos/bitcoin-btc-logo.png"],
["Solana","PoH",65000,9,"Very Low","High-speed Apps","Yes","Medium","High","https://cryptologos.cc/logos/solana-sol-logo.png"],
["Cardano","PoS",250,6,"Low","Research","Yes","Medium","High","https://cryptologos.cc/logos/cardano-ada-logo.png"],
["Polkadot","NPoS",1000,7,"Low","Interoperability","Yes","Medium","High","https://cryptologos.cc/logos/polkadot-new-dot-logo.png"],
["Avalanche","PoS",4500,8,"Low","DeFi","Yes","Medium","High","https://cryptologos.cc/logos/avalanche-avax-logo.png"],
["Polygon","PoS",7000,8,"Very Low","Scaling","Yes","High","High","https://cryptologos.cc/logos/polygon-matic-logo.png"],
["Tron","DPoS",2000,7,"Very Low","Content","Yes","High","High","https://cryptologos.cc/logos/tron-trx-logo.png"],
["Tezos","LPoS",40,5,"Low","Governance","Yes","Medium","High","https://cryptologos.cc/logos/tezos-xtz-logo.png"],
["BSC","PoSA",300,6,"Low","DeFi","Yes","High","Medium","https://cryptologos.cc/logos/bnb-bnb-logo.png"]
], columns=["Name","Consensus","TPS","Score","Fees","UseCase","SmartContracts","Wallet","Energy","Logo"])

# Normalize TPS for radar chart
df["TPS_scaled"] = df["TPS"] / df["TPS"].max() * 10

# -------------------------
# TITLE
# -------------------------
st.title("🚀 Blockchain Intelligence Dashboard")

# -------------------------
# FILTERS
# -------------------------
st.sidebar.title("🔍 Filters")

search = st.sidebar.text_input("Search Blockchain")
fee_filter = st.sidebar.selectbox("Fees", ["All","Low","Very Low","High"])

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search, case=False)]

if fee_filter != "All":
    filtered_df = filtered_df[filtered_df["Fees"] == fee_filter]

# -------------------------
# BEST BLOCKCHAIN (SMART LOGIC)
# -------------------------
if not filtered_df.empty:
    best = filtered_df.sort_values(by=["Score","TPS"], ascending=False).iloc[0]
    st.success(f"🏆 Best Overall: {best['Name']} (Balanced Performance + Ecosystem)")

# -------------------------
# CARDS UI
# -------------------------
st.subheader("🔗 Platforms Overview")

cols = st.columns(3)
for i, row in filtered_df.iterrows():
    with cols[i % 3]:
        st.image(row["Logo"], width=60)
        st.markdown(f"### {row['Name']}")
        st.write(f"⚡ TPS: {row['TPS']}")
        st.write(f"📊 Score: {row['Score']}/10")
        st.write(f"💰 Fees: {row['Fees']}")
        st.write(f"📜 Smart Contracts: {row['SmartContracts']}")
        st.write(f"👛 Wallet: {row['Wallet']}")
        st.caption(f"Use: {row['UseCase']}")

# -------------------------
# RADAR CHART (🔥 TOP FEATURE)
# -------------------------
st.subheader("🕸️ Multi-Metric Radar Comparison")

selected = st.multiselect("Select up to 3 blockchains", df["Name"], default=["Ethereum","Solana"])

if selected:
    radar_df = df[df["Name"].isin(selected)]
    fig = go.Figure()

    for _, row in radar_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row["TPS_scaled"], row["Score"], 8 if row["SmartContracts"]=="Yes" else 2],
            theta=["Speed","Ecosystem","Smart Contracts"],
            fill='toself',
            name=row["Name"]
        ))

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# BAR GRAPH
# -------------------------
st.subheader("📊 TPS Comparison")
fig = px.bar(filtered_df, x="Name", y="TPS", color="Consensus")
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# SMART CONTRACT FLOW (🔥 VISUAL EXPLANATION)
# -------------------------
st.subheader("📜 Smart Contract Flow")

st.markdown("""
User ➝ Wallet ➝ Smart Contract ➝ Blockchain ➝ Result

- User initiates transaction  
- Wallet signs it  
- Smart contract executes logic  
- Blockchain validates  
- Output is stored permanently  
""")

# -------------------------
# WALLET SIMULATION (🔥 UNIQUE FEATURE)
# -------------------------
st.subheader("👛 Wallet Interaction Simulator")

amount = st.slider("Select Transaction Amount", 1, 100, 10)

if st.button("Simulate Transaction"):
    st.info(f"Processing {amount} tokens...")
    st.success("Transaction Confirmed on Blockchain ✅")

# -------------------------
# ADVANCED RECOMMENDATION
# -------------------------
st.subheader("🤖 Intelligent Recommendation")

goal = st.selectbox("Your Goal", ["DeFi","Speed","Low Fees","Smart Contracts"])

if st.button("Suggest"):
    if goal == "Speed":
        res = df.sort_values(by="TPS", ascending=False).iloc[0]
    elif goal == "Low Fees":
        res = df[df["Fees"]=="Very Low"].iloc[0]
    elif goal == "Smart Contracts":
        res = df[df["SmartContracts"]=="Yes"].iloc[0]
    else:
        res = df.iloc[0]

    st.success(f"Recommended: {res['Name']}")
    st.write(f"Best for {goal}")

# -------------------------
# DARK MODE
# -------------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown("<style>body {background-color:#0e1117;color:white;}</style>", unsafe_allow_html=True)
