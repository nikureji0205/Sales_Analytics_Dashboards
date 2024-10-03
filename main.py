import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor

st.set_page_config(layout="wide")

#Reading the data

df = pd.read_csv("data.csv")

df = Preprocessor.fetch_time_features(df)

st.sidebar.title("Filters")

# Financial Year Filter
selected_year = Preprocessor.multiselect("Select Financial Year", df["Financial_Year"].unique())
#Retailer Filter
select_retailer = Preprocessor.multiselect("Select Retailer", df["Retailer"].unique())
# company Filter
select_Company = Preprocessor.multiselect("Select Company",df["Company"].unique())
#Financial month filter
select_month = Preprocessor.multiselect("Select Financial month",df["Financial_Month"].unique())


# Global filtering
filtered_df = df[(df["Financial_Year"].isin(selected_year))&(df["Retailer"].isin(select_retailer))&(df["Company"].isin(select_Company))&(df["Financial_Month"].isin(select_month))]

#Title for dashboard
st.title("Sales Analytics Dashboard")

#Creating columns for Indicator or KPIs

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label = "Total sales" , value = int(filtered_df["Amount"].sum()))
with col2:
    st.metric(label = "Total margin" , value = int(filtered_df["Margin"].sum()))
with col3:
    st.metric(label = "Total transactions" , value = len(filtered_df["Margin"]))
with col4:
    st.metric(label = "Margin percentage(in %)", value = int(filtered_df["Margin"].sum()*100/filtered_df["Amount"].sum()))

#month on month sales
year_sales = filtered_df[["Financial_Year","Financial_Month","Amount"]].groupby(["Financial_Year","Financial_Month"]).sum().reset_index().pivot(index = "Financial_Month",columns = "Financial_Year",values = "Amount")
st.line_chart(year_sales, x_label = "Financial_Month",y_label = "Total sales")

col5 , col6 = st.columns(2)

#Retailer Revenue

with col5:
    st.title("Retailer count by revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(retailer_count, x_label = "percentage revenue",y_label = "retailer_count")

with col6:
    st.title("Companies count by revenue %")
    company_count = Preprocessor.fetch_top_revenue_companies(filtered_df)
    company_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(company_count, x_label = "percentage revenue",y_label = "company_count")  