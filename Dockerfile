FROM python:3.8-buster

# Make sure pip and git are installed
RUN apt-get update && apt-get install -y python3-pip

# Upgrade pip
RUN pip3 install --upgrade pip

# Add the project folder to the container
ADD app /app

# Add the src folder to the container
ADD src /src

# Add the requirements.txt file to the container
ADD requirements.txt /requirements.txt

# Add the data folder to the container
ADD data /data

# copy production config to .streamlit folder
RUN mv .streamlit/prod-config.toml .streamlit/config.toml

# install the requirements
RUN pip3 install -r requirements.txt

# run the streamlit app
CMD ["streamlit", "run", "app/main/main.py"]