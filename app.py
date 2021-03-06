from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin
import logger
import smtplib

app = Flask(__name__)



# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()

    sessionID=req.get('responseId')


    result = req.get("queryResult")
    user_says=result.get("queryText")
    log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    cust_name=parameters.get("Person_name")
    #print(cust_name)
    cust_contact = parameters.get("Person_number")
    cust_email=parameters.get("Peron_email")
    cust_date= parameters.get("Person_date")
    intent = result.get("intent").get('displayName')
    if (intent=='Booking'):
        s = smtplib.SMTP('smtp.gmail.com', 587)
  
        # start LS for security
        s.starttls()
        # Authentication
        s.login("***@gmail.com", "*****")
        # message to be sent
        message = "Your Booking for " + cust_name +" has been confirmed for "+cust_date
        # sending the mail
        s.sendmail("kchawla.cse15@gmail.com", cust_email, message)
        # terminating the session
        s.quit() 
        fulfillmentText="We have send the details to the team. Please wait you will recieve the confirmation on mail"
        log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    else:
        log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)


if __name__ == '__main__':
    app.run()
