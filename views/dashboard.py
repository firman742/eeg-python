import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import mysql.connector
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 


# read csv from a github repo
# df = pd.read_csv("https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv")


# dashboard title
st.title("Real-Time / Live Data EEG Dashboard")

# connect into mysql
connection = mysql.connector.connect(
    host='sql12.freesqldatabase.com',
    user='sql12721291',
    password='1THfkC4yXz',
    database='sql12721291',
)

cursor = connection.cursor()

cursor.execute("Select * from eeg_table")
data = cursor.fetchall()

df = pd.DataFrame(data,columns=cursor.column_names)
st.dataframe(df)