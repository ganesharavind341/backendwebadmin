from flask import Flask, render_template, url_for, request, session, redirect, Response,jsonify
import json
import pymongo
import bcrypt
from getData import getMongoConn,connectUsers,connectChat
from funcTion import genJojoId
from funcTion import genJojoId,genCompanyId
from flask_cors import CORS,cross_origin
import jwt
from datetime import datetime, timedelta
from functools import wraps
import getData
from flask_socketio import SocketIO


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
mongo =  getMongoConn()
app.secret_key = 'BAD_SECRET_KEY'
socketio = SocketIO(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = (request.headers.get('Authorization'))
        
        if request.headers:
            
    
            try: 
                data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
                print(data)
                return data
            except:
                print("here")
                return jsonify({'message' : 'Token is invalid!'}), 401

        elif not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        
        return f(data, args, *kwargs)

    return decorated





@app.route('/')
@token_required
@cross_origin(origin='*')
def home(data):
    if 'jojoId' in session:
        return jsonify(data)
    return jsonify({"isLoggedIn" : False}),401

@app.route('/getProfileData', methods=['GET','POST'])
@token_required
@cross_origin(origin='*')
def getProfileData(data):

    import getData
    data = getData.getProfileData(data['companyId'])
    data21 = getData.getDeskStaffSchema(data['companyId'])

    return json.dumps({"profile":data,"staff" : data21})


@app.route('/getDeskStaffData', methods=['GET','POST'])
@token_required
@cross_origin(origin='*')
def getDeskstaffData(data):
    import getData
    data = getData.getDeskStaffSchema(data["jojoId"])
    return(json.dumps(data))

@app.route('/getSingleStaffData', methods=['GET','POST'])
@token_required
@cross_origin(origin='*')
def getSingleStaffData(data):
    import getData
    data = getData.getDeskStaffSchema(data["jojoId"])
    print(request.get_data())
    for x in data:
        print(str(request.data.decode('utf8')))
        if x['addId'] == str(request.get_data().decode('utf8')):
                return(json.dumps(x))
        
    return "NULL"


@app.route('/getBusData', methods=['GET','POST'])
@token_required 
@cross_origin(origin='*')
def getBusData(data):
    print(data)
    import getData
    data = getData.getBusSchema(data['companyId'])
    print(data)
    return(json.dumps(data))    

@app.route('/getDriverData', methods=['GET','POST'])
@token_required
@cross_origin(origin='*',allow_headers=True)   
def getDriveData(data):
    import getData
    data = getData.getDriverSchema(data['companyId'])
    print(data)
    return(json.dumps(data))    

@app.route('/getTripCompanyData', methods=['GET','POST'])
# @token_required
# @cross_origin(origin='*')
def getTripComanyData(data):
    # import getData
    # data = getData.getTripSchema(data["jojoId"])
    # print(json.dump(data))
    # print(data)
    data = {"key":"message received"}
    return(json.dumps(data))    

@app.route('/getChatData', methods=['GET','POST'])
@token_required
@cross_origin(origin='*')
def getChatData(data):
    import getData
    data = getData.getChat(data["jojoId"])
    print(data)
    return(json.dumps(data))    



@app.route('/getTransactionData', methods=['GET','POST'])
@token_required
@cross_origin(origin='*')
def getTransactionData():
    import getData
    data = getData.getTransactionData("jojoId1001ha")
    return (json.dumps(list(data)))

@app.route('/login', methods=['GET','POST'])
@cross_origin(origin='*')
def login():
    users =  connectUsers()
    getLoginTryer =  request.get_json()
    loginTryer = users.find_one({'jojoId' : getLoginTryer['jojoId']})
    if loginTryer:
        if (bcrypt.checkpw(str(getLoginTryer['password']).encode('utf8'),loginTryer['password'])):
            session['username'] = getLoginTryer['jojoId']
            session['ip'] = request.base_url
            # print(session)
            session['logged_in'] = True
            token = (jwt.encode({
            'jojoId': session['username'],
            'companyId' : loginTryer['companyId'],
            'expiration': str(datetime.now() + timedelta(minutes=30))},app.config['SECRET_KEY'], algorithm="HS256"))
            print(type(token))
            token = {"token" : str(token)}
            return jsonify(token)
        else:
            return "wrong pass"

    return 'Invalid username/password combination'










@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        transations = getData.connectCompanyData()
        data = request.json
        print(data)
        print("here")
        dataInsert = {
                    "ownerName": data["ownerName"],
                    "ownerAddress": data["ownerAddress"],
                    "ownerMail": data["ownerMail"],
                    "ownerPhone": data["ownerPhone"],
                    "companyName": data["companyName"],
                    "companyAddress": data["companyAddress"],
                    "companyId": genCompanyId(data["companyName"]),
                    "companyMail": data["companyMail"],
                    "companyPhone":data["companyPhone"],
                    "companyDocument": data["companyDocument"],
                    "companyBio": data["companyBio"],
                    "ownerIdProof": data["ownerIdProof"],
                    "jojoId" : genJojoId(data["companyName"]),
                    "numberOfBuses" : 0,
                    "numberOfPilots" : 0,
                    "numberOfLogins" : 0,
                    "numberOfOnDesks" : 0,
                    "rating": 5.0
                }
        print(dataInsert)
        print("here")

        transations.insert_one(dataInsert) 
        print("here")

        return jsonify({"jojoId" : dataInsert["jojoId"], "companyId" : dataInsert["companyId"] })
        
@app.route('/registerCreds', methods=['POST', 'GET'])
def register2():
    if request.method == 'POST':
        transations = connectUsers()
        data = request.json
        if str(data['password']) == str(data['confirmPassword']):
            hashedPassword = bcrypt.hashpw(str(data['password']).encode('utf-8'),bcrypt.gensalt())
            dataInsert = {
                    
                    "jojoId" : data["jojoId"],
                    "password" : hashedPassword 

                }
            transations.insert_one(dataInsert) 
            return "Done"
        else:
            return "Passwords doesnt Match"




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=86)