import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Dashboad" , page_icon="🌍" , layout="wide")
st.header("Percentile, sales summary by category")
st.markdown("##") # <br>

#load css
with open('style.css') as f:
   st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

theme_plotly = None
#load dataset /exel file
df=pd.read_excel('data.xlsx', sheet_name='group3')

#grid system, columns
tab1, tab2 = st.tabs(["Raw Data sheet","Sales By Percentiles"])
with tab1:
    with st.expander("show workbook"):
        #shwdata = st.multiselect('Filter :', df.columns,default=["SALES","ORDERDATE","STATUS","YEAR_ID","PRODUCTLINE","CUSTOMERNAME","CITY","COUNTRY"])
        #st.dataframe(df[shwdata],use_container_width=True)
        
        selected_productlines = st.multiselect('Filter :', options=df["PRODUCTLINE"].unique(), default=list(df["PRODUCTLINE"].unique()))
        
        # Fix query to use 'isin' for multiple selections
        if selected_productlines:
            filtered_df = df[df["PRODUCTLINE"].isin(selected_productlines)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

with tab2.header("Sales By Percentage"):
 c1,c2,c3,c4,c5=st.columns(5)
 with c1:
    st.info('Percentile 25%', icon="🌏")
    st.metric(label='USD', value=f"{np.percentile(df['SALES'],25):,.2f}")
 with c2:
    st.info('Percentile 50%', icon="🌏")
    st.metric(label='USD', value=f"{np.percentile(df['SALES'],50):,.2f}")
 with c3:
    st.info('Percentile 75%', icon="🌏")
    st.metric(label='USD', value=f"{np.percentile(df['SALES'],75):,.2f}")
 with c4:
    st.info('Percentile 100%', icon="🌏")
    st.metric(label='USD', value=f"{np.percentile(df['SALES'],100):,.2f}")
 with c5:
    st.info('Percentile 0%', icon="🌏")
    st.metric(label='USD', value=f"{np.percentile(df['SALES'],0):,.2f}")

def filterdata():
   
   column=st.sidebar.selectbox('select a colum',['COUNTRY','PRODUCTLINE','CITY','YEAR_ID'])
   type_of_column=st.sidebar.radio("what kind of analysis",['categorical','numerical'])

   c1,c2=st.columns([2,1])
   with c1:
      if type_of_column=='categorical':
         dist=pd.DataFrame(df[column].value_counts())
         fig=px.bar(dist, title='categoty by count', orientation="h")
         fig.update_layout(legend_title=None, xaxis_title="observation",yaxis_title='count')
         st.write(fig, theme=theme_plotly)
      else:
         st.subheader("number summary")
         st.dataframe(df['SALES'].describe(),use_container_width=True)

   with c2:
      st.subheader("Total Sales")
      st.metric(label="USD", value=f"{np.sum(df['SALES'], 0):,.2f}",help="sum",delta=np.average(df['SALES']),
       delta_color="inverse")
      
filterdata()      



   
              

