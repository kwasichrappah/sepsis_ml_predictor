import streamlit as st


# Set page config
st.set_page_config(
    page_title="Sepsis ML Predictor",
    page_icon="🛖",
    layout="wide",
)




st.title ("Sepssis ML Predictor WebApp")
st.write("This is a ML model application that predicts whether a patient is likely to have Sepssis or not.")
st.write("It uses ML algorithms to make these predictions.")
tab1, tab2, tab3 = st.tabs(["Problem Statement","Key Features", "Key Metrics and Success Criteria"])

with tab1:
    st.subheader('Problem Statement', divider='red')
    st.subheader("This project aims to :rainbow[predict Sepssis Diagnosis].")
    st.markdown("Sepsis is a serious condition in which the body responds improperly to an infection.\
                    The infection-fighting processes turn on the body, causing the organs to work poorly.\
                Sepsis may progress to septic shock. This is a dramatic drop in blood pressure that can damage the lungs, kidneys, liver and other organs.\
                When the damage is severe, it can lead to death.\
                Early treatment of sepsis improves chances for survival.")
    
with tab2:
    st.subheader('Key Features in the model', divider='orange')
    st.markdown("- Patient Records ")
    st.markdown("- Insurance ")
    st.markdown("- Sepssis status ")

with tab3:
    st.subheader("Key Metrics and Success Criteria",divider = "green")
    st.markdown("• Model Accuracy : The ability of the machine learning model to accurately predict Sepssis diagnosis.")
    st.markdown("• Model Interpretability : The degree to which the model’s predictions and insights can be understood and utilized by stakeholders.")
    

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    .custom-text {
        font-size: 12px; /* Adjust the font size as needed */
        text-align: right;
        color: #000; /* Optionally, you can also change the text color */
        margin: 0; /* Adjust margin as needed */
        padding: 0; /* Adjust padding as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create text input and apply custom class
user_input = 'Created by Emmanuel Chrappah'

# Apply the custom class to the displayed text
st.markdown(f'<p class="custom-text">{user_input}</p>', unsafe_allow_html=True)









# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How I can be contacted?',
    ('chrappahkwasi@gmail.com','chrappahkwasi@gmail.com', '0209100603')
)
        





















#streamlit run "c:/Users/chrap/OneDrive - ECG Ghana/Emmanuel Chrappah/Azubi Africa/git_hub_repos/streamlit_fundamentals/src/app.py"     