

import streamlit as st
import pandas as pd
import plotly.express as px


# Load eBay dataset
ebay = pd.read_csv("/Users/anani/Data Management/Streamlit individual/ebay_streamlit_data.csv")
# Set page configuration
st.set_page_config(
    page_title="eBay Inventory Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Main Page Title
st.title("📊 eBay Inventory Dashboard")
st.markdown("Welcome to the eBay Inventory Dashboard. Explore key metrics and insights below.")


st.header("🔍 Filter Options")
st.markdown("Use these filters to explore the dataset")

# Multiselect filters
col1, col2 = st.columns(2)
with col1:
    storage_filter = st.multiselect(
        "Filter by Storage Type",
        options=ebay['Storage Type'].unique(),
        default=[]
    )
with col2:
    brand_filter = st.multiselect(
        "Filter by Brand",
        options=ebay['Brand'].unique(),
        default=[]
    )

# Apply filters
filtered_ebay = ebay.copy()
if storage_filter:
    filtered_ebay = filtered_ebay[filtered_ebay['Storage Type'].isin(storage_filter)]
if brand_filter:
    filtered_ebay = filtered_ebay[filtered_ebay['Brand'].isin(brand_filter)]

st.write("Filtered Data:")
st.dataframe(filtered_ebay)



### Inventory Analysis
st.header("📦 Inventory Analysis")

st.subheader("Laptop Inventory")
st.markdown("This bar chart shows the distribution of laptops based on their type")

type_counts = ebay['Type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Frequency']
st.bar_chart(type_counts.set_index('Type'))

st.markdown("Notebook/Laptops are our best-selling items, making it essential to analyze the types of laptops we offer in detail.")

# Theme colors for eBay
EBAY_COLORS = [ "#E53238", "#0064D2", "#F5AF02", "#86B817", "#9147FF", "#FF9900", "#17A398" ]

type_counts = filtered_ebay['Type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Frequency']

fig_type = px.pie(
    type_counts,
    values='Frequency',
    names='Type',
    title='Distribution of Laptop Types',
    color_discrete_sequence=EBAY_COLORS,
    hole=0.4
)
fig_type.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_type, use_container_width=True)

st.markdown("**Insight:** Notebook/Laptops are our best-selling items, making it essential to analyze them in detail.")

# Notebook/Laptop Breakdown
st.subheader("Notebook/Laptop OS Distribution")

# Data Cleaning for OS
notebooklaptop_df = filtered_ebay[filtered_ebay['Type'] == 'Notebook/Laptop'].copy()
notebooklaptop_df['OS'] = notebooklaptop_df['OS'].replace(
    to_replace=[
        'Windows 10 Pro', 'Windows 10', 'Windows 10 Home', 'Windows 10 Home 64',
        'Microsoft Windows 10 Professional', 'Windows 10 S', 'Windows XP'
    ],
    value='Windows 10'
)
notebooklaptop_df['OS'] = notebooklaptop_df['OS'].replace(
    to_replace=[
        'Windows 11 Home', 'Windows 11', 'Windows 11 Home S', 'Windows 11 S mode',
        'Windows 11 S Mode', 'Windows 11 Pro', 'windows 11'
    ],
    value='Windows 11'
)

# OS Distribution Pie Chart
os_counts = notebooklaptop_df['OS'].value_counts().reset_index()
os_counts.columns = ['OS', 'Frequency']

fig_os = px.pie(
    os_counts,
    values='Frequency',
    names='OS',
    title='OS Distribution in Notebook/Laptops',
    color_discrete_sequence=EBAY_COLORS,
    hole=0.4
)
fig_os.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_os, use_container_width=True)

st.markdown("""
Our inventory is predominantly comprised of devices running **Windows 10**, **Windows 11**, and **Chrome OS**.
Given the rapid pace of technological advancements, it is essential to implement efficient strategies for
inventory turnover to accommodate emerging technologies.
""")

# Storage vs. Price Analysis
st.header("💾 Price vs. Operating System")
st.markdown("Analyze the relationship between operating system and price. The chart highlights how storage type affects pricing.")

fig_storage_price = px.box(
    notebooklaptop_df,
    x="OS",
    y="Price",
    color="Storage Type",
    title="Price Distribution by OS and Storage Type",
    labels={"OS": "Operating System", "Price": "Price (USD)"},
    color_discrete_sequence=EBAY_COLORS,
    notched=True
)
st.plotly_chart(fig_storage_price, use_container_width=True)

# Dynamic Brand and Type Analysis
st.header("🎨 Brand and Type Analysis")
st.markdown("Explore how SSD capacity and price vary across different brands and laptop types.")

# Selection Filters
col1, col2 = st.columns(2)
with col1:
    selected_type = st.selectbox(
        "Select a Laptop Type:",
        options=ebay['Type'].unique(),
        key="type_select"
    )
with col2:
    selected_brands = st.multiselect(
        "Select Brand(s):",
        options=ebay['Brand'].unique(),
        default=ebay['Brand'].unique(),
        key="brand_select"
    )

# SSD Capacity Slider
min_ssd = int(ebay['SSD Capacity (GB)'].min())
max_ssd = int(ebay['SSD Capacity (GB)'].max())
selected_ssd = st.slider(
    "Select SSD Capacity Range (GB):",
    min_value=min_ssd,
    max_value=max_ssd,
    value=(min_ssd, max_ssd),
    key="ssd_slider"
)

# Filter data based on selections
filtered_data = ebay[
    (ebay['Type'] == selected_type) &
    (ebay['Brand'].isin(selected_brands)) &
    (ebay['SSD Capacity (GB)'] >= selected_ssd[0]) &
    (ebay['SSD Capacity (GB)'] <= selected_ssd[1])
]

# Scatter Plot
fig_scatter = px.scatter(
    filtered_data,
    x="SSD Capacity (GB)",
    y="Price",
    color="Brand",
    size="Price",
    title=f"Price vs. SSD Capacity for {selected_type}",
    labels={"SSD Capacity (GB)": "SSD Capacity (GB)", "Price": "Price (USD)"},
    color_discrete_sequence=EBAY_COLORS,
    hover_data=['Model']
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
**Key Takeaways:**

- **Brands, Operating Systems, and Storage Types** are crucial factors influencing consumer decisions when purchasing laptops.
- To maintain high profits and efficient inventory turnover, prioritize acquiring laptops that meet the following criteria:
  - **Operating Systems:** Windows 10 and Windows 11
  - **Storage Types:** SSD or HDD
  - **Preferred Brands:** Lenovo, Microsoft, or HP
""")



