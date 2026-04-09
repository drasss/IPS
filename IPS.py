import streamlit as st
import pandas as pd
import numpy as np
#IPS sets in french for social position index
st.set_page_config(page_title="IPS Lycée",layout="wide")
st.title("IPS")
r,s=st.tabs(["Recherche","Statistiques"])

df = pd.read_csv("data.csv", sep=";", encoding="utf-8", low_memory=False, header=0)
df=df[df["Rentrée scolaire"]=="2025-2026"]
df_sort=pd.DataFrame(df.sort_values(by="IPS de l'établissement", ascending=False).dropna(subset=["IPS de l'établissement"])[["Région académique","Académie","Département","Nom de la commune","UAI","Nom de l'établissement","IPS de l'établissement"]])

def sub_df(label, df_sort):
    return pd.DataFrame(df_sort[df_sort[label]==df_sort[df_sort["UAI"]==UAI][label].values[0]].to_numpy(), columns=df_sort.columns)

def ranking(df_sort):
    return df_sort.index[df_sort["UAI"]==UAI].values[0]+1,len(df_sort)


research =r.expander("Rechercher le nom du lycée")
research_col=research.columns([2,5])
ville_lycee=research_col[0].selectbox("Sélectionnez une ville", [""] + list(df['Nom de la commune'].unique()))
if ville_lycee=="":
    nom_lycee=research_col[1].selectbox("Sélectionnez un lycée", [""] + list(df['Nom de l\'établissement'].unique()))
    UAI=""
elif ville_lycee:
    nom_lycee=research_col[1].selectbox("Sélectionnez un lycée", [""] + list(df[df['Nom de la commune'] == ville_lycee]['Nom de l\'établissement'].unique()))
    if nom_lycee=="":
        UAI=""
    else:
        UAI=df[df['Nom de l\'établissement']==nom_lycee][df['Nom de la commune']==ville_lycee]["UAI"].values[0]
if UAI!="":
    cols=r.columns(5)
    #Commune
    df_C=sub_df("Nom de la commune", df_sort)
    cols[0].write("## Commune :")
    cols[0].write("### " + str(ranking(df_C)[0]) + " / " + str(ranking(df_C)[1]))
    # Département
    df_D=sub_df("Département", df_sort)
    cols[1].write("## Département :")
    cols[1].write("### " + str(ranking(df_D)[0]) + " / " + str(ranking(df_D)[1]))
    # Académie
    df_A=sub_df("Académie", df_sort)
    cols[2].write("## Académie :")
    cols[2].write("### " + str(ranking(df_A)[0]) + " / " + str(ranking(df_A)[1]))  
    # région académique
    df_RA=sub_df("Région académique", df_sort)
    cols[3].write("## Région :")
    cols[3].write("### " + str(ranking(df_RA)[0]) + " / " + str(ranking(df_RA)[1]))
    #France : 
    df_FR=pd.DataFrame(df_sort.to_numpy(), columns=df_sort.columns)
    cols[4].write("## France : ")
    cols[4].write("### " + str(ranking(df_FR)[0]) + " / " + str(ranking(df_FR)[1]))
 

s.write(df_sort)


    