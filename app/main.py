import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from utils import fetch_data, preprocess_data  # Assuming these functions are defined in utils.py


# Load and preprocess the data
# @st.cache_data
def load_data():
    benin_df = fetch_data('data/benin-malanville.csv')
    sierraleone_df = fetch_data('data/sierraleone-bumbuna.csv')
    togo_df = fetch_data('data/togo-dapaong_qc.csv')
    
    benin_df['Region'] = 'Benin'
    sierraleone_df['Region'] = 'Sierra Leone'
    togo_df['Region'] = 'Togo'
    
    combined_df = pd.concat([benin_df, sierraleone_df, togo_df])
    combined_df = preprocess_data(combined_df)  # Assuming this handles missing values, outliers, etc.
    
    return combined_df

def main():
    st.set_page_config(page_title="EDA", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed")
    custom_cs = """
    <style>
        div.block-container {
            padding-top: 1.5rem; /* Adjust this value to reduce padding-top */
        }
        #MainMenu { visibility: hidden; }
        .stDeployButton { visibility: hidden; }
        .stButton button {
            background-color: #000000;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #00bfff; /* Cyan blue on hover */
            color: white; /* Change text color to white on hover */
        }
    </style>
    """
    st.markdown(custom_cs, unsafe_allow_html=True)
    custom_css = """
    <style>
        div.block-container {
            padding-top: 1.5rem; /* Adjust this value to reduce padding-top */
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


    col1, col2 = st.columns([0.1,0.9])

    html_title = """
        <style>
        .title_dash{
        font-weight:bold;
        padding:1px;
        border-radius:6px
        }
        </style>
        <center> <h2 class = "title_dash"> MoonLight Energy Solutions - Solar Data Dashboard </h2> </center>
        """
    with col2:
        st.markdown(html_title, unsafe_allow_html=True)
    

    data = load_data()




    st.sidebar.header("Dashboard Controls")
    selected_region = st.sidebar.selectbox("Select Region", options=data['Region'].unique())
    selected_variable = st.sidebar.selectbox("Select Variable to Visualize", options=['GHI', 'DNI', 'DHI', 'Tamb', 'WS'])

    st.write(f"## Overview of {selected_region} Data")
    region_data = data[data['Region'] == selected_region]




    time_series_fig = px.line(region_data, x='Timestamp', y=selected_variable, title=f'{selected_variable} Over Time in {selected_region} (Time Series Analysis) ')
    st.plotly_chart(time_series_fig)

  
  
    st.subheader("Correlation Analysis")
    corr_matrix = region_data[['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'WS', 'WSgust']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("Temperature Analysis")
    st.write("Explore the relationship between temperature and solar irradiance.")
    tmoda_vs_ghi = px.scatter(region_data, x='TModA', y='GHI', title="TModA vs. GHI")
    st.plotly_chart(tmoda_vs_ghi)

    st.subheader("Interactive Histograms")
    selected_hist_var = st.selectbox("Select a variable to display its histogram", ['GHI', 'DNI', 'DHI', 'WS', 'Tamb'])
    fig, ax = plt.subplots()
    sns.histplot(region_data[selected_hist_var], bins=20, ax=ax)
    ax.set_title(f'{selected_hist_var} Histogram in {selected_region}')
    st.pyplot(fig)

if __name__ == '__main__':
    main()
    