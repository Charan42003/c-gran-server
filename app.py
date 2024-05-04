from flask import Flask, render_template, request, jsonify, url_for
from pymongo import MongoClient, errors
from flask_cors import CORS
from bson.objectid import ObjectId
import sys
import os

app = Flask(__name__)
dbUrl = os.environ.get('MONGODB_URL')


try:
    client = MongoClient(dbUrl)
    # print("Connected to DB")
except errors.ConfigurationError:
#   print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)
db = client['cgran-bookings']
Bookings = db['bookings']

CORS(app) #prevent the cors error


#postRequest _ Registed Bookings
@app.route("/", methods=["GET"])
def home():
    return "<h1>Booking Api</h1>"

#postRequest _ Registed Bookings
@app.route("/postBooking", methods=["POST"])
def postBooking():
    body = request.json
    fullName = body['fullName']
    email = body['email']
    phoneNo = body['phoneNo']
    people = body['people']
    time = body['time']
    date = body['date']
    # print(fullName, email, phoneNo, people, time, date)
    data = {
        "FullName":fullName,
        "Email":email,
        "PhoneNo":phoneNo,
        "People":people,
        "Time":time,
        "Date":date
    }
    user = Bookings.insert_one(data)
    uid = user.inserted_id
    dataDict = {
        "id": str(uid),
        "fullName":fullName,
        "email":email,
        "phoneNo":phoneNo,
        "people":people,
        "time":time,
        "date":date
    }
    return jsonify({
        "msg": "Booked Successfully",
        "data": dataDict
    })


#getRequest - Get all bookings from database
@app.route("/getBookings", methods=["GET"])
def getBookings():
    allBookings = Bookings.find()
    # print(allBookings)
    jsonData = []
    for data in allBookings:
        id = data['_id']
        FullName = data['FullName']
        Email = data['Email']
        PhoneNo = data['PhoneNo']
        People = data['People']
        Time = data['Time']
        Date = data['Date']
        datadict = {
            "id": str(id),
            "fullName":FullName,
            "email":Email,
            "phoneNo":PhoneNo,
            "people":People,
            "time":Time,
            "date":Date
        }
        jsonData.append(datadict)
    
    return jsonify({
        "data": jsonData
    })


#deleteRequest - delete Data from Database
@app.route("/checkout", methods=["DELETE"])
def checkout():
    id = request.json['_id']
    Bookings.delete_one({'_id': ObjectId(id)})
    # print(deletedbooking.deleted_count)
    return jsonify({
        "msg": "Checked out Successfully"
    })

# if(__name__ == "__main__"):
#     app.run(debug=True)