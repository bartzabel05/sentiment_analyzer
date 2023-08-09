from flask import Flask,redirect,url_for,render_template,request,jsonify,make_response,flash,session
import joblib
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import time
import numpy as np
# from sklearn import partial_fit

with open("trained_sgd_classifier (1).joblib","rb") as f:
    sgd_classifier=joblib.load(f)

with open("tfidf_vectorizer.joblib","rb") as f:
    vectorizer=joblib.load(f)


while True:
    try:
        conn=psycopg2.connect(host="localhost",database="Sentiment_Analysis",user="postgres",password="kartik05",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ",error)
        time.sleep(2)


def insertData(input_txt,modelPred,trueSentiment):
    try:
        data=(input_txt,modelPred,trueSentiment)
        sql="""INSERT INTO public.sentiments(user_text,model_sentiment,true_sentiment) VALUES(%s,%s,%s)"""
        cursor.execute(sql,data)
        conn.commit()
    except psycopg2.Error as e:
        print("Error inserting data:",e)
        return None
    finally:
        pass

def fetchData():
    try:
        sql="""SELECT id,user_text,model_sentiment,true_sentiment from public.sentiments"""
        cursor.execute(sql)
        rows=cursor.fetchall()
        return rows
    
    except psycopg2.Error as e:
        print("Error fetching data:",e)
        return None
    finally:
        pass

app=Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/form",methods=['POST','GET'])
def input_form():
    if request.method=='POST':
        text_input=request.form["txt_input"]
        # print(text_input)
        # return text_input
        ls_inp=[]
        ls_inp.append(text_input)
        # text_input_list.append(text_input)
        vec_inp=vectorizer.transform(ls_inp)
        pred_inp=sgd_classifier.predict(vec_inp)
        return render_template('response.html',input_text=text_input,vector=vec_inp,sentiment=pred_inp[0])
    
    else:
        return render_template('chat.html')

@app.route('/feedback',methods=['POST'])
def feedback():
    if request.method=='POST':
        user_sentiment=request.form['feedback']
        input_txt=request.form['inp_text']
        model_pred=request.form['model_sentiment']

        if(user_sentiment=='yes'):
            true_sentiment=int(model_pred)
            
        elif(user_sentiment=='no'):
            if(model_pred==1):
                true_sentiment=0
            elif(model_pred==0):
                true_sentiment=1
        
        vec_inp=vectorizer.transform([input_txt])
        sgd_classifier.partial_fit(vec_inp,[true_sentiment],classes=np.array([0,1]))
        print("Partial Fit successful")
        print(type(vec_inp))
        print(type(true_sentiment))

        insertData(input_txt,model_pred,true_sentiment)

        return render_template('feedback.html')

@app.route('/api/data')
def fetch():
    rows=fetchData()
    if not rows:
        return {"message":"No Data present in Database"}
    
    return rows

if __name__=='__main__':
    app.run(debug=True)