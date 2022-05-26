import flask
from flask import Flask,render_template,request
import os
import pickle
import pandas as pd
with open(f'model/car_price_prediction.sav', 'rb') as f:
    model = pickle.load(f)
app = flask.Flask(__name__, template_folder='templates')

pic_folder=os.path.join('static')
app.config['UPLOAD_FOLDER']=pic_folder

@app.route('/')
def main():
    pic1=os.path.join(app.config['UPLOAD_FOLDER'],'maruti-suzuki.jpg')
    pic2=os.path.join(app.config['UPLOAD_FOLDER'],'hyundai.jpg')

    return(flask.render_template('home_page.html',maruti_image=pic1,hyundai_image=pic2))

@app.route('/swift',methods=['GET','POST'])
def swift():
    if request.method=='POST':
       Kms_Driven= request.form.get("KmsDriven")
       year=request.form.get("year")
       Seller_type=request.form.get("Seller_Type")
       if Seller_type=="Individual":
            Seller_type=1;
       if Seller_type=="Dealer":
            Seller_type=0;

       Transmission=request.form.get("Transmission")
       if Transmission=="Manual":
            Transmission=1;
       else:
            Transmission=0;


       Fuel_type=request.form.get("Fuel_Type")
       if Fuel_type=="Petrol":
            Fuel_type=0;
       if Fuel_type=="Diesel":
            Fuel_type=1;
       if Fuel_type=="CNG":
            Fuel_type=2;
       Owners=request.form.get("Owners")
       selling_price=6.5
       input_variables=pd.DataFrame([[year,6.5,Kms_Driven,Fuel_type, Seller_type,Transmission, Owners]],columns=['Year','Present_Price','Kms_Driven','Fuel_Type','Seller_Type','Transmission','Owner'],dtype=float)
       prediction = model.predict(input_variables)[0]
      
       return (flask.render_template('swift.html',result=prediction))

    return(flask.render_template('swift.html'))


if __name__ == '__main__':


    app.run()