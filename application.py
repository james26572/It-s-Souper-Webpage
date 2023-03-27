import flask
import os
from flask import request,jsonify
import pandas as pd
from pyexcel import Sheet,get_sheet
import csv
import boto3
import io

 
application = flask.Flask(__name__,static_folder='assets')

# Only enable Flask debugging if an env var is set to true
application.debug = os.environ.get('FLASK_DEBUG') in ['true', 'True']

# Get application version from env
app_version = os.environ.get('APP_VERSION')

# Get cool new feature flag from env
enable_cool_new_feature = os.environ.get('ENABLE_COOL_NEW_FEATURE') in ['true', 'True']

@application.route('/',methods = ["POST","GET"])
def home():
    
    
    return flask.render_template('index.html',
                                    
                                    flask_debug=application.debug,
                                    app_version=app_version,
                                    enable_cool_new_feature=enable_cool_new_feature,
                                    )
    


@application.route('/handle_data', methods=['POST'])
def handle_data():
    email = request.form["email"]
    subject = request.form["subject"]
    text = request.form["message"]
    print(email)

    # save locally
    with open("customerInfo\messages.csv",'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([email,subject,text])

    #save to cloud
    s3 = boto3.resource('s3')
    bucket_name = 'jimsbins'
    key_name = 'messages.csv'

    # Open the file for appending
    obj = s3.Object(bucket_name, key_name)
    body = obj.get()['Body']
    lines = body.read().decode('utf-8').split('\n')
    output = io.StringIO()
    writer = csv.writer(output)
    
    for line in lines:
        if line.strip(): # Skip empty lines
            writer.writerow(line.split(','))
    writer.writerow([email,subject,text])
    output.seek(0)
    obj.put(Body=output.getvalue().encode('utf-8'))

    return flask.render_template('message_received.html')
    # return a response


@application.route('/handle_subscribe',methods = ['POST'])
def handle_subscribe():
    email = request.form["email"]
    print(email)
    #save locally
    with open('customerInfo\emails.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Write the input data as a new row in the CSV file
        writer.writerow([ email])

    # save to cloud
    s3 = boto3.resource('s3')
    bucket_name = 'jimsbins'
    key_name = 'emails.csv'

    # Open the file for appending
    obj = s3.Object(bucket_name, key_name)
    body = obj.get()['Body']
    lines = body.read().decode('utf-8').split('\n')
    output = io.StringIO()
    writer = csv.writer(output)
    
    for line in lines:
        if line.strip(): # Skip empty lines
            writer.writerow(line.split(','))
    writer.writerow([email])
    output.seek(0)
    obj.put(Body=output.getvalue().encode('utf-8'))
   
    
    return flask.render_template('email_received.html')
 
if __name__ == '__main__':
    application.run(host='0.0.0.0',debug=True)