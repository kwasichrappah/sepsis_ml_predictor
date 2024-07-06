import streamlit as st
import pandas as pd
import matplotlib as plt
import pyodbc  
import joblib
import sys
import numpy as np
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# Streamlit page configuration
st.set_page_config(page_title="Data", page_icon="💾", layout="wide")



with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

if __name__ == "__main__":

    
   authenticator = stauth.Authenticate(
   config['credentials'],
   config['cookie']['name'],
   config['cookie']['key'],
   config['cookie']['expiry_days'],
   config['pre-authorized']
   )


authenticator.login(location='sidebar')

if st.session_state["authentication_status"]:
    authenticator.logout(location = 'sidebar')
    st.write(f'Welcome *{st.session_state["name"]}*')
    
    st.header("Collection of data from AirTigo Telecommunications")

    com_df= pd.read_csv("./data/customer_churn_merged.csv")

    col1, col2 = st.columns(2)
    with col2:
        option = st.selectbox('Select interested category...', options=["All", "Numerical", "Categorical","Boolean"])

    cat = com_df.select_dtypes(include='object').columns.tolist()
    num = com_df.select_dtypes(include='number').columns.tolist()
    bool = com_df.select_dtypes(include='bool').columns.tolist()

    if option == 'Categorical':
        filtered_df = com_df[cat]
    elif option == 'Numerical':
              filtered_df = com_df[num]
    elif option == 'Boolean':
            filtered_df = com_df[bool]          
    else:
            filtered_df = com_df


    with st.container(border = True,height = 650):
        st.dataframe(filtered_df.style.background_gradient(cmap='Blues'), height=600,width=600,use_container_width= True,hide_index=True
                
                
                
                )
    st.caption('Data was gathered from :blue[an SQL database and a CSV file]')


    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How I can be contacted?',
    ('chrappahkwasi@gmail.com','chrappahkwasi@gmail.com', '0209100603')
)