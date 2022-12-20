import time  # to simulate a real time data, time loop
from PIL import Image
import numpy as np  # np mean, np random
import pytz
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from datetime import datetime
from datetime import date
import base64
from pathlib import Path
#import EolosESGdatos carga
from EolosESGdatos import Carga,EOLOSmetricesg
from streamlit_autorefresh import st_autorefresh
from streamlit_autorefresh import st_autorefresh
# from streamlit_aggrid import AgGrid
import streamlit.components.v1 as components
#from bloxs import B


#st.experimental_rerun()
######################################
# Page setting
######################################

pathicono="c:/produccion/resources/img/"
pathicono="./resources/img/"
icono = Image.open(pathicono+'logo1.jpeg')

st.set_page_config(
    page_title="Global Eolos -MVP V 1.0",
    page_icon=icono,
    layout="wide",
)
# with open('style.css') as f:
    # st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.write('<style>div.block-container{padding-top:1.8rem;}</style>', unsafe_allow_html=True)
#Put your logo here:
ruta = "c:/produccion/resources/img/"
cargalogo = ruta +'logo7.png'

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
    
    
#From there, you can use the image in your app as follows:
header_html = "<img src='data:image/png;base64,{}' class='img-fluid'><br><b>Environmental Asset Management".format(
    img_to_bytes(cargalogo)
)
st.markdown(
    header_html, unsafe_allow_html=True,
)
###################################################################3
###################################################################
#####################################################################3
### FONTS
def style():
    css = """
    <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet"> 
    <style>
    @font-face {
        font-family: 'My Font';
        font-style: normal;
        src: url(assets/fonts/myfont.tff) format('truetype');;
    }
    .sidebar-text{
        font-family: 'Roboto', sans-serif;
    }
    .standard-text{
        font-family: 'My Font';
    }
    </style>
    """
    st.markdown(style,unsafe_allow_html=True)


#################################################################################################3
###################################################################
# LINK TO THE CSS FILE
with open('style2022.css')as f:
 st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

df = pd.read_csv("avocado-updated-2020.csv")



# — PANDAS ANALYSIS
df.drop_duplicates(inplace = True) # drop duplicates


#2015
yr_15 = round(df[df['year'] == 2015]['total_bags'].sum())#2016
yr_16 = round(df[df['year'] == 2016]['total_bags'].sum())#2017
yr_17 = round(df[df['year'] == 2017]['total_bags'].sum())#2018
yr_18 = round(df[df['year'] == 2018]['total_bags'].sum())#2019
yr_19 = round(df[df['year'] == 2019]['total_bags'].sum())#2020
yr_20 = round(df[df['year'] == 2020]['total_bags'].sum())
# calculate percentage increase between 2015 and 2020
per_increase = round((int(yr_20 - yr_15)/ yr_15) * 100, 1)
percent_increase = f"{per_increase}%"







StrNombreArchivo = "./resources/data/basemvp1.xlsx"
df_CA,iTmpTotalEmiPro,df_ConTotales = EOLOSmetricesg(StrNombreArchivo)





tabs = st.tabs(["Datos", "KPI","ESG-Ranking", "Reporte"])

tab_metrics  = tabs[0]
with tab_metrics:
    st.write(df_CA)
    st.write(df_ConTotales)

tab_plots = tabs[1]
with tab_plots:
    st.title('Bloxs example in Streamlit')

tab_plots = tabs[2]
with tab_plots:
    # WE CREATE FOUR COLUMNS HERE TO HOLD THE METRIC
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label = "2015 Sales",value = (yr_15),)
    col2.metric(label = "2016 Sales",value = (yr_16),delta = round(float((yr_16-yr_15)/yr_15)*100,1))
    col3.metric(label = "2017 Sales",value = (yr_17),delta = round(float((yr_17 - yr_16)/yr_16) *100))
    col4.metric(label = "2018 Sales",value = (yr_18),delta = round(float((yr_18 - yr_17)/yr_17) *100,1))
    st.markdown("<hr/>", unsafe_allow_html = True)
    col5, col6, col7 = st.columns(3)
    col5.metric(label = "2019 Sales",value = (yr_19),delta = round(float((yr_19 - yr_18)/yr_18) *100, 1))
    col6.metric(label = "2020 Sales",value = (yr_20),delta = round(float((yr_20 - yr_19)/yr_19) *100))
    col7.metric(label = "% increase between 2015–2020",value = (percent_increase))


tab_reports = tabs[3]
with tab_reports:
    item = B([
        B("123", "Display line chart", points=[1,4,2,3,5,6]),
        B("786", "Display bar chart", points=[1,4,2,3,5,6], chart_type="bar"),
        B("123", "Display bar chart", points=[1,4,2,3,5,6], chart_type="bar")
    ])._repr_html_()
    components.html(item, height=300)#, scrolling=True)
