import streamlit as st
import pandas as pd
import joblib
import os
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

#setting page title and icon
st.set_page_config(
    page_title = "Sepsis Prediction Page",
    page_icon = "🎯",
    layout = 'wide'
)

#Loading the models into streamlit app
st.cache_resource(show_spinner="Models Loading")
def load_catboost_pipeline():
    pipeline = joblib.load("./models/tuned/catboost_pred.joblib")
    return pipeline


st.cache_resource(show_spinner="Models Loading")
def load_logistic_regressor_pipeline():
    pipeline = joblib.load('./models/log_reg_pred.joblib')
    return pipeline


st.cache_resource(show_spinner="Models Loading")
def load_svc_pipeline():
    pipeline = joblib.load('./models/svc_pred.joblib')
    return pipeline


st.cache_resource(show_spinner="Models Loading")
def load_xgboost_pipeline():
    pipeline = joblib.load('./models/best_gs_model.joblib')
    return pipeline

#Selecting model for prediction
def select_model():
        col1,col2 = st.columns(2)

        with col2:
             st.selectbox('Select a Model', options = ['XGBoost','CatBoost','Logistic Regressor','SVC'],key='selected_model')

        if st.session_state['selected_model'] == 'CatBoost':
             pipeline = load_catboost_pipeline()
        
        elif st.session_state['selected_model'] == 'Logistic Regressor':
             pipeline = load_logistic_regressor_pipeline()

        elif st.session_state['selected_model'] == 'XGBoost':
             pipeline = load_xgboost_pipeline()
        else:
             pipeline = load_svc_pipeline()

        #encoder to inverse transform the result
        encoder = 1#joblib.load('./models/encoder.joblib')
        return pipeline,encoder


#Prediction and probability variables state at the start of the webapp
if 'prediction' not in st.session_state:
     st.session_state['prediction'] = None
if 'probability' not in st.session_state:
     st.session_state['probability'] = None


#Making prediction 
def make_prediction(pipeline,encoder):
     PRG= st.session_state['PRG']
     PL= st.session_state['PL']
     PR = st.session_state['PR']
     SK = st.session_state['SK']
     TS= st.session_state['TS']
     M11 = st.session_state['M11']
     BD2 = st.session_state['BD2']
     Age = st.session_state['Age']
     Insurance = st.session_state['Insurance']


     columns = ['PRG','PL','PR','SK','TS','M11','BD2','Age','Insurance']
     
     data = [[PRG,PL,PR,SK,TS,M11,BD2,Age,Insurance]]
     
     #create dataframe
     df = pd.DataFrame(data,columns=columns)



     df.to_csv('.\\data\\history.csv',mode='a',header = not os.path.exists('./data/history.csv'),index=False)

     #Make prediction
     
     pred = pipeline.predict(df)
     prediction = int(pred[0])


     #Updating state
     if  prediction == 1:
        st.session_state['prediction']='Yes'
     else:
          st.session_state['prediction'] ='No'
     

     return st.session_state['prediction']

#Display form on the streamlit app to take user
def display_form():
     pipeline,encoder = select_model()

     with st.form('input-features'):
          col1,col3 = st.tabs(["Patient Information", "Blood Work Information"])

          with col1:
               st.write ('### Patient Information')
               st.number_input("Insert your age",key='Age', min_value=20, max_value=70, step=1) #Age
               st.number_input("Please enter your BMI",key='M11', min_value=10, max_value=80, step=2) #BMI
               st.selectbox("Do you have Insurance",[0,1]
                            ,index=None,placeholder="Select 1 for Yes or 0 for No...",key = 'Insurance')#Insurance
               st.number_input("Insert Blood Pressure value",key='PR', min_value=20, max_value=120, step=2) #Blood Pressure


          with col3:
               st.write('### Blood Work Information')
               st.number_input("Insert PL Blood Work value",key='PL', min_value=25, max_value=200, step=5) #Blood Work 1
               st.number_input("Insert SK Blood Work value",key='SK', min_value=0, max_value=80, step=2) #Blood Work 2
               st.number_input("Insert TS Blood Work value",key='TS', min_value=0, max_value=600, step=10) #Blood Work 3
               st.number_input("Insert BD2 Blood Work value",key='BD2', min_value=0.0, max_value=2.5, step=0.1) #Blood Work 4
               st.number_input("Insert PRG Blood Work value",key='PRG', min_value=0.0, max_value=15.0, step=1.5) #Plasma Glucose
               

          st.form_submit_button('Predict',on_click = make_prediction,kwargs = dict(pipeline = pipeline,encoder=encoder))



with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)



if __name__ == '__main__':
     
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
   st.title("Make a Prediction")
   display_form()

   st.write(st.session_state['prediction'])



    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How I can be contacted?',
    ('chrappahkwasi@gmail.com','chrappahkwasi@gmail.com', '0209100603')
)