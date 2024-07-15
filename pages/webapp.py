import streamlit as st
import requests
 
 
backend_url = "http://127.0.0.1:8000"
 
#set up page config
st.set_page_config(
    page_title='Predict Page',
    layout='wide'
)
 
 
def show_form():
    st.title('sepsis prediction app')
 
    with st.form('input-feature'):
    # input fields for sepsis features
        st.header("Input Sepsis Features ")
 
        col1, col2 = st.columns(2)
 
        with col1:
            PRG = st.number_input("PRG", min_value=0.0, max_value=50.0, step=0.1, key='prg')
            PL = st.number_input("PL", min_value=0.0, max_value=300.0, step=0.1, key='pl'  )
            PR = st.number_input("PR", min_value= 0.0, max_value=200.0, step=0.1, key= 'pr')
            SK = st.number_input("SK", min_value= 0.0, max_value=200.0, step=0.1, key= 'sk')
        with col2:
            TS = st.number_input("TS", min_value= 0.0, max_value=1000.0, step=0.1, key= 'ts')
            M11 = st.number_input("M11", min_value= 0.0, max_value=100.0, step=0.1, key= 'm11')
            BD2 = st.number_input("BD2", min_value= 0.0, max_value=10.0, step=0.1, key= 'bd2')
            Age = st.number_input("Age", min_value= 0.0, max_value=120.0, step=0.1, key= 'age')
            Insurance = st.number_input("Insurance", min_value= 0.0, max_value=1.0, step=1.0, key= 'insurance')
 
         # predict button
        if st.form_submit_button('Predict Sepsis'):
            # create dictionary with input data
            input_data = {
                "PRG": PRG,
                "PL" : PL,
                "PR" : PR,
                "SK" : SK,
                "TS" : TS,
                "M11": M11,
                "BD2": BD2,
                "Age": Age,
                "Insurance": Insurance
            }
 
            #send a request to the FastAPI backend
            response = requests.post(f"{backend_url}/xgb_model", json=input_data)
 
            # Display the prediction
            if response.status_code == 200:
                prediction = response.json()['prediction']
                st.success(prediction)
            else:
                st.error(f"Error: {response.json()['detail']}")
 
if __name__== '__main__':
    show_form()