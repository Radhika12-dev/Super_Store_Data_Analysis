import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings

warnings.filterwarnings('ignore')

#Streamlit is used to create interactive dashborads using python
#Here we are setting the page by giving the title of the page, adding some emojis supported by streamlit
st.set_page_config(page_title="Superstore Dashboard", page_icon=":department_store:", layout='wide')

st.title(" :department_store: SuperStore EDA")

#this is to put the title of the dashboard at proper place we are using some CSS
st.markdown('<style>div.block-container{padding:top:2rem;}</style>', unsafe_allow_html=True)

#giving options to the user to upload the file in any of the format and the basis of that data dashboard will act
f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))

if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename)

else:
    #if there is no file we will upload our file
    df = pd.read_csv("sample_data.csv", encoding = "utf-8")

#Time period of data user want to see
col1, col2 = st.columns((2))
df['Order Date'] = pd.to_datetime(df['Order Date'])

#Getting min and max date from data set
startdate = pd.to_datetime(df['Order Date']).min()
enddate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startdate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", enddate))

#Filtering the data on the basis of the dates provided by the user
df = df[(df['Order Date']>=date1) & (df['Order Date']<=date2)].copy()

