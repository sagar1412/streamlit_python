import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import plotly.express as px
import psycopg2
from sqlalchemy import create_engine

#Display the the header
st.header("Pandas Data to PSQL Database Connection ")
# Reading the Csv File
csv_loc = st.text_input('Enter CSV File Location')
if len(csv_loc)>0:
    df_csv=pd.read_csv(csv_loc)
    df_csv.columns = df_csv.columns.str.replace(" ","")
    st.write(df_csv)
else:
    st.write("Enter the location for the CSV Path")

#Readin the Json File
json_loc = st.text_input('Enter Json  File Location')
if len(json_loc)>0:
    with open(json_loc,'r') as f:
        data = json.loads(f.read())
        df_nested_list = pd.json_normalize(data, record_path =['objects'])
        st.write(df_nested_list)
else:
    st.write("Enter the location for the Json Path")

#Reading the Excel File
excel_loc = st.text_input('Enter Excel File Location')
if len(excel_loc)>0:
    df_excel=pd.read_excel(excel_loc)
    df_excel.columns = df_excel.columns.str.replace(" ","")
    st.write(df_excel)
else:
    st.write("Enter the location for the Excel Path")
try:
    #Merging all the Files
    if len(df_nested_list)>=0:
        df = pd.concat([df_nested_list,df_csv,df_excel],axis=0)
        df.drop(columns = 'ID',inplace = True)
        df.reset_index(inplace=True,drop = True)
        df.rename(columns = {'Newcolumn':'Company'}, inplace = True)
        st.header("Combined Data from all the Three file types")
        st.write(df)
    else:
        st.write("Input the Data")

    st.subheader("Cleaning all the Data")
    df.reset_index(inplace=True)
    df.rename(columns = {'Newcolumn':'Company'}, inplace = True)
    df["FirstName"] = df["FirstNameLastName"].apply(lambda x : x.split(" ")[0])
    df["LastName"]  = df["FirstNameLastName"].apply(lambda x : x.split(" ")[1])
    df.drop(columns= 'FirstNameLastName' ,inplace= True)
    df.drop(columns='index',inplace=True)
    st.header("Finale CSV File")
    st.write(df)

    st.write(df.describe(include="object"))

    fig = px.pie(hole=0.2,
    labels=df.JobTitle.values,
    names = df.JobTitle.unique(),
    )
    st.header("Donut Chart")
    st.plotly_chart(fig)


    if st.checkbox('Upload the Data to DataBase '):
        st.subheader('Enter Credentials')
        ip = st.text_input('Enter Ip')
        port = st.text_input('Enter Port')
        db_name = st.text_input("Enter DB Name")
        table_name = st.text_input('Enter Table Name')
        user = st.text_input('Enter User')
        password = st.text_input('Enter Password')
        try:
            if st.button("Upload Data to DB"):
                conn_string = 'postgresql://'+user+':'+password+'@'+ip+":"+port+"/postgres"
                db = create_engine(conn_string)
                conn = db.connect()
                st.write("connection sucessfull")
                df.to_sql(table_name, con=conn, if_exists='replace',index=False)
                conn = psycopg2.connect(conn_string)
                conn.autocommit = True
                cursor = conn.cursor()
                conn.close()
                st.write('Data Uploaded to the DB')

            else:
                st.write('Upload Data to DB')
        except:
            st.write("Data has not been uploaded to DB due to error")
except:
    st.write("Input the Data")