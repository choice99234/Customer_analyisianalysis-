import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# Set page configuration
st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
st.header("Sales Summary by Category")


# Load custom CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load dataset 
file_path = 'data.xlsx'
df = pd.read_excel(file_path, sheet_name='group3')

# Tabs for different sections of the dashboard
tab1, tab2, tab3 = st.tabs(["Raw Data Sheet", "Sales By Percentiles", "Add New Data"])

# Tab 1: Display raw data with filtering option
with tab1:
    with st.expander("Show workbook"):
        selected_productlines = st.multiselect('Filter :', options=df["PRODUCTLINE"].unique(), default=list(df["PRODUCTLINE"].unique()))
        
        # Filter the dataframe based on selected product lines
        if selected_productlines:
            filtered_df = df[df["PRODUCTLINE"].isin(selected_productlines)]
            st.dataframe(filtered_df, use_container_width=True)
          
        else:
            st.dataframe(df, use_container_width=True)

# Tab 2: Display sales by percentiles
with tab2:
    st.header("Sales By Percentiles")
    
    # Columns for displaying percentile metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        st.info('Percentile 25%', icon="🌏")
        st.metric(label='USD', value=f"{np.percentile(df['SALES'], 25):,.2f}")
    
    with c2:
        st.info('Percentile 50%', icon="🌏")
        st.metric(label='USD', value=f"{np.percentile(df['SALES'], 50):,.2f}")
    
    with c3:
        st.info('Percentile 75%', icon="🌏")
        st.metric(label='USD', value=f"{np.percentile(df['SALES'], 75):,.2f}")
    
    with c4:
        st.info('Percentile 100%', icon="🌏")
        st.metric(label='USD', value=f"{np.percentile(df['SALES'], 100):,.2f}")
    
    with c5:
        st.info('Percentile 0%', icon="🌏")
        st.metric(label='USD', value=f"{np.percentile(df['SALES'], 0):,.2f}")

# Tab 3: Form to add new data manually
with tab3:
 with st.expander("Show workbook"):
    st.header("Add New Data Manually")

    # Create a form for users to input new data
    with st.form(key="new_data_form"):
        st.write("Enter the new data to be added to the Excel file:")

        # Input fields for the new data
        productline = st.text_input("Product Line")
        sales = st.number_input("Sales", min_value=0.0, format="%.2f")
        order_date = st.date_input("Order Date")
        status = st.selectbox("Order Status", ["Shipped", "Pending", "Cancelled"])
        year_id = st.number_input("Year id")
        customer_name =st.text_input("Customer Name")
        average_rating =st.number_input("Average Rating")
        city = st.text_input("City")
        country = st.text_input("Country")
        # Submit button
        submit_button = st.form_submit_button(label="Add Data")
    
    # If the form is submitted
    if submit_button:
        # Create a new row as a DataFrame
        new_row = pd.DataFrame({
            "PRODUCTLINE": [productline],
            "SALES": [sales],
            "ORDERDATE": [order_date],
            "STATUS": [status],
            "YEAR_ID": [year_id],
            "COUNTRY": [country],
            "CITY": [city],
            "average_rating": [average_rating],
            "CUSTOMER_NAME": [customer_name],

        })
        
        # Append the new row to the existing dataframe
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # Save the updated dataframe back to the Excel file
        with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer:
            updated_df.to_excel(writer, sheet_name='group3', index=False)
        
        # Display success message and show updated data
        st.success("New data added successfully!")
        st.subheader("Updated Data Preview")
        st.dataframe(updated_df, use_container_width=True)
def filterdata():
    # Sidebar filter for category
    category = st.sidebar.multiselect("Filter By Category:", options=df["PRODUCTLINE"].unique(), default=df["PRODUCTLINE"].unique())

    # Filter the dataframe based on selected categories
    selection_query = df[df["PRODUCTLINE"].isin(category)]
    st.markdown('---') 
    # Display total profit
   
    total_profit = selection_query["SALES"].sum()
    

    column=st.sidebar.selectbox('select a colum',['COUNTRY','PRODUCTLINE','CITY','YEAR_ID','STATUS']) 
    type_of_column=st.sidebar.radio("what kind of analysis",['categorical','numerical'])

    # First row for total profit and average rating
    first_column, second_column = st.columns([2,1])
    
    with first_column:
        if type_of_column=='categorical':
         dist=pd.DataFrame(df[column].value_counts())
         fig=px.bar(dist, title='categoty by count', orientation="h")
         fig.update_layout(legend_title=None, xaxis_title="observation",yaxis_title='count')
         st.write(fig,)
        else:
         st.subheader("Number Summary")
         st.dataframe(df['SALES'].describe(),use_container_width=True)
         

    with second_column:
        st.markdown("### TOTAL SALES:")
        st.metric(label="USD", value=f"{np.sum(df['SALES'], 0):,.2f}",help="sum",delta=np.average(df['SALES']),
        delta_color="inverse")
 

    st.markdown('---')  # Horizontal divider

    # Group sales by product line, but exclude non-numeric columns such as datetime
    numeric_columns = selection_query.select_dtypes(include=[np.number]).columns
    profit_by_category = selection_query.groupby(by=["PRODUCTLINE"])[numeric_columns].sum()[["SALES"]]

    # Bar chart for profit by product line
    profit_by_category_barchart = px.bar(profit_by_category, 
                                         x="SALES", 
                                         y=profit_by_category.index, 
                                         title="Sales by Product Line", 
                                         color_discrete_sequence=["#17f50c"])

    profit_by_category_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", 
                                              xaxis=dict(showgrid=False),)

    # Pie chart for profit distribution by product line
    profit_by_category_piechart = px.pie(profit_by_category, 
                                         names=profit_by_category.index, 
                                         values="SALES", 
                                         title="Sales % by Product Line", 
                                         hole=.3,
                                         color=profit_by_category.index, 
                                         color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Display the charts side by side
    left_column, right_column = st.columns(2)
    left_column.plotly_chart(profit_by_category_barchart, use_container_width=True)
    right_column.plotly_chart(profit_by_category_piechart, use_container_width=True)

# Call the filterdata function to display the charts and stats
filterdata()