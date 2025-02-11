import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

#Creating the side bar options for users using sidebar option
st.sidebar.header("Choose your filter:")
region = st.sidebar.multiselect("Pick your region", df["Region"].unique())

#If user did not select any region then we will use the complete data otherwise filter the data on the selected region
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

#Select the state from the selected region
state = st.sidebar.multiselect("Pick your state", df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]

#Select the city from the state
city = st.sidebar.multiselect("Pick your city:", df3['City'].unique())
if not city:
    df4 = df3.copy()
else:
    df4 = df3[df3['City'].isin(city)]

#Filter the data based on region, state and city
#Applying the permutations and combinations

if not region and not state and not city:
    filtered_data = df
elif not state and not city:
    filtered_data = df[df['Region'].isin(region)]
elif not region and not state:
    filtered_data = df[df['city'].isin(city)]
elif not region and not city:
    filtered_data = df[df['state'].isin(state)]
elif state and city:
    filtered_data = df3[df['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_data = df3[df['Region'].isin(region) & df3['City'].isin(city)]
elif state and region:
    filtered_data = df3[df['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_data = df3[df3['City'].isin(city)]
else:
    filtered_data = df3[df3['Region'].isin(region) & df3['City'].isin(city) & df3['State'].isin(state)]

#Creating the bar chart for sales of each category on filtered data
category_df = filtered_data.groupby(by=['Category'], as_index=False)['Sales'].sum()

#As we have already divided the window into 2 parts while showing start date and end date, so we will show this chart in first half
with col1:
    st.subheader("Category wise sales")
    fig = px.bar(category_df, x='Category', y='Sales', text = ["${:,.2f}".format(x) for x in category_df['Sales']],
            template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height = 200)

with col2:
    st.subheader("Region wise sales")
    fig = px.pie(filtered_data, values= "Sales", names= "Region", hole=0.5 )
    fig.update_traces(text=filtered_data['Region'], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


#In case you want to download the data on the basis of your selection
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category_Viewdata"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name="Category.csv", mime = "text/csv",
                           help = "Click here to download data as csv file")

with cl2:
    with st.expander("Region_Viewdata"):
        region_df = filtered_data.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(region_df.style.background_gradient(cmap="Oranges"))
        csv =  region_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name="Region.csv", mime = "text/csv",
                           help = "Click here to download data as csv file")