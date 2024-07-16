import streamlit as st
import requests
 
 
backend_url = "http://127.0.0.1:8000"
 
#set up page config
st.set_page_config(
    page_title = "Sepsis Prediction",
    page_icon = "🎯",
    layout = 'wide'
)


#Selecting model for prediction
def select_model():
        col1,col2 = st.columns(2)

        with col2:
             st.selectbox('Select a Model', options = ['XGBoost','CatBoost','Logistic Regressor','SVC'],key='selected_model')

        if st.session_state['selected_model'] == 'CatBoost':
             pipeline ='/catboost_model'
        
        elif st.session_state['selected_model'] == 'Logistic Regressor':
             pipeline = '/logreg_model'

        elif st.session_state['selected_model'] == 'XGBoost':
             pipeline = '/xgb_model'
        else:
             pipeline = '/svc_model'

        
        return pipeline


 
def show_form():
    st.title('sepsis prediction app')
 
    with st.form('input-feature'):
    # input fields for sepsis features
        st.header("Input Sepsis Features ")
 
        col1,col2 = st.tabs(["Patient Information", "Blood Work Information"])
 
        with col1:
            st.write ('### Patient Information')
            st.number_input("Age", min_value= 0.0, max_value=120.0, step=0.1, key= 'age') #Age
            st.number_input("M11", min_value= 0.0, max_value=100.0, step=0.1, key= 'm11') #BMI
            st.selectbox("Do you have Insurance",[0,1]
                            ,index=None,placeholder="Select 1 for Yes or 0 for No...",key = 'insurance')#Insurance
            st.number_input("PR", min_value= 0.0, max_value=200.0, step=0.1, key= 'pr')#Blood Pressure
            
            
            
        with col2:
            st.write('### Blood Work Information')
            st.number_input("PL", min_value=0.0, max_value=300.0, step=0.1, key='pl'  ) #Blood Work 1
            st.number_input("SK", min_value= 0.0, max_value=200.0, step=0.1, key= 'sk') #Blood Work 2
            st.number_input("TS", min_value= 0.0, max_value=1000.0, step=0.1, key= 'ts') #Blood Work 3
            st.number_input("BD2", min_value= 0.0, max_value=10.0, step=0.1, key= 'bd2') #Blood Work 4
            st.number_input("PRG", min_value=0.0, max_value=50.0, step=0.1, key='prg') #Plasma Glucose
            
                # Define a custom class for the submit button

            
        
        st.form_submit_button('Predict',on_click = make_prediction)
         # predict button

def make_prediction():
            # create dictionary with input data
            input_data = {
                "PRG": st.session_state['prg'],
                "PL" : st.session_state['pl'],
                "PR" : st.session_state['pr'],
                "SK" : st.session_state['sk'],
                "TS" : st.session_state['ts'],
                "M11": st.session_state['m11'],
                "BD2": st.session_state['bd2'],
                "Age": st.session_state['age'],
                "Insurance": st.session_state['insurance']
            }
 
            #send a request to the FastAPI backend
            pipeline = select_model()
            response = requests.post(f"{backend_url}{pipeline}", json=input_data)
 
            # Display the prediction
            if response.status_code == 200:
                prediction = response.json()['prediction']
                st.session_state['prediction'] = prediction
                probability = response.json()['probability']
                st.session_state['probability'] = probability
            else:
                st.error(f"Error: {response.json()['detail']}")

#Prediction and probability variables state at the start of the webapp
if 'prediction' not in st.session_state:
     st.session_state['prediction'] = None            
if 'probability' not in st.session_state:
     st.session_state['probability'] = None  

if __name__== '__main__':
    show_form()
    st.write(st.session_state['prediction'])
    st.write(st.session_state['probability'])