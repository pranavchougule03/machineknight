import pandas as pd
import numpy as np
import pickle

model = pickle.load(open('rf_model.sav', 'rb'))

def pred(df):
    responce = df['id']
    x = df.iloc[:,1:].values
    y = model.predict_proba(x)
    responce = pd.concat([responce,pd.DataFrame(y[:,1],columns=['dropout_probability'])],axis=1)
    return responce

df = pd.read_csv('data.csv',sep=';')
df['id'] = df.index
x = df.drop(['Target'],axis=1)
y = pred(x[:15])
print(y)