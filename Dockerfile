FROM python:3.9.16-slim

WORKDIR /streamlit

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app/streamlit.py"]