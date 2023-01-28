# streamlit-twitter-dashboard
## Intro
This repo aims to create a simple dashboard to follow certain twitter trends and tweets. 

For this we are going to use python and to make this experience easier and interactive we will use streamlit. 

With streamlit we can create simple interactive web app dashboards which could be used for EDA, Forecasting, other visualizations and more.

## Prerequisites
1. You will need api key, secret key and bearer key to connect to the twitter API. You can get this by signing up in twitter developer page. Applying for the Elevated account will give you a wider access to the available APIs.
2. Please make sure you have docker installed in your local machine.

3. If you don't want to run the app from docker you can still run it in your local machine (preferably in a virtual machine).

## Run with Docker
Build the image:

naming the image is not mandatory.
```zsh
docker build . -t streamlit-dashboard
```
Now we can run the app.

`-d` is used to run the docker image in detached mode. not mandatory.

`-p 8501:8501` is used to map the ports from the docker container to the local machine. On default the port for the streamlit app is 8501

`-v` we use volumes to reference files in the directory of local machine to the container so that when we make changes to our python file the web app gets updated automatically. Without using volumes you have to re-run the container everytime you make any changes.

We also have the option to run our app through `docker-compose` which will be shown later on. In this case we don't have to define port mapping and volumes each time we want to run the container.

```zsh
docker run -d -p 8501:8501 -v $(pwd):/streamlit streamlit-dashboard
```
Now you can visit `localhost:8501`.

## Run with docker-compose

Will be added.

## Run with venv
Make sure you have venv installed.
```sh
# create the virtual environment in your directory
python3 -m venv venv 

# activate the vitrual environment
source venv/bin/activate

# install dependencies
pip3 install -r requirements.txt

# run streamlit
streamlit run  app/streamlit.py
```


