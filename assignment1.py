import streamlit as st
import seaborn as sns 
import matplotlib.pyplot as plt
import random 
import ssl
import time 
from streamlit_gsheets import GSheetsConnection #i don't know why but i with github it was easier to use a requirements.txt for this with this git+https://github.com/streamlit/gsheets-connection


ssl._create_default_https_context = ssl._create_unverified_context # I had an issue with certification for seaborn i do not know why but its the only way i found to solve it 
spreadsheet = "https://docs.google.com/spreadsheets/d/1ortiq5jwQGdLD0BJobWlAN9K-f8F2ah1I_lZts5vq4E/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=spreadsheet)

#df = sns.load_dataset('tips')

st.title(""":red[Do Men or Women tip more?]""")

def plot_seaborn_bar(df): #plot the first graph 
    fig, ax = plt.subplots()
    sns.barplot(x="sex", y="tip", data=df, estimator=lambda x: x.mean(), ax=ax, hue= "sex")
    ax.set_title("Average Tip by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Average Tip in USD")
    st.pyplot(fig)


def plot_seaborn_box(df): # plot the second graph
    fig, ax = plt.subplots()
    sns.boxplot(x="sex", y="tip", data=df, ax=ax, hue="sex")
    ax.set_title("Tip Distribution by Gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Tip Amount in USD")
    st.pyplot(fig)

#initiate all the states espacially to calculate the time later on 
if "chart" not in st.session_state:
    st.session_state.chart = None
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "response_time" not in st.session_state:
    st.session_state.response_time = None

#creating the first button 
random_button = st.button("Show Chart", type="primary")
if random_button:
    st.session_state.chart = random.choice(["bar", "box"]) #the graph is randomly chosen
    st.session_state.start_time = time.time() 


if st.session_state.chart:
    if st.session_state.chart == "bar":
        plot_seaborn_bar(df)
        chart_name = "Bar Plot"
    if st.session_state.chart == "box":
        plot_seaborn_box(df)
        chart_name = "Box Plot"
        
    #second button that only appear after
    answer = st.button("I answered your question", type="primary")
    if answer:
        end_time = time.time()
        st.session_state.response_time = round(end_time - st.session_state.start_time, 2) #rounding so its easier to read 
        st.write(f" :clock1: You took **{st.session_state.response_time}** seconds to answer the question. :clock1: ") 

