import pandas as pd
import numpy as np
import pickle

model = pickle.load(open('rf_model.sav', 'rb'))

def pred(df):
    responce = df['id']
    x = df.iloc[:,1:].values
    y = model.predict_proba(x)
    y1 = []
    for en in y[:,1]:
        print(en)
        if en < 0.45 :
            y1.append('low-risk')
        elif en > 0.55:
            y1.append('high-risk')
        else:
            y1.append('neutral')


    responce = pd.concat([responce,pd.DataFrame(y1,columns=['dropout_probability'])],axis=1)
    return responce

if __name__=='__main__':
    df = pd.read_csv('data.csv',sep=';')
    df['id'] = df.index
    x = df.drop(['Target'],axis=1)
    y = pred(x[:15])
    print(y)