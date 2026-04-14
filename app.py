import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Blockchain Analyzer", layout="wide")

# -----------------------
# Load Data
# -----------------------
df = pd.DataFrame([
["Ethereum","PoS",30,"High","Smart Contracts","Yes","High","Medium"],
["Bitcoin","PoW",7,"High","Currency","No","High","Low"],
["Solana","PoH",65000,"Very Low","High-speed Apps","Yes","Medium","High"],
["Cardano","PoS",250,"Low","Research-based","Yes","Medium","High"],
["Polkadot","NPoS",1000,"Low","Interoperability","Yes","Medium","High"],
["Avalanche","PoS",4500,"Low","DeFi","Yes","Medium","High"],
["Polygon","PoS",7000,"Very Low","Scaling","Yes","High","High"],
["Tron","DPoS",2000,"Very Low","Content Sharing","Yes","High","High"],
["Tezos","LPoS",40,"Low","Governance","Yes","Medium","High"],
["Binance Smart Chain","PoSA",300,"Low","DeFi","Yes","High","Medium"]
], columns=["Name","Consensus","TPS","Fees","UseCase","SmartContracts","WalletSupport","EnergyEfficiency"])

st.title("🚀 Blockchain Platforms Analyzer")

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("🔍 Filters")

search = st.sidebar.text_input("Search Blockchain")
consensus_filter = st.sidebar.multiselect("Consensus", df["Consensus"].unique())

if search:
    df = df[df["Name"].str.contains(search, case=False)]

if consensus_filter:
    df = df[df["Consensus"].isin(consensus_filter)]

# -----------------------
# Sorting
# -----------------------
sort_option = st.sidebar.selectbox("Sort By", ["None", "TPS High", "TPS Low"])

if sort_option == "TPS High":
    df = df.sort_values(by="TPS", ascending=False)
elif sort_option == "TPS Low":
    df = df.sort_values(by="TPS", ascending=True)

# -----------------------
# Best Blockchain
# -----------------------
best = df.loc[df["TPS"].idxmax()]
st.success(f"🔥 Fastest Blockchain: {best['Name']} ({best['TPS']} TPS)")

# -----------------------
# Table
# -----------------------
st.dataframe(df, use_container_width=True)

# -----------------------
# BAR CHART
# -----------------------
st.subheader("📊 TPS Comparison")
fig = px.bar(df, x="Name", y="TPS", title="Transactions Per Second")
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# PIE CHART (Consensus)
# -----------------------
st.subheader("🧩 Consensus Distribution")
fig2 = px.pie(df, names="Consensus", title="Consensus Types")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# SMART CONTRACTS VISUAL
# -----------------------
st.subheader("📜 Smart Contract Support")
sc_counts = df["SmartContracts"].value_counts()
fig3 = px.pie(values=sc_counts.values, names=sc_counts.index)
st.plotly_chart(fig3)

# -----------------------
# WALLET SUPPORT VISUAL
# -----------------------
st.subheader("👛 Wallet Support Comparison")
fig4 = px.bar(df, x="Name", y="WalletSupport")
st.plotly_chart(fig4)

# -----------------------
# ENERGY EFFICIENCY
# -----------------------
st.subheader("⚡ Energy Efficiency")
fig5 = px.bar(df, x="Name", y="EnergyEfficiency")
st.plotly_chart(fig5)

# -----------------------
# BLOCKCHAIN DETAILS
# -----------------------
st.subheader("🔎 Detailed View")

selected = st.selectbox("Select Blockchain", df["Name"])
details = df[df["Name"] == selected].iloc[0]

st.write(f"Consensus: {details['Consensus']}")
st.write(f"TPS: {details['TPS']}")
st.write(f"Fees: {details['Fees']}")
st.write(f"Use Case: {details['UseCase']}")
st.write(f"Smart Contracts: {details['SmartContracts']}")
st.write(f"Wallet Support: {details['WalletSupport']}")

# -----------------------
# RECOMMENDATION SYSTEM
# -----------------------
st.subheader("🤖 Best Blockchain Recommendation")

if st.button("Suggest Best"):
    best_choice = df.sort_values(by=["TPS"], ascending=False).iloc[0]
    st.info(f"Recommended: {best_choice['Name']}")

# -----------------------
# DARK MODE
# -----------------------
if st.toggle("🌙 Dark Mode"):
    st.markdown(
        "<style>body {background-color:#0e1117;color:white;}</style>",
        unsafe_allow_html=True
    )