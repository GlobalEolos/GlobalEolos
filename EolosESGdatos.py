# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 12:53:16 2022

@author: cvh_2
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
import traceback
from datetime import datetime

StrNombreArchivo = "./resources/data/basemvp1.xlsx"
df_ResumenCA = pd.DataFrame(columns=['Proceso', 'Tipo', 'TotalFactor', 'TotalConsumo', 'TotalGasto'])
dfResultado = pd.DataFrame(columns=['Proceso', 'Tipo', 'TotalFactor','SubTotalEPPConsumo', 'TotalConsumo', 'TotalGasto'])


def print_custom_error_message():
    exc_type, exc_value, exc_tb = sys.exc_info()
    stack_summary = traceback.extract_tb(exc_tb)
    end = stack_summary[-1]

    err_type = type(exc_value).__name__
    err_msg = str(exc_value)
    date = datetime.strftime(datetime.now(), "%B %d, %Y | %I:%M %p")

    # print(f"On {date}, a {err_type} occured in {end.filename} inside {end.name} on line {end.lineno} with the error message: {err_msg}.")
    print(f"{date}")
    print(f"{err_type} archivo {end.filename}")
    print(f"Dentro {end.name} linea: {end.lineno}")
    print(f"Error msg: {err_msg}.")

def Carga(archivo):
    df_ConEle = pd.read_excel(archivo, sheet_name="ConElect") 
    df_ConEle['Tipo']='ELE'
    df_ConGas = pd.read_excel(archivo, sheet_name="ConGas") 
    df_ConGas['Tipo']='GAS'
    df_ConH2O = pd.read_excel(archivo, sheet_name="ConAgua") 
    df_ConH2O['Tipo']='H2O'
    df_ConDie = pd.read_excel(archivo, sheet_name="ConDiesel") 
    df_ConDie['Tipo']='DIE'
    df_CA = pd.concat([df_ConEle, df_ConGas,df_ConH2O, df_ConDie], axis=0)
    #data = df_CA.sort_values(by=['NumMes'])
    data = df_CA.sort_index()
    return data

def ConsumosTotales(df_CA):
    dfResultado = pd.DataFrame(columns=['Proceso', 'Tipo', 'TotalFactor', 'TotalConsumo', 'TotalGasto'])
    rslt_df = pd.DataFrame()
    index = 0
    for x in df_CA['Proceso'].unique() :
        for y in df_CA['Tipo'].unique() :
            print(df_CA['Tipo'].unique() )
            rslt_df = df_CA[(df_CA['Proceso'] == x) & (df_CA['Tipo'] == y)]
            dfResultado.loc[index,'Proceso'] = x
            dfResultado.loc[index,'Tipo']  = y
            dfResultado.loc[index,'TotalFactor'] = rslt_df['Fe'].sum()
            dfResultado.loc[index,'TotalConsumo']= rslt_df['Consumo'].sum()
            dfResultado.loc[index,'SubTotalEPPConsumo']= rslt_df['Fe'].sum()*rslt_df['Consumo'].sum()
            dfResultado.loc[index,'TotalGasto']= rslt_df['Valor'].sum()
            index = index + 1
    return dfResultado
    
def TotalEmiPro(df_CA):
    TotalEmiEmp = 0
    TotalFactor  = 0
    TotalConsumo = 0
    TotalEmiEmp = 0
    for row in df_CA.iterrows(): 
        TotalFactor  = row[1][2]
        TotalConsumo = row[1][4]
        TotalEmiEmp = (TotalFactor * TotalConsumo) + TotalEmiEmp
    return TotalEmiEmp

def EOLOSmetricesg(dfdata):
    df_CA =  pd. DataFrame() 
    df_ConTotales =  pd. DataFrame() 
    iTmpTotalEmiPro = 0
    try:
        #if dfdata:
            df_CA = Carga(dfdata)
            df_ConTotales = ConsumosTotales(df_CA)
            iTmpTotalEmiPro  = TotalEmiPro(df_ConTotales)
    except:
        print_custom_error_message()
    return df_CA,iTmpTotalEmiPro,df_ConTotales
#EOLOSmetricesg(StrNombreArchivo)

