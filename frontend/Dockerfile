#*'''#runtime or python application 
FROM python:3.11.0  

#copy the requrements to a tmp file
COPY requirements.txt /tmp/requirements.txt 

# Install the dependencies specified in the requirements.txt file
RUN python -m pip install --timeout 300 -r /tmp/requirements.txt

COPY . /app 

WORKDIR /app 

EXPOSE 3000

CMD ["streamlit","run", "1_Profile.py","--server.port=8501"]


#to upload the work unto docker as an image docker build -t sepsiswebpageimage ./frontend




