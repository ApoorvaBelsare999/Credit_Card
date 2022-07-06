# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:39:24 2022

@author: user
"""

import pickle
import numpy as np 
#import streamlit as st
import time
import pandas as pd
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

import streamlit as st
st.set_page_config(
    page_title="Main",
    page_icon="👋",
)



loaded_model=pickle.load(open('trained_model.sav','rb'))
scaler=pickle.load(open('scaler.sav','rb'))

def convert_df(df):
     return df.to_csv(index = False).encode('utf-8')
 
def func(input):
    input_as_numpy_array = np.asarray(input)
    input_dt = pd.DataFrame([input_as_numpy_array], columns=['LIMIT_BAL','PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6','BILL_AMT5','PAY_AMT2'])
    columns=input_dt.columns
    scaled_dt = scaler.transform(input_dt)
    scaled_dt = pd.DataFrame(scaled_dt, columns=[columns])
    input_reshape=  input_as_numpy_array.reshape(1,-1)
    prediction=loaded_model.predict(input_reshape)
    print (prediction)
    if(prediction[0]==0):
        return'No default payment next month'
    else:
        return'default payment next month'
        
def func_csv(input):
    input_as_numpy_array = np.asarray(input)
    input_reshape=  input_as_numpy_array.reshape(1,-1)
    prediction=loaded_model.predict(input_reshape)
    print (prediction)
    if(prediction[0]==0):
        return'person will not default'
    else:
        return'person will default'
    
def main():
    
    image = Image.open('credit_card_image.jpg')
    logo = Image.open('aress_logo.jpg')
    
    col1,col2  = st.columns(2)
    
    with col1:
        st.title('Credit Card Payment')
        
    
    with col2:
        st.image(image,width=250)

    with st.sidebar:
    
        st.image(logo,width=250,use_column_width=True)
        
  
         
    
    LIMIT_BAL = st.text_input('Limit Balance Available')
    PAY_0 = st.text_input('pay_0')
    PAY_2 = st.text_input('pay_2')
    PAY_3 = st.text_input('pay_3')
    PAY_4 = st.text_input('pay_4')
    PAY_5 = st.text_input('pay_5')
    PAY_6 = st.text_input('pay_6')
    BILL_AMT5 = st.text_input('Bill_Amount_5')
    PAY_AMT2 = st.text_input('pay_amount_2')
    
    try:
        if LIMIT_BAL and PAY_0 and PAY_2 and PAY_3 and PAY_4 and PAY_5 and PAY_6 and BILL_AMT5 and PAY_AMT2!=[]:
        
            Payment =''
            if st.button('Please click for prediction'):
                Payment = func([LIMIT_BAL,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT5,PAY_AMT2])
                with st.spinner('Wait for it...'):
                    time.sleep(5)
                    st.success(Payment)
                    if Payment=='This person will not default':
                        st.snow()
                    else:
                        st.image('better_luck.jpg')

        else:
            st.write("please enter all values")
    except:
        st.write("please enter only integer values")
        pass
    
    st.info('You can upload the file for prediction')
   
    uploaded_file = st.file_uploader("Choose a csv file for making prediction")
    if uploaded_file is not None:
     try:
        try:
            df = pd.read_csv(uploaded_file)
        except:
            df = pd.read_excel(uploaded_file)
     except:
        st.write("Please upload the CSV or Excel file only")
        
     try:
        if st.button('Please click for prediction'):
            with st.spinner('Wait for it...'):
                prediction = []
                df1 = df[['LIMIT_BAL','PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6','BILL_AMT5','PAY_AMT2']]
                for i in range(len(df1)):
                    Payment = func_csv(df1.iloc[0].tolist())
                    prediction.append(Payment)
                df['Prediction']= prediction
                try:
                    df = df.drop(['default payment next month'],axis=1)
                except:
                    df = df
                csv = convert_df(df)
                st.download_button(label="Download File With the prediction as CSV",data=csv,file_name='File With the prediction.csv',mime='text/csv')  
                st.success("Prediction for the file is done")
                st.snow()             
     except:
         st.success('CSV file does not match with required columns')

if __name__== '__main__':
    main()
