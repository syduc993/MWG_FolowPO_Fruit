import os
from datetime import datetime
import pandas as pd
import numpy as np
import pyodbc
import warnings
warnings.filterwarnings("ignore")
import plotly.express as px
import streamlit as st
pd.set_option('display.float_format', '{:.2f}'.format)





@st.experimental_memo # this is changed to st.experimantal_singleton
def connect_db():
    source_file = "C:/Users/lesyd/OneDrive/MWG_BHX/Theo dõi PX/PX/"
    excel_file_list = os.listdir(source_file)
    df = pd.DataFrame()
    for excel_files in excel_file_list:
        if excel_files.endswith(".xlsx"):
            strfile = source_file + excel_files
            conn_str = (r'Driver={{Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)}};'
                r'DBQ={}; ReadOnly=0').format(strfile)
            conn =  pyodbc.connect(conn_str, autocommit=True)
            crsr = conn.cursor()
        for worksheet in crsr.tables():
            str_sql = "SELECT [Mã siêu thị],[Tên siêu thị],[Ngày xuất],[Mã sản phẩm],[Tên sản phẩm],[Số lượng],[Đơn giá xuất],[retailprice],[Hình thức xuất] FROM "  + "[" + worksheet[2] + "]"
            df1 = pd.read_sql(str_sql, conn)
            df = df.append(df1)
        conn.close()
    return df


df = connect_db()

df['Số lượng'] = df['Số lượng'].astype(float).sum()
df['Ngày xuất'] = pd.to_datetime(df['Ngày xuất']).dt.date

df.loc[df["Đơn giá xuất"]<df["retailprice"],"Tình trạng"] ="Giảm giá "
df.loc[df["Đơn giá xuất"]==df["retailprice"],"Tình trạng"] ="Nguyên giá "

table = pd.pivot_table(df, values='Số lượng', index=['Ngày xuất'],
                    columns=['Tình trạng'], aggfunc=np.sum)

df2 = table.reset_index()

fig = px.bar(df2, x='Ngày xuất', y=['Giảm giá ', 'Nguyên giá '],barmode='group')
fig.show()

st.write(fig)